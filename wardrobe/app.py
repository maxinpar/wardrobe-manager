"""The Flask app. Five screens: Today, Catalogue, Outfits, Wear log, Laundry.

No build step, no JS framework: Jinja templates and one stylesheet. Host and
port come from the environment, so pointing it at 0.0.0.0 makes it reachable
from a phone on the same wifi without touching the code.

There is no auth. If you ever expose this beyond the LAN, add it in
require_login() below — that is the one obvious place for it.
"""

from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from . import config, db, picker

app = Flask(__name__)
app.secret_key = "wardrobe-local"  # only used for flash messages on localhost

TZ = ZoneInfo(config.TIMEZONE)


def today() -> date:
    return datetime.now(TZ).date()


@app.before_request
def require_login():
    """No auth in v1. Add it here if this ever leaves the LAN."""
    return None


# ------------------------------------------------------------- helpers --

ITEM_SELECT = """
SELECT i.*, c.label AS cat_label, c.sort_order AS cat_sort,
       v.label AS verdict_label, v.wearable,
       COALESCE(l.state_code, 'clean') AS laundry_state,
       ls.label AS laundry_label,
       -- The generated retail render is the preferred catalogue image; a real
       -- photo of this garment is the fallback, and the hex swatch after that.
       -- starts_with(filename, id) is what makes a photo this item's own: a
       -- shared group-reference shot (three loafers in one frame) is named for
       -- the group, so it never stands in as a photo of one of them.
       (SELECT p.thumb_path FROM photos p
         WHERE p.item_id = i.id
           AND (p.is_render OR starts_with(p.source_filename, i.id))
         ORDER BY p.is_render DESC, p.sort_order LIMIT 1) AS thumb_path,
       (SELECT p.is_render FROM photos p
         WHERE p.item_id = i.id
           AND (p.is_render OR starts_with(p.source_filename, i.id))
         ORDER BY p.is_render DESC, p.sort_order LIMIT 1) AS thumb_is_render,
       (SELECT count(*) FROM photos p WHERE p.item_id = i.id) AS photo_count,
       (SELECT string_agg(o.occasion_code, ',' ORDER BY o.occasion_code)
          FROM item_occasions o WHERE o.item_id = i.id) AS occasions
FROM items i
JOIN categories c ON c.code = i.cat_code
JOIN verdicts v ON v.code = i.verdict_code
LEFT JOIN item_laundry l ON l.item_id = i.id
LEFT JOIN laundry_states ls ON ls.code = COALESCE(l.state_code, 'clean')
"""


def get_setting(conn, key: str, default: str | None = None) -> str | None:
    row = db.fetch_one(conn, "SELECT value FROM app_settings WHERE key = %s", (key,))
    return row["value"] if row else default


def set_setting(conn, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO app_settings (key, value) VALUES (%s, %s) "
        "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
        (key, value),
    )


def set_laundry(conn, item_id: str, state: str) -> None:
    conn.execute(
        "INSERT INTO item_laundry (item_id, state_code, changed_at) "
        "VALUES (%s, %s, now()) "
        "ON CONFLICT (item_id) DO UPDATE SET state_code = EXCLUDED.state_code, "
        "changed_at = now()",
        (item_id, state),
    )


# --------------------------------------------------------------- routes --


@app.route("/")
def home():
    return redirect(url_for("today_view"))


@app.route("/today")
def today_view():
    with db.connect() as conn:
        temp_raw = request.args.get("temp") or get_setting(conn, "weather.temp_c", "18")
        rain_raw = request.args.get("rain")
        if rain_raw is None:
            rain = get_setting(conn, "weather.rain", "0") == "1"
        else:
            rain = rain_raw == "1"
        allow_disliked = request.args.get("allow_disliked") == "1"

        try:
            temp_c = float(temp_raw)
        except (TypeError, ValueError):
            temp_c = None

        if request.args:
            set_setting(conn, "weather.temp_c", str(temp_c if temp_c is not None else ""))
            set_setting(conn, "weather.rain", "1" if rain else "0")
            conn.commit()

        looks = picker.load_looks(conn)
        best, ranked, rejected = picker.pick(
            looks, today(), temp_c=temp_c, rain=rain, allow_disliked=allow_disliked
        )
        thumbs = photo_thumbs(conn)

    return render_template(
        "today.html",
        best=best,
        ranked=ranked[1:],
        rejected=rejected,
        temp_c=temp_c,
        rain=rain,
        allow_disliked=allow_disliked,
        band=picker.weather_band(temp_c),
        thumbs=thumbs,
        day=today(),
    )


def photo_thumbs(conn) -> dict[str, dict]:
    """item_id -> {thumb, hex, is_render, no_photo} for the little garment chips."""
    rows = db.fetch_all(
        conn,
        """
        SELECT i.id, i.hex, i.no_photo,
               (SELECT p.thumb_path FROM photos p
                 WHERE p.item_id = i.id
                   AND (p.is_render OR starts_with(p.source_filename, i.id))
                 ORDER BY p.is_render DESC, p.sort_order LIMIT 1) AS thumb_path,
               (SELECT p.is_render FROM photos p
                 WHERE p.item_id = i.id
                   AND (p.is_render OR starts_with(p.source_filename, i.id))
                 ORDER BY p.is_render DESC, p.sort_order LIMIT 1) AS is_render
        FROM items i
        """,
    )
    return {r["id"]: r for r in rows}


@app.route("/today/wear", methods=["POST"])
def wear_today():
    slug = request.form["outfit_slug"]
    item_ids = request.form.getlist("item_id")

    with db.connect() as conn:
        outfit = db.fetch_one(conn, "SELECT id, name FROM outfits WHERE slug = %s", (slug,))
        if outfit is None:
            abort(404)

        row = db.fetch_one(
            conn,
            "INSERT INTO wear_events (worn_on, outfit_id, context, temp_c, rain) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (
                today(),
                outfit["id"],
                request.form.get("context") or None,
                request.form.get("temp_c") or None,
                request.form.get("rain") == "1",
            ),
        )
        event_id = row["id"]
        for item_id in item_ids:
            conn.execute(
                "INSERT INTO wear_event_items (wear_event_id, item_id) VALUES (%s, %s)",
                (event_id, item_id),
            )
            set_laundry(conn, item_id, "worn")
        conn.commit()

    flash(f"Logged “{outfit['name']}” for today. Those garments are now marked worn.")
    return redirect(url_for("log_view", rate=event_id))


@app.route("/catalogue")
def catalogue():
    filters = {
        "cat": request.args.get("cat") or "",
        "verdict": request.args.get("verdict") or "",
        "scope": request.args.get("scope") or "",
        "role": request.args.get("role") or "",
        "formality": request.args.get("formality") or "",
        "occasion": request.args.get("occasion") or "",
        "state": request.args.get("state") or "",
        "q": (request.args.get("q") or "").strip(),
    }

    where = []
    params: list = []
    if filters["cat"]:
        where.append("i.cat_code = %s")
        params.append(filters["cat"])
    if filters["verdict"]:
        where.append("i.verdict_code = %s")
        params.append(filters["verdict"])
    if filters["scope"]:
        where.append("i.scope_code = %s")
        params.append(filters["scope"])
    if filters["role"]:
        where.append("i.role_code = %s")
        params.append(filters["role"])
    if filters["formality"]:
        where.append("i.formality_rank = %s")
        params.append(int(filters["formality"]))
    if filters["occasion"]:
        where.append(
            "EXISTS (SELECT 1 FROM item_occasions io WHERE io.item_id = i.id "
            "AND io.occasion_code = %s)"
        )
        params.append(filters["occasion"])
    if filters["state"]:
        where.append("COALESCE(l.state_code, 'clean') = %s")
        params.append(filters["state"])
    if filters["q"]:
        where.append(
            "(i.name ILIKE %s OR i.colour ILIKE %s OR i.material ILIKE %s "
            "OR i.notes ILIKE %s)"
        )
        params.extend([f"%{filters['q']}%"] * 4)

    sql = ITEM_SELECT
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY c.sort_order, i.name"

    with db.connect() as conn:
        items = db.fetch_all(conn, sql, params)
        lookups = load_lookups(conn)

    return render_template(
        "catalogue.html", items=items, filters=filters, lookups=lookups
    )


def load_lookups(conn) -> dict:
    return {
        "categories": db.fetch_all(conn, "SELECT * FROM categories ORDER BY sort_order"),
        "verdicts": db.fetch_all(conn, "SELECT * FROM verdicts ORDER BY sort_order"),
        "scopes": db.fetch_all(conn, "SELECT * FROM scopes ORDER BY code"),
        "roles": db.fetch_all(conn, "SELECT * FROM colour_roles ORDER BY sort_order"),
        "occasions": db.fetch_all(conn, "SELECT * FROM occasions ORDER BY sort_order"),
        "states": db.fetch_all(conn, "SELECT * FROM laundry_states ORDER BY sort_order"),
    }


@app.route("/item/<item_id>")
def item_detail(item_id: str):
    with db.connect() as conn:
        item = db.fetch_one(conn, ITEM_SELECT + " WHERE i.id = %s", (item_id,))
        if item is None:
            abort(404)
        photos = db.fetch_all(
            conn,
            "SELECT p.*, a.label AS angle_label, "
            "       (NOT p.is_render AND NOT starts_with(p.source_filename, i.id)) "
            "         AS is_group_reference "
            "FROM photos p JOIN items i ON i.id = p.item_id "
            "LEFT JOIN photo_angles a ON a.code = p.angle_code "
            "WHERE p.item_id = %s ORDER BY p.is_render DESC, p.sort_order",
            (item_id,),
        )
        occasions = db.fetch_all(
            conn,
            "SELECT o.code, o.label FROM item_occasions io "
            "JOIN occasions o ON o.code = io.occasion_code WHERE io.item_id = %s "
            "ORDER BY o.sort_order",
            (item_id,),
        )
        sources = {
            r["field_name"]: r["source"]
            for r in db.fetch_all(
                conn,
                "SELECT field_name, source FROM item_field_sources WHERE item_id = %s",
                (item_id,),
            )
        }
        in_outfits = db.fetch_all(
            conn,
            "SELECT o.slug, o.name, oi.slot_role, oi.is_alternate FROM outfit_items oi "
            "JOIN outfits o ON o.id = oi.outfit_id WHERE oi.item_id = %s "
            "ORDER BY o.sort_order",
            (item_id,),
        )
        worn = db.fetch_all(
            conn,
            "SELECT w.id, w.worn_on, w.rating FROM wear_event_items wi "
            "JOIN wear_events w ON w.id = wi.wear_event_id WHERE wi.item_id = %s "
            "ORDER BY w.worn_on DESC",
            (item_id,),
        )
        states = db.fetch_all(conn, "SELECT * FROM laundry_states ORDER BY sort_order")

    return render_template(
        "item.html",
        item=item,
        photos=photos,
        occasions=occasions,
        sources=sources,
        in_outfits=in_outfits,
        worn=worn,
        states=states,
    )


@app.route("/item/<item_id>/state", methods=["POST"])
def item_state(item_id: str):
    state = request.form["state"]
    with db.connect() as conn:
        set_laundry(conn, item_id, state)
        conn.commit()
    return redirect(request.form.get("next") or url_for("item_detail", item_id=item_id))


@app.route("/outfits")
def outfits_view():
    show_hidden = request.args.get("show_hidden") == "1"
    with db.connect() as conn:
        looks = picker.load_looks(conn)
        thumbs = photo_thumbs(conn)

    groups = {"everyday": [], "sharp": []}
    for look in looks:
        if look.hidden_by_default and not show_hidden:
            continue
        blockers = []
        for item in look.primary():
            state = item["laundry_state"]
            if state != "clean":
                labels = {
                    "worn": "already worn",
                    "in_wash": "in the wash",
                    "at_tailor": "at the tailor",
                }
                blockers.append(f"{item['name']} is {labels.get(state, state)}")
        groups.setdefault(look.register, []).append((look, blockers))

    return render_template(
        "outfits.html", groups=groups, show_hidden=show_hidden, thumbs=thumbs
    )


@app.route("/log")
def log_view():
    rate = request.args.get("rate", type=int)
    with db.connect() as conn:
        events = db.fetch_all(
            conn,
            "SELECT w.*, o.name AS outfit_name, o.slug AS outfit_slug "
            "FROM wear_events w LEFT JOIN outfits o ON o.id = w.outfit_id "
            "ORDER BY w.worn_on DESC, w.id DESC",
        )
        worn_items = db.fetch_all(
            conn,
            "SELECT wi.wear_event_id, wi.free_text, wi.is_base_layer, i.id, i.name "
            "FROM wear_event_items wi LEFT JOIN items i ON i.id = wi.item_id "
            "ORDER BY wi.id",
        )
    by_event: dict[int, list] = {}
    for row in worn_items:
        by_event.setdefault(row["wear_event_id"], []).append(row)

    return render_template("log.html", events=events, items=by_event, rate=rate)


@app.route("/log/<int:event_id>/rate", methods=["POST"])
def rate_event(event_id: int):
    rating = request.form.get("rating") or None
    with db.connect() as conn:
        conn.execute(
            "UPDATE wear_events SET rating = %s, note = %s, context = COALESCE(%s, context) "
            "WHERE id = %s",
            (rating, request.form.get("note") or None, request.form.get("context") or None, event_id),
        )
        conn.commit()
    flash("Saved.")
    return redirect(url_for("log_view"))


@app.route("/laundry")
def laundry_view():
    with db.connect() as conn:
        states = db.fetch_all(conn, "SELECT * FROM laundry_states ORDER BY sort_order")
        items = db.fetch_all(
            conn, ITEM_SELECT + " WHERE i.scope_code = 'core' ORDER BY c.sort_order, i.name"
        )
    by_state: dict[str, list] = {s["code"]: [] for s in states}
    for item in items:
        by_state.setdefault(item["laundry_state"], []).append(item)
    return render_template("laundry.html", states=states, by_state=by_state)


@app.route("/laundry/bulk", methods=["POST"])
def laundry_bulk():
    source = request.form["from"]
    target = request.form["to"]
    with db.connect() as conn:
        conn.execute(
            "UPDATE item_laundry SET state_code = %s, changed_at = now() "
            "WHERE state_code = %s",
            (target, source),
        )
        conn.commit()
    flash(f"Moved everything {source.replace('_', ' ')} to {target.replace('_', ' ')}.")
    return redirect(url_for("laundry_view"))


@app.route("/photos/<path:relative_path>")
def photo(relative_path: str):
    return send_from_directory(config.photo_store(), relative_path)


def main() -> None:
    app.run(host=config.app_host(), port=config.app_port(), debug=True)


if __name__ == "__main__":
    main()

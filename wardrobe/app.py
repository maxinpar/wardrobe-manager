"""The Flask app. Today, Catalogue, Fits, Wear log, Laundry.

No build step, no JS framework: Jinja templates and one stylesheet. Host and
port come from the environment, so pointing it at 0.0.0.0 makes it reachable
from a phone on the same wifi without touching the code.

Write paths in v1 are deliberately narrow. The importer owns the catalogue and
the fits; the app owns laundry state, the wear log, and the three things on a
fit that are Max's alone: `killer`, `score` and `style`. It never computes any
of those three — a number he typed is never silently changed.

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

from . import config, db, picker, seed_data

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
       -- noPhoto means "no INDIVIDUAL photo", which is two different problems.
       -- A garment sharing a group shot has an image to look at; a garment with
       -- nothing at all does not, and only the second is a lost photo.
       (SELECT count(*) FROM photos p
         WHERE p.item_id = i.id AND NOT p.is_render
           AND NOT starts_with(p.source_filename, i.id)) > 0 AS has_group_shot,
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


def photo_thumbs(conn) -> dict[str, dict]:
    """item_id -> {thumb, hex, is_render, no_photo} for the garment chips."""
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


def fit_metadata(conn) -> dict[str, dict]:
    """Per-fit bands, seasons, good/bad occasions and unmet jobs, for display."""
    meta: dict[str, dict] = {}

    def bucket(fit_id):
        return meta.setdefault(
            fit_id,
            {"bands": [], "seasons": [], "good_for": [], "bad_for": [], "jobs": []},
        )

    for row in db.fetch_all(
        conn,
        "SELECT ftb.fit_id, t.label FROM fit_temp_bands ftb "
        "JOIN temp_bands t ON t.code = ftb.band_code ORDER BY t.sort_order",
    ):
        bucket(row["fit_id"])["bands"].append(row["label"])

    for row in db.fetch_all(
        conn,
        "SELECT fs.fit_id, s.label FROM fit_seasons fs "
        "JOIN seasons s ON s.code = fs.season_code ORDER BY s.sort_order",
    ):
        bucket(row["fit_id"])["seasons"].append(row["label"])

    for row in db.fetch_all(
        conn,
        "SELECT fo.fit_id, fo.kind, o.label FROM fit_occasions fo "
        "JOIN occasions o ON o.code = fo.occasion_code ORDER BY o.sort_order",
    ):
        bucket(row["fit_id"])[
            "good_for" if row["kind"] == "good" else "bad_for"
        ].append(row["label"])

    for row in db.fetch_all(
        conn,
        "SELECT id, fit_id, text, item_id FROM fit_preconditions "
        "WHERE NOT done ORDER BY id",
    ):
        bucket(row["fit_id"])["jobs"].append(row)

    return meta


def fit_ratings(conn) -> dict[str, dict]:
    """Average wear rating per fit — displayed NEXT TO score, never merged in."""
    rows = db.fetch_all(
        conn,
        "SELECT fit_id, round(avg(rating)::numeric, 1) AS avg_rating, "
        "count(*) AS wearings FROM wear_events "
        "WHERE fit_id IS NOT NULL AND rating IS NOT NULL GROUP BY fit_id",
    )
    return {r["fit_id"]: r for r in rows}


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

        fits = picker.load_fits(conn)
        best, ranked, rejected = picker.pick(
            fits, today(), temp_c=temp_c, rain=rain, allow_disliked=allow_disliked
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


@app.route("/today/wear", methods=["POST"])
def wear_today():
    fit_id = request.form["fit_id"]
    item_ids = request.form.getlist("item_id")

    with db.connect() as conn:
        fit = db.fetch_one(conn, "SELECT id, name FROM fits WHERE id = %s", (fit_id,))
        if fit is None:
            abort(404)

        row = db.fetch_one(
            conn,
            "INSERT INTO wear_events (worn_on, fit_id, context, temp_c, rain) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (
                today(),
                fit["id"],
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

    flash(f"Logged “{fit['name']}” for today. Those garments are now marked worn.")
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

    # A retired item is out of the catalogue, but still reachable by direct link
    # so that a wear event referencing it can be followed.
    where.insert(0, "i.retired_at IS NULL")
    sql = ITEM_SELECT + " WHERE " + " AND ".join(where)
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
        "seasons": db.fetch_all(conn, "SELECT * FROM seasons ORDER BY sort_order"),
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
        in_fits = db.fetch_all(
            conn,
            "SELECT f.id, f.name, fi.role, fi.is_alternate FROM fit_items fi "
            "JOIN fits f ON f.id = fi.fit_id WHERE fi.item_id = %s "
            "ORDER BY f.sort_order",
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
        in_fits=in_fits,
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


# ------------------------------------------------------------------ fits --


@app.route("/fits")
def fits_view():
    show_hidden = request.args.get("show_hidden") == "1"
    only_killer = request.args.get("killer") == "1"
    season = request.args.get("season") or ""
    blocked_only = request.args.get("blocked") == "1"

    with db.connect() as conn:
        fits = picker.load_fits(conn)
        thumbs = photo_thumbs(conn)
        meta = fit_metadata(conn)
        ratings = fit_ratings(conn)
        lookups = load_lookups(conn)
        # Season is a browsing label: it filters this list and nothing else.
        by_season = {
            r["fit_id"]: r["codes"]
            for r in db.fetch_all(
                conn,
                "SELECT fit_id, array_agg(season_code) AS codes "
                "FROM fit_seasons GROUP BY fit_id",
            )
        }

    groups: dict[str, list] = {"everyday": [], "sharp": []}
    blocked_count = 0
    job_count = set()

    for fit in fits:
        problems = picker.staleness(fit)
        if problems:
            blocked_count += 1
        for job in fit.blocked_by:
            job_count.add(job)

        if fit.hidden_by_default and not show_hidden:
            continue
        if only_killer and not fit.killer:
            continue
        if season and season not in (by_season.get(fit.id) or []):
            continue
        if blocked_only and not problems:
            continue

        groups.setdefault(fit.register, []).append((fit, problems))

    return render_template(
        "fits.html",
        groups=groups,
        show_hidden=show_hidden,
        only_killer=only_killer,
        season=season,
        blocked_only=blocked_only,
        thumbs=thumbs,
        meta=meta,
        ratings=ratings,
        lookups=lookups,
        blocked_count=blocked_count,
        job_count=len(job_count),
        total=len(fits),
    )


@app.route("/fit/<fit_id>")
def fit_detail(fit_id: str):
    with db.connect() as conn:
        fits = {f.id: f for f in picker.load_fits(conn)}
        fit = fits.get(fit_id)
        if fit is None:
            abort(404)
        thumbs = photo_thumbs(conn)
        meta = fit_metadata(conn).get(fit_id, {})
        ratings = fit_ratings(conn).get(fit_id)
        row = db.fetch_one(
            conn,
            "SELECT source, formality_rank, rain_safe, hero_image_path, "
            "hero_thumb_path, hero_is_generated, vetted FROM fits WHERE id = %s",
            (fit_id,),
        )
        sources = {
            r["field_name"]: r["source"]
            for r in db.fetch_all(
                conn,
                "SELECT field_name, source FROM fit_field_sources WHERE fit_id = %s",
                (fit_id,),
            )
        }
        all_jobs = db.fetch_all(
            conn,
            "SELECT id, text, item_id, done, done_at FROM fit_preconditions "
            "WHERE fit_id = %s ORDER BY done, id",
            (fit_id,),
        )
        worn = db.fetch_all(
            conn,
            "SELECT id, worn_on, rating, note FROM wear_events WHERE fit_id = %s "
            "ORDER BY worn_on DESC",
            (fit_id,),
        )
        worn_photos = db.fetch_all(
            conn,
            "SELECT p.stored_path, p.thumb_path, w.worn_on FROM wear_event_photos p "
            "JOIN wear_events w ON w.id = p.wear_event_id WHERE w.fit_id = %s "
            "ORDER BY w.worn_on DESC, p.sort_order",
            (fit_id,),
        )

    return render_template(
        "fit.html",
        fit=fit,
        row=row,
        meta=meta,
        ratings=ratings,
        sources=sources,
        jobs=all_jobs,
        worn=worn,
        worn_photos=worn_photos,
        thumbs=thumbs,
        problems=picker.staleness(fit),
        rules=seed_data.STYLING_RULES,
    )


@app.route("/fit/<fit_id>/killer", methods=["POST"])
def fit_killer(fit_id: str):
    """Max's promotion flag. Only ever set by him, right here."""
    killer = request.form.get("killer") == "1"
    with db.connect() as conn:
        conn.execute("UPDATE fits SET killer = %s WHERE id = %s", (killer, fit_id))
        conn.commit()
    return redirect(request.form.get("next") or url_for("fit_detail", fit_id=fit_id))


@app.route("/fit/<fit_id>/score", methods=["POST"])
def fit_score(fit_id: str):
    """Max's own 1-10. Typed by him; nothing else ever writes this column."""
    raw = (request.form.get("score") or "").strip()
    score = int(raw) if raw else None
    if score is not None and not 1 <= score <= 10:
        abort(400)
    with db.connect() as conn:
        conn.execute("UPDATE fits SET score = %s WHERE id = %s", (score, fit_id))
        conn.commit()
    flash("Score saved." if score else "Score cleared.")
    return redirect(url_for("fit_detail", fit_id=fit_id))


@app.route("/fit/<fit_id>/style", methods=["POST"])
def fit_style(fit_id: str):
    with db.connect() as conn:
        conn.execute(
            "UPDATE fits SET style = %s WHERE id = %s",
            ((request.form.get("style") or "").strip() or None, fit_id),
        )
        # Once he has touched it, it stops being a draft and the importer
        # stops offering one.
        conn.execute(
            "INSERT INTO fit_field_sources (fit_id, field_name, source) "
            "VALUES (%s, 'style', 'manual') "
            "ON CONFLICT (fit_id, field_name) DO UPDATE SET source = 'manual', "
            "updated_at = now()",
            (fit_id,),
        )
        conn.commit()
    return redirect(url_for("fit_detail", fit_id=fit_id))


@app.route("/precondition/<int:job_id>", methods=["POST"])
def precondition_done(job_id: int):
    done = request.form.get("done") == "1"
    with db.connect() as conn:
        conn.execute(
            "UPDATE fit_preconditions SET done = %s, done_at = CASE WHEN %s THEN now() "
            "ELSE NULL END WHERE id = %s",
            (done, done, job_id),
        )
        conn.commit()
    flash("Job done." if done else "Job reopened.")
    return redirect(request.form.get("next") or url_for("fits_view"))


# -------------------------------------------------------------- wear log --


@app.route("/log")
def log_view():
    rate = request.args.get("rate", type=int)
    with db.connect() as conn:
        events = db.fetch_all(
            conn,
            "SELECT w.*, f.name AS fit_name, f.id AS fit_slug "
            "FROM wear_events w LEFT JOIN fits f ON f.id = w.fit_id "
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
            (
                rating,
                request.form.get("note") or None,
                request.form.get("context") or None,
                event_id,
            ),
        )
        conn.commit()
    flash("Saved.")
    return redirect(url_for("log_view"))


# --------------------------------------------------------------- laundry --


@app.route("/laundry")
def laundry_view():
    with db.connect() as conn:
        states = db.fetch_all(conn, "SELECT * FROM laundry_states ORDER BY sort_order")
        items = db.fetch_all(
            conn,
            ITEM_SELECT + " WHERE i.scope_code = 'core' AND i.retired_at IS NULL"
            " ORDER BY c.sort_order, i.name",
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

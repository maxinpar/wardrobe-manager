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
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from werkzeug.utils import secure_filename

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

from . import config, db, fit_derive, picker, seed_data, wardrobes, week

app = Flask(__name__)
app.secret_key = "wardrobe-local"  # only used for flash messages on localhost

TZ = ZoneInfo(config.TIMEZONE)


def today() -> date:
    return datetime.now(TZ).date()


@app.before_request
def require_login():
    """No auth in v1. Add it here if this ever leaves the LAN."""
    return None


@app.context_processor
def header_weather():
    """The header's read-only weather chips. Today is where it's actually set."""
    try:
        with db.connect() as conn:
            raw = get_setting(conn, "weather.temp_c", "18")
            rain = get_setting(conn, "weather.rain", "0") == "1"
    except Exception:
        raw, rain = "18", False
    try:
        temp_c = float(raw)
        label = f"{temp_c:g}°C"
    except (TypeError, ValueError):
        temp_c, label = None, "—"
    return {
        "weather": {
            "temp_c": temp_c,
            "temp_label": label,
            "band": picker.weather_band(temp_c),
            "rain": rain,
        }
    }


# --------------------------------------------------- the two wardrobes --


def get_wardrobe(conn) -> str:
    return wardrobes.normalise(get_setting(conn, "wardrobe.mode", wardrobes.DEFAULT))


@app.context_processor
def header_wardrobe():
    """The wardrobe switch, on every page, with the size of each side on it.

    The counts are what the switch is FOR: they say how much of the closet each
    mode reaches. They are counted the same way the closet counts, so the number
    on the pill and the number of cards below it cannot drift apart.
    """
    try:
        with db.connect() as conn:
            mode = get_wardrobe(conn)
            counts = {
                m: db.fetch_one(
                    conn,
                    "SELECT count(*) AS n FROM items i WHERE i.retired_at IS NULL "
                    "AND i.gone_at IS NULL AND i.verdict_code = 'Keep' AND "
                    + wardrobes.clause(m),
                )["n"]
                for m in wardrobes.MODES
            }
    except Exception:
        mode, counts = wardrobes.DEFAULT, {m: 0 for m in wardrobes.MODES}
    return {
        "wardrobe": mode,
        "wardrobe_counts": counts,
        "wardrobe_modes": wardrobes.MODES,
        "wardrobe_labels": wardrobes.LABELS,
        "never_pluralised": wardrobes.NEVER_PLURALISED,
    }


@app.route("/wardrobe/<mode>", methods=["POST"])
def set_wardrobe(mode: str):
    """Flip the whole app between the everyday and golf wardrobes.

    Switching CLEARS the builder draft, the selected fit and the selected
    garment. A half-migrated draft — work trousers in a golf fit — is worse than
    an empty one, so the redirect drops those keys rather than carrying them.
    """
    if mode not in wardrobes.MODES:
        abort(404)
    with db.connect() as conn:
        set_setting(conn, "wardrobe.mode", mode)
        conn.commit()

    target = request.form.get("next") or url_for("today_view")
    split = urlsplit(target)
    if split.scheme or split.netloc:      # never redirect off-site
        return redirect(url_for("today_view"))
    keep = [
        part
        for part in split.query.split("&")
        if part and part.split("=")[0] not in ("item", "fit", "rank", "cat")
    ]
    return redirect(split.path + ("?" + "&".join(keep) if keep else ""))


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
       -- "has an image" is not "has been photographed". Three states, badged
       -- separately: photographed, render-only (the crew tees), and nothing.
       (SELECT count(*) FROM photos p
         WHERE p.item_id = i.id AND NOT p.is_render
           AND NOT starts_with(p.source_filename, i.id)) > 0 AS has_group_shot,
       (SELECT count(*) FROM photos p
         WHERE p.item_id = i.id AND p.is_render) > 0 AS has_render,
       (SELECT count(*) FROM photos p
         WHERE p.item_id = i.id AND NOT p.is_render
           AND starts_with(p.source_filename, i.id)) > 0 AS photographed,
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
    """What to wear today, in the week it belongs to.

    A fit is a base plus a top: the base holds Monday to Friday and only the top
    rotates, so this screen is a week with today marked, not a single day.
    """
    with db.connect() as conn:
        temp_raw = request.args.get("temp") or get_setting(conn, "weather.temp_c", "18")
        rain_raw = request.args.get("rain")
        rain = (
            get_setting(conn, "weather.rain", "0") == "1"
            if rain_raw is None
            else rain_raw == "1"
        )
        allow_disliked = request.args.get("allow_disliked") == "1"

        try:
            temp_c = float(temp_raw)
        except (TypeError, ValueError):
            temp_c = None

        if request.args.get("temp") is not None or rain_raw is not None:
            set_setting(conn, "weather.temp_c", str(temp_c if temp_c is not None else ""))
            set_setting(conn, "weather.rain", "1" if rain else "0")
            conn.commit()

        now = today()
        start = week.week_start(now)
        today_index = week.weekday_index(now)
        plan = week.get_or_create(conn, now)

        mode = get_wardrobe(conn)
        golf_fits = golf_fit_ids(conn)
        # Today picks out of the active wardrobe only. With no fit to show, the
        # whole layout is suppressed rather than drawn around a null pick —
        # `showing` stays None and today.html renders its empty card.
        fits = {
            f.id: f
            for f in picker.load_fits(conn)
            if (f.id in golf_fits) == (mode == "golf")
        }
        _, ranked, rejected = picker.pick(
            list(fits.values()), now, temp_c=temp_c, rain=rain, allow_disliked=allow_disliked
        )

        # Which fit is showing: the adopted base if there is one, otherwise the
        # picker's ranking, which `rank` steps through.
        rank_index = request.args.get("rank", type=int) or 0
        showing = None
        adopted = plan["base_fit_id"] and fits.get(plan["base_fit_id"])
        if adopted and not request.args.get("rank"):
            showing = next((c for c in ranked if c.fit.id == adopted.id), None)
        if showing is None and ranked:
            rank_index = max(0, min(rank_index, len(ranked) - 1))
            showing = ranked[rank_index]
        if showing is not None:
            rank_index = ranked.index(showing)

        day_index = request.args.get("day", type=int)
        day_index = today_index if day_index is None else max(0, min(day_index, 4))

        week_days = week.days(conn, start)
        rotation = week.rotation(conn, showing.fit) if showing else []

        # A week nobody has planned still shows a plan — from the rotation of
        # whatever fit is on screen — it just isn't stored until you adopt it.
        for row in week_days:
            if row["top_item_id"] is None and rotation:
                row["top_item_id"] = rotation[row["weekday"] % len(rotation)]
                row["provisional"] = True
                item = db.fetch_one(
                    conn, "SELECT name, hex FROM items WHERE id = %s", (row["top_item_id"],)
                )
                row["top_name"], row["top_hex"] = item["name"], item["hex"]
            row["is_today"] = row["weekday"] == today_index
            row["is_past"] = row["weekday"] < today_index
            row["selected"] = row["weekday"] == day_index

        selected_day = week_days[day_index]
        day_top = selected_day["top_item_id"]

        pieces = week.base_pieces(showing.fit, day_top) if showing else []
        if showing and day_top and not any(p["item_id"] == day_top for p in pieces):
            top = db.fetch_one(
                conn,
                "SELECT id AS item_id, name FROM items WHERE id = %s",
                (day_top,),
            )
            pieces.insert(0, {**top, "role": "top", "note": None, "is_alternate": False})

        bike = (
            week.bike_notes(conn, showing.fit, pieces)
            if showing and selected_day["commutes"]
            else None
        )
        renders = item_renders(conn)
        wearings = wearings_by_fit(conn).get(showing.fit.id, 0) if showing else 0
        meta = fit_metadata(conn).get(showing.fit.id, {}) if showing else {}

    return render_template(
        "today.html",
        showing=showing,
        # Two different nothings, and they need different words: a wardrobe with
        # no fits in it at all, versus one whose fits are all blocked today.
        wardrobe_empty=not fits,
        pieces=pieces,
        base=[p for p in pieces if p["role"] != "top"],
        day_top=day_top,
        week_days=week_days,
        selected_day=selected_day,
        today_index=today_index,
        day_index=day_index,
        adopted=bool(adopted and showing and adopted.id == showing.fit.id),
        bike=bike,
        renders=renders,
        meta=meta,
        wearings=wearings,
        rank_index=rank_index,
        rank_total=len(ranked),
        rejected=rejected,
        temp_c=temp_c,
        rain=rain,
        allow_disliked=allow_disliked,
        band=picker.weather_band(temp_c),
        day=now,
    )


@app.route("/today/adopt", methods=["POST"])
def adopt_fit():
    """Adopting a fit sets this week's base and plans the tops over it."""
    fit_id = request.form["fit_id"]
    with db.connect() as conn:
        fits = {f.id: f for f in picker.load_fits(conn)}
        fit = fits.get(fit_id)
        if fit is None:
            abort(404)
        start = week.week_start(today())
        week.get_or_create(conn, today())
        week.adopt(conn, start, fit)
        conn.commit()
    flash(f"“{fit.name}” is this week's base. Only the top changes now.")
    return redirect(request.form.get("next") or url_for("today_view"))


@app.route("/today/day/<int:weekday>/context", methods=["POST"])
def set_day_context(weekday: int):
    """Office or home. The default pattern is a starting point, not a rule."""
    context = request.form["context"]
    with db.connect() as conn:
        week.get_or_create(conn, today())
        conn.execute(
            "UPDATE week_days SET context_code = %s WHERE week_start = %s AND weekday = %s",
            (context, week.week_start(today()), weekday),
        )
        conn.commit()
    return redirect(request.form.get("next") or url_for("today_view", day=weekday))


@app.route("/today/day/<int:weekday>/top", methods=["POST"])
def set_day_top(weekday: int):
    with db.connect() as conn:
        week.get_or_create(conn, today())
        conn.execute(
            "UPDATE week_days SET top_item_id = %s WHERE week_start = %s AND weekday = %s",
            (request.form["item_id"], week.week_start(today()), weekday),
        )
        conn.commit()
    return redirect(request.form.get("next") or url_for("today_view", day=weekday))


@app.route("/today/wear", methods=["POST"])
def wear_today():
    """Log today's wearing, and record it against the day in the week.

    Only the garments actually worn go to `worn` — and `worn` does not block a
    fit, which is the point of a base that holds for five days. Only the wash
    and the tailor block.
    """
    fit_id = request.form["fit_id"]
    item_ids = request.form.getlist("item_id")

    with db.connect() as conn:
        fit = db.fetch_one(conn, "SELECT id, name FROM fits WHERE id = %s", (fit_id,))
        if fit is None:
            abort(404)

        context = request.form.get("context") or None
        row = db.fetch_one(
            conn,
            "INSERT INTO wear_events (worn_on, fit_id, context, temp_c, rain) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (
                today(),
                fit["id"],
                context,
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

        # Tie it to the day, so the week strip shows what actually happened.
        week.get_or_create(conn, today())
        conn.execute(
            "UPDATE week_days SET wear_event_id = %s WHERE week_start = %s AND weekday = %s",
            (event_id, week.week_start(today()), week.weekday_index(today())),
        )
        conn.commit()

    flash(f"Logged “{fit['name']}”. Those garments are marked worn — still wearable.")
    return redirect(request.form.get("next") or url_for("today_view"))


@app.route("/closet")
@app.route("/catalogue")
def catalogue():
    """The closet: every garment, grouped, with what state it's in.

    A binned garment drops out of here but is not deleted — it stays behind the
    `Gone` filter, keeps its wear history, and stays in the fits that use it.
    """
    filters = {
        "cat": request.args.get("cat") or "",
        "state": request.args.get("state") or "",
        "decision": request.args.get("decision") == "1",
        "no_render": request.args.get("no_render") == "1",
        "gone": request.args.get("gone") == "1",
        "q": (request.args.get("q") or "").strip(),
    }
    selected_id = request.args.get("item") or ""

    where = ["i.retired_at IS NULL"]
    params: list = []
    where.append("i.gone_at IS NOT NULL" if filters["gone"] else "i.gone_at IS NULL")

    if filters["cat"]:
        where.append("i.cat_code = %s")
        params.append(filters["cat"])
    if filters["state"]:
        where.append("COALESCE(l.state_code, 'clean') = %s")
        params.append(filters["state"])
    if filters["decision"]:
        # Anything carrying an unresolved judgement.
        where.append("i.verdict_code IN ('Tailor', 'Replace', 'Bin')")
    if filters["q"]:
        where.append(
            "(i.name ILIKE %s OR i.colour ILIKE %s OR i.material ILIKE %s "
            "OR i.notes ILIKE %s)"
        )
        params.extend([f"%{filters['q']}%"] * 4)

    with db.connect() as conn:
        # The closet shows one wardrobe at a time. This is not a chip you can
        # clear — the switch in the header is the only way out of it.
        mode = get_wardrobe(conn)
        where.append(wardrobes.clause(mode))
        sql = (
            ITEM_SELECT + " WHERE " + " AND ".join(where)
            + " ORDER BY c.sort_order, i.name"
        )
        items = db.fetch_all(conn, sql, params)
        lookups = load_lookups(conn)

        # The category chips are derived from what is actually in the active
        # wardrobe, never a fixed list. A hardcoded one omitted Hats and Shorts
        # — the two categories the golf wardrobe is mostly made of — so its
        # largest groups had no way to be reached.
        lookups["categories"] = db.fetch_all(
            conn,
            "SELECT c.* FROM categories c WHERE EXISTS ("
            "  SELECT 1 FROM items i WHERE i.cat_code = c.code"
            "    AND i.retired_at IS NULL AND i.gone_at IS NULL AND "
            + wardrobes.clause(mode)
            + ") ORDER BY c.sort_order",
        )
        usage = {
            r["item_id"]: r["n"]
            for r in db.fetch_all(
                conn,
                "SELECT item_id, count(DISTINCT fit_id) AS n FROM fit_items GROUP BY item_id",
            )
        }
        gone_count = db.fetch_one(
            conn,
            "SELECT count(*) AS n FROM items WHERE gone_at IS NOT NULL AND retired_at IS NULL",
        )["n"]
        total = db.fetch_one(
            conn,
            "SELECT count(*) AS n FROM items i WHERE i.retired_at IS NULL "
            "AND i.gone_at IS NULL AND " + wardrobes.clause(mode),
        )["n"]

        selected = None
        if selected_id:
            selected = db.fetch_one(conn, ITEM_SELECT + " WHERE i.id = %s", (selected_id,))
            if selected is None:
                abort(404)
            selected = dict(selected)
            selected["photos"] = db.fetch_all(
                conn,
                "SELECT p.*, a.label AS angle_label FROM photos p "
                "LEFT JOIN photo_angles a ON a.code = p.angle_code "
                "WHERE p.item_id = %s ORDER BY p.is_render DESC, p.sort_order",
                (selected_id,),
            )
            selected["fits"] = db.fetch_all(
                conn,
                "SELECT DISTINCT f.id, f.name, fi.role, fi.is_alternate FROM fit_items fi "
                "JOIN fits f ON f.id = fi.fit_id WHERE fi.item_id = %s ORDER BY f.name",
                (selected_id,),
            )
            selected["actions"] = db.fetch_all(
                conn,
                "SELECT id, required, status, note FROM item_actions "
                "WHERE item_id = %s ORDER BY status, id",
                (selected_id,),
            )
            selected["occasions"] = db.fetch_all(
                conn,
                "SELECT o.label FROM item_occasions io JOIN occasions o "
                "ON o.code = io.occasion_code WHERE io.item_id = %s ORDER BY o.sort_order",
                (selected_id,),
            )

    if filters["no_render"]:
        items = [i for i in items if not i["thumb_is_render"]]

    groups: dict[str, list] = {}
    for item in items:
        groups.setdefault(item["cat_label"], []).append(item)

    summary = {
        "shown": len(items),
        "total": total,
        "no_render": sum(1 for i in items if not i["thumb_is_render"]),
        "not_clean": sum(1 for i in items if i["laundry_state"] != "clean"),
        "gone": gone_count,
    }

    filters_query = {k: v for k, v in request.args.items() if k != "item"}

    return render_template(
        "closet.html",
        filters_query=filters_query,
        groups=groups,
        filters=filters,
        lookups=lookups,
        usage=usage,
        summary=summary,
        selected=selected,
        states=lookups["states"],
        verdicts=lookups["verdicts"],
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
    """The garment detail is a drawer over the closet now."""
    return redirect(url_for("catalogue", item=item_id))


@app.route("/closet/bulk", methods=["POST"])
def closet_bulk():
    """Move everything selected to one laundry state."""
    state = request.form["state"]
    item_ids = request.form.getlist("item_id")
    with db.connect() as conn:
        for item_id in item_ids:
            set_laundry(conn, item_id, state)
        conn.commit()
    flash(f"{len(item_ids)} garment(s) → {state.replace('_', ' ')}.")
    return redirect(request.form.get("next") or url_for("catalogue"))


@app.route("/item/<item_id>/verdict", methods=["POST"])
def item_verdict(item_id: str):
    """Set the verdict by hand, and make it stick against the next import."""
    verdict = request.form["verdict"]
    with db.connect() as conn:
        conn.execute(
            "UPDATE items SET verdict_code = %s WHERE id = %s", (verdict, item_id)
        )
        conn.execute(
            "INSERT INTO item_field_sources (item_id, field_name, source, note) "
            "VALUES (%s, 'verdict_code', 'manual', 'set in the app') "
            "ON CONFLICT (item_id, field_name) DO UPDATE SET source = 'manual', "
            "updated_at = now()",
            (item_id,),
        )
        conn.commit()
    return redirect(request.form.get("next") or url_for("catalogue", item=item_id))


@app.route("/item/<item_id>/gone", methods=["POST"])
def item_gone(item_id: str):
    """Binned: it has physically gone. Reversible, and nothing is deleted."""
    gone = request.form.get("gone") == "1"
    with db.connect() as conn:
        row = db.fetch_one(conn, "SELECT name FROM items WHERE id = %s", (item_id,))
        if row is None:
            abort(404)
        conn.execute(
            "UPDATE items SET gone_at = %s WHERE id = %s",
            (datetime.now(TZ) if gone else None, item_id),
        )
        # Stamped manual either way: whether a garment still exists is Max's
        # call, so an older export must not be able to bin it again — or, worse,
        # quietly put a binned one back in the rotation.
        conn.execute(
            "INSERT INTO item_field_sources (item_id, field_name, source, note) "
            "VALUES (%s, 'gone_at', 'manual', %s) "
            "ON CONFLICT (item_id, field_name) "
            "DO UPDATE SET source = 'manual', note = EXCLUDED.note, updated_at = now()",
            (item_id, "binned in the app" if gone else "put back in the closet"),
        )
        affected = db.fetch_one(
            conn,
            "SELECT count(DISTINCT fit_id) AS n FROM fit_items WHERE item_id = %s",
            (item_id,),
        )["n"]
        conn.commit()

    if gone:
        flash(
            f"“{row['name']}” has gone. {affected} fit(s) that use it stay, marked as "
            "needing a substitute — nothing was deleted."
        )
    else:
        flash(f"“{row['name']}” is back in the closet.")
    return redirect(request.form.get("next") or url_for("catalogue", item=item_id))


@app.route("/item/<item_id>/state", methods=["POST"])
def item_state(item_id: str):
    state = request.form["state"]
    with db.connect() as conn:
        set_laundry(conn, item_id, state)
        conn.commit()
    return redirect(request.form.get("next") or url_for("item_detail", item_id=item_id))


# ------------------------------------------------------------------ fits --

# The roles the builder offers live in wardrobes.py, because there are now two
# anatomies of them — the everyday one and the golf one — and they are easier to
# read side by side than apart. The builder's "knit" and "top" slots both land
# in the `top` role either way, because that is how the data already models
# them: when a fit has both, the knit is the top and the polo or tee goes
# underneath as the `base`. See slot_roles().

# Sort order for the pieces in the detail drawer. `hat` is the golf builder's
# slot name; it saves as `accessory` because the fit schema has no hat role.
ROLE_ORDER = ["hat", "outer", "layer", "top", "base", "bottom", "shoe", "belt", "accessory"]


def crested_ids(conn) -> set[str]:
    """Every garment the catalogue says carries a club crest."""
    return {
        row["id"]
        for row in db.fetch_all(conn, "SELECT id, formality_note FROM items")
        if wardrobes.is_crested(row["formality_note"])
    }


def golf_ids(conn) -> set[str]:
    return {
        row["id"]
        for row in db.fetch_all(
            conn, "SELECT i.id FROM items i WHERE " + wardrobes.GOLF_CLAUSE
        )
    }


def golf_fit_ids(conn) -> set[str]:
    """Which fits belong to the golf wardrobe.

    The occasion is the real answer. The second half is a safety net for fits
    saved before any of the golf tagging existed: a fit built on a crested club
    polo is a golf fit whatever its metadata says. A plain golf polo is not
    enough on its own — half the golf wardrobe is deliberately wearable off the
    course, and treating those as proof would drag everyday fits across.
    """
    ids = {
        row["fit_id"]
        for row in db.fetch_all(
            conn,
            "SELECT DISTINCT fit_id FROM fit_occasions "
            "WHERE occasion_code = 'golf' AND kind = 'good'",
        )
    }
    crested_golf = golf_ids(conn) & crested_ids(conn)
    if crested_golf:
        ids |= {
            row["fit_id"]
            for row in db.fetch_all(
                conn,
                "SELECT DISTINCT fit_id FROM fit_items WHERE item_id = ANY(%s)",
                (sorted(crested_golf),),
            )
        }
    return ids


def builder_pool(conn, mode: str, role: str, cats: tuple[str, ...]) -> tuple[list, bool]:
    """The garments offered for one slot, and whether they had to be borrowed.

    Two rules the first build got wrong and that are worth stating:
      * NO CAP. A `.slice(0, 10)` is the single reason the wardrobe felt
        invisible — most of the closet could not be reached from the builder.
      * NO RENDER REQUIRED. Requiring a picture hid every render-less garment;
        they fall back to a hex swatch instead.
    """
    sql = (
        "SELECT id, name, cat_code, hex, warmth, formality_rank, rain_unsafe, "
        "formality_note FROM items i "
        "WHERE i.retired_at IS NULL AND i.gone_at IS NULL AND i.scope_code = 'core' "
        "AND i.verdict_code IN ('Keep', 'Tailor') AND i.cat_code = ANY(%s) AND "
    )
    rows = db.fetch_all(conn, sql + wardrobes.clause(mode) + " ORDER BY name", (list(cats),))
    if rows or mode != "golf" or role != wardrobes.BORROWED_SLOT:
        return rows, False

    # Nothing in Knitwear or Outerwear is tagged golf, so the slot borrows light
    # casual layers rather than showing an empty shelf — and says that it did.
    borrowed = db.fetch_all(
        conn,
        sql + wardrobes.EVERYDAY_CLAUSE
        + " AND COALESCE(i.warmth, 3) <= %s ORDER BY name",
        (list(cats), wardrobes.BORROWED_MAX_WARMTH),
    )
    return borrowed, True


# Chip order for the REGISTER group. Anything not listed still shows, after
# these, alphabetically — a new register appears in the bar on its own.
REGISTER_ORDER = ("everyday", "sharp", "casual")


class FitFilters:
    """Gallery filter state. Query-side only — filters never mutate a fit."""

    KEYS = ("register", "killer", "state", "band", "occasion", "hidden", "binned", "mode")

    def __init__(self, args):
        self.register = args.get("register") or ""
        self.killer = args.get("killer") == "1"
        self.state = args.get("state") or ""       # wearable | blocked
        self.band = args.get("band") or ""
        self.occasion = args.get("occasion") or ""
        self.hidden = args.get("hidden") == "1"
        # Binned fits are their own shelf, not a mixed-in extra: on, you see
        # only them, exactly as the Closet does for binned garments.
        self.binned = args.get("binned") == "1"
        # Not a filter: which way the same set of fits is drawn. It rides in the
        # query with them so that changing a chip doesn't throw you back to
        # Details, and so a view can be linked to.
        self.mode = "renders" if args.get("mode") == "renders" else "details"

    def current(self) -> dict:
        out = {}
        if self.mode != "details":
            out["mode"] = self.mode
        if self.register:
            out["register"] = self.register
        if self.killer:
            out["killer"] = "1"
        if self.state:
            out["state"] = self.state
        if self.band:
            out["band"] = self.band
        if self.occasion:
            out["occasion"] = self.occasion
        if self.hidden:
            out["hidden"] = "1"
        if self.binned:
            out["binned"] = "1"
        return out

    def toggled(self, param: str, value: str) -> dict:
        """The query for clicking a filter chip: on if off, off if already on."""
        out = self.current()
        if param in ("killer", "hidden", "binned"):
            if out.get(param):
                out.pop(param)
            else:
                out[param] = "1"
        elif not value:
            out.pop(param, None)
        elif out.get(param) == value:
            out.pop(param)
        else:
            out[param] = value
        return out

    def in_mode(self, mode: str) -> dict:
        """The same filters, drawn the other way."""
        out = self.current()
        out.pop("mode", None)
        if mode != "details":
            out["mode"] = mode
        return out


def item_renders(conn) -> dict[str, dict]:
    """item_id -> the image to show it with.

    The retail render wins: they are all shot on white, which is why every photo
    ground in this design is white. A real photo of the garment is the fallback,
    and the hex swatch the fallback after that.
    """
    rows = db.fetch_all(
        conn,
        """
        SELECT i.id, i.hex, i.name,
               (SELECT p.thumb_path FROM photos p
                 WHERE p.item_id = i.id
                   AND (p.is_render OR starts_with(p.source_filename, i.id))
                 ORDER BY p.is_render DESC, p.sort_order LIMIT 1) AS thumb
        FROM items i WHERE i.retired_at IS NULL
        """,
    )
    return {r["id"]: {"thumb": r["thumb"], "hex": r["hex"], "name": r["name"]} for r in rows}


def fit_rows(conn) -> dict[str, dict]:
    rows = db.fetch_all(
        conn,
        "SELECT id, source, formality_rank, rain_safe, hero_image_path, "
        "hero_thumb_path, hero_is_generated, vetted, composition_known, "
        "category_code FROM fits",
    )
    return {r["id"]: r for r in rows}


def fit_sources(conn) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for row in db.fetch_all(
        conn, "SELECT fit_id, field_name, source FROM fit_field_sources"
    ):
        out.setdefault(row["fit_id"], {})[row["field_name"]] = row["source"]
    return out


def fit_categories(conn) -> list[dict]:
    """The authored categories, in the authored order.

    `sort_order` is that order and the only one: reading it here rather than
    hard-coding a list means a category added by a migration lands where the
    migration put it, and a fit moved between categories lands where the
    category belongs rather than where the first fit happened to appear.
    """
    return db.fetch_all(
        conn, "SELECT code, label, sort_order FROM fit_categories ORDER BY sort_order, code"
    )


# The trailing section. Its cards are never hidden — a fit with no category
# still has to be reachable, and hiding it was a real bug in the first pass.
UNCATEGORISED = "Not in a category yet"

# Migration 063 wrote the golf labels as "Golf — Old school". The separator is
# an em dash there and a middle dot elsewhere in the app, so both are tried.
GOLF_LABEL_PREFIXES = ("Golf — ", "Golf · ", "Golf - ")


def strip_golf_prefix(label: str) -> str:
    for prefix in GOLF_LABEL_PREFIXES:
        if label.startswith(prefix):
            return label[len(prefix):]
    return label


def section_cards(cards: list[dict], categories: list[dict]) -> list[dict] | None:
    """Group the grid into category sections, or None to leave it flat.

    None when nothing in this wardrobe carries a category: headers over a single
    unnamed section are furniture, not structure. Empty categories are dropped —
    six of the nine golf ones have no fits and would otherwise be six headers
    over nothing — but every one of them is still offered in the fit pane's
    picker, which is where an empty category is useful.
    """
    if not any(c["meta"].get("category") for c in cards):
        return None

    by_code: dict[str, list] = {}
    for card in cards:
        by_code.setdefault(card["meta"].get("category") or "", []).append(card)

    sections = []
    for category in categories:
        group = by_code.get(category["code"])
        if group:
            sections.append(
                {
                    "code": category["code"],
                    # "Golf — Old school" reads as "Old school" here: the
                    # wardrobe switch in the header has already said Golf, and
                    # saying it again on every heading is the app talking to
                    # itself. Only that exact prefix is stripped — a category
                    # actually called "Golf" would keep its name.
                    "label": strip_golf_prefix(category["label"]),
                    "cards": group,
                }
            )
    if by_code.get(""):
        sections.append({"code": "", "label": UNCATEGORISED, "cards": by_code[""]})
    return sections


def wearings_by_fit(conn) -> dict[str, int]:
    return {
        r["fit_id"]: r["n"]
        for r in db.fetch_all(
            conn,
            "SELECT fit_id, count(*) AS n FROM wear_events "
            "WHERE fit_id IS NOT NULL GROUP BY fit_id",
        )
    }


def build_cards(conn):
    """Everything the gallery and the drawer need, in one pass."""
    fits = picker.load_fits(conn)
    meta = fit_metadata(conn)
    rows = fit_rows(conn)
    ratings = fit_ratings(conn)
    wearings = wearings_by_fit(conn)

    band_codes = {}
    for r in db.fetch_all(conn, "SELECT fit_id, band_code FROM fit_temp_bands"):
        band_codes.setdefault(r["fit_id"], []).append(r["band_code"])
    occasion_codes = {}
    for r in db.fetch_all(
        conn, "SELECT fit_id, occasion_code FROM fit_occasions WHERE kind = 'good'"
    ):
        occasion_codes.setdefault(r["fit_id"], []).append(r["occasion_code"])
    season_codes = {}
    for r in db.fetch_all(conn, "SELECT fit_id, season_code FROM fit_seasons"):
        season_codes.setdefault(r["fit_id"], []).append(r["season_code"])

    cards = []
    for fit in fits:
        row = rows.get(fit.id, {})
        m = dict(meta.get(fit.id, {"bands": [], "seasons": [], "good_for": [], "bad_for": [], "jobs": []}))
        m["formality_rank"] = row.get("formality_rank")
        m["rain_safe"] = row.get("rain_safe", True)
        m["authored"] = (row.get("source") or "").startswith("killer-looks")
        m["composition_known"] = row.get("composition_known", True)
        m["category"] = row.get("category_code")
        m["band_codes"] = band_codes.get(fit.id, [])
        m["occasion_codes"] = occasion_codes.get(fit.id, [])
        m["season_codes"] = season_codes.get(fit.id, [])

        # The hero now loads with the fit in picker.load_fits — one source, so
        # a screen that does not build cards still gets its render.

        cards.append(
            {
                "fit": fit,
                "meta": m,
                "problems": picker.staleness(fit),
                "gone_pieces": picker.gone_pieces(fit),
                "rating": ratings.get(fit.id),
                "wearings": wearings.get(fit.id, 0),
                "source": row.get("source"),
            }
        )
    return cards


@app.route("/fits")
def fits_view():
    filters = FitFilters(request.args)
    selected_id = request.args.get("fit") or ""
    building = request.args.get("build") == "1"

    with db.connect() as conn:
        mode = get_wardrobe(conn)
        golf_fits = golf_fit_ids(conn)
        # One wardrobe's fits. Everything below — the chip counts, the summary,
        # the empty state — is counted off this, so no number on the page can
        # describe a fit the page will not show.
        cards = [c for c in build_cards(conn)
                 if (c["fit"].id in golf_fits) == (mode == "golf")]
        renders = item_renders(conn)
        sources = fit_sources(conn)
        categories = fit_categories(conn)
        selected = None
        builder = None

        if selected_id:
            match = next((c for c in cards if c["fit"].id == selected_id), None)
            if match is None:
                abort(404)
            selected = dict(match)
            selected["sources"] = sources.get(selected_id, {})
            selected["pieces"] = sorted(
                match["fit"].items,
                key=lambda i: (ROLE_ORDER.index(i["role"]) if i["role"] in ROLE_ORDER else 99,
                               i["is_alternate"], i["position"]),
            )
            selected["jobs"] = db.fetch_all(
                conn,
                "SELECT id, text, done, done_at FROM fit_preconditions "
                "WHERE fit_id = %s ORDER BY done, id",
                (selected_id,),
            )
            selected["worn"] = db.fetch_all(
                conn,
                "SELECT worn_on, rating, note, context FROM wear_events "
                "WHERE fit_id = %s ORDER BY worn_on DESC",
                (selected_id,),
            )

        if building:
            crested = crested_ids(conn)
            builder = {
                "roles": [(r, label, opt) for r, label, opt, _ in wardrobes.roles(mode)],
                "candidates": {},
                "borrowed": {},
                "crested": crested,
                "mode": mode,
            }
            for role, label, _, cats in wardrobes.roles(mode):
                rows, borrowed = builder_pool(conn, mode, role, cats)
                builder["candidates"][role] = rows
                builder["borrowed"][role] = borrowed
            # The note under the switch is counted off the SAME pools the slots
            # render. Hardcoding it drifted immediately — the note claimed 18
            # legs while the slot showed 16, because two golf legs are Replace
            # and Tailor.
            builder["note_counts"] = [
                (len(builder["candidates"][role]), label)
                for role, label, _, _ in wardrobes.roles(mode)
                if not builder["borrowed"][role]
            ]

    # Counted over the live shelf — a binned fit is not "blocked", it is out.
    live = [c for c in cards if not c["fit"].gone]
    counts = {
        "total": len(live),
        "wearable": sum(1 for c in live if not c["problems"]),
        "blocked": sum(1 for c in live if c["problems"]),
        "rendered": sum(1 for c in live if c["fit"].render),
        "binned": len(cards) - len(live),
    }

    # Every chip carries a count. They answer "how many fits would this chip
    # show me", so they are NOT narrowed by the other active filters — only by
    # the roll-neck toggle, which decides what is on the shelf at all.
    base = [c for c in live if filters.hidden or not c["fit"].hidden_by_default]
    registers = sorted({c["fit"].register for c in base if c["fit"].register},
                       key=lambda r: (REGISTER_ORDER.index(r)
                                      if r in REGISTER_ORDER else 99, r))
    chip_counts = {
        "all": len(base),
        "register": {r: sum(1 for c in base if c["fit"].register == r)
                     for r in registers},
        "wearable": sum(1 for c in base if not c["problems"]),
        "blocked": sum(1 for c in base if c["problems"]),
        "killer": sum(1 for c in base if c["fit"].killer),
        "band": {b: sum(1 for c in base if b in c["meta"]["band_codes"])
                 for b in ("cold", "mild", "warm")},
        "occasion": {k: sum(1 for c in base if k in c["meta"]["occasion_codes"])
                     for k in ("client", "dinner")},
        # What the toggle would ADD, which is why it is written with a "+".
        "hidden": sum(1 for c in live if c["fit"].hidden_by_default),
        "binned": counts["binned"],
    }

    shown = []
    for c in cards:
        fit, m = c["fit"], c["meta"]
        # Binned is binned: out of the gallery unless you ask for that shelf.
        if fit.gone != filters.binned:
            continue
        if fit.hidden_by_default and not filters.hidden:
            continue
        if filters.register and fit.register != filters.register:
            continue
        if filters.killer and not fit.killer:
            continue
        if filters.state == "wearable" and c["problems"]:
            continue
        if filters.state == "blocked" and not c["problems"]:
            continue
        if filters.band and filters.band not in m["band_codes"]:
            continue
        if filters.occasion and filters.occasion not in m["occasion_codes"]:
            continue
        shown.append(c)

    # Renders is the same set of fits drawn at size, so it can only show the
    # ones that have an image — that is the whole point of the view, not a
    # filter you can clear.
    if filters.mode == "renders":
        shown = [c for c in shown if c["fit"].render]

    # A fit built on a garment that has gone sinks to the very bottom: it can
    # never come back on its own, unlike a wash or a tailoring job. Below that,
    # a fit with a render sorts first — the picture is the fastest way in.
    shown.sort(
        key=lambda c: (
            bool(c["gone_pieces"]),
            c["fit"].render is None,
            c["fit"].sort_order,
        )
    )

    return render_template(
        "fits.html",
        cards=shown,
        # Details only. Renders is one wall of pictures on purpose, and cutting
        # it into sections would put a heading between every four of them.
        sections=section_cards(shown, categories) if filters.mode != "renders" else None,
        categories=categories,
        # No fits at all in this wardrobe — not "no fits matching these chips".
        # The chips, the summary line and the grid are all suppressed for it:
        # rendering them with zeros ("All 0, Everyday 0, Sharp 0…" above blank
        # space) reads as broken rather than as empty.
        wardrobe_empty=not live,
        counts=counts,
        chip_counts=chip_counts,
        registers=registers,
        filters=filters,
        mode=filters.mode,
        renders=renders,
        selected=selected,
        building=building,
        builder=builder,
        rules=seed_data.STYLING_RULES,
    )


@app.route("/looks")
def looks_view():
    """Kept as a redirect. Looks is a mode of Fits, not a place of its own.

    It was briefly its own tab — that is where the renders view came from — but
    a fit and its picture are the same thing, so having both in the nav meant
    two doors into one room. The route stays so old links still land.
    """
    return redirect(url_for("fits_view", mode="renders"))


@app.route("/fit/<fit_id>")
def fit_detail(fit_id: str):
    """The detail is a drawer over the gallery now, not its own page."""
    return redirect(url_for("fits_view", fit=fit_id))


@app.route("/fit/<fit_id>/rename", methods=["POST"])
def fit_rename(fit_id: str):
    name = (request.form.get("name") or "").strip()
    if not name:
        abort(400)
    with db.connect() as conn:
        conn.execute("UPDATE fits SET name = %s WHERE id = %s", (name, fit_id))
        # From here the name is his, and the importer stops refreshing it from
        # the seed file.
        conn.execute(
            "INSERT INTO fit_field_sources (fit_id, field_name, source) "
            "VALUES (%s, 'name', 'manual') "
            "ON CONFLICT (fit_id, field_name) DO UPDATE SET source = 'manual', "
            "updated_at = now()",
            (fit_id,),
        )
        conn.commit()
    return redirect(request.form.get("next") or url_for("fits_view", fit=fit_id))


@app.route("/fit/<fit_id>/wear", methods=["POST"])
def fit_log_wear(fit_id: str):
    """Log a wearing of this fit: today, with an optional rating and note.

    The garments go to 'worn' the same way the Today screen does it.
    """
    rating = request.form.get("rating") or None
    with db.connect() as conn:
        fit = db.fetch_one(conn, "SELECT id, name FROM fits WHERE id = %s", (fit_id,))
        if fit is None:
            abort(404)
        row = db.fetch_one(
            conn,
            "INSERT INTO wear_events (worn_on, fit_id, rating, note) "
            "VALUES (%s, %s, %s, %s) RETURNING id",
            (today(), fit_id, rating, request.form.get("note") or None),
        )
        items = db.fetch_all(
            conn,
            "SELECT item_id FROM fit_items WHERE fit_id = %s AND NOT is_alternate",
            (fit_id,),
        )
        for item in items:
            conn.execute(
                "INSERT INTO wear_event_items (wear_event_id, item_id) VALUES (%s, %s)",
                (row["id"], item["item_id"]),
            )
            set_laundry(conn, item["item_id"], "worn")
        conn.commit()

    flash(f"Logged “{fit['name']}” for today. Those garments are now marked worn.")
    return redirect(request.form.get("next") or url_for("fits_view", fit=fit_id))


def slot_roles(picks: dict[str, str]) -> list[tuple[str, str]]:
    """Turn the builder's slots into (item_id, role) pairs.

    A knit and a top together mean the knit is worn over the top — knit takes
    the `top` role and the lighter garment becomes the `base` under it. That
    matches how fits-batch-2.md writes "knit + tee", and it is what keeps the
    week's rotation working: only the rotating layer is a Tops item.
    """
    rows = []
    knit, top = picks.get("knit"), picks.get("top")
    for slot, item_id in picks.items():
        if slot in ("knit", "top"):
            continue
        # The golf builder has a hat slot; the fit schema has no hat role, so it
        # saves as an accessory. A real `hat` role would be better — see the
        # open items in docs/HANDOFF-GOLF-WARDROBE.md.
        rows.append((item_id, "accessory" if slot == "hat" else slot))
    if knit and top:
        rows.append((knit, "top"))
        rows.append((top, "base"))
    elif knit:
        rows.append((knit, "top"))
    elif top:
        rows.append((top, "top"))
    return rows


def slugify(name: str) -> str:
    cleaned = "".join(c.lower() if c.isalnum() else "_" for c in name)
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_") or "untitled"


@app.route("/fits/new", methods=["POST"])
def fit_create():
    """Save a built fit.

    The metadata is derived server-side with wardrobe/fit_derive.py — the same
    rules the builder's strip previews — and recorded as 'derived', so a later
    hand-correction is authoritative and an import never overwrites it.
    """
    name = (request.form.get("name") or "").strip()
    picks = {
        slot: request.form.get(slot)
        for slot in wardrobes.ALL_SLOTS
        if request.form.get(slot)
    }
    rows = slot_roles(picks)
    if not name or len(rows) < 3:
        flash("A fit needs a name and at least three pieces.")
        return redirect(url_for("fits_view", build=1))

    with db.connect() as conn:
        mode = get_wardrobe(conn)
        fit_id = "fit_" + slugify(name)
        if db.fetch_one(conn, "SELECT id FROM fits WHERE id = %s", (fit_id,)):
            fit_id = f"{fit_id}_{today().strftime('%m%d')}"

        # The register stays `everyday`. The handoff asked for `casual`, which is
        # the prototype's vocabulary, not this database's — `registers` holds
        # everyday and sharp and nothing else, so writing casual is a foreign
        # key violation. It is also unnecessary: register says how dressed-up a
        # fit is, and what makes this a golf fit is the occasion below.
        conn.execute(
            "INSERT INTO fits (id, name, register_code, vetted, source, sort_order) "
            "VALUES (%s, %s, 'everyday', false, %s, 200)",
            (fit_id, name, f"built in the app {today().isoformat()}"),
        )
        for position, (item_id, role) in enumerate(rows, start=1):
            conn.execute(
                "INSERT INTO fit_items (fit_id, item_id, role, position) "
                "VALUES (%s, %s, %s, %s)",
                (fit_id, item_id, role, position),
            )

        garments = db.fetch_all(
            conn,
            """
            SELECT fi.item_id, fi.role, fi.position, fi.is_alternate,
                   i.cat_code AS cat, i.warmth, i.rain_unsafe, i.formality_rank,
                   (SELECT array_agg(io.occasion_code) FROM item_occasions io
                     WHERE io.item_id = i.id) AS occasions
            FROM fit_items fi JOIN items i ON i.id = fi.item_id
            WHERE fi.fit_id = %s
            """,
            (fit_id,),
        )
        bands = fit_derive.temp_bands(garments)
        for band in bands:
            conn.execute(
                "INSERT INTO fit_temp_bands (fit_id, band_code) VALUES (%s, %s)",
                (fit_id, band),
            )
        for season in fit_derive.seasons(bands):
            conn.execute(
                "INSERT INTO fit_seasons (fit_id, season_code) VALUES (%s, %s)",
                (fit_id, season),
            )
        occasions = fit_derive.good_for(garments)
        # A fit built in the golf wardrobe IS a golf fit, even when the derived
        # intersection loses the tag — and it does lose it as soon as the knit
        # slot borrows a casual layer, because nothing in Knitwear is tagged
        # golf. Without this the fit would save and then vanish from the
        # wardrobe it was built in.
        forced_golf = mode == "golf" and "golf" not in occasions
        if forced_golf:
            occasions = occasions + ["golf"]
        for occasion in occasions:
            conn.execute(
                "INSERT INTO fit_occasions (fit_id, occasion_code, kind) "
                "VALUES (%s, %s, 'good')",
                (fit_id, occasion),
            )
        conn.execute(
            "UPDATE fits SET rain_safe = %s, formality_rank = %s WHERE id = %s",
            (fit_derive.rain_safe(garments), fit_derive.formality_rank(garments), fit_id),
        )
        for field in ("temp_bands", "seasons", "good_for", "rain_safe", "formality_rank"):
            conn.execute(
                "INSERT INTO fit_field_sources (fit_id, field_name, source) "
                "VALUES (%s, %s, %s)",
                # good_for stops being derived the moment golf is forced onto
                # it: that came from which wardrobe Max was in, not from the
                # garments, and an import must not quietly derive it away.
                (fit_id, field, "manual" if field == "good_for" and forced_golf else "derived"),
            )
        # score, killer and style are never derived: they are Max's to set.
        for field in ("killer", "score"):
            conn.execute(
                "INSERT INTO fit_field_sources (fit_id, field_name, source) "
                "VALUES (%s, %s, 'manual')",
                (fit_id, field),
            )
        conn.commit()

    flash(f"Saved “{name}”. Its metadata is a first guess — correct anything that's wrong.")
    return redirect(url_for("fits_view", fit=fit_id))



# Where uploaded renders live, under the photo store. One file per fit, named
# from the fit id, so re-uploading replaces rather than accumulating.
RENDER_UPLOAD_DIR = "fits/uploads"
RENDER_MAX_EDGE = 1000       # the long edge; a 5/8 card needs nothing more
RENDER_QUALITY = 84


def store_render(fit_id: str, stream) -> str:
    """Save an uploaded render, downscaled. Returns the store-relative path.

    The client downscales before sending — a phone photo over wifi is the case
    this feature exists for — but the server does it again rather than trusting
    it, because a form posted without JavaScript sends the original file.
    """
    from PIL import Image

    image = Image.open(stream)
    image.load()                      # fails here, before anything is written,
    if image.mode not in ("RGB", "L"):  # if the file is not really an image
        image = image.convert("RGB")
    image.thumbnail((RENDER_MAX_EDGE, RENDER_MAX_EDGE), Image.LANCZOS)

    target_dir = config.photo_store() / RENDER_UPLOAD_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    name = f"{secure_filename(fit_id)}.jpg"
    image.save(target_dir / name, "JPEG", quality=RENDER_QUALITY, optimize=True)
    return f"{RENDER_UPLOAD_DIR}/{name}"


@app.route("/fit/<fit_id>/render", methods=["POST"])
def fit_render_upload(fit_id: str):
    """Attach a render to a fit. Beats every file-based source for this fit."""
    with db.connect() as conn:
        if db.fetch_one(conn, "SELECT 1 AS x FROM fits WHERE id = %s", (fit_id,)) is None:
            abort(404)

    upload = request.files.get("render")
    if upload is None or not upload.filename:
        flash("No image was chosen.")
        return redirect(request.form.get("next") or url_for("fits_view", fit=fit_id))

    try:
        stored = store_render(fit_id, upload.stream)
    except Exception:
        # A non-image is ignored rather than half-written; the design says a
        # dropped non-image is dropped silently, but a chosen one deserves a word.
        flash("That file isn't an image the app can read — nothing was changed.")
        return redirect(request.form.get("next") or url_for("fits_view", fit=fit_id))

    with db.connect() as conn:
        conn.execute(
            "UPDATE fits SET render_upload_path = %s, render_uploaded_at = %s "
            "WHERE id = %s",
            (stored, datetime.now(TZ), fit_id),
        )
        conn.commit()
    return redirect(request.form.get("next") or url_for("fits_view", fit=fit_id))


@app.route("/fit/<fit_id>/render/remove", methods=["POST"])
def fit_render_remove(fit_id: str):
    """Drop the upload. The file-based render underneath is untouched, so this
    reverts to it — or to the piece strip if there was never one."""
    with db.connect() as conn:
        row = db.fetch_one(
            conn, "SELECT render_upload_path FROM fits WHERE id = %s", (fit_id,)
        )
        if row is None:
            abort(404)
        conn.execute(
            "UPDATE fits SET render_upload_path = NULL, render_uploaded_at = NULL "
            "WHERE id = %s",
            (fit_id,),
        )
        conn.commit()

    if row["render_upload_path"]:
        stored = config.photo_store() / row["render_upload_path"]
        stored.unlink(missing_ok=True)
    return redirect(request.form.get("next") or url_for("fits_view", fit=fit_id))


@app.route("/fit/<fit_id>/gone", methods=["POST"])
def fit_gone(fit_id: str):
    """Bin a fit — you don't want it, or its garments have gone. Reversible.

    Nothing is deleted: the composition, the render, your score and every wear
    event stay. Distinct from hiding the roll-neck, which is a preference about
    a fit that is still in play.
    """
    gone = request.form.get("gone") == "1"
    with db.connect() as conn:
        row = db.fetch_one(conn, "SELECT name FROM fits WHERE id = %s", (fit_id,))
        if row is None:
            abort(404)
        conn.execute(
            "UPDATE fits SET gone_at = %s WHERE id = %s",
            (datetime.now(TZ) if gone else None, fit_id),
        )
        # Manual either way, on the same rule as a binned garment: whether a fit
        # is wanted is Max's call, so no later import can bin it or revive it.
        conn.execute(
            "INSERT INTO fit_field_sources (fit_id, field_name, source, note) "
            "VALUES (%s, 'gone_at', 'manual', %s) "
            "ON CONFLICT (fit_id, field_name) "
            "DO UPDATE SET source = 'manual', note = EXCLUDED.note, updated_at = now()",
            (fit_id, "binned in the app" if gone else "put back in the rotation"),
        )
        conn.commit()

    if gone:
        flash(
            f"“{row['name']}” is binned. It stops being offered and leaves the "
            "gallery — nothing was deleted, and the Binned shelf brings it back."
        )
    else:
        flash(f"“{row['name']}” is back in the rotation.")
    return redirect(request.form.get("next") or url_for("fits_view"))


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
    return redirect(request.form.get("next") or url_for("fits_view", fit=fit_id))


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
    return redirect(request.form.get("next") or url_for("fits_view", fit=fit_id))


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


# The six filter chips. Priority chips narrow the open list — a high-priority
# gap you have already bought is not something to go shopping for.
GAP_FILTERS = ("open", "high", "medium", "low", "bought", "not_a_gap")


def gap_matches(gap, show: str) -> bool:
    if show in ("bought", "not_a_gap"):
        return gap["status"] == show
    if show in ("high", "medium", "low"):
        return gap["status"] == "open" and gap["priority"] == show
    return gap["status"] == "open"


@app.route("/gaps")
def gaps_view():
    """What isn't in the wardrobe, why that hurts, and what would fix it.

    Hand-authored only. Nothing on this screen is derived from the closet at
    render time — `unlocks` in particular is a claim made when the gap was
    written, and computing it would let it drift.
    """
    show = request.args.get("show") or "open"
    if show not in GAP_FILTERS:
        show = "open"

    with db.connect() as conn:
        gaps = db.fetch_all(conn, "SELECT * FROM gaps ORDER BY sort_order, id")

        buy_at: dict[str, list[str]] = {}
        for r in db.fetch_all(
            conn, "SELECT gap_id, retailer FROM gap_buy_at ORDER BY gap_id, sort_order"
        ):
            buy_at.setdefault(r["gap_id"], []).append(r["retailer"])

        candidates: dict[str, list] = {}
        for r in db.fetch_all(
            conn,
            "SELECT id, gap_id, name, source, url, price, added_by FROM gap_candidates "
            "ORDER BY gap_id, added_by DESC, id",
        ):
            candidates.setdefault(r["gap_id"], []).append(r)

        replaces: dict[str, list] = {}
        for r in db.fetch_all(
            conn,
            "SELECT gr.gap_id, i.id, i.name FROM gap_replaces gr "
            "JOIN items i ON i.id = gr.item_id ORDER BY gr.gap_id, i.name",
        ):
            replaces.setdefault(r["gap_id"], []).append(r)

    for g in gaps:
        g["buy_at"] = buy_at.get(g["id"], [])
        g["candidates"] = candidates.get(g["id"], [])
        g["replaces"] = replaces.get(g["id"], [])

    # Counts are of exactly the rows each chip shows, so the header and the
    # chips can never disagree with the grid.
    counts = {f: sum(1 for g in gaps if gap_matches(g, f)) for f in GAP_FILTERS}

    return render_template(
        "gaps.html",
        gaps=[g for g in gaps if gap_matches(g, show)],
        counts=counts,
        show=show,
        total=len(gaps),
    )


@app.route("/gaps/<gap_id>/status", methods=["POST"])
def gap_status(gap_id: str):
    """Bought it, or not a gap after all. Both toggle back to open, and neither
    deletes anything — a decision you can reverse is worth recording."""
    wanted = request.form.get("status", "open")
    if wanted not in ("open", "bought", "not_a_gap"):
        abort(400)
    with db.connect() as conn:
        row = db.fetch_one(conn, "SELECT status FROM gaps WHERE id = %s", (gap_id,))
        if row is None:
            abort(404)
        # Pressing the button a second time puts it back.
        status = "open" if row["status"] == wanted else wanted
        conn.execute(
            "UPDATE gaps SET status = %s, status_changed_at = %s, updated_at = now() "
            "WHERE id = %s",
            (status, datetime.now(TZ) if status != "open" else None, gap_id),
        )
        conn.commit()
    return redirect(request.form.get("next") or url_for("gaps_view"))


@app.route("/gaps/<gap_id>/candidate", methods=["POST"])
def gap_candidate(gap_id: str):
    """Paste a link. One action, not a form: the URL is the whole entry."""
    url = (request.form.get("url") or "").strip()
    if not url:
        return redirect(request.form.get("next") or url_for("gaps_view"))
    with db.connect() as conn:
        if db.fetch_one(conn, "SELECT 1 AS x FROM gaps WHERE id = %s", (gap_id,)) is None:
            abort(404)
        # added_by 'user' is the flag the importer reads to leave this alone.
        conn.execute(
            "INSERT INTO gap_candidates (gap_id, name, source, url, added_by) "
            "VALUES (%s, %s, %s, %s, 'user')",
            (gap_id, (request.form.get("name") or "").strip() or url,
             urlsplit(url).netloc or None, url),
        )
        conn.commit()
    return redirect(request.form.get("next") or url_for("gaps_view"))


@app.route("/laundry")
def laundry_view():
    with db.connect() as conn:
        states = db.fetch_all(conn, "SELECT * FROM laundry_states ORDER BY sort_order")
        items = db.fetch_all(
            conn,
            ITEM_SELECT + " WHERE i.scope_code = 'core' AND i.retired_at IS NULL"
            " AND i.gone_at IS NULL"
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

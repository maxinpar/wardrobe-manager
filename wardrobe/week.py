"""The week's base, and the top that rotates on top of it.

The model, from the design handoff: **a fit is a base plus a top**. The base —
knit, bottom, shoe, belt — is chosen once and holds Monday to Friday. Only the
top changes day to day. Adopting a fit therefore *is* setting the week's base.

Two things follow, and they are why this is stored rather than derived:

  * What you wore on Monday is a fact. Re-deriving the week from whatever fit
    happens to rank first today would rewrite history every morning.
  * Thursday's top is a decision. A plan you can't see tomorrow isn't a plan.

The rotation itself is derived, and deliberately conservative: it prefers tops
that another hand-reasoned fit already pairs with this same bottom, so every day
of the week is still a combination somebody thought about.
"""

from __future__ import annotations

from datetime import date, timedelta

from . import db

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# The default shape of a week. Editable per day; this is only the starting point
# for a week nobody has touched yet.
DEFAULT_CONTEXTS = ["office", "office", "office", "home", "home"]

# The rotating layer is a polo, a shirt or a tee. A knit is part of the base.
ROTATING_CATEGORIES = ("Tops",)

RIDE_JACKET_PATTERN = ("biker", "bomber", "waxed", "leather")

BASE_ROLES = ("layer", "top", "bottom", "shoe", "belt", "outer")


def week_start(day: date) -> date:
    """The Monday of that day's week."""
    return day - timedelta(days=day.weekday())


def weekday_index(day: date) -> int:
    """Mon..Fri as 0..4. A weekend day previews the coming Monday."""
    return min(day.weekday(), 4)


def get_or_create(conn, day: date) -> dict:
    start = week_start(day)
    plan = db.fetch_one(
        conn, "SELECT * FROM week_plans WHERE week_start = %s", (start,)
    )
    if plan is None:
        conn.execute("INSERT INTO week_plans (week_start) VALUES (%s)", (start,))
        for index, context in enumerate(DEFAULT_CONTEXTS):
            conn.execute(
                "INSERT INTO week_days (week_start, weekday, context_code) "
                "VALUES (%s, %s, %s)",
                (start, index, context),
            )
        conn.commit()
        plan = db.fetch_one(
            conn, "SELECT * FROM week_plans WHERE week_start = %s", (start,)
        )
    return plan


def days(conn, start: date) -> list[dict]:
    rows = db.fetch_all(
        conn,
        """
        SELECT d.weekday, d.context_code, d.top_item_id, d.wear_event_id,
               c.label AS context_label, c.commutes,
               i.name AS top_name, i.hex AS top_hex
        FROM week_days d
        JOIN day_contexts c ON c.code = d.context_code
        LEFT JOIN items i ON i.id = d.top_item_id
        WHERE d.week_start = %s
        ORDER BY d.weekday
        """,
        (start,),
    )
    for row in rows:
        row["day"] = WEEKDAYS[row["weekday"]]
    return rows


def rotation(conn, fit, exclude_unavailable: bool = True) -> list[str]:
    """Which tops rotate over this base, best first.

    In order of preference: the fit's own top, then tops that another fit pairs
    with this same bottom, then any Keep top. Anything in the wash is skipped —
    but merely `worn` is fine, which is the whole point of a base that holds.
    """
    picked: list[str] = []
    blocked = set()
    if exclude_unavailable:
        blocked = {
            r["item_id"]
            for r in db.fetch_all(
                conn,
                "SELECT item_id FROM item_laundry "
                "WHERE state_code IN ('in_wash', 'at_tailor')",
            )
        }

    rotatable = {
        r["id"]
        for r in db.fetch_all(
            conn,
            "SELECT id FROM items WHERE retired_at IS NULL AND gone_at IS NULL "
            "AND verdict_code = 'Keep' "
            "AND scope_code = 'core' AND cat_code = ANY(%s)",
            (list(ROTATING_CATEGORIES),),
        )
    }

    def push(item_id: str | None) -> None:
        if not item_id or item_id in picked or item_id in blocked:
            return
        if item_id not in rotatable:
            return
        picked.append(item_id)

    primaries = fit.primary()
    own_top = next((i for i in primaries if i["role"] == "top"), None)
    bottom = next((i for i in primaries if i["role"] == "bottom"), None)

    if own_top:
        push(own_top["item_id"])

    if bottom:
        for row in db.fetch_all(
            conn,
            """
            SELECT DISTINCT fi.item_id FROM fit_items fi
            WHERE NOT fi.is_alternate AND fi.role IN ('top', 'base')
              AND fi.fit_id IN (SELECT fit_id FROM fit_items
                                 WHERE item_id = %s AND NOT is_alternate)
            """,
            (bottom["item_id"],),
        ):
            push(row["item_id"])

    for row in db.fetch_all(
        conn,
        "SELECT id FROM items WHERE retired_at IS NULL AND gone_at IS NULL "
        "AND verdict_code = 'Keep' "
        "AND scope_code = 'core' AND cat_code = ANY(%s) ORDER BY name",
        (list(ROTATING_CATEGORIES),),
    ):
        if len(picked) >= len(WEEKDAYS):
            break
        push(row["id"])

    return picked


def plan_tops(conn, start: date, fit) -> None:
    """Fill in the week's tops from the rotation.

    A day that has already been worn is history and is left exactly as it is.
    """
    tops = rotation(conn, fit)
    if not tops:
        return
    for row in days(conn, start):
        if row["wear_event_id"] is not None:
            continue
        conn.execute(
            "UPDATE week_days SET top_item_id = %s WHERE week_start = %s AND weekday = %s",
            (tops[row["weekday"] % len(tops)], start, row["weekday"]),
        )


def adopt(conn, start: date, fit) -> None:
    """Adopting a fit sets the week's base, and plans the tops over it."""
    conn.execute(
        "UPDATE week_plans SET base_fit_id = %s, adopted_at = now() WHERE week_start = %s",
        (fit.id, start),
    )
    plan_tops(conn, start, fit)


def is_rotating(item: dict) -> bool:
    """Only a polo, shirt or tee rotates. A knit is part of the base."""
    return item.get("cat") in ROTATING_CATEGORIES or item["item_id"].startswith("tees_")


def base_pieces(fit, top_item_id: str | None) -> list[dict]:
    """The base: everything except the garment that rotates day to day.

    A knit in the `top` slot stays — it is base, and dropping it was the bug
    this comment exists to prevent.
    """
    return [
        item
        for item in fit.primary()
        if not (is_rotating(item) and item["item_id"] != top_item_id)
    ]


def bike_notes(conn, fit, pieces: list[dict]) -> dict:
    """What the ride needs: a rideable shoe, and what goes in the top-box."""
    shoe = next((i for i in pieces if i["role"] == "shoe"), None)
    notes: dict = {"shoe": shoe, "rideable": True, "substitute": None, "top_box": []}

    if shoe:
        row = db.fetch_one(
            conn, "SELECT bike_safe FROM items WHERE id = %s", (shoe["item_id"],)
        )
        notes["rideable"] = bool(row and row["bike_safe"])

    if not notes["rideable"]:
        # Name a clean substitute rather than silently swapping the fit.
        notes["substitute"] = db.fetch_one(
            conn,
            """
            SELECT i.id, i.name FROM items i
            LEFT JOIN item_laundry l ON l.item_id = i.id
            WHERE i.retired_at IS NULL AND i.gone_at IS NULL AND i.cat_code = 'Shoes'
              AND i.verdict_code = 'Keep' AND i.scope_code = 'core'
              AND i.bike_safe AND COALESCE(l.state_code, 'clean') = 'clean'
            ORDER BY i.name LIMIT 1
            """,
        )
        if shoe:
            notes["top_box"].append(f"{shoe['name']} — arrival only")

    wearing_jacket = any(
        i["role"] == "outer"
        and any(word in (i["name"] or "").lower() for word in RIDE_JACKET_PATTERN)
        for i in pieces
    )
    if not wearing_jacket:
        ride_jacket = db.fetch_one(
            conn,
            "SELECT id, name FROM items WHERE id = %s AND retired_at IS NULL "
            "AND gone_at IS NULL",
            ("outerwear_02_indindustrie-black-waxed-biker",),
        )
        if ride_jacket:
            notes["top_box"].append(f"{ride_jacket['name']} — the ride layer")

    return notes

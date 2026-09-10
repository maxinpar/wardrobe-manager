"""The week as a stored thing: which Monday it is, and its five day rows.

Two facts, and they are why this is stored rather than derived:

  * What you wore on Monday is a fact. Re-deriving the week from whatever fit
    ranks first this morning would rewrite history every day.
  * Thursday is a decision. A plan you can't see tomorrow isn't a plan.

WHAT USED TO LIVE HERE. `rotation()`, `plan_tops()`, `adopt()`, `base_pieces()`
and `bike_notes()` served the Today screen, which This Week replaced — see
`today_view` in app.py for why the two were the same act under different names.
The rotation in particular went looking for "some other top that goes with this
trouser" when a fit was not part of a set, and planned a week of days the app
had no picture of. A set is five days that were each thought about and each
rendered, and app.lay_set_across_week writes those five rows directly.
"""

from __future__ import annotations

from datetime import date, timedelta

from . import db

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# The shape a new week is created with. Nothing displays it any more — the
# office/home context went with the Today screen — but week_days.context_code is
# NOT NULL and the wear log still records which context a wearing happened in,
# so a new row needs a value and this is the one it gets.
DEFAULT_CONTEXTS = ["office", "office", "office", "home", "home"]


def week_start(day: date) -> date:
    """The Monday this day belongs to. A weekend belongs to the week ahead.

    Saturday and Sunday roll FORWARD, and this is the correction that made both
    of these functions do what they always said they did: weekday_index's
    docstring has claimed since 008 that "a weekend day previews the coming
    Monday" while `min(weekday, 4)` returned Friday, and week_start handed back
    the Monday of the week that had just finished. Between them, opening the app
    on a Saturday showed the week that was over, with Friday marked as today.

    Nothing is wearing clothes on a Saturday as far as this app is concerned, so
    the only useful answer on a weekend is the week about to start.
    """
    if day.weekday() > 4:
        return day + timedelta(days=7 - day.weekday())
    return day - timedelta(days=day.weekday())


def weekday_index(day: date) -> int:
    """Mon..Fri as 0..4. A weekend previews the coming Monday, so 0."""
    return day.weekday() if day.weekday() <= 4 else 0


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
               d.set_fit_id,
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

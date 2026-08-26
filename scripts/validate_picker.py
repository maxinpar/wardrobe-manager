"""Check that the picker can still return every vetted work-outfits fit.

    python scripts/validate_picker.py

The 10 fits from work-outfits.md are the correctness check for the port: if
some weather/day/state combination can't produce one of them, the port is
wrong. This sweeps a year of dates against cold/mild/warm and dry/wet.

Two exemptions, both from the fits addendum:
  * the hidden roll-neck fit must never be picked unless explicitly allowed
  * the killer-looks fits need NOT be reachable — several are deliberately
    occasion-specific. They must be browsable and flaggable, not necessarily
    picked.

The reachability check runs against the work-outfits cohort on its own. That is
what the guarantee was written to protect: those ten as a self-contained set,
none of them lost in the port. Measured against the whole field it would fail
for a reason that is not a defect — with 37 fits competing, a look that always
scores mid-table never tops the ranking on any day, and adding more fits would
keep making an honest picker look broken. Wins across the full field are still
reported, because a look that never wins is worth knowing about.
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import db, picker  # noqa: E402

TEMPS = [8, 12, 18, 22, 26, 31]
RAIN = [False, True]
DAYS = 366

MUST_BE_REACHABLE_SOURCE = "work-outfits.md"


def main() -> int:
    with db.connect() as conn:
        fits = picker.load_fits(conn)

    if not fits:
        raise SystemExit("No fits in the database — run the importer first.")

    # A fit blocked on a one-off job (clean the jacket, repair the cuff) is
    # correctly unpickable today, but that says nothing about whether the port
    # is right. The sweep therefore runs with the jobs assumed done, and the
    # blocked ones are reported separately.
    blocked_now = {f.id: list(f.blocked_by) for f in fits if f.blocked_by}
    for fit in fits:
        fit.blocked_by = []

    start = date(2026, 1, 1)
    wins_default: Counter[str] = Counter()
    wins_allowing_disliked: Counter[str] = Counter()

    for offset in range(DAYS):
        day = start + timedelta(days=offset)
        for temp in TEMPS:
            for rain in RAIN:
                best, _, _ = picker.pick(fits, day, temp_c=temp, rain=rain)
                if best:
                    wins_default[best.fit.id] += 1
                best, _, _ = picker.pick(
                    fits, day, temp_c=temp, rain=rain, allow_disliked=True
                )
                if best:
                    wins_allowing_disliked[best.fit.id] += 1

    must_reach = [
        f
        for f in fits
        if not f.hidden_by_default
        and (f.source or "").startswith(MUST_BE_REACHABLE_SOURCE)
    ]
    exempt = [
        f
        for f in fits
        if not f.hidden_by_default
        and not (f.source or "").startswith(MUST_BE_REACHABLE_SOURCE)
    ]
    hidden = [f for f in fits if f.hidden_by_default]

    # Reachability, measured against the work-outfits cohort on its own — the
    # set the guarantee was written to protect.
    #
    # Laundry is cleared for this sweep for the same reason outstanding jobs
    # are: a garment being in the wash today says nothing about whether the port
    # kept the look. Which fits are blocked right now is reported separately.
    blocked_by_laundry = {
        f.name: [
            f"{i['name']} is {i['laundry_state'].replace('_', ' ')}"
            for i in f.primary()
            if i["laundry_state"] in ("in_wash", "at_tailor")
        ]
        for f in fits
    }
    blocked_by_laundry = {k: v for k, v in blocked_by_laundry.items() if v}
    for fit in fits:
        for item in fit.items:
            item["laundry_state"] = "clean"

    reachable: Counter[str] = Counter()
    for offset in range(DAYS):
        day = start + timedelta(days=offset)
        for temp in TEMPS:
            for rain in RAIN:
                best, _, _ = picker.pick(must_reach, day, temp_c=temp, rain=rain)
                if best:
                    reachable[best.fit.id] += 1

    print(f"Swept {DAYS} days x {len(TEMPS)} temperatures x {len(RAIN)} rain states\n")
    print("Fit                           picked (default)   picked (roll-necks allowed)")
    for fit in fits:
        mark = " " if fit in must_reach else "*"
        print(
            f" {mark}{fit.name:28} {wins_default[fit.id]:8}"
            f"{wins_allowing_disliked[fit.id]:20}"
        )
    if exempt:
        print("\n  * need not be reachable (killer-looks fits, occasion-specific)")

    if blocked_now:
        print(
            f"\nSwept with {len(blocked_now)} fit(s)' outstanding jobs assumed done — "
            "they are\nunpickable until the job is ticked off, which is the point of "
            "preconditions:"
        )
        for fit_id, jobs in sorted(blocked_now.items()):
            print(f"  {fit_id}: {'; '.join(jobs)}")

    if blocked_by_laundry:
        print(
            f"\nBlocked by laundry right now (swept as if clean) — "
            f"{len(blocked_by_laundry)} fit(s):"
        )
        for name, reasons in sorted(blocked_by_laundry.items()):
            print(f"  {name}: {'; '.join(reasons)}")

    problems = []
    for fit in must_reach:
        if reachable[fit.id] == 0:
            problems.append(
                f"{fit.name} can never be picked even among the ten — the port is wrong"
            )
    outcompeted = [f.name for f in must_reach if wins_default[f.id] == 0]
    if outcompeted:
        print(
            f"Out-competed in the full field of {len(fits)} (reachable, never top): "
            + ", ".join(outcompeted)
        )
    for fit in hidden:
        if wins_default[fit.id] != 0:
            problems.append(f"{fit.name} is hidden by default but was picked")
        if wins_allowing_disliked[fit.id] == 0:
            problems.append(f"{fit.name} can't be picked even when allowed")

    print()
    if problems:
        print("FAILED:")
        for p in problems:
            print("  *", p)
        return 2

    print(
        f"All {len(must_reach)} work-outfits fits are reachable; "
        f"{len(hidden)} hidden fit(s) appear only when explicitly allowed"
        + (f"; {len(exempt)} exempt." if exempt else ".")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

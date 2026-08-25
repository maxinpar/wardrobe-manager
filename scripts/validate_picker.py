"""Check that the picker can return every vetted look.

    python scripts/validate_picker.py

The 10 looks are the correctness check for the port: if some weather/day/state
combination can't produce one of them, the port is wrong. This sweeps a year of
dates against cold/mild/warm and dry/wet and reports which look wins when.

The hidden roll-neck look is checked separately, with allow_disliked on — by
default it must never be picked.
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


def main() -> int:
    with db.connect() as conn:
        looks = picker.load_looks(conn)

    if not looks:
        raise SystemExit("No vetted looks in the database — run the importer first.")

    start = date(2026, 1, 1)
    wins_default = Counter()
    wins_allowing_disliked = Counter()

    for offset in range(DAYS):
        day = start + timedelta(days=offset)
        for temp in TEMPS:
            for rain in RAIN:
                best, _, _ = picker.pick(looks, day, temp_c=temp, rain=rain)
                if best:
                    wins_default[best.look.slug] += 1
                best, _, _ = picker.pick(
                    looks, day, temp_c=temp, rain=rain, allow_disliked=True
                )
                if best:
                    wins_allowing_disliked[best.look.slug] += 1

    vetted = [l for l in looks if not l.hidden_by_default]
    hidden = [l for l in looks if l.hidden_by_default]

    print(f"Swept {DAYS} days x {len(TEMPS)} temperatures x {len(RAIN)} rain states\n")
    print("Look                          picked (default)   picked (roll-necks allowed)")
    for look in looks:
        print(
            f"  {look.name:28} {wins_default[look.slug]:8}"
            f"{wins_allowing_disliked[look.slug]:20}"
        )

    problems = []
    for look in vetted:
        if wins_default[look.slug] == 0:
            problems.append(f"{look.name} is never picked — the port is wrong")
    for look in hidden:
        if wins_default[look.slug] != 0:
            problems.append(f"{look.name} is hidden by default but was picked")
        if wins_allowing_disliked[look.slug] == 0:
            problems.append(f"{look.name} can't be picked even when allowed")

    print()
    if problems:
        print("FAILED:")
        for p in problems:
            print("  *", p)
        return 2

    print(
        f"All {len(vetted)} vetted looks are reachable; "
        f"{len(hidden)} hidden look(s) appear only when explicitly allowed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

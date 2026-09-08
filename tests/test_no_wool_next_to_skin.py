"""No wool against skin — asserted against the live catalogue.

Max does not wear wool, cashmere or merino next to his skin. That rule lived in
a CLAUDE.md inside the Claude Project, where the code cannot see it and nothing
enforces it: thirteen fits had broken it, several of them with renders that
clearly showed a white tee at the neckline the garment list did not mention.

Copying the doc into the repo would have made two copies to drift apart. This is
the rule written where it can bite instead — the next fit that puts a cashmere
crew straight onto skin fails here rather than waiting for someone to reread a
document.

TWO THINGS THE RULE HAS TO GET RIGHT, and both were wrong in the first phrasing:

  * MATERIAL, NOT CATEGORY. `Knitwear` sweeps in cotton and acrylic knits that
    are fine. The objection is to the fibre.

  * WHAT IS ACTUALLY INNERMOST. `layer` sits OUTSIDE `top` in this schema, so a
    wool V-neck over a shirt never touches skin. Checking "any wool in top or
    layer with no base row" flags eleven fits that are already covered — the
    golf quarter-zips over a polo, the suit waistcoat over a shirt. Only the
    innermost garment is against skin.

Roll-necks are exempt: one is worn alone, and a tee under it is lumpy at the
neck. That is rules-and-context.md §2 rule 5, not an exception invented here.

Needs the database. Skipped when there isn't one, so the offline suite still
runs.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import db  # noqa: E402

# The fibres Max will not wear against skin. Matched against items.material,
# which is free text off the garment's own label.
WOOL = r"(wool|cashmere|merino|lambswool|alpaca|angora)"

# Innermost first. A fit's against-skin garment is the first of these it has.
INNERMOST_FIRST = ("base", "top", "layer", "outer")

AGAINST_SKIN_SQL = f"""
WITH innermost AS (
  SELECT DISTINCT ON (f.id)
         f.id AS fit_id, f.name AS fit_name, fi.role,
         i.id AS item_id, i.name AS garment, i.neck_code, i.material
  FROM fits f
  JOIN fit_items fi ON fi.fit_id = f.id AND NOT fi.is_alternate
                   AND fi.role = ANY(%s)
  JOIN items i ON i.id = fi.item_id
  WHERE f.gone_at IS NULL
  ORDER BY f.id, array_position(%s::text[], fi.role)
)
SELECT fit_id, fit_name, role, item_id, garment, material
FROM innermost
WHERE material ~* '{WOOL}'
  -- Worn alone by definition; a tee under one is wrong, not missing.
  AND COALESCE(neck_code, '') <> 'roll'
ORDER BY fit_id
"""


@pytest.fixture(scope="module")
def offenders():
    try:
        with db.connect() as conn:
            return db.fetch_all(
                conn, AGAINST_SKIN_SQL, (list(INNERMOST_FIRST), list(INNERMOST_FIRST))
            )
    except Exception as exc:  # no database on this machine, or it is asleep
        pytest.skip(f"needs the wardrobe database: {exc}")


def test_no_wool_garment_sits_against_skin(offenders):
    """Every fit whose innermost garment is wool must have something under it."""
    assert offenders == [], "wool against skin in:\n" + "\n".join(
        f"  {row['fit_id']}: {row['garment']} ({row['material']}) as {row['role']}"
        for row in offenders
    )


def test_the_roll_neck_is_still_worn_alone():
    """The exemption is real and must not be quietly closed by a later pass.

    If someone 'fixes' the roll-neck by putting a tee under it, this fails —
    which is the point. It is worn alone.
    """
    try:
        with db.connect() as conn:
            rows = db.fetch_all(
                conn,
                "SELECT f.id FROM fits f "
                "JOIN fit_items t ON t.fit_id = f.id AND NOT t.is_alternate "
                "JOIN items i ON i.id = t.item_id AND i.neck_code = 'roll' "
                "WHERE EXISTS (SELECT 1 FROM fit_items b "
                "              WHERE b.fit_id = f.id AND b.role = 'base' "
                "                AND NOT b.is_alternate)",
            )
    except Exception as exc:
        pytest.skip(f"needs the wardrobe database: {exc}")
    assert rows == [], f"a tee has been put under a roll-neck in: {[r['id'] for r in rows]}"

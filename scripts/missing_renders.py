"""Which items still have no generated retail render, and what to name the file.

    python scripts/missing_renders.py
    python scripts/missing_renders.py --all      # include out-of-scope items

Renders are the preferred catalogue image, so this is the worklist for getting
every garment showing one. Drop a new render into
`<PHOTO_SOURCE_ROOT>/Retail/<name>` using the filename printed here, then re-run
`scripts/import_photos.py --commit` and it is picked up automatically.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import db  # noqa: E402

SQL = """
SELECT i.id, i.cat_code, i.name, i.colour, i.material, i.retail_prefix,
       i.no_photo, i.scope_code,
       EXISTS (SELECT 1 FROM photos p
                WHERE p.item_id = i.id AND NOT p.is_render) AS has_photo
FROM items i
WHERE NOT EXISTS (SELECT 1 FROM photos p WHERE p.item_id = i.id AND p.is_render)
  AND (%s OR i.scope_code = 'core')
ORDER BY i.no_photo DESC, i.cat_code, i.id
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="include scope 'out' items")
    parser.add_argument("--database-url", default=None)
    args = parser.parse_args()

    with db.connect(args.database_url) as conn:
        rows = db.fetch_all(conn, SQL, (args.all,))
        total = db.fetch_one(conn, "SELECT count(*) AS n FROM items")["n"]
        with_render = db.fetch_one(
            conn, "SELECT count(DISTINCT item_id) AS n FROM photos WHERE is_render"
        )["n"]

    print(f"{with_render} of {total} items have a render. {len(rows)} listed below.\n")

    priority = [r for r in rows if r["no_photo"]]
    if priority:
        print("HIGHEST VALUE — no real photo exists at all, so the app shows a swatch:")
        for r in priority:
            print(f"  {r['id']}_retail.png")
            print(f"      {r['cat_code']:10} {r['name']} · {r['colour']}")
        print()

    rest = [r for r in rows if not r["no_photo"]]
    if rest:
        print("Has real photos, render would still be nicer in the grid:")
        for r in rest:
            print(f"  {r['id']}_retail.png")
            print(f"      {r['cat_code']:10} {r['name']} · {r['colour']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

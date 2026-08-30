"""Import data/gaps.json into Postgres.

    python scripts/import_gaps.py             # dry run: says what would change
    python scripts/import_gaps.py --commit    # actually writes

Properties this script guarantees:

  * data/gaps.json is opened read-only and never rewritten.
  * Idempotent: upsert on gaps.id, so re-running changes nothing the second time.
  * It NEVER writes `status` or `status_changed_at` on a row that already
    exists. Marking a gap bought and re-importing must leave it bought — that is
    the exact failure the fits importer was built to avoid.
  * It never deletes a gap_candidates row with added_by = 'user'. A link Max
    pasted into a card is his, not the importer's.
  * A gap in the database but absent from the JSON is left alone, not deleted —
    the same conservatism as the item importer, for the same reason.

There is no reconciliation step: unlike items and fits there is no baseline for
gaps, so there is nothing to check the counts against.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import config, db  # noqa: E402

SOURCE_JSON = config.REPO_ROOT / "data" / "gaps.json"

# Authored fields. The importer owns these and refreshes them every run.
# `status` and `status_changed_at` are deliberately absent: they are app-owned.
AUTHORED = {
    "category": "category",
    "priority": "priority",
    "title": "title",
    "rationale": "rationale",
    "unlocks": "unlocks",
    "spec": "spec",
    "size": "size",
    "budget": "budget",
    "image_path": "image",
    "image_is_placeholder": "image_is_placeholder",
}


def load() -> list[dict]:
    doc = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    return doc["gaps"]


def as_item_ids(value) -> list[str]:
    """`replaces` is a string for one item and a list for several."""
    if not value:
        return []
    return [value] if isinstance(value, str) else list(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true", help="write; otherwise dry run")
    parser.add_argument("--database-url", default=None)
    args = parser.parse_args()

    gaps = load()
    print(f"{SOURCE_JSON.name}: {len(gaps)} gaps\n")

    with db.connect(args.database_url) as conn:
        existing = {
            r["id"]: r for r in db.fetch_all(conn, "SELECT id, status FROM gaps")
        }
        known_items = {r["id"] for r in db.fetch_all(conn, "SELECT id FROM items")}

        missing_items: list[str] = []
        inserted = updated = 0

        for index, gap in enumerate(gaps):
            gap_id = gap["id"]
            values = {col: gap.get(key) for col, key in AUTHORED.items()}
            values["sort_order"] = index * 10
            is_new = gap_id not in existing

            for item_id in as_item_ids(gap.get("replaces")):
                if item_id not in known_items:
                    missing_items.append(f"{gap_id} -> {item_id}")

            if is_new:
                inserted += 1
                print(f"  NEW      {gap_id}  {gap['title']}")
            else:
                updated += 1
                held = existing[gap_id]["status"]
                note = "" if held == "open" else f"   (keeping status={held})"
                print(f"  refresh  {gap_id}  {gap['title']}{note}")

            if not args.commit:
                continue

            cols = list(values) + ["id"]
            conn.execute(
                f"INSERT INTO gaps ({', '.join(cols)}) "
                f"VALUES ({', '.join(['%s'] * len(cols))}) "
                "ON CONFLICT (id) DO UPDATE SET "
                # status and status_changed_at are NOT in this list, and must
                # never be added to it.
                + ", ".join(f"{c} = EXCLUDED.{c}" for c in values)
                + ", updated_at = now()",
                tuple(values.values()) + (gap_id,),
            )

            conn.execute("DELETE FROM gap_buy_at WHERE gap_id = %s", (gap_id,))
            for order, retailer in enumerate(gap.get("buy_at") or []):
                conn.execute(
                    "INSERT INTO gap_buy_at (gap_id, retailer, sort_order) "
                    "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (gap_id, retailer, order),
                )

            conn.execute("DELETE FROM gap_replaces WHERE gap_id = %s", (gap_id,))
            for item_id in as_item_ids(gap.get("replaces")):
                if item_id in known_items:
                    conn.execute(
                        "INSERT INTO gap_replaces (gap_id, item_id) VALUES (%s, %s) "
                        "ON CONFLICT DO NOTHING",
                        (gap_id, item_id),
                    )

            # Only the imported candidates are replaced. Anything Max pasted in
            # is added_by 'user' and is left exactly where it is.
            conn.execute(
                "DELETE FROM gap_candidates WHERE gap_id = %s AND added_by = 'import'",
                (gap_id,),
            )
            for cand in gap.get("candidates") or []:
                conn.execute(
                    "INSERT INTO gap_candidates (gap_id, name, source, url, price, added_by) "
                    "VALUES (%s, %s, %s, %s, %s, 'import')",
                    (gap_id, cand["name"], cand.get("source"), cand.get("url"),
                     cand.get("price")),
                )

        orphaned = sorted(set(existing) - {g["id"] for g in gaps})
        if orphaned:
            print(f"\n  left alone (in the database, not in the JSON): {', '.join(orphaned)}")

        if missing_items:
            print("\nSTOP — `replaces` points at items that do not exist:")
            for line in missing_items:
                print(f"  {line}")
            return 1

        if args.commit:
            conn.commit()
            print(f"\nCommitted: {inserted} new, {updated} refreshed.")
        else:
            print(f"\nDry run: {inserted} would be new, {updated} refreshed. "
                  "Re-run with --commit to write.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

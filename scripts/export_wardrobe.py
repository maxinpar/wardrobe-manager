"""Regenerate wardrobe.json from the database.

    python scripts/export_wardrobe.py                    # writes export/wardrobe.json
    python scripts/export_wardrobe.py --out some/path.json
    python scripts/export_wardrobe.py --compare data/wardrobe.json

Once the database is canonical, the JSON in the Claude Project goes stale
immediately and those sessions start giving wrong advice. This puts the file
back: same field names, same shape, same formatting (1-space indent, non-ASCII
kept as-is), with `generated` bumped to today. Drop the output straight into
the Claude Project.

One deliberate difference from the hand-maintained file: key order within each
item is canonicalised. The source file had six different key orders from months
of editing; the data is identical, and --compare verifies that by value.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import config, db  # noqa: E402

# The full key order, taken from the outerwear items (the only ones carrying
# every field). Items without the optional keys simply omit them.
KEY_ORDER = [
    "slug", "cat", "name", "colour", "hex", "role", "neck", "cut", "material",
    "weight", "formality", "fit", "condition", "verdict", "verdictNote", "scope",
    "worksAlone", "pairs", "layer", "avoid", "notes", "warmth", "weatherproof",
    "careNote", "noPhoto", "photoRef", "photoPrefix", "retailPrefix", "id",
]

# JSON field -> database column, for the fields that are a straight copy.
COLUMN_FOR = {
    "slug": "slug",
    "cat": "cat_code",
    "name": "name",
    "colour": "colour",
    "hex": "hex",
    "role": "role_code",
    "neck": "neck_raw",
    "cut": "cut",
    "material": "material",
    "weight": "weight_code",
    "formality": "formality_raw",
    "fit": "fit",
    "condition": "condition",
    "verdict": "verdict_code",
    "verdictNote": "verdict_note",
    "scope": "scope_code",
    "pairs": "pairs",
    "layer": "layer",
    "avoid": "avoid",
    "notes": "notes",
    "photoRef": "photo_ref",
    "photoPrefix": "photo_prefix",
    "retailPrefix": "retail_prefix",
}


def build_payload(conn, generated: str) -> dict:
    owner = db.fetch_one(
        conn, "SELECT value FROM app_settings WHERE key = 'catalogue.owner'"
    )
    profile = db.fetch_one(
        conn, "SELECT value FROM app_settings WHERE key = 'catalogue.profile'"
    )

    sources = {}
    for row in db.fetch_all(
        conn,
        "SELECT item_id, field_name, source FROM item_field_sources "
        "WHERE field_name IN ('warmth', 'weatherproof_rain', 'weatherproof_wind')",
    ):
        sources.setdefault(row["item_id"], {})[row["field_name"]] = row["source"]

    items = []
    for row in db.fetch_all(
        conn, "SELECT * FROM items ORDER BY created_at, id"
    ):
        item = {}
        for key in KEY_ORDER:
            if key in COLUMN_FOR:
                # the JSON uses "" where the database uses NULL
                item[key] = row[COLUMN_FOR[key]] if row[COLUMN_FOR[key]] is not None else ""
            elif key == "worksAlone":
                item[key] = row["works_alone"]  # genuinely nullable in the JSON
            elif key == "noPhoto":
                item[key] = row["no_photo"]
            elif key == "id":
                item[key] = row["id"]
            elif key == "warmth":
                if sources.get(row["id"], {}).get("warmth") == "imported":
                    item[key] = row["warmth"]
            elif key == "weatherproof":
                if sources.get(row["id"], {}).get("weatherproof_rain") == "imported":
                    item[key] = {
                        "rain": row["weatherproof_rain"],
                        "wind": row["weatherproof_wind"],
                    }
            elif key == "careNote":
                if row["care_note"] is not None:
                    item[key] = row["care_note"]
        items.append(item)

    return {
        "generated": generated,
        "owner": json.loads(owner["value"]) if owner else "Max",
        "profile": json.loads(profile["value"]) if profile else {},
        "items": items,
    }


def compare(exported: dict, original_path: Path) -> list[str]:
    """Value-by-value comparison against the file this all came from."""
    original = json.loads(original_path.read_text(encoding="utf-8"))
    problems = []

    if original.get("owner") != exported.get("owner"):
        problems.append("owner differs")
    if original.get("profile") != exported.get("profile"):
        problems.append("profile differs")

    by_id = {i["id"]: i for i in original["items"]}
    exported_by_id = {i["id"]: i for i in exported["items"]}

    missing = set(by_id) - set(exported_by_id)
    extra = set(exported_by_id) - set(by_id)
    if missing:
        problems.append(f"missing from export: {sorted(missing)}")
    if extra:
        problems.append(f"not in the original: {sorted(extra)}")

    for item_id in sorted(set(by_id) & set(exported_by_id)):
        a, b = by_id[item_id], exported_by_id[item_id]
        if set(a) != set(b):
            problems.append(
                f"{item_id}: key set differs "
                f"(+{sorted(set(b) - set(a))} -{sorted(set(a) - set(b))})"
            )
        for key in sorted(set(a) & set(b)):
            if a[key] != b[key]:
                problems.append(f"{item_id}.{key}: {a[key]!r} != {b[key]!r}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=None, help="output path")
    parser.add_argument("--compare", default=None, help="verify against this JSON file")
    parser.add_argument("--database-url", default=None)
    parser.add_argument("--generated", default=None, help="override the generated date")
    args = parser.parse_args()

    generated = args.generated or datetime.now(ZoneInfo(config.TIMEZONE)).date().isoformat()
    out = Path(args.out) if args.out else config.REPO_ROOT / "export" / "wardrobe.json"

    with db.connect(args.database_url) as conn:
        payload = build_payload(conn, generated)

    out.parent.mkdir(parents=True, exist_ok=True)
    # 1-space indent and real UTF-8, matching the hand-maintained file.
    out.write_text(
        json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {out}  ({len(payload['items'])} items, generated {generated})")

    if args.compare:
        problems = compare(payload, Path(args.compare))
        if problems:
            print(f"\nRound-trip FAILED against {args.compare}:")
            for p in problems[:60]:
                print("  *", p)
            if len(problems) > 60:
                print(f"  … and {len(problems) - 60} more")
            return 2
        print(f"Round-trip clean: every field matches {args.compare} exactly.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

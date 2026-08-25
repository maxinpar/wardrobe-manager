"""Import data/wardrobe.json into Postgres, plus the vetted outfits and wear log.

    python scripts/import_wardrobe.py             # dry run: says what would change
    python scripts/import_wardrobe.py --commit    # actually writes

Properties this script guarantees:

  * data/wardrobe.json is opened read-only and never rewritten.
  * Idempotent: upsert on items.id, so re-running changes nothing the second time.
  * It never touches app-owned state — laundry, the wear log, or any derived
    field Max has corrected by hand (item_field_sources.source = 'manual').
  * It reconciles the imported counts against the known-good numbers and fails
    loudly rather than papering over a mismatch.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import config, db, derive, seed_data  # noqa: E402

SOURCE_JSON = config.REPO_ROOT / "data" / "wardrobe.json"

# The numbers this dataset is known to have. If the import doesn't reconcile
# against these, something is wrong with the data or with this script — stop.
EXPECTED = {
    "total": 69,
    "cat": {
        "Knitwear": 18,
        "Trousers": 12,
        "Shoes": 12,
        "Belts": 11,
        "Tops": 10,
        "Outerwear": 6,
    },
    "verdict": {"Keep": 45, "Tailor": 10, "Bin": 8, "Replace": 6},
    "scope": {"core": 65, "out": 4},
    "no_photo": 13,
}

# Straight copies from the JSON. These are catalogue truth; the importer always
# refreshes them.
CATALOGUE_FIELDS = {
    "slug": "slug",
    "cat_code": "cat",
    "name": "name",
    "colour": "colour",
    "hex": "hex",
    "role_code": "role",
    "neck_raw": "neck",
    "cut": "cut",
    "material": "material",
    "weight_code": "weight",
    "formality_raw": "formality",
    "fit": "fit",
    "condition": "condition",
    "verdict_code": "verdict",
    "verdict_note": "verdictNote",
    "scope_code": "scope",
    "works_alone": "worksAlone",
    "pairs": "pairs",
    "layer": "layer",
    "avoid": "avoid",
    "notes": "notes",
    "care_note": "careNote",
    "no_photo": "noPhoto",
    "photo_ref": "photoRef",
    "photo_prefix": "photoPrefix",
    "retail_prefix": "retailPrefix",
}

# Guessed on import, overridable by hand.
DERIVED_FIELDS = [
    "neck_code",
    "formality_rank",
    "formality_note",
    "warmth",
    "weatherproof_rain",
    "weatherproof_wind",
    "rain_unsafe",
    "pattern",
    "occasions",
]

ALL_ITEM_COLUMNS = list(CATALOGUE_FIELDS) + [
    f for f in DERIVED_FIELDS if f != "occasions"
]


def empty_to_none(value):
    return None if value == "" else value


def source_of_derived(item: dict) -> dict[str, str]:
    """Which 'derived' columns actually came from the JSON for this item.

    Only outerwear carries warmth and weatherproof today. Recording those as
    'imported' rather than 'derived' is what lets export_wardrobe.py rebuild the
    original JSON shape — the other 63 items must not grow a warmth key.
    """
    sources = {f: "derived" for f in DERIVED_FIELDS}
    if item.get("warmth") is not None:
        sources["warmth"] = "imported"
    if item.get("weatherproof") is not None:
        sources["weatherproof_rain"] = "imported"
        sources["weatherproof_wind"] = "imported"
    return sources


def build_row(item: dict) -> tuple[dict, list[str], list[str]]:
    """Return (column values, occasions, parse warnings) for one JSON item."""
    warnings = []
    row = {"id": item["id"]}

    for column, json_field in CATALOGUE_FIELDS.items():
        row[column] = empty_to_none(item.get(json_field))

    rank, note = derive.formality(item.get("formality"))
    if item.get("formality") and rank is None:
        warnings.append(f"{item['id']}: could not rank formality {item['formality']!r}")

    row["formality_rank"] = rank
    row["formality_note"] = note
    row["neck_code"] = derive.neck_code(item.get("neck"))
    if item.get("neck") and row["neck_code"] is None:
        warnings.append(f"{item['id']}: unrecognised neck {item['neck']!r}")

    row["warmth"] = derive.warmth(item)
    rain, wind = derive.weatherproof(item)
    row["weatherproof_rain"] = rain
    row["weatherproof_wind"] = wind
    row["rain_unsafe"] = derive.rain_unsafe(item)
    row["pattern"] = derive.pattern(item)

    return row, derive.occasions(item, rank), warnings


def manual_fields(conn, item_id: str) -> set[str]:
    rows = db.fetch_all(
        conn,
        "SELECT field_name FROM item_field_sources "
        "WHERE item_id = %s AND source = 'manual'",
        (item_id,),
    )
    return {r["field_name"] for r in rows}


def upsert_item(
    conn,
    row: dict,
    occasions: list[str],
    changes: list[str],
    derived_sources: dict[str, str] | None = None,
) -> None:
    derived_sources = derived_sources or {f: "derived" for f in DERIVED_FIELDS}
    item_id = row["id"]
    existing = db.fetch_one(conn, "SELECT * FROM items WHERE id = %s", (item_id,))
    protected = manual_fields(conn, item_id)

    if existing is None:
        columns = ["id"] + ALL_ITEM_COLUMNS
        placeholders = ", ".join(["%s"] * len(columns))
        conn.execute(
            f"INSERT INTO items ({', '.join(columns)}) VALUES ({placeholders})",
            [row[c] for c in columns],
        )
        changes.append(f"NEW      {item_id}")
    else:
        updates = {}
        for column in ALL_ITEM_COLUMNS:
            if column in protected:
                continue
            if existing[column] != row[column]:
                updates[column] = row[column]
        if updates:
            assignments = ", ".join(f"{c} = %s" for c in updates)
            conn.execute(
                f"UPDATE items SET {assignments} WHERE id = %s",
                list(updates.values()) + [item_id],
            )
            for column, value in updates.items():
                changes.append(
                    f"UPDATE   {item_id}.{column}: "
                    f"{existing[column]!r} -> {value!r}"
                )

    # field provenance
    for column in CATALOGUE_FIELDS:
        conn.execute(
            "INSERT INTO item_field_sources (item_id, field_name, source) "
            "VALUES (%s, %s, 'imported') "
            "ON CONFLICT (item_id, field_name) DO NOTHING",
            (item_id, column),
        )
    for column in DERIVED_FIELDS:
        conn.execute(
            "INSERT INTO item_field_sources (item_id, field_name, source) "
            "VALUES (%s, %s, %s) "
            "ON CONFLICT (item_id, field_name) DO UPDATE SET source = EXCLUDED.source "
            "WHERE item_field_sources.source <> 'manual'",
            (item_id, column, derived_sources.get(column, "derived")),
        )

    if "occasions" not in protected:
        current = {
            r["occasion_code"]
            for r in db.fetch_all(
                conn,
                "SELECT occasion_code FROM item_occasions WHERE item_id = %s",
                (item_id,),
            )
        }
        wanted = set(occasions)
        if current != wanted:
            conn.execute("DELETE FROM item_occasions WHERE item_id = %s", (item_id,))
            for code in sorted(wanted):
                conn.execute(
                    "INSERT INTO item_occasions (item_id, occasion_code) VALUES (%s, %s)",
                    (item_id, code),
                )
            if existing is not None:
                changes.append(
                    f"UPDATE   {item_id}.occasions: "
                    f"{sorted(current)} -> {sorted(wanted)}"
                )

    # App-owned laundry row: created once, never reset by a re-import.
    conn.execute(
        "INSERT INTO item_laundry (item_id, state_code) VALUES (%s, 'clean') "
        "ON CONFLICT (item_id) DO NOTHING",
        (item_id,),
    )


# ------------------------------------------------------------ outfit seeds --


def resolve_item(conn, item_id: str) -> None:
    """Assert the reference resolves to exactly one catalogue row."""
    rows = db.fetch_all(conn, "SELECT id FROM items WHERE id = %s", (item_id,))
    if len(rows) != 1:
        raise SystemExit(
            f"Outfit/wear seed references {item_id!r}, which matched {len(rows)} "
            f"items. Every reference must resolve to exactly one id — fix the "
            f"mapping in wardrobe/seed_data.py rather than guessing."
        )


def seed_outfits(conn, changes: list[str]) -> None:
    for outfit in seed_data.OUTFITS:
        for item_id, *_ in outfit["items"]:
            resolve_item(conn, item_id)

        existing = db.fetch_one(
            conn, "SELECT * FROM outfits WHERE slug = %s", (outfit["slug"],)
        )
        if existing is None:
            row = db.fetch_one(
                conn,
                "INSERT INTO outfits (slug, name, register_code, rationale, "
                "hidden_by_default, vetted, sort_order) "
                "VALUES (%s, %s, %s, %s, %s, true, %s) RETURNING id",
                (
                    outfit["slug"],
                    outfit["name"],
                    outfit["register"],
                    outfit["rationale"],
                    outfit["hidden_by_default"],
                    outfit["sort_order"],
                ),
            )
            outfit_id = row["id"]
            changes.append(f"NEW      outfit {outfit['slug']}")
        else:
            outfit_id = existing["id"]
            conn.execute(
                "UPDATE outfits SET name = %s, register_code = %s, rationale = %s, "
                "hidden_by_default = %s, sort_order = %s WHERE id = %s",
                (
                    outfit["name"],
                    outfit["register"],
                    outfit["rationale"],
                    outfit["hidden_by_default"],
                    outfit["sort_order"],
                    outfit_id,
                ),
            )

        conn.execute("DELETE FROM outfit_items WHERE outfit_id = %s", (outfit_id,))
        for item_id, slot_role, position, is_alternate, note in outfit["items"]:
            conn.execute(
                "INSERT INTO outfit_items (outfit_id, item_id, slot_role, position, "
                "is_alternate, note) VALUES (%s, %s, %s, %s, %s, %s)",
                (outfit_id, item_id, slot_role, position, is_alternate, note),
            )


def seed_wear_events(conn, changes: list[str]) -> None:
    for event in seed_data.WEAR_EVENTS:
        for item_id, _ in event["items"]:
            resolve_item(conn, item_id)

        existing = db.fetch_one(
            conn,
            "SELECT id FROM wear_events WHERE worn_on = %s AND context IS NOT DISTINCT FROM %s",
            (event["worn_on"], event["context"]),
        )
        if existing is not None:
            continue  # already seeded; never duplicate or overwrite the log

        outfit_id = None
        if event["outfit_slug"]:
            row = db.fetch_one(
                conn, "SELECT id FROM outfits WHERE slug = %s", (event["outfit_slug"],)
            )
            outfit_id = row["id"] if row else None

        row = db.fetch_one(
            conn,
            "INSERT INTO wear_events (worn_on, outfit_id, context, temp_c, rain, "
            "rating, note, tweak) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (
                event["worn_on"],
                outfit_id,
                event["context"],
                event["temp_c"],
                event["rain"],
                event["rating"],
                event["note"],
                event["tweak"],
            ),
        )
        event_id = row["id"]
        for item_id, is_base in event["items"]:
            conn.execute(
                "INSERT INTO wear_event_items (wear_event_id, item_id, is_base_layer) "
                "VALUES (%s, %s, %s)",
                (event_id, item_id, is_base),
            )
        for text, is_base in event.get("free_text_items", []):
            conn.execute(
                "INSERT INTO wear_event_items (wear_event_id, free_text, is_base_layer) "
                "VALUES (%s, %s, %s)",
                (event_id, text, is_base),
            )
        changes.append(f"NEW      wear event {event['worn_on']}")


# ---------------------------------------------------------------- reporting --


def photo_prefix_report(items: list[dict]) -> tuple[list[str], bool]:
    """Which photoPrefixes match no file on disk. Read-only against Drive."""
    try:
        root = config.photo_source_root()
    except SystemExit:
        return ["PHOTO_SOURCE_ROOT not set — skipped the photo check"], False
    if not root.exists():
        return [f"{root} not reachable — skipped the photo check"], False

    folders = {
        "Knitwear": "Knitwear",
        "Tops": "Shirts",
        "Trousers": "Trousers",
        "Shoes": "Shoes",
        "Belts": "Belts",
        "Outerwear": "Outerwear",
    }
    listings = {}
    for cat, folder in folders.items():
        path = root / folder
        listings[cat] = [p.name for p in path.iterdir()] if path.exists() else []

    unmatched = []
    for item in items:
        prefix = item.get("photoPrefix")
        if not prefix:
            continue
        names = listings.get(item["cat"], [])
        if not any(n.startswith(prefix) for n in names):
            flag = " (noPhoto: true)" if item.get("noPhoto") else ""
            unmatched.append(f"{item['id']}: prefix {prefix!r} matched no file{flag}")
    return unmatched, True


def reconcile(items: list[dict]) -> list[str]:
    problems = []
    if len(items) != EXPECTED["total"]:
        problems.append(f"item count {len(items)} != expected {EXPECTED['total']}")

    for field, key in (("cat", "cat"), ("verdict", "verdict"), ("scope", "scope")):
        counts = Counter(i[field] for i in items)
        for value, expected in EXPECTED[key].items():
            if counts.get(value, 0) != expected:
                problems.append(
                    f"{field} {value}: got {counts.get(value, 0)}, expected {expected}"
                )
        for value in counts:
            if value not in EXPECTED[key]:
                problems.append(f"{field} {value}: unexpected value, not in the baseline")

    no_photo = sum(1 for i in items if i.get("noPhoto"))
    if no_photo != EXPECTED["no_photo"]:
        problems.append(f"noPhoto count {no_photo} != expected {EXPECTED['no_photo']}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true", help="write (default: dry run)")
    parser.add_argument("--database-url", default=None)
    parser.add_argument("--json", default=None, help="override the source JSON path")
    parser.add_argument(
        "--quiet-changes", action="store_true", help="summarise changes instead of listing them"
    )
    args = parser.parse_args()

    source = Path(args.json) if args.json else SOURCE_JSON
    payload = json.loads(source.read_text(encoding="utf-8"))
    items = payload["items"]

    print(f"Source: {source}  (generated {payload.get('generated')})")
    print(f"Mode:   {'COMMIT' if args.commit else 'DRY RUN — nothing will be written'}\n")

    problems = reconcile(items)
    if problems:
        print("STOP — the source data does not reconcile against the known baseline:")
        for p in problems:
            print("  *", p)
        return 2

    changes: list[str] = []
    warnings: list[str] = []
    derived_summary = defaultdict(Counter)

    with db.connect(args.database_url) as conn:
        # Top-level owner/profile: kept verbatim so the export can rebuild the
        # exact JSON shape the Claude Project expects.
        for key, value in (
            ("catalogue.owner", json.dumps(payload.get("owner"))),
            ("catalogue.profile", json.dumps(payload.get("profile"), ensure_ascii=False)),
        ):
            conn.execute(
                "INSERT INTO app_settings (key, value) VALUES (%s, %s) "
                "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
                (key, value),
            )

        for item in items:
            row, occasions, item_warnings = build_row(item)
            warnings.extend(item_warnings)
            derived_summary["formality_rank"][row["formality_rank"]] += 1
            derived_summary["warmth"][row["warmth"]] += 1
            derived_summary["pattern"][row["pattern"]] += 1
            derived_summary["rain_unsafe"][row["rain_unsafe"]] += 1
            for code in occasions:
                derived_summary["occasions"][code] += 1
            upsert_item(conn, row, occasions, changes, source_of_derived(item))

        seed_outfits(conn, changes)
        seed_wear_events(conn, changes)

        # ---- report, read back from the database inside the transaction ----
        print("Imported counts (read back from the database)")
        for label, sql in (
            ("category", "SELECT cat_code AS k, count(*) AS n FROM items GROUP BY 1 ORDER BY 1"),
            ("verdict", "SELECT verdict_code AS k, count(*) AS n FROM items GROUP BY 1 ORDER BY 1"),
            ("scope", "SELECT scope_code AS k, count(*) AS n FROM items GROUP BY 1 ORDER BY 1"),
        ):
            rows = db.fetch_all(conn, sql)
            joined = " · ".join(f"{r['k']} {r['n']}" for r in rows)
            print(f"  {label:9} {joined}")

        total = db.fetch_one(conn, "SELECT count(*) AS n FROM items")["n"]
        no_photo = db.fetch_one(
            conn, "SELECT count(*) AS n FROM items WHERE no_photo"
        )["n"]
        outfits = db.fetch_one(conn, "SELECT count(*) AS n FROM outfits")["n"]
        hidden = db.fetch_one(
            conn, "SELECT count(*) AS n FROM outfits WHERE hidden_by_default"
        )["n"]
        outfit_items = db.fetch_one(conn, "SELECT count(*) AS n FROM outfit_items")["n"]
        wear = db.fetch_one(conn, "SELECT count(*) AS n FROM wear_events")["n"]
        print(f"  {'total':9} {total} items · {no_photo} with no photo")
        print(
            f"  {'outfits':9} {outfits} ({outfits - hidden} shown, {hidden} hidden by "
            f"default) · {outfit_items} slot rows"
        )
        print(f"  {'wear log':9} {wear} event(s)")

        db_problems = reconcile_db(conn)

        print("\nDerived values (first pass — correct any of these by hand later)")
        for field in ("formality_rank", "warmth", "pattern", "rain_unsafe", "occasions"):
            counts = derived_summary[field]
            joined = " · ".join(f"{k}: {v}" for k, v in sorted(counts.items(), key=str))
            print(f"  {field:15} {joined}")

        unmatched, checked = photo_prefix_report(items)
        print("\nPhoto prefixes with no file on disk")
        if not checked:
            print("  " + unmatched[0])
        elif unmatched:
            for line in unmatched:
                print("  *", line)
        else:
            print("  none — every photoPrefix matched at least one file")

        print("\nFields this import could not parse")
        if warnings:
            for w in warnings:
                print("  *", w)
        else:
            print("  none")

        stale = db.fetch_all(
            conn,
            "SELECT id, name FROM items WHERE cat_code = 'Trousers' "
            "AND verdict_code = 'Tailor' ORDER BY id",
        )
        if stale:
            print(
                f"\nNEEDS A DECISION — {len(stale)} trousers still say verdict 'Tailor'"
            )
            print(
                "  All trousers came back from the tailor on 2026-08-20 and are "
                "wearable as-is,\n  but wardrobe.json still says Tailor. Imported "
                "as-is, as you asked.\n\n  There is no edit UI in v1, so flip them "
                "with this. The second statement is\n  what stops the next import "
                "putting 'Tailor' back:\n\n"
                "    UPDATE items SET verdict_code = 'Keep'\n"
                "     WHERE cat_code = 'Trousers' AND verdict_code = 'Tailor';\n\n"
                "    INSERT INTO item_field_sources (item_id, field_name, source, note)\n"
                "    SELECT id, 'verdict_code', 'manual', 'tailored 2026-08-20'\n"
                "      FROM items WHERE cat_code = 'Trousers'\n"
                "    ON CONFLICT (item_id, field_name)\n"
                "    DO UPDATE SET source = 'manual', updated_at = now();"
            )
            for row in stale:
                print(f"    {row['id']}  {row['name']}")

        print(f"\nChanges: {len(changes)}")
        if changes and not args.quiet_changes:
            for line in changes[:200]:
                print("  ", line)
            if len(changes) > 200:
                print(f"   … and {len(changes) - 200} more")

        if db_problems:
            print("\nSTOP — the database does not reconcile against the baseline:")
            for p in db_problems:
                print("  *", p)
            conn.rollback()
            return 2

        if args.commit:
            conn.commit()
            print("\nCommitted.")
        else:
            conn.rollback()
            print("\nDry run — rolled back. Re-run with --commit to write.")

    return 0


def reconcile_db(conn) -> list[str]:
    problems = []
    total = db.fetch_one(conn, "SELECT count(*) AS n FROM items")["n"]
    if total != EXPECTED["total"]:
        problems.append(f"items in DB: {total}, expected {EXPECTED['total']}")

    for key, column in (("cat", "cat_code"), ("verdict", "verdict_code"), ("scope", "scope_code")):
        rows = db.fetch_all(
            conn, f"SELECT {column} AS k, count(*) AS n FROM items GROUP BY 1"
        )
        counts = {r["k"]: r["n"] for r in rows}
        for value, expected in EXPECTED[key].items():
            if counts.get(value, 0) != expected:
                problems.append(
                    f"{column} {value}: {counts.get(value, 0)} in DB, expected {expected}"
                )

    no_photo = db.fetch_one(conn, "SELECT count(*) AS n FROM items WHERE no_photo")["n"]
    if no_photo != EXPECTED["no_photo"]:
        problems.append(f"no_photo in DB: {no_photo}, expected {EXPECTED['no_photo']}")

    orphans = db.fetch_all(
        conn,
        "SELECT oi.item_id FROM outfit_items oi "
        "LEFT JOIN items i ON i.id = oi.item_id WHERE i.id IS NULL",
    )
    if orphans:
        problems.append(f"outfit_items referencing unknown ids: {orphans}")
    return problems


if __name__ == "__main__":
    raise SystemExit(main())

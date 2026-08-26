"""Prove the export round-trips: DB -> JSON -> scratch DB -> JSON, identical.

    python scripts/roundtrip_check.py

What it does:
  1. exports the live database to a temporary JSON file
  2. creates a scratch database (default name: wardrobe_roundtrip)
  3. runs the migrations on it, then imports the exported JSON into it
  4. exports the scratch database and compares the two JSON files field by field
  5. compares row counts between the two databases
  6. drops the scratch database it created (--keep to leave it)

The only thing this ever drops is the scratch database it just made. It never
touches the live one.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import psycopg
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import config, db  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
GENERATED = "2000-01-01"  # pinned, so the two exports are comparable


def run(*args: str) -> None:
    result = subprocess.run([sys.executable, *args], text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(f"step failed: {' '.join(args)}")


def scratch_url(base_url: str, name: str) -> str:
    parts = conninfo_to_dict(base_url)
    parts["dbname"] = name
    return make_conninfo(**parts)


def admin_url(base_url: str) -> str:
    return scratch_url(base_url, "postgres")


def counts(url: str) -> dict[str, int]:
    tables = [
        "items", "item_occasions", "item_field_sources", "fits", "fit_items",
        "fit_temp_bands", "fit_seasons", "fit_occasions", "fit_preconditions",
        "wear_events", "wear_event_items", "item_laundry",
    ]
    out = {}
    with db.connect(url) as conn:
        for table in tables:
            out[table] = db.fetch_one(conn, f"SELECT count(*) AS n FROM {table}")["n"]
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch-db", default="wardrobe_roundtrip")
    parser.add_argument("--keep", action="store_true", help="don't drop the scratch DB")
    args = parser.parse_args()

    live_url = config.database_url()
    scratch = scratch_url(live_url, args.scratch_db)

    tmp = Path(tempfile.mkdtemp(prefix="wardrobe-roundtrip-"))
    first = tmp / "from-live.json"
    second = tmp / "from-scratch.json"

    print("1. exporting the live database")
    run(str(SCRIPTS / "export_wardrobe.py"), "--out", str(first), "--generated", GENERATED)

    print(f"2. creating scratch database {args.scratch_db}")
    with psycopg.connect(admin_url(live_url), autocommit=True) as conn:
        conn.execute(
            sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(args.scratch_db))
        )
        conn.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(args.scratch_db))
        )

    try:
        print("3. migrating and importing into the scratch database")
        run(str(SCRIPTS / "migrate.py"), "--database-url", scratch)
        run(
            str(SCRIPTS / "import_wardrobe.py"),
            "--commit",
            "--quiet-changes",
            "--json",
            str(first),
            "--database-url",
            scratch,
        )

        print("4. exporting the scratch database")
        run(
            str(SCRIPTS / "export_wardrobe.py"),
            "--out", str(second),
            "--generated", GENERATED,
            "--database-url", scratch,
        )

        a = json.loads(first.read_text(encoding="utf-8"))
        b = json.loads(second.read_text(encoding="utf-8"))

        problems = []
        if a != b:
            by_id_a = {i["id"]: i for i in a["items"]}
            by_id_b = {i["id"]: i for i in b["items"]}
            for item_id in sorted(set(by_id_a) | set(by_id_b)):
                if by_id_a.get(item_id) != by_id_b.get(item_id):
                    problems.append(f"item {item_id} differs")
            if a["profile"] != b["profile"]:
                problems.append("profile differs")
            if a["owner"] != b["owner"]:
                problems.append("owner differs")

        print("5. comparing row counts")
        live_counts = counts(live_url)
        scratch_counts = counts(scratch)
        for table, n in live_counts.items():
            marker = "ok " if scratch_counts[table] == n else "DIFF"
            print(f"   {marker} {table:20} live {n:4}  scratch {scratch_counts[table]:4}")
            if scratch_counts[table] != n:
                problems.append(
                    f"{table}: {n} live vs {scratch_counts[table]} in the scratch DB"
                )

        if problems:
            print("\nROUND-TRIP FAILED:")
            for p in problems[:40]:
                print("  *", p)
            return 2

        print(
            f"\nRound-trip clean: {len(a['items'])} items exported, re-imported and "
            "re-exported with identical values, and every table count matches."
        )
    finally:
        if not args.keep:
            with psycopg.connect(admin_url(live_url), autocommit=True) as conn:
                conn.execute(
                    sql.SQL("DROP DATABASE IF EXISTS {}").format(
                        sql.Identifier(args.scratch_db)
                    )
                )
            print(f"Dropped the scratch database {args.scratch_db}.")
        else:
            print(f"Left the scratch database {args.scratch_db} in place.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Apply the numbered .sql files in migrations/, once each, in order.

    python scripts/migrate.py            # apply anything not yet applied
    python scripts/migrate.py --status   # just say what would run
    python scripts/migrate.py --database-url postgresql://...   # e.g. the scratch DB

Migrations are plain SQL and are never rewritten once applied. Nothing here
drops anything: the only DDL is in the migration files themselves.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import db  # noqa: E402
from wardrobe.config import REPO_ROOT  # noqa: E402

MIGRATIONS_DIR = REPO_ROOT / "migrations"

CREATE_TRACKING_TABLE = """
CREATE TABLE IF NOT EXISTS schema_migrations (
  filename   text PRIMARY KEY,
  applied_at timestamptz NOT NULL DEFAULT now()
)
"""


def migration_files() -> list[Path]:
    return sorted(MIGRATIONS_DIR.glob("*.sql"))


def applied(conn) -> set[str]:
    rows = db.fetch_all(conn, "SELECT filename FROM schema_migrations")
    return {r["filename"] for r in rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", action="store_true", help="report only, apply nothing")
    parser.add_argument("--database-url", default=None, help="override DATABASE_URL")
    args = parser.parse_args()

    files = migration_files()
    if not files:
        print("No migrations found in", MIGRATIONS_DIR)
        return 1

    with db.connect(args.database_url) as conn:
        conn.execute(CREATE_TRACKING_TABLE)
        conn.commit()
        done = applied(conn)

        pending = [f for f in files if f.name not in done]
        for f in files:
            mark = "applied" if f.name in done else "PENDING"
            print(f"  {mark:>7}  {f.name}")

        if args.status:
            print(f"\n{len(pending)} pending.")
            return 0

        if not pending:
            print("\nNothing to do.")
            return 0

        for f in pending:
            print(f"\nApplying {f.name} …")
            conn.execute(f.read_text(encoding="utf-8"))
            conn.execute(
                "INSERT INTO schema_migrations (filename) VALUES (%s)", (f.name,)
            )
            conn.commit()
            print(f"  ok")

        print(f"\nApplied {len(pending)} migration(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

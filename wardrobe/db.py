"""Database access. Thin wrapper over psycopg — no ORM, no connection pool."""

from __future__ import annotations

from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from . import config


@contextmanager
def connect(url: str | None = None, autocommit: bool = False):
    """Open a connection with dict rows and the local timezone set."""
    with psycopg.connect(
        config.database_url(url), row_factory=dict_row, autocommit=autocommit
    ) as conn:
        conn.execute(f"SET TIME ZONE '{config.TIMEZONE}'")
        yield conn


def fetch_all(conn, sql: str, params=None) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchall()


def fetch_one(conn, sql: str, params=None) -> dict | None:
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchone()

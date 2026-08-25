"""Configuration, read from .env. Nothing here has a hardcoded absolute path."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(REPO_ROOT / ".env")

TIMEZONE = os.environ.get("APP_TIMEZONE", "Australia/Sydney")


def database_url(override: str | None = None) -> str:
    url = override or os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit(
            "DATABASE_URL is not set. Copy .env.example to .env and fill it in "
            "(see README, 'Getting set up')."
        )
    return url


def photo_source_root() -> Path:
    """The Google Drive folder. Read-only — nothing is ever written here."""
    raw = os.environ.get("PHOTO_SOURCE_ROOT")
    if not raw:
        raise SystemExit("PHOTO_SOURCE_ROOT is not set (see .env.example).")
    return Path(raw)


def photo_store() -> Path:
    """Where the app keeps its own copies of the photos."""
    raw = os.environ.get("PHOTO_STORE", "photos")
    path = Path(raw)
    return path if path.is_absolute() else REPO_ROOT / path


def app_host() -> str:
    return os.environ.get("APP_HOST", "127.0.0.1")


def app_port() -> int:
    return int(os.environ.get("APP_PORT", "5005"))

"""The 35 fits in data/fits.json — the 2026-08-27 export.

This supersedes the markdown sources for everything except the ten in
work-outfits.md, which reference garments by display name and stay hand-mapped
in seed_data.py exactly as the brief requires.

Two things this module refuses to do, both on purpose:

  * **It never guesses a composition.** Eight fits (C7, C8, W7, W8, K7, K8, S3,
    S4) carry `"items": null` and `compositionKnown: false`: the renders are
    real, the garment lists were lost when a session was compacted. A list
    inferred from a filename slug would be indistinguishable from a fact six
    months from now, so those fits import with the render, the name and nothing
    else, flagged for Max to fill in from the picture.
  * **It never invents an id.** A fit's id comes from its render filename, which
    is how the 20 already in the database keep the ids they have. The seven from
    killer-looks.md have no render, so their ids are written out below.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .config import REPO_ROOT

SOURCE_PATH = REPO_ROOT / "data" / "fits.json"

# The killer-looks fits have no render to take an id from, and they already
# exist in the database under these ids. Mapped by hand, once.
KILLER_LOOK_IDS = {
    "kl1": "fit_the_shawl",
    "kl2": "fit_oatmeal_and_navy_wool",
    "kl3": "fit_blazer_over_burgundy",
    "kl4": "fit_cardigan_and_brioni",
    "kl5": "fit_navy_knit_and_stone",
    "kl6": "fit_the_vest_done_right",
    "kl7": "fit_sage_and_tan",
}

# The export's categories are a different axis from register. Only `smart`
# implies the sharp register; everything else is everyday.
REGISTER_BY_CATEGORY = {"smart": "sharp"}

ITEM_ID = re.compile(r"\b((?:tops|tees|trousers|shoes|belts|outerwear)_[a-z0-9_-]+|[a-z][a-z0-9-]*-[a-z0-9-]+)\b")

# A catch that names a job to do first is a precondition, not just a warning.
PRECONDITION_HINTS = ("repair the", "whiten-wash", "clean the", "spot-clean", "wipe the")


def fit_id(entry: dict) -> str:
    """From the render filename, or from the hand-written map."""
    render = entry.get("render")
    if render:
        return re.sub(r"_render\.[a-z]+$", "", render, flags=re.I)
    code = entry["code"]
    if code in KILLER_LOOK_IDS:
        return KILLER_LOOK_IDS[code]
    raise SystemExit(
        f"fits.json: {code} has neither a render nor a known id — add it to "
        "KILLER_LOOK_IDS rather than letting the importer invent one."
    )


def _alternates(entry: dict, known_ids: set[str]) -> list[tuple]:
    """An `alternate` line is prose that usually names an item id."""
    text = entry.get("alternate")
    if not text:
        return []
    rows = []
    for candidate in ITEM_ID.findall(text):
        if candidate in known_ids:
            rows.append((candidate, "outer" if "outerwear" in candidate else "top",
                         1, True, text))
    return rows


def load(known_ids: set[str], path: Path | None = None) -> list[dict]:
    """Parse the export into the shape wardrobe/seed_data.py's FITS uses.

    `known_ids` is every item id in the database, used to check references and
    to pick real ids out of the free-text `alternate` lines.
    """
    payload = json.loads((path or SOURCE_PATH).read_text(encoding="utf-8"))
    fits = []

    for sort_index, entry in enumerate(payload["fits"], start=40):
        composition_known = entry.get("compositionKnown", True)
        rows: list[tuple] = []

        for slot in entry.get("items") or []:
            rows.append((slot["itemId"], slot["role"], slot["position"], False, None))
        rows.extend(_alternates(entry, known_ids))

        catch = entry.get("catch")
        preconditions = []
        if catch and any(h in catch.lower() for h in PRECONDITION_HINTS):
            preconditions.append((catch.split(".")[0].strip(), None))

        fit = {
            "id": fit_id(entry),
            "name": entry["name"],
            "register": REGISTER_BY_CATEGORY.get(entry.get("category"), "everyday"),
            "category": entry.get("category"),
            "sort_order": sort_index,
            "hidden_by_default": False,
            "commentary": entry.get("commentary"),
            "catch": catch,
            "source": entry.get("source"),
            "items": rows,
            "preconditions": preconditions,
            "composition_known": composition_known,
            "render": entry.get("render"),
        }

        # Metadata is authored in the export, so it is imported as written and
        # never re-derived — except on the render-only fits, where there is
        # nothing to derive it from either.
        if composition_known:
            fit.update(
                {
                    "temp_bands": entry.get("temp") or [],
                    "rain_safe": bool(entry.get("rainSafe")),
                    "formality_rank": entry.get("formalityRank"),
                    "good_for": entry.get("goodFor") or [],
                    "bad_for": entry.get("badFor") or [],
                }
            )
        fits.append(fit)

    return fits

"""The 20 fits in data/fits-batch-2.md, read from the document itself.

Unlike work-outfits.md, this file references every garment by its wardrobe.json
id, so there is nothing to disambiguate and nothing to fuzzy-match: the importer
asserts each id resolves to exactly one item and stops if one doesn't. Parsing
the document beats transcribing it — the prose is long, and a transcription slip
would be silent.

Its metadata (temp bands, rain-safety, formality, good/bad-for) is authored in
the document, so it is imported as written and never re-derived.

Two things the format leaves implicit:

  * Roles. The document lists garments outermost-first without labelling them,
    so the role comes from the item's category, with `A + B` meaning B is worn
    under A — that is how the crew tees end up as `base`.
  * Fit ids. The generated fit renders on Drive are named
    `fit_<code>_<slug>_render.png`, and the slug is not derivable from the fit's
    title, so the code -> id mapping is written out below. Getting it wrong
    doesn't break the import, it just means a fit never finds its render.
"""

from __future__ import annotations

import re
from pathlib import Path

from .config import REPO_ROOT

SOURCE = "fits-batch-2.md 2026-08-26"
SOURCE_PATH = REPO_ROOT / "data" / "fits-batch-2.md"

# code -> the id, which is also the stem of its render on Drive.
# K5 and K6 have no render yet; their ids follow the same shape.
FIT_IDS = {
    "W1": "fit_w1_white-polo-and-sage",
    "W2": "fit_w2_grey-vneck-and-cobalt",
    "W3": "fit_w3_blue-vneck-and-beige",
    "W4": "fit_w4_brioni-and-air-max",
    "W5": "fit_w5_brown-cashmere-and-gingham",
    "W6": "fit_w6_red-vneck-and-stone",
    "C1": "fit_c1_slate-and-biker",
    "C2": "fit_c2_raspberry-and-navy-wool",
    "C3": "fit_c3_blue-vneck-vest-and-stone",
    "C4": "fit_c4_red-under-black",
    "C5": "fit_c5_oatmeal-and-cobalt",
    "C6": "fit_c6_pale-blue-vest-and-black",
    "K1": "fit_k1_burgundy-and-black",
    "K2": "fit_k2_club-navy-and-loafers",
    "K3": "fit_k3_mustard-and-black",
    "K4": "fit_k4_navy-knit-and-beige",
    "K5": "fit_k5_sage-and-black",
    "K6": "fit_k6_biker-and-blue",
    "S1": "fit_s1_blazer-over-a-vneck",
    "S2": "fit_s2_overcoat-over-shawl",
}

# The categories the document groups fits under, and the register each maps to.
REGISTER_BY_CODE = {"W": "everyday", "C": "everyday", "K": "everyday", "S": "sharp"}

# Category -> role. A cardigan is a layer rather than a top; a tee worn under
# something is a base, which is handled separately.
ROLE_BY_CAT = {
    "Outerwear": "outer",
    "Knitwear": "top",
    "Tops": "top",
    "Trousers": "bottom",
    "Shoes": "shoe",
    "Belts": "belt",
}

HEADING = re.compile(r"^## ([WCKS]\d)\.\s+(.+?)\s*$", re.M)
META = re.compile(
    r"\*\*temp:\*\*\s*(?P<temp>[^·]+)·\s*\*\*rain_safe:\*\*\s*(?P<rain>true|false)"
    r"[^·]*·\s*\*\*formality:\*\*\s*(?P<formality>\d)"
)
OCCASIONS = re.compile(
    r"\*\*good_for:\*\*\s*(?P<good>[^·]+)·\s*\*\*bad_for:\*\*\s*(?P<bad>.+)"
)
ITEMS_LINE = re.compile(r"^`[^`]+`(?:\s*[+·]\s*`[^`]+`)*\s*$", re.M)
PROSE = re.compile(r"\*\*(commentary|catch):\*\*\s*(.+?)(?=\n\*\*|\n\n|\n_|\Z)", re.S)
ALTERNATE = re.compile(r"^_alternate:\s*`([^`]+)`(.*?)_\s*$", re.M)

# A catch that names a job to do first is a precondition, not just a warning.
PRECONDITION_HINTS = ("repair the", "whiten-wash", "clean the")


def _blocks(text: str) -> list[tuple[str, str, str]]:
    """(code, name, body) for each fit, stopping before the render appendix."""
    text = text.split("# Retail render filenames per fit")[0]
    matches = list(HEADING.finditer(text))
    out = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out.append((m.group(1), m.group(2), text[m.end():end]))
    return out


def _roles(groups: list[list[str]], categories: dict[str, str]) -> list[tuple]:
    """Assign a role per garment, in the order the document lists them."""
    rows = []
    position = 0
    for group in groups:
        position += 1
        for depth, item_id in enumerate(group):
            cat = categories.get(item_id)
            role = ROLE_BY_CAT.get(cat, "top")
            if depth > 0:
                # "knit + tee" — the second garment is worn underneath.
                role = "base"
            elif cat == "Knitwear" and item_id.endswith("cardigan"):
                role = "layer"
            rows.append((item_id, role, position, False, None))
    return rows


def load(categories: dict[str, str], path: Path | None = None) -> list[dict]:
    """Parse the document into the same shape as wardrobe/seed_data.py's FITS.

    `categories` maps item id -> category, which is what decides each garment's
    role. It comes from the database, so a garment that doesn't exist yet is
    visible immediately as an unresolved reference rather than a wrong role.
    """
    text = (path or SOURCE_PATH).read_text(encoding="utf-8")
    fits = []

    for sort_index, (code, name, body) in enumerate(_blocks(text), start=20):
        meta = META.search(body)
        occ = OCCASIONS.search(body)
        items_line = ITEMS_LINE.search(body)
        if not (meta and occ and items_line):
            raise SystemExit(f"fits-batch-2.md: could not parse {code} ({name})")

        groups = [
            [ref.strip().strip("`").strip() for ref in group.split("+")]
            for group in items_line.group(0).split("·")
        ]
        prose = {kind: value.strip().replace("\n", " ") for kind, value in PROSE.findall(body)}
        catch = prose.get("catch")

        rows = _roles(groups, categories)
        alternate = ALTERNATE.search(body)
        if alternate:
            item_id = alternate.group(1)
            note = alternate.group(2).strip(" ,—-") or None
            rows.append((item_id, ROLE_BY_CAT.get(categories.get(item_id), "top"),
                         1, True, note))

        preconditions = []
        if catch and any(h in catch.lower() for h in PRECONDITION_HINTS):
            # The job is the first sentence; the rest is styling advice.
            first = catch.split(".")[0].strip()
            preconditions.append((first, None))

        fits.append(
            {
                "id": FIT_IDS[code],
                "name": name,
                "register": REGISTER_BY_CODE[code[0]],
                "sort_order": sort_index,
                "hidden_by_default": False,
                "formality_rank": int(meta.group("formality")),
                "temp_bands": [b.strip() for b in meta.group("temp").split(",")],
                "rain_safe": meta.group("rain") == "true",
                "good_for": [o.strip() for o in occ.group("good").split(",")],
                "bad_for": [o.strip() for o in occ.group("bad").split(",")],
                "commentary": prose.get("commentary", ""),
                "catch": catch,
                "source": SOURCE,
                "items": rows,
                "preconditions": preconditions,
            }
        )
    return fits

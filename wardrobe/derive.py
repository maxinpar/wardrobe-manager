"""First-pass values for the fields the catalogue never had.

Everything in here is a *guess*, recorded in item_field_sources as 'derived'.
The importer refreshes derived values on every run but never overwrites a value
Max has corrected by hand (source 'manual') — a hand-correction is permanently
authoritative over the guess.
"""

from __future__ import annotations

import re

# ------------------------------------------------------------- formality --

# The free-text formality collapses onto four base terms. A slashed value
# ("Casual / smart-casual") sits between its two halves.
_FORMALITY_TERMS = {
    "sportswear": 1,
    "sporty": 1,
    "casual": 2,
    "smart-casual": 4,
    "smart": 5,
}

_PARENTHETICAL = re.compile(r"\(([^)]*)\)")


def formality(raw: str | None) -> tuple[int | None, str | None]:
    """'Casual (club crest)' -> (2, 'club crest').

    The parenthetical is kept because it carries the reason the item is capped.
    """
    if not raw:
        return None, None

    note_match = _PARENTHETICAL.search(raw)
    note = note_match.group(1).strip() if note_match else None

    base = _PARENTHETICAL.sub("", raw).strip()
    scores = []
    for part in base.split("/"):
        term = part.strip().lower()
        if term in _FORMALITY_TERMS:
            scores.append(_FORMALITY_TERMS[term])

    if not scores:
        return None, note

    # round half up, so 'Smart / smart-casual' lands on 5 rather than 4
    rank = int(sum(scores) / len(scores) + 0.5)
    return max(1, min(5, rank)), note


# ------------------------------------------------------------- occasions --

# Seeded from the notes and from the exclusion list in work-outfits.md
# ("Kept out of the daily rotation"). Everything not named here gets the
# default: work + casual.
OCCASION_OVERRIDES = {
    # borderline-golf, excluded from work outfits
    "tops_06_vuori-grey-green-polo": ["golf", "casual"],
    "belts_08_cuater-grey-braided-stretch": ["golf", "casual"],
    # a crest reads as uniform -> casual only
    "lyle-scott-club-navy-vneck": ["casual"],
    # scope 'out' items
    "anko-black-quarterzip-fleece": ["gym"],
    "shoes_09a_nike-airmax-running": ["gym"],
    "shoes_06_zegna-black-monk": ["formal"],
    "shoes_08c_megis-driving-moc": ["casual"],
    # riding gear, not an office layering piece
    "outerwear_01_zara-brown-leather-bomber": ["casual"],
    # too formal for this office day to day; kept for client days and dinners
    "outerwear_04_indaco-brown-wool-overcoat": ["work", "casual", "formal"],
}

DEFAULT_OCCASIONS = ["work", "casual"]


def occasions(item: dict, formality_rank: int | None) -> list[str]:
    if item["id"] in OCCASION_OVERRIDES:
        return list(OCCASION_OVERRIDES[item["id"]])

    result = list(DEFAULT_OCCASIONS)
    if formality_rank is not None and formality_rank >= 5:
        result.append("formal")
    return result


# ---------------------------------------------------------------- warmth --

_WEIGHT_WARMTH = {
    "Fine": 2,
    "Light-Mid": 2,
    "Mid": 3,
    "Mid-Heavy": 4,
    "Chunky": 5,
}

_WARM_MATERIALS = re.compile(
    r"cashmere|wool|merino|lambswool|alpaca|fleece|down|padded|quilted|shearling",
    re.I,
)

# Shoes and belts have no weight and warmth means little for them: give them a
# neutral 2 so the picker's arithmetic still works.
_NO_WEIGHT_DEFAULT = 2


def warmth(item: dict) -> int:
    """1-5 for every item, not just outerwear."""
    if item.get("warmth") is not None:
        return int(item["warmth"])

    base = _WEIGHT_WARMTH.get(item.get("weight") or "", _NO_WEIGHT_DEFAULT)
    if _WARM_MATERIALS.search(item.get("material") or ""):
        base += 1
    return max(1, min(5, base))


# ------------------------------------------------------------- weather --

_RAIN_UNSAFE = re.compile(r"suede|nubuck", re.I)


def rain_unsafe(item: dict) -> bool:
    """Suede and nubuck stay home in the rain (styling rule 13)."""
    blob = " ".join(
        str(item.get(field) or "")
        for field in ("name", "material", "cut", "colour", "notes")
    )
    return bool(_RAIN_UNSAFE.search(blob))


def weatherproof(item: dict) -> tuple[bool, bool]:
    """(rain, wind). Only outerwear carries these in the JSON; default false."""
    wp = item.get("weatherproof") or {}
    return bool(wp.get("rain", False)), bool(wp.get("wind", False))


# ------------------------------------------------------------ bike-safe --

# A loafer or a moccasin comes off at speed. Those travel in the top-box and go
# on at the other end; everything else can be ridden in.
_NOT_RIDEABLE = re.compile(r"loafer|moc|moccasin|mocassin|slipper", re.I)


def bike_safe(item: dict) -> bool:
    if item.get("cat") != "Shoes":
        return True
    blob = " ".join(str(item.get(f) or "") for f in ("name", "cut", "notes"))
    return not _NOT_RIDEABLE.search(blob)


# --------------------------------------------------------------- pattern --

# The wardrobe is essentially all plain. These are the only exceptions called
# out in rules-and-context.md §6.
PATTERN_OVERRIDES = {
    "lyle-scott-club-navy-vneck": "Club crest",
    "tops_07_manfinity-greige-navy-tip-polo": "Contrast tipping",
    "tops_08_manfinity-blue-mustard-polo": "Contrast tipping",
    "trousers_06_stone-gingham": "Gingham waistband facing",
}

DEFAULT_PATTERN = "Plain"


def pattern(item: dict) -> str:
    return PATTERN_OVERRIDES.get(item["id"], DEFAULT_PATTERN)


# ------------------------------------------------------------------ neck --

# neck is free text with descriptive variants; normalise to a lookup code and
# keep the original in neck_raw.
_NECK_CODES = [
    "polo collar",
    "quarter-zip",
    "button/mock",
    "cardigan",
    "v-neck",
    "crew",
    "shawl",
    "roll",
]


def neck_code(raw: str | None) -> str | None:
    if not raw:
        return None
    lowered = raw.lower()
    for code in _NECK_CODES:
        if lowered.startswith(code):
            return code
    for code in _NECK_CODES:
        if code in lowered:
            return code
    return None

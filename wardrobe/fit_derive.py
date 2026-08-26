"""First-pass fit metadata, derived from the garments in the fit.

Everything here is a guess, recorded in fit_field_sources as 'derived'. The
importer refreshes derived values on every run and never overwrites one Max has
corrected by hand.

Deliberately NOT derived:
  * score   — his 1-10 opinion. Manual by definition.
  * killer  — his promotion flag.
  * style   — his characterisation.
  * bad_for — a negative claim. Deriving "this fit is wrong for X" from an
              absence in the item data would invent warnings he never made.
"""

from __future__ import annotations

BAND_COLD = "cold"
BAND_MILD = "mild"
BAND_WARM = "warm"

LAYER_ROLES = ("top", "layer", "outer", "base")

# The occasion codes items actually carry. good_for is derived within this
# vocabulary only; client/dinner/weekend/riding exist for Max to set by hand.
ITEM_OCCASION_VOCAB = ("work", "casual", "golf", "formal", "gym")

SEASONS_FOR_BAND = {
    BAND_COLD: ["winter"],
    BAND_MILD: ["autumn", "spring"],
    BAND_WARM: ["summer"],
}


def _layers(items: list[dict]) -> list[dict]:
    return [i for i in items if not i["is_alternate"] and i["role"] in LAYER_ROLES]


def centre_band(items: list[dict]) -> str:
    """The band a fit is built for — the old picker's inference, kept intact."""
    layers = _layers(items)
    if not layers:
        return BAND_MILD

    # A second layer — cardigan, blazer, vest, coat — makes it a cold fit.
    if len(layers) >= 2:
        return BAND_COLD

    only = layers[0]
    warmth = only["warmth"] or 3
    if warmth >= 4:
        return BAND_COLD
    # A polo on its own is the warm-weather answer; a knit on its own is mild.
    if only["cat"] == "Tops" and warmth <= 3:
        return BAND_WARM
    return BAND_MILD


def temp_bands(items: list[dict]) -> list[str]:
    """Which bands the fit is wearable in. Most span two.

    Everything is workable in mild, so a cold or warm fit picks up mild as well.
    """
    centre = centre_band(items)
    bands = {centre, BAND_MILD}
    return [b for b in (BAND_COLD, BAND_MILD, BAND_WARM) if b in bands]


def rain_safe(items: list[dict]) -> bool:
    """False if any garment in the fit proper is suede or nubuck."""
    return not any(i["rain_unsafe"] for i in items if not i["is_alternate"])


def formality_rank(items: list[dict]) -> int | None:
    """The mean formality of the garments, rounded — same 1-5 scale as items."""
    ranks = [
        i["formality_rank"]
        for i in items
        if not i["is_alternate"] and i["formality_rank"] is not None
    ]
    if not ranks:
        return None
    return max(1, min(5, int(sum(ranks) / len(ranks) + 0.5)))


def good_for(items: list[dict]) -> list[str]:
    """Occasions every garment in the fit allows.

    An intersection, not a union: a fit is only right for work if each piece is.
    That is what makes the golf polo keep its fit out of the work list.
    """
    sets = [
        set(i["occasions"] or [])
        for i in items
        if not i["is_alternate"]
    ]
    if not sets:
        return []
    shared = set.intersection(*sets)
    return [o for o in ITEM_OCCASION_VOCAB if o in shared]


def seasons(bands: list[str]) -> list[str]:
    """Browsing label only. Nothing in the picker may read this."""
    out = []
    for band in bands:
        for season in SEASONS_FOR_BAND[band]:
            if season not in out:
                out.append(season)
    return out

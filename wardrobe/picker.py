"""The outfit picker, ported from WardrobeKit.pick().

It chooses among the vetted looks. It does not generate new combinations —
that is deliberate: the 10 looks carry hand-reasoned styling rules that a
generator would quietly break. Free combinatorial generation is a follow-up.

Scoring, per rules-and-context.md §3:

  * weather band — cold (< 14 °C) / mild (14–22) / warm (> 22)
  * rain safety — rain rules out suede and nubuck
  * a Friday bonus for the cardigan look
  * a bonus for wear-as-is over needs-tailoring
  * a stable per-day rotation

New in this version: a look whose garments aren't clean is skipped, with the
reason said out loud ("Friday layer is out — the grey polo is in the wash").

pick() is deterministic per calendar day: same outfit all day, a different one
tomorrow. There is no random() anywhere — the rotation is seeded from the date,
so the page can be re-rendered as often as you like without flickering.

The functions here take plain dicts, so they can be tested from fixtures with
no database.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import date

COLD_BELOW = 14
WARM_ABOVE = 22

BAND_COLD = "cold"
BAND_MILD = "mild"
BAND_WARM = "warm"

# scoring weights
BAND_EXACT = 3.0
BAND_ADJACENT = 1.0
FRIDAY_BONUS = 2.0
WEAR_AS_IS_BONUS = 1.0
ROTATION_MAX = 2.0

FRIDAY_LOOK = "friday-layer"  # the cardigan look

_ADJACENT = {
    BAND_COLD: {BAND_MILD},
    BAND_MILD: {BAND_COLD, BAND_WARM},
    BAND_WARM: {BAND_MILD},
}


def weather_band(temp_c: float | None) -> str:
    if temp_c is None:
        return BAND_MILD
    if temp_c < COLD_BELOW:
        return BAND_COLD
    if temp_c > WARM_ABOVE:
        return BAND_WARM
    return BAND_MILD


@dataclass
class Look:
    """One vetted outfit, flattened for scoring."""

    slug: str
    name: str
    register: str
    rationale: str
    hidden_by_default: bool
    sort_order: int
    # each entry: {item_id, name, slot_role, position, is_alternate, warmth,
    #              rain_unsafe, verdict, laundry_state, cat}
    items: list[dict] = field(default_factory=list)

    def primary(self) -> list[dict]:
        return [i for i in self.items if not i["is_alternate"]]

    def alternates_for(self, slot_role: str, position: int) -> list[dict]:
        return [
            i
            for i in self.items
            if i["is_alternate"]
            and i["slot_role"] == slot_role
            and i["position"] == position
        ]


@dataclass
class Candidate:
    look: Look
    score: float
    band: str
    chosen: list[dict]         # the garments as picked, after substitutions
    substitutions: list[str]   # human-readable "swapped X for Y because …"
    reasons: list[str]         # why it scored what it scored


@dataclass
class Rejection:
    look: Look
    reason: str


def look_band(look: Look) -> str:
    """Which weather this look is for, from the warmth of its garments.

    Tops and outer layers decide it — a shoe's warmth says nothing useful about
    the weather, and belts say nothing at all.
    """
    layers = [
        i for i in look.primary() if i["slot_role"] in ("top", "mid-layer", "outer")
    ]
    if not layers:
        return BAND_MILD

    # Anything with a second layer — cardigan, blazer, vest, coat — is a cold look.
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


def rotation_value(slug: str, day: date) -> float:
    """A stable pseudo-random 0..ROTATION_MAX, fixed for a given day and look."""
    digest = hashlib.sha256(f"{day.isoformat()}:{slug}".encode()).hexdigest()
    return (int(digest[:8], 16) % 1000) / 1000 * ROTATION_MAX


def _unavailable(item: dict) -> str | None:
    """Why this garment can't be worn today, or None."""
    if item["laundry_state"] and item["laundry_state"] != "clean":
        labels = {
            "worn": "already worn",
            "in_wash": "in the wash",
            "at_tailor": "at the tailor",
        }
        return labels.get(item["laundry_state"], item["laundry_state"])
    if item["verdict"] == "Bin":
        return "binned"
    return None


def evaluate(
    look: Look,
    day: date,
    temp_c: float | None = None,
    rain: bool = False,
    allow_disliked: bool = False,
    allow_tailoring: bool = True,
) -> Candidate | Rejection:
    """Score one look for one day, substituting alternates where it helps."""
    if look.hidden_by_default and not allow_disliked:
        return Rejection(look, f"{look.name} is hidden by default (roll-neck)")

    chosen: list[dict] = []
    substitutions: list[str] = []

    for item in look.primary():
        blocker = _unavailable(item)
        if blocker is None and rain and item["rain_unsafe"]:
            blocker = f"not rain-safe ({item['material_hint'] or 'suede'})"
        if blocker is None and not allow_tailoring and item["verdict"] == "Tailor":
            blocker = "still needs tailoring"

        if blocker is None:
            chosen.append(item)
            continue

        replacement = None
        for alt in look.alternates_for(item["slot_role"], item["position"]):
            if _unavailable(alt) is not None:
                continue
            if rain and alt["rain_unsafe"]:
                continue
            if not allow_tailoring and alt["verdict"] == "Tailor":
                continue
            replacement = alt
            break

        if replacement is None:
            return Rejection(
                look, f"{look.name} is out — the {item['name']} is {blocker}"
            )

        chosen.append(replacement)
        substitutions.append(
            f"{replacement['name']} instead of the {item['name']} ({blocker})"
        )

    band = look_band(look)
    target = weather_band(temp_c)
    reasons = []

    if band == target:
        score = BAND_EXACT
        reasons.append(f"built for {band} weather")
    elif target in _ADJACENT[band]:
        score = BAND_ADJACENT
        reasons.append(f"a {band}-weather look, workable in {target}")
    else:
        score = 0.0
        reasons.append(f"a {band}-weather look on a {target} day")

    if day.weekday() == 4 and look.slug == FRIDAY_LOOK:
        score += FRIDAY_BONUS
        reasons.append("Friday — the cardigan look")

    if all(i["verdict"] != "Tailor" for i in chosen):
        score += WEAR_AS_IS_BONUS
        reasons.append("wearable as-is")

    if rain and any(i["weatherproof_rain"] for i in chosen):
        score += 0.5
        reasons.append("has a rain-ready layer")

    score += rotation_value(look.slug, day)

    return Candidate(
        look=look,
        score=round(score, 3),
        band=band,
        chosen=chosen,
        substitutions=substitutions,
        reasons=reasons,
    )


def pick(
    looks: list[Look],
    day: date,
    temp_c: float | None = None,
    rain: bool = False,
    allow_disliked: bool = False,
    allow_tailoring: bool = True,
    exclude: list[str] | None = None,
) -> tuple[Candidate | None, list[Candidate], list[Rejection]]:
    """Return (today's pick, the ranked runners-up, the rejected looks)."""
    exclude = set(exclude or [])
    candidates: list[Candidate] = []
    rejections: list[Rejection] = []

    for look in looks:
        if look.slug in exclude:
            rejections.append(Rejection(look, f"{look.name} was excluded by hand"))
            continue
        result = evaluate(look, day, temp_c, rain, allow_disliked, allow_tailoring)
        if isinstance(result, Rejection):
            rejections.append(result)
        else:
            candidates.append(result)

    # sort_order breaks any remaining tie, so the result is fully deterministic
    candidates.sort(key=lambda c: (-c.score, c.look.sort_order))
    best = candidates[0] if candidates else None
    return best, candidates, rejections


# ------------------------------------------------------------- loading --


def _rain_unsafe_word(*fields) -> str | None:
    """Which word makes this garment rain-unsafe — 'suede' or 'nubuck'."""
    blob = " ".join(f or "" for f in fields).lower()
    for word in ("nubuck", "suede"):
        if word in blob:
            return word
    return None


LOOKS_SQL = """
SELECT o.slug, o.name, o.register_code, o.rationale, o.hidden_by_default,
       o.sort_order,
       oi.item_id, i.name AS item_name, i.material, i.cat_code,
       oi.slot_role, oi.position, oi.is_alternate, oi.note,
       i.warmth, i.rain_unsafe, i.weatherproof_rain, i.verdict_code,
       COALESCE(l.state_code, 'clean') AS laundry_state
FROM outfits o
JOIN outfit_items oi ON oi.outfit_id = o.id
JOIN items i ON i.id = oi.item_id
LEFT JOIN item_laundry l ON l.item_id = i.id
WHERE o.vetted
ORDER BY o.sort_order, oi.position, oi.is_alternate
"""


def load_looks(conn) -> list[Look]:
    from . import db as _db

    looks: dict[str, Look] = {}
    for row in _db.fetch_all(conn, LOOKS_SQL):
        look = looks.get(row["slug"])
        if look is None:
            look = Look(
                slug=row["slug"],
                name=row["name"],
                register=row["register_code"],
                rationale=row["rationale"],
                hidden_by_default=row["hidden_by_default"],
                sort_order=row["sort_order"],
            )
            looks[row["slug"]] = look
        look.items.append(
            {
                "item_id": row["item_id"],
                "name": row["item_name"],
                "material_hint": _rain_unsafe_word(row["material"], row["item_name"]),
                "cat": row["cat_code"],
                "slot_role": row["slot_role"],
                "position": row["position"],
                "is_alternate": row["is_alternate"],
                "note": row["note"],
                "warmth": row["warmth"],
                "rain_unsafe": row["rain_unsafe"],
                "weatherproof_rain": row["weatherproof_rain"],
                "verdict": row["verdict_code"],
                "laundry_state": row["laundry_state"],
            }
        )
    return list(looks.values())

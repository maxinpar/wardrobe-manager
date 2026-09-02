"""The fit picker, ported from WardrobeKit.pick().

It chooses among the seeded fits. It does not generate new combinations — that
is deliberate: the fits carry hand-reasoned styling rules a generator would
quietly break. The builder is v2.

Scoring, per rules-and-context.md §3:

  * weather band — cold (< 14 °C) / mild (14–22) / warm (> 22)
  * rain safety — rain rules out suede and nubuck
  * a Friday bonus for the cardigan fit
  * a bonus for wear-as-is over needs-tailoring
  * a stable per-day rotation

Two things the fits addendum changes:

  * The temperature band is READ from fits.temp_bands, not inferred here. A fit
    usually spans two bands. Seasons are a browsing label and are never read by
    this module — if you find yourself writing season logic here, you have
    misread the spec.
  * A stale fit — one whose garment is in the wash, binned, out of scope, or
    blocked on an unmet precondition — is skipped, and the reason is said out
    loud. Where the fit offers an alternate for that slot, the alternate is
    substituted and the fit is rescued rather than skipped.

pick() is deterministic per calendar day: same fit all day, a different one
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

FRIDAY_FIT = "fit_friday_layer"  # the cardigan fit

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
class Fit:
    """One seeded fit, flattened for scoring."""

    id: str
    name: str
    register: str
    commentary: str
    catch: str | None
    style: str | None
    score: int | None            # Max's own 1-10. Read only; never written here.
    killer: bool
    hidden_by_default: bool
    sort_order: int
    source: str | None = None    # which pass produced it, e.g. 'work-outfits.md 2026-08-24'
    gone: bool = False           # binned. Loaded, never scored — see evaluate().
    hero_path: str | None = None      # the full-look render, if one exists
    hero_thumb: str | None = None
    hero_is_generated: bool = True    # a render must never imply a wearing
    render_upload: str | None = None  # uploaded in the app; outranks the hero
    # The same fit rendered WITH its optional layer. A variant of the hero, not
    # a rival to it: the hero is the without-layer render because the fit has to
    # stand up without the layer. NULL for every fit that has no optional layer.
    layered_path: str | None = None
    layered_thumb: str | None = None

    # Resolution order, in one place so no screen can disagree with another:
    # the upload wins, then the file-based hero, then the piece-strip fallback.
    @property
    def render(self) -> str | None:
        return self.render_upload or self.hero_path

    @property
    def render_thumb(self) -> str | None:
        """An upload has no generated thumbnail — it is already downscaled."""
        return self.render_upload or self.hero_thumb or self.hero_path

    @property
    def render_is_upload(self) -> bool:
        return bool(self.render_upload)

    @property
    def layered_render(self) -> str | None:
        """The layered render's thumbnail, falling back to the full image."""
        return self.layered_thumb or self.layered_path

    @property
    def has_two_looks(self) -> bool:
        """Whether this fit can be shown as a pair.

        An upload is excluded on purpose: it replaces the hero, so pairing it
        with the layered render would caption someone else's picture "without
        the layer". The pair only means anything when both halves came from the
        same generated set.
        """
        return bool(self.layered_path) and not self.render_is_upload

    @property
    def layer_piece(self) -> str | None:
        """The garment that comes off — named, so the note can say which.

        The note is the real answer: the golf batch writes "Optional — comes off
        at the range" on the piece that does, and a fit can carry both a layer
        and an outer. Role is the fallback for the fits whose slots were written
        before that convention, and `layer` is tried before `outer` because an
        outer over a layer is the one that stays on.
        """
        for item in self.items:
            if item["is_alternate"]:
                continue
            if (item.get("note") or "").strip().lower().startswith("optional"):
                return item["name"]
        for role in ("layer", "outer"):
            for item in self.items:
                if item["role"] == role and not item["is_alternate"]:
                    return item["name"]
        return None
    temp_bands: list[str] = field(default_factory=list)
    # each entry: {item_id, name, role, position, is_alternate, warmth,
    #              rain_unsafe, verdict, scope, laundry_state, cat}
    items: list[dict] = field(default_factory=list)
    # unmet one-off jobs blocking this fit
    blocked_by: list[str] = field(default_factory=list)

    def primary(self) -> list[dict]:
        return [i for i in self.items if not i["is_alternate"]]

    def alternates_for(self, role: str, position: int) -> list[dict]:
        return [
            i
            for i in self.items
            if i["is_alternate"] and i["role"] == role and i["position"] == position
        ]


@dataclass
class Candidate:
    fit: Fit
    score: float
    band: str
    chosen: list[dict]         # the garments as picked, after substitutions
    substitutions: list[str]   # human-readable "swapped X for Y because …"
    reasons: list[str]         # why it scored what it scored


@dataclass
class Rejection:
    fit: Fit
    reason: str


def rotation_value(fit_id: str, day: date) -> float:
    """A stable pseudo-random 0..ROTATION_MAX, fixed for a given day and fit."""
    digest = hashlib.sha256(f"{day.isoformat()}:{fit_id}".encode()).hexdigest()
    return (int(digest[:8], 16) % 1000) / 1000 * ROTATION_MAX


def unavailable(item: dict) -> str | None:
    """Why this garment can't be worn today, or None.

    Computed from current item state every time — never stored. A stored
    'wearable' boolean would go stale, which is the exact failure it would exist
    to prevent.
    """
    # Physically gone outranks the rest — a garment that no longer exists is
    # not "in the wash" and not merely "binned" in the verdict sense. Kept
    # distinct from the Bin verdict below, which is only an opinion that it
    # should go; see migrations/009_gone.sql.
    if item.get("gone"):
        return "gone"
    # `worn` means used since its last wash and STILL WEARABLE. It does not
    # block a fit — that is the whole point of a base that holds five days.
    # Only the wash and the tailor make a garment unavailable.
    state = item.get("laundry_state")
    if state in ("in_wash", "at_tailor"):
        return {"in_wash": "in the wash", "at_tailor": "at the tailor"}[state]
    if item["verdict"] == "Bin":
        return "binned"
    if item["verdict"] == "Replace":
        return "on the way out (Replace)"
    if item.get("scope") == "out":
        return "out of scope"
    if item.get("retired"):
        return "no longer in the catalogue"
    return None


def staleness(fit: Fit) -> list[str]:
    """Everything currently blocking this fit, named. Empty means wearable.

    The Fits screen shows these as badges and never hides the fit; the picker
    skips it and says why.
    """
    problems = []
    for item in fit.primary():
        blocker = unavailable(item)
        if blocker is None:
            continue
        # An alternate that is itself fine rescues the slot.
        if any(
            unavailable(alt) is None
            for alt in fit.alternates_for(item["role"], item["position"])
        ):
            continue
        problems.append(f"{item['name']} is {blocker}")
    for job in fit.blocked_by:
        problems.append(f"Blocked: {job}")
    return problems


def gone_pieces(fit: Fit) -> list[str]:
    """Names of this fit's garments that are physically gone and unrescued.

    Separate from staleness() because a gone garment is permanent — the fit
    sorts to the bottom of the gallery and stays there — where in the wash or
    at the tailor clears on its own.
    """
    out = []
    for item in fit.primary():
        if not item.get("gone"):
            continue
        if any(
            unavailable(alt) is None
            for alt in fit.alternates_for(item["role"], item["position"])
        ):
            continue
        out.append(item["name"])
    return out


def evaluate(
    fit: Fit,
    day: date,
    temp_c: float | None = None,
    rain: bool = False,
    allow_disliked: bool = False,
    allow_tailoring: bool = True,
) -> Candidate | Rejection:
    """Score one fit for one day, substituting alternates where it helps."""
    # Binned is binned. Ahead of every other test, and not reachable by
    # allow_disliked — that switch is for the roll-neck, which is a preference.
    if fit.gone:
        return Rejection(fit, f"{fit.name} is binned")

    if fit.hidden_by_default and not allow_disliked:
        return Rejection(fit, f"{fit.name} is hidden by default (roll-neck)")

    if fit.blocked_by:
        return Rejection(fit, f"{fit.name} is blocked: {'; '.join(fit.blocked_by)}")

    chosen: list[dict] = []
    substitutions: list[str] = []

    for item in fit.primary():
        blocker = unavailable(item)
        if blocker is None and rain and item["rain_unsafe"]:
            blocker = f"not rain-safe ({item['material_hint'] or 'suede'})"
        if blocker is None and not allow_tailoring and item["verdict"] == "Tailor":
            blocker = "still needs tailoring"

        if blocker is None:
            chosen.append(item)
            continue

        replacement = None
        for alt in fit.alternates_for(item["role"], item["position"]):
            if unavailable(alt) is not None:
                continue
            if rain and alt["rain_unsafe"]:
                continue
            if not allow_tailoring and alt["verdict"] == "Tailor":
                continue
            replacement = alt
            break

        if replacement is None:
            return Rejection(fit, f"{fit.name} is out — the {item['name']} is {blocker}")

        chosen.append(replacement)
        substitutions.append(
            f"{replacement['name']} instead of the {item['name']} ({blocker})"
        )

    target = weather_band(temp_c)
    bands = fit.temp_bands or [BAND_MILD]
    reasons = []

    if target in bands:
        score = BAND_EXACT
        reasons.append(f"built for {target} weather")
    elif any(target in _ADJACENT[b] for b in bands):
        score = BAND_ADJACENT
        reasons.append(f"a {'/'.join(bands)} fit, workable in {target}")
    else:
        score = 0.0
        reasons.append(f"a {'/'.join(bands)} fit on a {target} day")

    if day.weekday() == 4 and fit.id == FRIDAY_FIT:
        score += FRIDAY_BONUS
        reasons.append("Friday — the cardigan fit")

    if all(i["verdict"] != "Tailor" for i in chosen):
        score += WEAR_AS_IS_BONUS
        reasons.append("wearable as-is")

    if rain and any(i["weatherproof_rain"] for i in chosen):
        score += 0.5
        reasons.append("has a rain-ready layer")

    score += rotation_value(fit.id, day)

    return Candidate(
        fit=fit,
        score=round(score, 3),
        band="/".join(bands),
        chosen=chosen,
        substitutions=substitutions,
        reasons=reasons,
    )


def pick(
    fits: list[Fit],
    day: date,
    temp_c: float | None = None,
    rain: bool = False,
    allow_disliked: bool = False,
    allow_tailoring: bool = True,
    exclude: list[str] | None = None,
) -> tuple[Candidate | None, list[Candidate], list[Rejection]]:
    """Return (today's pick, the ranked runners-up, the rejected fits)."""
    exclude = set(exclude or [])
    candidates: list[Candidate] = []
    rejections: list[Rejection] = []

    for fit in fits:
        if fit.id in exclude:
            rejections.append(Rejection(fit, f"{fit.name} was excluded by hand"))
            continue
        result = evaluate(fit, day, temp_c, rain, allow_disliked, allow_tailoring)
        if isinstance(result, Rejection):
            rejections.append(result)
        else:
            candidates.append(result)

    # sort_order breaks any remaining tie, so the result is fully deterministic
    candidates.sort(key=lambda c: (-c.score, c.fit.sort_order))
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


FITS_SQL = """
SELECT f.id, f.name, f.register_code, f.commentary, f.catch, f.style, f.score,
       f.killer, f.hidden_by_default, f.sort_order, f.source,
       f.hero_image_path, f.hero_thumb_path, f.hero_is_generated,
       f.render_upload_path, f.layered_image_path, f.layered_thumb_path,
       (f.gone_at IS NOT NULL) AS fit_gone,
       fi.item_id, i.name AS item_name, i.material, i.cat_code,
       fi.role, fi.position, fi.is_alternate, fi.note,
       i.warmth, i.rain_unsafe, i.weatherproof_rain, i.verdict_code, i.scope_code,
       (i.retired_at IS NOT NULL) AS retired,
       (i.gone_at IS NOT NULL) AS gone,
       COALESCE(l.state_code, 'clean') AS laundry_state
FROM fits f
-- LEFT so a fit whose garment list was lost still loads. Eight of them exist:
-- the render is real, the composition is unknown, and a fit that cannot even be
-- opened is worse than one that says so.
LEFT JOIN fit_items fi ON fi.fit_id = f.id
LEFT JOIN items i ON i.id = fi.item_id
LEFT JOIN item_laundry l ON l.item_id = i.id
ORDER BY f.sort_order, fi.position, fi.is_alternate
"""

BANDS_SQL = "SELECT fit_id, band_code FROM fit_temp_bands ORDER BY fit_id, band_code"

BLOCKERS_SQL = (
    "SELECT fit_id, text FROM fit_preconditions WHERE NOT done ORDER BY fit_id, id"
)


def load_fits(conn) -> list[Fit]:
    from . import db as _db

    bands: dict[str, list[str]] = {}
    for row in _db.fetch_all(conn, BANDS_SQL):
        bands.setdefault(row["fit_id"], []).append(row["band_code"])

    blockers: dict[str, list[str]] = {}
    for row in _db.fetch_all(conn, BLOCKERS_SQL):
        blockers.setdefault(row["fit_id"], []).append(row["text"])

    fits: dict[str, Fit] = {}
    for row in _db.fetch_all(conn, FITS_SQL):
        fit = fits.get(row["id"])
        if fit is None:
            fit = Fit(
                id=row["id"],
                name=row["name"],
                register=row["register_code"],
                commentary=row["commentary"],
                catch=row["catch"],
                style=row["style"],
                score=row["score"],
                killer=row["killer"],
                hidden_by_default=row["hidden_by_default"],
                sort_order=row["sort_order"],
                source=row["source"],
                gone=row["fit_gone"],
                hero_path=row["hero_image_path"],
                hero_thumb=row["hero_thumb_path"],
                hero_is_generated=row["hero_is_generated"],
                render_upload=row["render_upload_path"],
                layered_path=row["layered_image_path"],
                layered_thumb=row["layered_thumb_path"],
                temp_bands=[
                    b
                    for b in (BAND_COLD, BAND_MILD, BAND_WARM)
                    if b in bands.get(row["id"], [])
                ],
                blocked_by=blockers.get(row["id"], []),
            )
            fits[row["id"]] = fit
        if row["item_id"] is None:
            continue          # a fit with no known composition
        fit.items.append(
            {
                "item_id": row["item_id"],
                "name": row["item_name"],
                "material_hint": _rain_unsafe_word(row["material"], row["item_name"]),
                "cat": row["cat_code"],
                "role": row["role"],
                "position": row["position"],
                "is_alternate": row["is_alternate"],
                "note": row["note"],
                "warmth": row["warmth"],
                "rain_unsafe": row["rain_unsafe"],
                "weatherproof_rain": row["weatherproof_rain"],
                "verdict": row["verdict_code"],
                "scope": row["scope_code"],
                "laundry_state": row["laundry_state"],
                "retired": row["retired"],
                "gone": row["gone"],
            }
        )
    return list(fits.values())

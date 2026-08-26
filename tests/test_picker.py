"""Picker and fit behaviour, from fixtures. Runs offline — no database needed.

    python -m pytest tests
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import fit_derive, picker  # noqa: E402


def garment(
    item_id,
    name,
    role,
    position,
    *,
    cat="Knitwear",
    warmth=3,
    rain_unsafe=False,
    weatherproof_rain=False,
    verdict="Keep",
    scope="core",
    laundry_state="clean",
    is_alternate=False,
    note=None,
    formality_rank=3,
    occasions=("work", "casual"),
):
    return {
        "item_id": item_id,
        "name": name,
        "material_hint": "suede" if rain_unsafe else None,
        "cat": cat,
        "role": role,
        "position": position,
        "is_alternate": is_alternate,
        "note": note,
        "warmth": warmth,
        "rain_unsafe": rain_unsafe,
        "weatherproof_rain": weatherproof_rain,
        "verdict": verdict,
        "scope": scope,
        "laundry_state": laundry_state,
        "formality_rank": formality_rank,
        "occasions": list(occasions),
    }


def make_fit(
    fit_id="fit_friday_layer",
    hidden=False,
    items=None,
    sort_order=1,
    bands=("mild",),
    blocked_by=(),
    killer=False,
    score=None,
):
    return picker.Fit(
        id=fit_id,
        name=fit_id.replace("fit_", "").replace("_", " ").title(),
        register="everyday",
        commentary="because",
        catch=None,
        style=None,
        score=score,
        killer=killer,
        hidden_by_default=hidden,
        sort_order=sort_order,
        temp_bands=list(bands),
        blocked_by=list(blocked_by),
        items=items
        or [
            garment("polo", "grey polo", "top", 1, cat="Tops"),
            garment("jeans", "indigo jeans", "bottom", 2),
            garment("boots", "brown Chelsea", "shoe", 3),
        ],
    )


FRIDAY = date(2026, 8, 21)  # a Friday
MONDAY = date(2026, 8, 24)


def test_weather_bands():
    assert picker.weather_band(9) == "cold"
    assert picker.weather_band(13.9) == "cold"
    assert picker.weather_band(14) == "mild"
    assert picker.weather_band(22) == "mild"
    assert picker.weather_band(22.1) == "warm"
    assert picker.weather_band(None) == "mild"


def test_same_day_is_stable_and_next_day_can_differ():
    fits = [make_fit("fit_a", sort_order=1), make_fit("fit_b", sort_order=2)]
    first, _, _ = picker.pick(fits, MONDAY, temp_c=18)
    again, _, _ = picker.pick(fits, MONDAY, temp_c=18)
    assert first.fit.id == again.fit.id  # no random(), no flicker

    rotation = {
        picker.pick(fits, date(2026, 9, d), temp_c=18)[0].fit.id for d in range(1, 29)
    }
    assert rotation == {"fit_a", "fit_b"}  # the rotation does move


def test_the_picker_reads_stored_bands_not_the_garments():
    """A fit declared warm scores as warm even if its garments look mild."""
    warm = make_fit("fit_warm", bands=("warm", "mild"))
    assert "built for warm weather" in picker.evaluate(warm, MONDAY, temp_c=28).reasons


def test_a_fit_spanning_two_bands_matches_both():
    fit = make_fit("fit_spanning", bands=("cold", "mild"))
    assert "built for cold weather" in picker.evaluate(fit, MONDAY, temp_c=10).reasons
    assert "built for mild weather" in picker.evaluate(fit, MONDAY, temp_c=18).reasons


def test_rain_rules_out_suede_and_says_so():
    fit = make_fit(
        "fit_suede",
        items=[
            garment("polo", "grey polo", "top", 1, cat="Tops"),
            garment("chino", "stone chino", "bottom", 2),
            garment("loafer", "suede penny loafer", "shoe", 3, rain_unsafe=True),
        ],
    )
    assert isinstance(
        picker.evaluate(fit, MONDAY, temp_c=18, rain=False), picker.Candidate
    )

    wet = picker.evaluate(fit, MONDAY, temp_c=18, rain=True)
    assert isinstance(wet, picker.Rejection)
    assert "suede penny loafer" in wet.reason and "rain" in wet.reason


def test_an_alternate_rescues_a_fit_rather_than_it_disappearing():
    """The addendum's point: rescue beats skip."""
    fit = make_fit(
        "fit_swappable",
        items=[
            garment("polo", "grey polo", "top", 1, cat="Tops"),
            garment("chino", "stone chino", "bottom", 2),
            garment("sneaker", "Ecco sneaker", "shoe", 3, laundry_state="in_wash"),
            garment("derby", "leather derby", "shoe", 3, is_alternate=True),
        ],
    )
    result = picker.evaluate(fit, MONDAY, temp_c=18)
    assert isinstance(result, picker.Candidate)
    assert [i["item_id"] for i in result.chosen] == ["polo", "chino", "derby"]
    assert "leather derby instead of the Ecco sneaker" in result.substitutions[0]
    # and it is not reported stale, because the slot is covered
    assert picker.staleness(fit) == []


def test_laundry_state_blocks_a_fit_and_names_the_garment():
    fit = make_fit(
        "fit_friday_layer",
        items=[
            garment("polo", "grey polo", "top", 1, cat="Tops", laundry_state="in_wash"),
            garment("jeans", "indigo jeans", "bottom", 2),
        ],
    )
    result = picker.evaluate(fit, FRIDAY, temp_c=15)
    assert isinstance(result, picker.Rejection)
    assert result.reason == "Friday Layer is out — the grey polo is in the wash"
    assert picker.staleness(fit) == ["grey polo is in the wash"]


def test_worn_does_not_block_a_fit_but_the_wash_does():
    """A base holds five days, so wearing a garment cannot take it out of play."""
    worn = make_fit(
        "fit_worn",
        items=[
            garment("polo", "grey polo", "top", 1, cat="Tops", laundry_state="worn"),
            garment("jeans", "indigo jeans", "bottom", 2),
        ],
    )
    assert isinstance(picker.evaluate(worn, MONDAY, temp_c=18), picker.Candidate)
    assert picker.staleness(worn) == []

    for blocking in ("in_wash", "at_tailor"):
        fit = make_fit(
            "fit_blocked_" + blocking,
            items=[
                garment("polo", "grey polo", "top", 1, cat="Tops", laundry_state=blocking),
                garment("jeans", "indigo jeans", "bottom", 2),
            ],
        )
        assert isinstance(picker.evaluate(fit, MONDAY, temp_c=18), picker.Rejection)
        assert picker.staleness(fit), f"{blocking} should block"


def test_staleness_names_binned_and_out_of_scope_items_without_hiding_the_fit():
    fit = make_fit(
        "fit_stale",
        items=[
            garment("moto", "faux-leather moto", "outer", 1, verdict="Bin"),
            garment("trainer", "Nike running trainer", "shoe", 2, scope="out"),
        ],
    )
    problems = picker.staleness(fit)
    assert "faux-leather moto is binned" in problems
    assert "Nike running trainer is out of scope" in problems
    # the picker skips it, but the fit still exists to be shown with badges
    assert isinstance(picker.evaluate(fit, MONDAY, temp_c=18), picker.Rejection)


def test_an_unmet_precondition_blocks_a_fit_and_is_named():
    fit = make_fit("fit_blocked", blocked_by=["Repair the Fedeli cuff"])
    result = picker.evaluate(fit, MONDAY, temp_c=18)
    assert isinstance(result, picker.Rejection)
    assert "Repair the Fedeli cuff" in result.reason
    assert picker.staleness(fit) == ["Blocked: Repair the Fedeli cuff"]

    fit.blocked_by = []
    assert isinstance(picker.evaluate(fit, MONDAY, temp_c=18), picker.Candidate)


def test_friday_bonus_applies_only_to_the_cardigan_fit_on_a_friday():
    friday_fit = make_fit(picker.FRIDAY_FIT)
    other = make_fit("fit_other")

    assert "Friday — the cardigan fit" in picker.evaluate(
        friday_fit, FRIDAY, temp_c=18
    ).reasons
    assert "Friday — the cardigan fit" not in picker.evaluate(
        friday_fit, MONDAY, temp_c=18
    ).reasons
    assert "Friday — the cardigan fit" not in picker.evaluate(
        other, FRIDAY, temp_c=18
    ).reasons


def test_roll_neck_fit_is_hidden_unless_allowed():
    fits = [make_fit("fit_the_sharp_one", hidden=True)]
    best, _, rejected = picker.pick(fits, MONDAY, temp_c=18)
    assert best is None
    assert "hidden by default" in rejected[0].reason

    best, _, _ = picker.pick(fits, MONDAY, temp_c=18, allow_disliked=True)
    assert best is not None


def test_wear_as_is_beats_needs_tailoring():
    as_is = picker.evaluate(make_fit("fit_as_is"), MONDAY, temp_c=18)
    needs_work = picker.evaluate(
        make_fit(
            "fit_needs_work",
            items=[
                garment("polo", "grey polo", "top", 1, cat="Tops"),
                garment("trouser", "unhemmed trouser", "bottom", 2, verdict="Tailor"),
            ],
        ),
        MONDAY,
        temp_c=18,
    )
    assert "wearable as-is" in as_is.reasons
    assert "wearable as-is" not in needs_work.reasons


def test_tailoring_can_be_ruled_out_entirely():
    fit = make_fit(
        "fit_needs_work",
        items=[
            garment("polo", "grey polo", "top", 1, cat="Tops"),
            garment("trouser", "unhemmed trouser", "bottom", 2, verdict="Tailor"),
        ],
    )
    result = picker.evaluate(fit, MONDAY, temp_c=18, allow_tailoring=False)
    assert isinstance(result, picker.Rejection)
    assert "still needs tailoring" in result.reason


def test_the_picker_never_touches_max_s_own_numbers():
    """score and killer are read-only here — the app is their only writer."""
    scored = make_fit("fit_scored", score=9, killer=True)
    result = picker.evaluate(scored, MONDAY, temp_c=18)
    assert scored.score == 9 and scored.killer is True

    # and his score contributes nothing to the computed rank
    unscored = make_fit("fit_scored", score=None, killer=False)
    assert picker.evaluate(unscored, MONDAY, temp_c=18).score == result.score


# --------------------------------------------------------- derivation --


def test_derived_bands_span_two_and_always_include_mild():
    layered = [
        garment("polo", "polo", "top", 1, cat="Tops"),
        garment("cardi", "cardigan", "layer", 2),
    ]
    polo_only = [garment("polo", "polo", "top", 1, cat="Tops", warmth=3)]
    knit_only = [garment("knit", "crew", "top", 1, warmth=3)]

    assert fit_derive.temp_bands(layered) == ["cold", "mild"]
    assert fit_derive.temp_bands(polo_only) == ["mild", "warm"]
    assert fit_derive.temp_bands(knit_only) == ["mild"]


def test_derived_seasons_follow_the_bands():
    assert fit_derive.seasons(["cold", "mild"]) == ["winter", "autumn", "spring"]
    assert fit_derive.seasons(["mild", "warm"]) == ["autumn", "spring", "summer"]


def test_good_for_is_the_intersection_so_a_golf_item_keeps_a_fit_out_of_work():
    items = [
        garment("polo", "golf polo", "top", 1, occasions=("golf", "casual")),
        garment("chino", "chino", "bottom", 2, occasions=("work", "casual")),
    ]
    assert fit_derive.good_for(items) == ["casual"]


def test_rain_safe_and_formality_are_derived_from_the_garments():
    items = [
        garment("polo", "polo", "top", 1, formality_rank=4),
        garment("loafer", "suede loafer", "shoe", 2, rain_unsafe=True, formality_rank=4),
    ]
    assert fit_derive.rain_safe(items) is False
    assert fit_derive.formality_rank(items) == 4
    assert fit_derive.rain_safe(items[:1]) is True


def test_alternates_are_ignored_by_the_derivation():
    items = [
        garment("polo", "polo", "top", 1, cat="Tops"),
        garment("coat", "overcoat", "outer", 2, is_alternate=True, warmth=5),
    ]
    assert fit_derive.temp_bands(items) == ["mild", "warm"]

"""Picker behaviour, from fixtures. Runs offline — no database needed.

    python -m pytest tests
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import picker  # noqa: E402


def garment(
    item_id,
    name,
    slot_role,
    position,
    *,
    cat="Knitwear",
    warmth=3,
    rain_unsafe=False,
    weatherproof_rain=False,
    verdict="Keep",
    laundry_state="clean",
    is_alternate=False,
    note=None,
):
    return {
        "item_id": item_id,
        "name": name,
        "material_hint": "suede" if rain_unsafe else "cotton",
        "cat": cat,
        "slot_role": slot_role,
        "position": position,
        "is_alternate": is_alternate,
        "note": note,
        "warmth": warmth,
        "rain_unsafe": rain_unsafe,
        "weatherproof_rain": weatherproof_rain,
        "verdict": verdict,
        "laundry_state": laundry_state,
    }


def make_look(slug="friday-layer", hidden=False, items=None, sort_order=1):
    return picker.Look(
        slug=slug,
        name=slug.replace("-", " ").title(),
        register="everyday",
        rationale="because",
        hidden_by_default=hidden,
        sort_order=sort_order,
        items=items
        or [
            garment("polo", "grey polo", "top", 1, cat="Tops"),
            garment("jeans", "indigo jeans", "trouser", 2),
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
    looks = [make_look("a", sort_order=1), make_look("b", sort_order=2)]
    first, _, _ = picker.pick(looks, MONDAY, temp_c=18)
    again, _, _ = picker.pick(looks, MONDAY, temp_c=18)
    assert first.look.slug == again.look.slug  # no random(), no flicker

    rotations = {
        picker.pick(looks, date(2026, 9, d), temp_c=18)[0].look.slug for d in range(1, 29)
    }
    assert rotations == {"a", "b"}  # the rotation does move


def test_rain_rules_out_suede_and_says_so():
    look = make_look(
        "suede-look",
        items=[
            garment("polo", "grey polo", "top", 1, cat="Tops"),
            garment("chino", "stone chino", "trouser", 2),
            garment("loafer", "suede penny loafer", "shoe", 3, rain_unsafe=True),
        ],
    )
    dry = picker.evaluate(look, MONDAY, temp_c=18, rain=False)
    assert isinstance(dry, picker.Candidate)

    wet = picker.evaluate(look, MONDAY, temp_c=18, rain=True)
    assert isinstance(wet, picker.Rejection)
    assert "suede penny loafer" in wet.reason and "rain" in wet.reason


def test_rain_substitutes_a_clean_alternate_rather_than_dropping_the_look():
    look = make_look(
        "swappable",
        items=[
            garment("polo", "grey polo", "top", 1, cat="Tops"),
            garment("chino", "stone chino", "trouser", 2),
            garment("loafer", "suede loafer", "shoe", 3, rain_unsafe=True),
            garment("derby", "leather derby", "shoe", 3, is_alternate=True),
        ],
    )
    wet = picker.evaluate(look, MONDAY, temp_c=18, rain=True)
    assert isinstance(wet, picker.Candidate)
    assert [i["item_id"] for i in wet.chosen] == ["polo", "chino", "derby"]
    assert "leather derby instead of the suede loafer" in wet.substitutions[0]


def test_laundry_state_blocks_a_look_and_names_the_garment():
    look = make_look(
        "friday-layer",
        items=[
            garment("polo", "grey polo", "top", 1, cat="Tops", laundry_state="in_wash"),
            garment("jeans", "indigo jeans", "trouser", 2),
        ],
    )
    result = picker.evaluate(look, FRIDAY, temp_c=15)
    assert isinstance(result, picker.Rejection)
    assert result.reason == "Friday Layer is out — the grey polo is in the wash"


def test_friday_bonus_applies_only_to_the_cardigan_look_on_a_friday():
    friday_look = make_look(picker.FRIDAY_LOOK)
    other = make_look("other")

    on_friday = picker.evaluate(friday_look, FRIDAY, temp_c=18)
    on_monday = picker.evaluate(friday_look, MONDAY, temp_c=18)
    assert "Friday — the cardigan look" in on_friday.reasons
    assert "Friday — the cardigan look" not in on_monday.reasons

    other_friday = picker.evaluate(other, FRIDAY, temp_c=18)
    assert "Friday — the cardigan look" not in other_friday.reasons


def test_roll_neck_look_is_hidden_unless_allowed():
    looks = [make_look("the-sharp-one", hidden=True)]
    best, _, rejected = picker.pick(looks, MONDAY, temp_c=18)
    assert best is None
    assert "hidden by default" in rejected[0].reason

    best, _, _ = picker.pick(looks, MONDAY, temp_c=18, allow_disliked=True)
    assert best is not None


def test_wear_as_is_beats_needs_tailoring():
    as_is = picker.evaluate(make_look("as-is"), MONDAY, temp_c=18)
    needs_work = picker.evaluate(
        make_look(
            "needs-work",
            items=[
                garment("polo", "grey polo", "top", 1, cat="Tops"),
                garment("trouser", "unhemmed trouser", "trouser", 2, verdict="Tailor"),
            ],
        ),
        MONDAY,
        temp_c=18,
    )
    assert "wearable as-is" in as_is.reasons
    assert "wearable as-is" not in needs_work.reasons


def test_tailoring_can_be_ruled_out_entirely():
    look = make_look(
        "needs-work",
        items=[
            garment("polo", "grey polo", "top", 1, cat="Tops"),
            garment("trouser", "unhemmed trouser", "trouser", 2, verdict="Tailor"),
        ],
    )
    result = picker.evaluate(look, MONDAY, temp_c=18, allow_tailoring=False)
    assert isinstance(result, picker.Rejection)
    assert "still needs tailoring" in result.reason


def test_binned_items_are_never_suggested():
    look = make_look(
        "binned",
        items=[garment("jacket", "pleather moto", "outer", 1, verdict="Bin")],
    )
    assert isinstance(picker.evaluate(look, MONDAY, temp_c=10), picker.Rejection)


def test_band_from_layers():
    two_layers = make_look(
        "layered",
        items=[
            garment("polo", "polo", "top", 1, cat="Tops"),
            garment("cardi", "cardigan", "mid-layer", 2),
        ],
    )
    polo_only = make_look(
        "polo-only", items=[garment("polo", "polo", "top", 1, cat="Tops", warmth=3)]
    )
    knit_only = make_look("knit-only", items=[garment("knit", "crew", "top", 1, warmth=3)])

    assert picker.look_band(two_layers) == "cold"
    assert picker.look_band(polo_only) == "warm"
    assert picker.look_band(knit_only) == "mild"

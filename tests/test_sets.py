"""What a set is, and the sentences the This Week screen writes about it.

Runs offline against fixtures. The three set shapes here are the three the
database actually holds, because each of them broke a different assumption
during the design:

  * black_canvas — a fixed GILET, and the top changes.
  * the_shawl    — a fixed KNIT in the `top` slot, and the tee UNDER it changes.
  * beige_brown  — NO fixed layer at all: the top itself is what varies.

Copy that reads correctly for the first two and contradicts the third is the
specific failure this file exists to catch.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import picker, sets  # noqa: E402


def garment(item_id, name, role, position=1, **extra):
    return {
        "item_id": item_id,
        "name": name,
        "role": role,
        "position": position,
        "is_alternate": False,
        "note": None,
        "cat": extra.get("cat", "Knitwear"),
        "warmth": 3,
        "rain_unsafe": False,
        "weatherproof_rain": False,
        "verdict": "Keep",
        "scope": "core",
        "laundry_state": "clean",
        "material_hint": extra.get("material_hint"),
        "rain_unsafe": extra.get("rain_unsafe", False),
        "formality_rank": 3,
        "occasions": ("work", "casual"),
    }


def fit(fit_id, name, items, position, variant_set, bands=("cold", "mild")):
    return picker.Fit(
        temp_bands=list(bands),
        id=fit_id,
        name=name,
        register="everyday",
        commentary="",
        catch=None,
        style=None,
        score=None,
        killer=False,
        hidden_by_default=False,
        sort_order=100,
        variant_set=variant_set,
        variant_position=position,
        items=items,
        hero_thumb=f"fits/thumbs/{fit_id}_render.jpg",
    )


BASE = [
    garment("trousers_11_black-coated-jeans", "Black coated straight jeans", "bottom", 4),
    garment("belts_11_black-classic-pin-buckle", "Black classic pin-buckle belt", "belt", 5),
    garment("shoes_03_ecco-black-nubuck", "Ecco nubuck sneaker", "shoe", 6, cat="Shoes",
            rain_unsafe=True, material_hint="nubuck"),
]

COLOURS = {
    "trousers_11_black-coated-jeans": "Black (coated / waxed finish)",
    "belts_11_black-classic-pin-buckle": "Black",
    "shoes_03_ecco-black-nubuck": "Black",
    "outerwear_06_anko-slate-puffer-vest": "Slate blue-grey",
    "ben-sherman-aubergine-shawl": "Aubergine",
    "tops_31_zara-charcoal-textured-shirt": "Charcoal",
    "tops_05_sage-pique-polo": "Sage green",
    "tees_02_grey-crew": "Grey",
    "tees_03_black-crew": "Black",
    "trousers_01_decathlon-beige": "Sand / warm beige",
    "belts_04_distressed-brown-everyday": "Rustic / distressed medium brown",
    "shoes_07_oxford-brown-chelsea": "Brown / chestnut",
}


class FakeConn:
    """Answers the four queries sets.load makes, and nothing else.

    A stub rather than a database because these are rules about words, and a
    rule about words that can only be checked against 297 live garments is a
    rule nobody checks.
    """

    def __init__(self, fits, names):
        self.fits = fits
        self.names = names

    def rows(self, sql):
        if "FROM variant_sets" in sql:
            return self.names
        if "short_name IS NOT NULL" in sql:
            return [{"id": "belts_04_distressed-brown-everyday", "short_name": "brown belt"}]
        if "SELECT id, colour FROM items" in sql:
            return [{"id": k, "colour": v} for k, v in COLOURS.items()]
        if "formality_rank" in sql:
            return [{"id": f.id, "formality_rank": 3} for f in self.fits]
        raise AssertionError(f"unexpected query: {sql}")


def fake_fetch_all(conn, sql, params=None):
    return conn.rows(sql)


def load(monkeypatch, fits, names):
    monkeypatch.setattr(sets.db, "fetch_all", fake_fetch_all)
    return sets.load(FakeConn(fits, names), fits)


# ------------------------------------------------------------------ sets ---


def gilet_set():
    """black_canvas: a fixed outer, and the top changes under it."""
    gilet = garment(
        "outerwear_06_anko-slate-puffer-vest", "Anko quilted puffer gilet", "outer", 1
    )
    tops = [
        ("fit_bc_charcoal-shirt", "tops_31_zara-charcoal-textured-shirt",
         "Zara Man charcoal textured shirt"),
        ("fit_bc_sage-polo", "tops_05_sage-pique-polo", "Sage green piqué polo"),
    ]
    return [
        fit(fit_id, name, [gilet, garment(item_id, name, "top", 2)] + BASE, i + 1,
            "black_canvas")
        for i, (fit_id, item_id, name) in enumerate(tops)
    ]


def shawl_set():
    """the_shawl: a fixed knit IN THE TOP SLOT, and the tee under it changes."""
    shawl = garment("ben-sherman-aubergine-shawl", "Ben Sherman shawl-collar", "top", 2)
    tees = [
        ("fit_sh_grey-tee", "tees_02_grey-crew", "Grey crew tee"),
        ("fit_sh_black-tee", "tees_03_black-crew", "Black crew tee"),
    ]
    return [
        fit(fit_id, name, [shawl, garment(item_id, name, "base", 3)] + BASE, i + 1,
            "the_shawl")
        for i, (fit_id, item_id, name) in enumerate(tees)
    ]


# beige_brown's own base: a Chelsea boot, which is not suede or nubuck and so
# survives a wet week. Separate from BASE on purpose — sharing the black set's
# nubuck sneaker would make every rain test pass for the wrong reason.
BROWN_BASE = [
    garment("trousers_01_decathlon-beige", "Decathlon chino", "bottom", 4),
    garment("belts_04_distressed-brown-everyday", "Distressed brown everyday belt", "belt", 5),
    garment("shoes_07_oxford-brown-chelsea", "Oxford Chelsea boot", "shoe", 6, cat="Shoes"),
]


def anchorless_set():
    """beige_brown: nothing is fixed above the waist — the top itself varies."""
    tops = [
        ("fit_bb_charcoal-shirt", "tops_31_zara-charcoal-textured-shirt",
         "Zara Man charcoal textured shirt"),
        ("fit_bb_sage-polo", "tops_05_sage-pique-polo", "Sage green piqué polo"),
    ]
    return [
        fit(fit_id, name, [garment(item_id, name, "top", 2)] + BROWN_BASE, i + 1,
            "beige_brown", bands=("cold", "mild", "warm"))
        for i, (fit_id, item_id, name) in enumerate(tops)
    ]


NAMES = [
    {"key": "black_canvas", "name": "Slate blue-grey gilet over black jeans",
     "source": "brief-fit-variant-sets.md", "sort_order": 10},
    {"key": "the_shawl", "name": "Aubergine shawl-collar over black jeans",
     "source": "brief-shawl-set-and-henley.md", "sort_order": 20},
    {"key": "beige_brown", "name": "Beige & brown",
     "source": "brief-beige-brown-set.md", "sort_order": 30},
]


# ----------------------------------------------------------------- base ----


def test_base_is_what_every_member_shares(monkeypatch):
    (built,) = load(monkeypatch, gilet_set(), NAMES)
    assert [p.role for p in built.base] == ["outer", "bottom", "belt", "shoe"]
    # The varying top is not part of the base, however many members carry one.
    assert all(p.role != "top" for p in built.base)


def test_anchor_is_the_fixed_layer_and_may_be_absent(monkeypatch):
    (gilet,) = load(monkeypatch, gilet_set(), NAMES)
    (shawl,) = load(monkeypatch, shawl_set(), NAMES)
    (plain,) = load(monkeypatch, anchorless_set(), NAMES)

    assert gilet.anchor.role == "outer"
    # A knit sitting in the `top` slot is still an anchor when it never changes.
    assert shawl.anchor.role == "top"
    assert plain.anchor is None


# ----------------------------------------------------------------- copy ----


def test_short_names_are_colour_plus_noun(monkeypatch):
    (built,) = load(monkeypatch, gilet_set(), NAMES)
    assert built.base_line() == (
        "the slate blue-grey gilet, black jeans, black belt, ecco nubuck sneaker"
    )


def test_a_shoe_keeps_its_brand(monkeypatch):
    """"black sneaker" loses the only thing worth saying about a shoe."""
    assert (
        sets.short_name(
            {"name": "Ecco nubuck sneaker", "colour": "Black", "role": "shoe"}
        )
        == "Ecco nubuck sneaker"
    )


def test_an_explicit_short_name_wins_over_the_rule(monkeypatch):
    """The rule derives "rustic belt" from this one, which is why it can be set."""
    assert (
        sets.short_name(
            {
                "name": "Distressed brown everyday belt",
                "colour": "Rustic / distressed medium brown",
                "role": "belt",
                "short_name": "brown belt",
            }
        )
        == "brown belt"
    )


def test_vary_line_is_derived_for_each_of_the_three_shapes(monkeypatch):
    (gilet,) = load(monkeypatch, gilet_set(), NAMES)
    (shawl,) = load(monkeypatch, shawl_set(), NAMES)
    (plain,) = load(monkeypatch, anchorless_set(), NAMES)

    assert gilet.vary_line() == (
        "The slate blue-grey gilet stays on; the top under it changes"
    )
    assert shawl.vary_line() == "Only what's under the aubergine shawl-collar changes"
    # The line that a hardcoded "the knit stays on" gets wrong.
    assert plain.vary_line() == "The top changes; trouser, belt and shoes stay put"


def test_sub_line_only_says_under_when_there_is_something_to_be_under(monkeypatch):
    (shawl,) = load(monkeypatch, shawl_set(), NAMES)
    (plain,) = load(monkeypatch, anchorless_set(), NAMES)

    assert shawl.sub_line(shawl.variants[0]).startswith(
        "Grey crew tee under the aubergine shawl-collar · "
    )
    assert "under" not in plain.sub_line(plain.variants[0]).split(" · ")[0]


def test_count_note_counts_the_days_left_open(monkeypatch):
    (built,) = load(monkeypatch, gilet_set(), NAMES)
    assert built.count_note() == "2 variants built, 3 days open"

    built.variants = built.variants * 3        # six variants for five days
    assert built.count_note() == "5 days covered"
    assert "1 more variant ready to swap in mid-week" in built.bench_note()


# ---------------------------------------------------------------- wash -----


def test_wash_line_names_the_trouser_the_anchor_and_what_was_worn(monkeypatch):
    (built,) = load(monkeypatch, shawl_set(), NAMES)
    line = sets.wash_line(built, built.variants)
    assert line == (
        "black jeans, the aubergine shawl-collar, plus Grey crew tee, Black crew tee"
    )
    # Belt and shoes stay out of the basket; the screen says so in its own words.
    assert "belt" not in line and "sneaker" not in line


def test_wash_line_survives_a_week_with_nothing_ticked_yet(monkeypatch):
    (built,) = load(monkeypatch, anchorless_set(), NAMES)
    assert sets.wash_line(built, []).endswith("plus whatever you wear under it")


# ---------------------------------------------------------------- edges ----


def test_a_lone_fit_is_not_a_set(monkeypatch):
    """One tagged fit has no varying garment, so there is nothing to lay out."""
    assert load(monkeypatch, gilet_set()[:1], NAMES) == []


def test_a_set_with_no_name_row_falls_back_to_its_key(monkeypatch):
    (built,) = load(monkeypatch, gilet_set(), [])
    assert built.name == "black canvas"


# -------------------------------------------------------------- weather ---
#
# The three states of the line under a set on the picker, and the one rule
# underneath them: rain outranks temperature, because a wet week has something
# you can do about it and being a degree off does not.


def test_bands_are_the_union_of_the_variants(monkeypatch):
    (built,) = load(monkeypatch, gilet_set(), NAMES)
    assert built.bands() == ["cold", "mild"]


def test_bands_come_back_coldest_first_however_they_were_stored(monkeypatch):
    fits = gilet_set()
    fits[0].temp_bands = ["warm"]
    fits[1].temp_bands = ["mild", "cold"]
    (built,) = load(monkeypatch, fits, NAMES)
    assert built.bands() == ["cold", "mild", "warm"]


def test_a_set_that_suits_the_week_says_what_it_is_built_for(monkeypatch):
    (built,) = load(monkeypatch, gilet_set(), NAMES)
    note = built.weather_note("mild", False, "10–18°C")
    assert note == {
        "text": "Built for cold and mild — right for 10–18°C.",
        "tone": "right",
    }


def test_a_set_for_the_wrong_end_of_the_thermometer_says_so(monkeypatch):
    (built,) = load(monkeypatch, gilet_set(), NAMES)
    note = built.weather_note("warm", False, "24–30°C")
    assert note["tone"] == "wrong-band"
    assert note["text"] == "A cold/mild set on a warm day."


def test_rain_outranks_the_band(monkeypatch):
    """Wet and the wrong band at once: the shoe is the actionable one."""
    (built,) = load(monkeypatch, gilet_set(), NAMES)
    note = built.weather_note("warm", True, "24–30°C")
    assert note["tone"] == "rained-out"
    assert note["text"] == "Wet week — the Ecco nubuck sneaker stays in."


def test_the_material_is_said_once(monkeypatch):
    """"the Ecco nubuck sneaker", never "the Ecco nubuck sneaker (nubuck)"."""
    (built,) = load(monkeypatch, gilet_set(), NAMES)
    assert built.shoe_phrase("nubuck") == "Ecco nubuck sneaker"
    assert built.shoe_phrase("suede") == "Ecco nubuck sneaker (suede)"


def test_a_set_with_a_rainproof_shoe_is_not_rained_out(monkeypatch):
    """beige_brown's Chelsea boot carries no rain flag, so a wet week is fine."""
    (built,) = load(monkeypatch, anchorless_set(), NAMES)
    assert built.rain_word() is None
    assert built.weather_note("mild", True, "10–18°C")["tone"] == "right"


def test_a_set_claiming_no_bands_makes_no_claim(monkeypatch):
    """Silence beats inventing a temperature the fits never said they suit."""
    fits = gilet_set()
    for f in fits:
        f.temp_bands = []
    (built,) = load(monkeypatch, fits, NAMES)
    assert built.weather_note("warm", False, "24–30°C") == {"text": "", "tone": "right"}


def test_and_list_never_says_and_twice():
    assert sets.and_list(["cold"]) == "cold"
    assert sets.and_list(["cold", "mild"]) == "cold and mild"
    assert sets.and_list(["cold", "mild", "warm"]) == "cold, mild and warm"


# --------------------------------------------------------- hero garments ---


def test_hero_leads_with_the_garment_that_makes_the_day(monkeypatch):
    (built,) = load(monkeypatch, gilet_set(), NAMES)
    pieces = built.hero_pieces(built.variants[0])
    assert [p["role"] for p in pieces] == ["top", "layer", "trouser", "belt", "shoe"]
    assert pieces[0]["name"] == "Zara Man charcoal textured shirt"


def test_a_set_that_varies_underneath_labels_it_under(monkeypatch):
    """`varyRole` read out loud: the shawl stays on, the tee under it changes."""
    (built,) = load(monkeypatch, shawl_set(), NAMES)
    pieces = built.hero_pieces(built.variants[0])
    assert pieces[0]["role"] == "under"
    assert pieces[1]["role"] == "layer"


def test_the_varying_piece_is_never_listed_twice(monkeypatch):
    (built,) = load(monkeypatch, shawl_set(), NAMES)
    for variant in built.variants:
        ids = [p["item_id"] for p in built.hero_pieces(variant)]
        assert len(ids) == len(set(ids))


def test_a_day_with_no_variant_still_lists_the_base(monkeypatch):
    (built,) = load(monkeypatch, gilet_set(), NAMES)
    pieces = built.hero_pieces(None)
    assert [p["role"] for p in pieces] == ["layer", "trouser", "belt", "shoe"]

"""The seeded fits and the wear log, re-keyed from display names to item ids.

work-outfits.md and outfit-log.md reference garments by display name, and names
are NOT unique — there are two "Zara Man V-neck" and three "Decathlon chino".
So the mapping is written out by hand here, explicitly, once. The importer
asserts that every id below resolves to exactly one row in items; nothing is
fuzzy-matched. Get this wrong and the picker recommends the wrong garment
forever, silently.

Prose is copied verbatim from work-outfits.md — that prose is the point of the
fits, so it is stored as written.

Fields deliberately left unset here:

  * `style` — Max's own short characterisation. Not invented; the seven fits in
    killer-looks.md carry theirs, and these ten can be filled in when he wants.
  * `score` — Max's 1-10 opinion. Manual by definition; the app never writes it.
  * `killer` — his promotion flag, set once he can see the fits side by side.

Alternates ("or the Ecco sneaker") are kept as is_alternate rows against the
same slot, so a fit whose sneaker is in the wash is rescued rather than skipped.
Where the source text is genuinely ambiguous about which garment it means —
look 6's "black belt", of which Max owns three — no row is created and the
ambiguity stays visible in the commentary rather than being guessed at.
"""

from __future__ import annotations

SOURCE_WORK_OUTFITS = "work-outfits.md 2026-08-24"

# role vocabulary: outer | layer | top | base | bottom | shoe | belt | accessory
FITS = [
    {
        "id": "fit_vest_and_jeans",
        "name": "Vest & jeans",
        "register": "everyday",
        "sort_order": 1,
        "hidden_by_default": False,
        "commentary": (
            "This is close to the literal uniform half the office wears. Grey polo is a "
            "true neutral, indigo denim is honest and current, the vest is completely "
            "normal here. Swap the polo for the Manfinity blue/mustard one for a bit "
            "more colour."
        ),
        "catch": None,
        "source": SOURCE_WORK_OUTFITS,
        "items": [
            ("tops_04_grey-pique-polo", "top", 1, False, None),
            ("tops_08_manfinity-blue-mustard-polo", "top", 1, True, "for a bit more colour"),
            ("trousers_09_celio-indigo-jeans", "bottom", 2, False, None),
            ("shoes_03_ecco-black-nubuck", "shoe", 3, False, None),
            ("outerwear_06_anko-slate-puffer-vest", "outer", 4, False, None),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_mustard_polo_and_sneaker",
        "name": "Mustard polo & sneaker",
        "register": "everyday",
        "sort_order": 2,
        "hidden_by_default": False,
        "commentary": (
            "Best-fitting polo in the cheap-synthetic set, real colour contrast against "
            "the sage/stone chino — reads current without trying."
        ),
        "catch": None,
        "source": SOURCE_WORK_OUTFITS,
        "items": [
            ("tops_08_manfinity-blue-mustard-polo", "top", 1, False, None),
            ("trousers_07_oxford-sage", "bottom", 2, False, None),
            ("trousers_06_stone-gingham", "bottom", 2, True, "light stone gingham chino"),
            ("shoes_09b_nike-airmax-1", "shoe", 3, False, "give it a clean first"),
            ("shoes_03_ecco-black-nubuck", "shoe", 3, True, None),
            ("outerwear_06_anko-slate-puffer-vest", "outer", 4, True, "for the commute if cold"),
        ],
        "preconditions": [
            ("Give the Nike Air Max 1 a clean", "shoes_09b_nike-airmax-1"),
        ],
    },
    {
        "id": "fit_friday_layer",
        "name": "Friday layer",
        "register": "everyday",
        "sort_order": 3,
        "hidden_by_default": False,
        "commentary": (
            "The cardigan is the only open-front layer owned; grounded on dark indigo."
        ),
        "catch": None,
        "source": SOURCE_WORK_OUTFITS,
        "items": [
            ("tops_04_grey-pique-polo", "top", 1, False, None),
            ("hm-black-cardigan", "layer", 2, False, None),
            ("trousers_09_celio-indigo-jeans", "bottom", 3, False, None),
            ("shoes_07_oxford-brown-chelsea", "shoe", 4, False, None),
            ("shoes_03_ecco-black-nubuck", "shoe", 4, True, "for a more casual version"),
            ("belts_04_distressed-brown-everyday", "belt", 5, False, None),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_everyday_burgundy",
        "name": "Everyday burgundy",
        "register": "everyday",
        "sort_order": 4,
        "hidden_by_default": False,
        "commentary": (
            "Dark over pale gives clean contrast; soft smart-casual either way. "
            "Add the Anko vest on top in winter."
        ),
        "catch": None,
        "source": SOURCE_WORK_OUTFITS,
        "items": [
            ("polo-rl-burgundy-cashmere-crew", "top", 1, False, None),
            ("trousers_01_decathlon-beige", "bottom", 2, False, None),
            ("shoes_07_oxford-brown-chelsea", "shoe", 3, False, None),
            ("belts_03_oxford-arlen-tan", "belt", 4, False, None),
            ("outerwear_06_anko-slate-puffer-vest", "outer", 5, True, "on top in winter"),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_navy_and_sage",
        "name": "Navy & sage",
        "register": "everyday",
        "sort_order": 5,
        "hidden_by_default": False,
        "commentary": "Navy over sage-grey is quiet and current.",
        "catch": None,
        "source": SOURCE_WORK_OUTFITS,
        "items": [
            ("topman-navy-crew", "top", 1, False, None),
            ("trousers_07_oxford-sage", "bottom", 2, False, None),
            ("shoes_02_andre-tan-brogue", "shoe", 3, False, None),
            ("shoes_03_ecco-black-nubuck", "shoe", 3, True, "to dress it down"),
            ("belts_03_oxford-arlen-tan", "belt", 4, False, None),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_leather_jacket_dressed_down",
        "name": "Leather jacket, dressed down",
        "register": "everyday",
        "sort_order": 6,
        "hidden_by_default": False,
        "commentary": (
            "Max hasn't worn this jacket in ages — no reason not to at this office. "
            "Gives a bit of edge on a day that wants it, without overdressing. "
            "(The source text also offers 'or black belt'; Max owns three black belts, "
            "so no specific one is pinned here.)"
        ),
        "catch": None,
        "source": SOURCE_WORK_OUTFITS,
        "items": [
            ("tops_04_grey-pique-polo", "top", 1, False, None),
            ("topman-navy-crew", "top", 1, True, None),
            ("outerwear_02_indindustrie-black-waxed-biker", "outer", 2, False,
             "clean the coating first"),
            ("trousers_09_celio-indigo-jeans", "bottom", 3, False, None),
            ("trousers_11_black-coated-jeans", "bottom", 3, True, None),
            ("shoes_03_ecco-black-nubuck", "shoe", 4, False, None),
            ("belts_04_distressed-brown-everyday", "belt", 5, False, None),
        ],
        "preconditions": [
            ("Clean the dusty coating off the IND Industrie biker jacket",
             "outerwear_02_indindustrie-black-waxed-biker"),
        ],
    },
    {
        "id": "fit_blazer_day",
        "name": "Blazer day",
        "register": "sharp",
        "sort_order": 7,
        "hidden_by_default": False,
        "commentary": (
            "This is the jacket Max already reaches for by default — correctly. The "
            "blazer does \"smart\" without reading stiff, especially over jeans instead "
            "of the wool trouser."
        ),
        "catch": None,
        "source": SOURCE_WORK_OUTFITS,
        "items": [
            ("polo-rl-burgundy-cashmere-crew", "top", 1, False, None),
            ("tops_04_grey-pique-polo", "top", 1, True, None),
            ("outerwear_03_grey-unbranded-blazer", "outer", 2, False, None),
            ("trousers_08_tyrwhitt-navy-wool", "bottom", 3, False, None),
            ("trousers_09_celio-indigo-jeans", "bottom", 3, True, None),
            ("shoes_04_churchs-apron-derby", "shoe", 4, False, None),
            ("belts_02_tan-vera-pelle", "belt", 5, False, None),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_smartest_polo",
        "name": "Smartest polo",
        "register": "sharp",
        "sort_order": 8,
        "hidden_by_default": False,
        "commentary": (
            "Best polo + best trouser + best shoe. Layer the grey blazer over it for "
            "even more polish on a client day."
        ),
        "catch": None,
        "source": SOURCE_WORK_OUTFITS,
        "items": [
            ("tops_02_brioni-white-blue-collar-polo", "top", 1, False, None),
            ("trousers_08_tyrwhitt-navy-wool", "bottom", 2, False, None),
            ("shoes_04_churchs-apron-derby", "shoe", 3, False, None),
            ("belts_02_tan-vera-pelle", "belt", 4, False, None),
            ("outerwear_03_grey-unbranded-blazer", "outer", 5, True,
             "for even more polish on a client day"),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_cold_and_client",
        "name": "Cold & client",
        "register": "sharp",
        "sort_order": 9,
        "hidden_by_default": False,
        "commentary": (
            "Not a daily coat — save this for genuinely cold days or when you want to "
            "look deliberately sharp (client meeting, dinner). Max is attached to this "
            "coat and it earns its place here rather than in daily rotation."
        ),
        "catch": "Not a daily coat — it reads overdressed on an ordinary office day.",
        "source": SOURCE_WORK_OUTFITS,
        "items": [
            ("polo-rl-burgundy-cashmere-crew", "top", 1, False, None),
            ("outerwear_04_indaco-brown-wool-overcoat", "outer", 2, False, None),
            ("trousers_04_oxford-stone", "bottom", 3, False, None),
            ("trousers_08_tyrwhitt-navy-wool", "bottom", 3, True, None),
            ("shoes_04_churchs-apron-derby", "shoe", 4, False, None),
            ("belts_02_tan-vera-pelle", "belt", 5, False, None),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_warm_weather_loafer",
        "name": "Warm-weather loafer",
        "register": "sharp",
        "sort_order": 10,
        "hidden_by_default": False,
        "commentary": "Sage + pale stone + brown suede is the easy summer answer.",
        "catch": "No-show socks with the loafers.",
        "source": SOURCE_WORK_OUTFITS,
        "items": [
            ("tops_05_sage-pique-polo", "top", 1, False, None),
            ("trousers_06_stone-gingham", "bottom", 2, False, None),
            ("shoes_08a_suede-penny-loafer", "shoe", 3, False, "no-show socks"),
            ("belts_02_tan-vera-pelle", "belt", 4, False, None),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_the_sharp_one",
        "name": "The sharp one",
        "register": "sharp",
        "sort_order": 11,
        "hidden_by_default": True,  # Max dislikes roll-necks
        "commentary": (
            "Hidden by default — Max dislikes roll-necks. Allow disliked looks in the "
            "picker to see it."
        ),
        "catch": "Roll-neck: worn alone, nothing under the collar.",
        "source": SOURCE_WORK_OUTFITS,
        "items": [
            ("zara-black-rollneck", "top", 1, False, None),
            ("trousers_04_oxford-stone", "bottom", 2, False, None),
            ("shoes_04_churchs-apron-derby", "shoe", 3, False, None),
            ("belts_02_tan-vera-pelle", "belt", 4, False, None),
        ],
        "preconditions": [],
    },
]

# The entire wear history as of 2026-08-25. A second event ("Moto & burgundy",
# 2026-08-26) is named in the fits addendum but its source entry has not been
# supplied, so it is not seeded here — inventing its items would be worse than
# leaving it out.
WEAR_EVENTS = [
    {
        "worn_on": "2026-08-17",
        "fit_id": None,  # "Burgundy & denim" is not one of the seeded fits
        "context": "Work (bank)",
        "temp_c": None,  # logged as "Cold", no number recorded
        "rain": True,  # "Cold + light rain"
        "rating": 8,
        "note": (
            "Works — warm, cohesive burgundy/tan/blue, trim, current, smart-casual-right "
            "for a cold casual work day. Brogues correct with denim; rubber sole good in "
            "the wet."
        ),
        "tweak": (
            "Jeans read mid-blue with some fade (leans weekend); a darker/cleaner indigo "
            "or the black jean lifts it for the office."
        ),
        "items": [
            ("polo-rl-burgundy-cashmere-crew", False),
            ("trousers_09_celio-indigo-jeans", False),
            ("shoes_02_andre-tan-brogue", False),
            ("belts_04_distressed-brown-everyday", False),
        ],
        # Not in the catalogue — no tees have ever been logged.
        "free_text_items": [("plain neutral tee", True)],
    },
]

# Reference text only. NOT implemented as checks in v1 — the 17 seeded fits are
# already hand-checked, and the checker ships with the v2 builder, which is the
# moment it earns its keep. Stored so the app can show the reasoning next to a
# fit, and so the builder has a spec to validate against.
STYLING_RULES = [
    "Belt colour tracks shoe colour. Brown belt with brown shoes, black with black. "
    "Never mixed.",
    "A pale top needs a dark bottom. Pale-on-pale washes out.",
    "V-neck knits cannot be worn alone — they need a tee underneath. No suitable tee "
    "is currently logged, which is why none of the seeded fits uses one of the 9 "
    "V-necks owned.",
    "No navy-on-navy, no blue-on-blue. Too close in tone to read as deliberate.",
    "The André tan brogue does not go with the navy wool trouser — too much brogueing "
    "against formal cloth.",
    "The Ecco sneaker and the André brogue both stay off the navy wool trouser.",
    "Roll-necks are worn alone, nothing under the collar. (Also: Max dislikes them.)",
    "Items with verdict Bin or Replace, or scope out, never appear in a fit.",
]

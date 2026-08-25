"""The 10 vetted looks and the wear log, re-keyed from display names to ids.

work-outfits.md and outfit-log.md reference garments by display name, and names
are NOT unique — there are two "Zara Man V-neck" and three "Decathlon chino".
So the mapping is written out by hand here, explicitly, once. The importer
asserts that every id below resolves to exactly one row in items; nothing is
fuzzy-matched. Get this wrong and the picker recommends the wrong garment
forever.

Rationale text is copied verbatim from work-outfits.md — that prose is the
point of the looks, so it is stored as written.

Alternates ("or the Ecco sneaker") are kept as is_alternate rows against the
same slot. Where the source text is genuinely ambiguous about which garment it
means — look 6's "black belt", of which Max owns three — no row is created and
the ambiguity stays visible in the rationale rather than being guessed at.
"""

from __future__ import annotations

# slot_role vocabulary: top | mid-layer | outer | trouser | shoe | belt
OUTFITS = [
    {
        "slug": "vest-and-jeans",
        "name": "Vest & jeans",
        "register": "everyday",
        "sort_order": 1,
        "hidden_by_default": False,
        "rationale": (
            "This is close to the literal uniform half the office wears. Grey polo is a "
            "true neutral, indigo denim is honest and current, the vest is completely "
            "normal here. Swap the polo for the Manfinity blue/mustard one for a bit "
            "more colour."
        ),
        "items": [
            ("tops_04_grey-pique-polo", "top", 1, False, None),
            ("tops_08_manfinity-blue-mustard-polo", "top", 1, True, "for a bit more colour"),
            ("trousers_09_celio-indigo-jeans", "trouser", 2, False, None),
            ("shoes_03_ecco-black-nubuck", "shoe", 3, False, None),
            ("outerwear_06_anko-slate-puffer-vest", "outer", 4, False, None),
        ],
    },
    {
        "slug": "mustard-polo-and-sneaker",
        "name": "Mustard polo & sneaker",
        "register": "everyday",
        "sort_order": 2,
        "hidden_by_default": False,
        "rationale": (
            "Best-fitting polo in the cheap-synthetic set, real colour contrast against "
            "the sage/stone chino — reads current without trying."
        ),
        "items": [
            ("tops_08_manfinity-blue-mustard-polo", "top", 1, False, None),
            ("trousers_07_oxford-sage", "trouser", 2, False, None),
            ("trousers_06_stone-gingham", "trouser", 2, True, "light stone gingham chino"),
            ("shoes_09b_nike-airmax-1", "shoe", 3, False, "give it a clean first"),
            ("shoes_03_ecco-black-nubuck", "shoe", 3, True, None),
            ("outerwear_06_anko-slate-puffer-vest", "outer", 4, True, "for the commute if cold"),
        ],
    },
    {
        "slug": "friday-layer",
        "name": "Friday layer",
        "register": "everyday",
        "sort_order": 3,
        "hidden_by_default": False,
        "rationale": (
            "The cardigan is the only open-front layer owned; grounded on dark indigo."
        ),
        "items": [
            ("tops_04_grey-pique-polo", "top", 1, False, None),
            ("hm-black-cardigan", "mid-layer", 2, False, None),
            ("trousers_09_celio-indigo-jeans", "trouser", 3, False, None),
            ("shoes_07_oxford-brown-chelsea", "shoe", 4, False, None),
            ("shoes_03_ecco-black-nubuck", "shoe", 4, True, "for a more casual version"),
            ("belts_04_distressed-brown-everyday", "belt", 5, False, None),
        ],
    },
    {
        "slug": "everyday-burgundy",
        "name": "Everyday burgundy",
        "register": "everyday",
        "sort_order": 4,
        "hidden_by_default": False,
        "rationale": (
            "Dark over pale gives clean contrast; soft smart-casual either way. "
            "Add the Anko vest on top in winter."
        ),
        "items": [
            ("polo-rl-burgundy-cashmere-crew", "top", 1, False, None),
            ("trousers_01_decathlon-beige", "trouser", 2, False, None),
            ("shoes_07_oxford-brown-chelsea", "shoe", 3, False, None),
            ("belts_03_oxford-arlen-tan", "belt", 4, False, None),
            ("outerwear_06_anko-slate-puffer-vest", "outer", 5, True, "on top in winter"),
        ],
    },
    {
        "slug": "navy-and-sage",
        "name": "Navy & sage",
        "register": "everyday",
        "sort_order": 5,
        "hidden_by_default": False,
        "rationale": "Navy over sage-grey is quiet and current.",
        "items": [
            ("topman-navy-crew", "top", 1, False, None),
            ("trousers_07_oxford-sage", "trouser", 2, False, None),
            ("shoes_02_andre-tan-brogue", "shoe", 3, False, None),
            ("shoes_03_ecco-black-nubuck", "shoe", 3, True, "to dress it down"),
            ("belts_03_oxford-arlen-tan", "belt", 4, False, None),
        ],
    },
    {
        "slug": "leather-jacket-dressed-down",
        "name": "Leather jacket, dressed down",
        "register": "everyday",
        "sort_order": 6,
        "hidden_by_default": False,
        "rationale": (
            "Max hasn't worn this jacket in ages — no reason not to at this office. "
            "Gives a bit of edge on a day that wants it, without overdressing. "
            "(The source text also offers 'or black belt'; Max owns three black belts, "
            "so no specific one is pinned here.)"
        ),
        "items": [
            ("tops_04_grey-pique-polo", "top", 1, False, None),
            ("topman-navy-crew", "top", 1, True, None),
            ("outerwear_02_indindustrie-black-waxed-biker", "outer", 2, False,
             "clean the coating first"),
            ("trousers_09_celio-indigo-jeans", "trouser", 3, False, None),
            ("trousers_11_black-coated-jeans", "trouser", 3, True, None),
            ("shoes_03_ecco-black-nubuck", "shoe", 4, False, None),
            ("belts_04_distressed-brown-everyday", "belt", 5, False, None),
        ],
    },
    {
        "slug": "blazer-day",
        "name": "Blazer day",
        "register": "sharp",
        "sort_order": 7,
        "hidden_by_default": False,
        "rationale": (
            "This is the jacket Max already reaches for by default — correctly. The "
            "blazer does \"smart\" without reading stiff, especially over jeans instead "
            "of the wool trouser."
        ),
        "items": [
            ("polo-rl-burgundy-cashmere-crew", "top", 1, False, None),
            ("tops_04_grey-pique-polo", "top", 1, True, None),
            ("outerwear_03_grey-unbranded-blazer", "outer", 2, False, None),
            ("trousers_08_tyrwhitt-navy-wool", "trouser", 3, False, None),
            ("trousers_09_celio-indigo-jeans", "trouser", 3, True, None),
            ("shoes_04_churchs-apron-derby", "shoe", 4, False, None),
            ("belts_02_tan-vera-pelle", "belt", 5, False, None),
        ],
    },
    {
        "slug": "smartest-polo",
        "name": "Smartest polo",
        "register": "sharp",
        "sort_order": 8,
        "hidden_by_default": False,
        "rationale": (
            "Best polo + best trouser + best shoe. Layer the grey blazer over it for "
            "even more polish on a client day."
        ),
        "items": [
            ("tops_02_brioni-white-blue-collar-polo", "top", 1, False, None),
            ("trousers_08_tyrwhitt-navy-wool", "trouser", 2, False, None),
            ("shoes_04_churchs-apron-derby", "shoe", 3, False, None),
            ("belts_02_tan-vera-pelle", "belt", 4, False, None),
            ("outerwear_03_grey-unbranded-blazer", "outer", 5, True,
             "for even more polish on a client day"),
        ],
    },
    {
        "slug": "cold-and-client",
        "name": "Cold & client",
        "register": "sharp",
        "sort_order": 9,
        "hidden_by_default": False,
        "rationale": (
            "Not a daily coat — save this for genuinely cold days or when you want to "
            "look deliberately sharp (client meeting, dinner). Max is attached to this "
            "coat and it earns its place here rather than in daily rotation."
        ),
        "items": [
            ("polo-rl-burgundy-cashmere-crew", "top", 1, False, None),
            ("outerwear_04_indaco-brown-wool-overcoat", "outer", 2, False, None),
            ("trousers_04_oxford-stone", "trouser", 3, False, None),
            ("trousers_08_tyrwhitt-navy-wool", "trouser", 3, True, None),
            ("shoes_04_churchs-apron-derby", "shoe", 4, False, None),
            ("belts_02_tan-vera-pelle", "belt", 5, False, None),
        ],
    },
    {
        "slug": "warm-weather-loafer",
        "name": "Warm-weather loafer",
        "register": "sharp",
        "sort_order": 10,
        "hidden_by_default": False,
        "rationale": "Sage + pale stone + brown suede is the easy summer answer.",
        "items": [
            ("tops_05_sage-pique-polo", "top", 1, False, None),
            ("trousers_06_stone-gingham", "trouser", 2, False, None),
            ("shoes_08a_suede-penny-loafer", "shoe", 3, False, "no-show socks"),
            ("belts_02_tan-vera-pelle", "belt", 4, False, None),
        ],
    },
    {
        "slug": "the-sharp-one",
        "name": "The sharp one",
        "register": "sharp",
        "sort_order": 11,
        "hidden_by_default": True,  # Max dislikes roll-necks
        "rationale": (
            "Hidden by default — Max dislikes roll-necks. Allow disliked looks in the "
            "picker to see it."
        ),
        "items": [
            ("zara-black-rollneck", "top", 1, False, None),
            ("trousers_04_oxford-stone", "trouser", 2, False, None),
            ("shoes_04_churchs-apron-derby", "shoe", 3, False, None),
            ("belts_02_tan-vera-pelle", "belt", 4, False, None),
        ],
    },
]

# The entire wear history as of 2026-08-25: one entry. Volume has to come from
# the new app making logging one tap.
WEAR_EVENTS = [
    {
        "worn_on": "2026-08-17",
        "outfit_slug": None,  # "Burgundy & denim" is not one of the vetted looks
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

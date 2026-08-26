"""The seeded fits and the wear log, re-keyed from display names to item ids.

work-outfits.md and outfit-log.md reference garments by display name, and names
are NOT unique — there are two "Zara Man V-neck" and three "Decathlon chino".
So the mapping is written out by hand here, explicitly, once. The importer
asserts that every id below resolves to exactly one row in items; nothing is
fuzzy-matched. Get this wrong and the picker recommends the wrong garment
forever, silently.

Prose is copied verbatim from work-outfits.md — that prose is the point of the
fits, so it is stored as written.

Two sources, imported differently:

  * work-outfits.md (10 fits) references garments by display name, so the
    mapping is hand-written below and every id is asserted to resolve to exactly
    one item. Their weather/occasion metadata is derived from the garments.
  * killer-looks.md (7 fits) references garments by id and authors its own
    bands, rain_safe, formality and good_for/bad_for. Those are imported as
    written, not re-derived.

Fields deliberately left unset here:

  * `score` — Max's 1-10 opinion. Manual by definition; the app never writes it.
  * `killer` — his promotion flag, set once he can see the fits side by side.

`style` is seeded from data/style-drafts.md as a *suggestion*, never as if Max
wrote it. The fit page labels it a draft until he edits it.

Alternates ("or the Ecco sneaker") are kept as is_alternate rows against the
same slot, so a fit whose sneaker is in the wash is rescued rather than skipped.
Where the source text is genuinely ambiguous about which garment it means —
look 6's "black belt", of which Max owns three — no row is created and the
ambiguity stays visible in the commentary rather than being guessed at.
"""

from __future__ import annotations

SOURCE_WORK_OUTFITS = "work-outfits.md 2026-08-24"
SOURCE_KILLER_LOOKS = "killer-looks.md 2026-08-26"

# Draft characterisations from data/style-drafts.md. Imported with
# source='suggested', NOT as if Max wrote them: the fit page shows them as
# drafts, and the moment he edits one it becomes 'manual' and authoritative.
STYLE_DRAFTS = {
    "fit_vest_and_jeans": "office-normal",
    "fit_mustard_polo_and_sneaker": "easy colour",
    "fit_friday_layer": "soft layering",
    "fit_everyday_burgundy": "warm neutral",
    "fit_navy_and_sage": "quiet, current",
    "fit_leather_jacket_dressed_down": "a bit of edge",
    "fit_blazer_day": "effort, not stiff",
    "fit_smartest_polo": "clean and sharp",
    "fit_cold_and_client": "deliberately dressed",
    "fit_warm_weather_loafer": "easy summer",
    "fit_the_sharp_one": "severe, minimal",
    "fit_the_shawl": "dark, textural",
    "fit_oatmeal_and_navy_wool": "quiet luxury",
    "fit_blazer_over_burgundy": "smart on denim",
    "fit_cardigan_and_brioni": "layered detail",
    "fit_navy_knit_and_stone": "effortless",
    "fit_the_vest_done_right": "uniform, upgraded",
    "fit_sage_and_tan": "warm and easy",
}

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
    # ---------------------------------------------------------------------
    # killer-looks.md — 7 fits, referenced BY ITEM ID in the source, so no
    # mapping table is needed here. Their metadata (bands, rain_safe,
    # formality, good_for/bad_for) is authored in that document, so it is
    # imported rather than derived — the importer will not overwrite it.
    # `killer` stays false on all of them: it is Max's flag to set.
    # ---------------------------------------------------------------------
    {
        "id": "fit_the_shawl",
        "name": "The Shawl",
        "register": "everyday",
        "sort_order": 12,
        "hidden_by_default": False,
        "formality_rank": 2,
        "temp_bands": ["cold", "mild"],
        "rain_safe": False,  # nubuck
        "good_for": ["work", "casual", "weekend"],
        "bad_for": ["client", "formal"],
        "commentary": (
            "The shawl-collar is recorded as the trimmest-fitting garment in the whole "
            "audit — best silhouette owned, and currently unworn. An all-black bottom "
            "half lets the proportions do the work. Aubergine is unusual without being "
            "loud."
        ),
        "catch": (
            "The coated jeans are greying at the thigh and seat. Check in daylight; swap "
            "to the Celio indigo if the wear reads."
        ),
        "source": SOURCE_KILLER_LOOKS,
        "items": [
            ("ben-sherman-aubergine-shawl", "top", 1, False, None),
            ("trousers_11_black-coated-jeans", "bottom", 2, False, None),
            ("trousers_09_celio-indigo-jeans", "bottom", 2, True,
             "if the coating wear shows"),
            ("shoes_03_ecco-black-nubuck", "shoe", 3, False, None),
            ("belts_11_black-classic-pin-buckle", "belt", 4, False, None),
            ("outerwear_02_indindustrie-black-waxed-biker", "outer", 5, True, "if cold"),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_oatmeal_and_navy_wool",
        "name": "Oatmeal & Navy Wool",
        "register": "sharp",
        "sort_order": 13,
        "hidden_by_default": False,
        "formality_rank": 4,
        "temp_bands": ["cold", "mild"],
        "rain_safe": True,
        "good_for": ["work", "client", "dinner"],
        "bad_for": ["casual", "weekend", "gym"],
        "commentary": (
            "Best knit, best trouser, best shoe — all three at once, which has never "
            "actually been done. Pale over dark at full strength; the most "
            "expensive-looking outfit in the wardrobe for zero spend. A client day or a "
            "dinner, not a Tuesday."
        ),
        "catch": "No black leather with navy wool — brown only.",
        "source": SOURCE_KILLER_LOOKS,
        "items": [
            ("fedeli-cashmere-crew", "top", 1, False, None),
            ("trousers_08_tyrwhitt-navy-wool", "bottom", 2, False, None),
            ("shoes_04_churchs-apron-derby", "shoe", 3, False, None),
            ("belts_02_tan-vera-pelle", "belt", 4, False, None),
        ],
        "preconditions": [
            ("Repair the Fedeli cuff hole and the neck mark", "fedeli-cashmere-crew"),
        ],
    },
    {
        "id": "fit_blazer_over_burgundy",
        "name": "Blazer Over Burgundy",
        "register": "sharp",
        "sort_order": 14,
        "hidden_by_default": False,
        "formality_rank": 3,
        "temp_bands": ["cold", "mild"],
        "rain_safe": True,
        "good_for": ["work", "client", "dinner"],
        "bad_for": ["gym", "golf"],
        "commentary": (
            "The blazer is already the reflex jacket, but it gets worn over trousers. "
            "Over jeans it reads \"made an effort\" instead of \"bank\". Grey, burgundy, "
            "indigo and chestnut is a complete colour story in four pieces."
        ),
        "catch": (
            "The blazer is full through the body. Wear it open — buttoned is where the "
            "boxiness shows."
        ),
        "source": SOURCE_KILLER_LOOKS,
        "items": [
            ("polo-rl-burgundy-cashmere-crew", "top", 1, False, None),
            ("outerwear_03_grey-unbranded-blazer", "outer", 2, False, None),
            ("trousers_09_celio-indigo-jeans", "bottom", 3, False, None),
            ("trousers_08_tyrwhitt-navy-wool", "bottom", 3, True, "for a smarter read"),
            ("shoes_04_churchs-apron-derby", "shoe", 4, False, None),
            ("belts_02_tan-vera-pelle", "belt", 5, False, None),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_cardigan_and_brioni",
        "name": "Cardigan & Brioni",
        "register": "everyday",
        "sort_order": 15,
        "hidden_by_default": False,
        "formality_rank": 3,
        "temp_bands": ["mild"],
        "rain_safe": False,  # nubuck
        "good_for": ["work", "casual", "dinner"],
        "bad_for": ["gym", "golf"],
        "commentary": (
            "The pale-blue chambray collar sitting out of a black cardigan is the best "
            "small detail in the wardrobe and it's currently buried. Quiet everywhere "
            "except that collar — which is how a good piece should work."
        ),
        "catch": "Cardigan open, never buttoned.",
        "source": SOURCE_KILLER_LOOKS,
        "items": [
            ("tops_02_brioni-white-blue-collar-polo", "top", 1, False, None),
            ("hm-black-cardigan", "layer", 2, False, None),
            ("trousers_09_celio-indigo-jeans", "bottom", 3, False, None),
            ("trousers_11_black-coated-jeans", "bottom", 3, True, None),
            ("shoes_03_ecco-black-nubuck", "shoe", 4, False, None),
            ("belts_11_black-classic-pin-buckle", "belt", 5, False, None),
        ],
        "preconditions": [
            ("Whiten-wash the Brioni — it has gone creamy and the contrast collar "
             "loses its point", "tops_02_brioni-white-blue-collar-polo"),
        ],
    },
    {
        "id": "fit_navy_knit_and_stone",
        "name": "Navy Knit & Stone",
        "register": "everyday",
        "sort_order": 16,
        "hidden_by_default": False,
        "formality_rank": 3,
        "temp_bands": ["mild", "warm"],
        "rain_safe": True,
        "good_for": ["work", "casual", "client"],
        "bad_for": ["gym"],
        "commentary": (
            "The only dark polo owned, and knitted rather than piqué, so it reads a full "
            "step smarter than the cheap ones without trying. Dark over pale, chestnut "
            "on the feet. Lowest-effort good outfit on the list; likely the spring "
            "default."
        ),
        "catch": (
            "Never over navy bottoms — navy-on-navy is too close. The polo is a size S, "
            "so check it isn't pulling across the chest."
        ),
        "source": SOURCE_KILLER_LOOKS,
        "items": [
            ("tops_10_navy-knit-polo", "top", 1, False, None),
            ("trousers_04_oxford-stone", "bottom", 2, False, None),
            ("shoes_04_churchs-apron-derby", "shoe", 3, False, None),
            ("shoes_07_oxford-brown-chelsea", "shoe", 3, True, None),
            ("belts_02_tan-vera-pelle", "belt", 4, False, None),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_the_vest_done_right",
        "name": "The Vest, Done Right",
        "register": "everyday",
        "sort_order": 17,
        "hidden_by_default": False,
        "formality_rank": 2,
        "temp_bands": ["cold"],
        "rain_safe": True,
        "good_for": ["work", "casual", "weekend"],
        "bad_for": ["client", "formal", "dinner"],
        "commentary": (
            "The highest-leverage change available, because the vest goes on every "
            "winter day anyway. Cashmere under it instead of a polo; a leather boot "
            "instead of a sneaker. Slate against burgundy is a good pairing neither "
            "piece gets credit for."
        ),
        "catch": (
            "The boot is what stops this reading dad-at-the-hardware-store. With a "
            "sneaker it flattens straight back out."
        ),
        "source": SOURCE_KILLER_LOOKS,
        "items": [
            ("polo-rl-burgundy-cashmere-crew", "top", 1, False, None),
            ("outerwear_06_anko-slate-puffer-vest", "outer", 2, False, None),
            ("trousers_09_celio-indigo-jeans", "bottom", 3, False, None),
            ("shoes_07_oxford-brown-chelsea", "shoe", 4, False, None),
            ("belts_04_distressed-brown-everyday", "belt", 5, False, None),
        ],
        "preconditions": [],
    },
    {
        "id": "fit_sage_and_tan",
        "name": "Sage & Tan",
        "register": "everyday",
        "sort_order": 18,
        "hidden_by_default": False,
        "formality_rank": 2,
        "temp_bands": ["mild", "warm"],
        "rain_safe": True,
        "good_for": ["work", "casual", "weekend"],
        "bad_for": ["client", "formal"],
        "commentary": (
            "Sage is the most flattering colour in the polo set and the fit benchmark of "
            "the synthetic ones. The brogue's blue sole caps the formality so it doesn't "
            "tip country-English."
        ),
        "catch": (
            "Nothing olive anywhere near this — sage and olive go muddy together. "
            "No-show socks."
        ),
        "source": SOURCE_KILLER_LOOKS,
        "items": [
            ("tops_05_sage-pique-polo", "top", 1, False, None),
            ("trousers_09_celio-indigo-jeans", "bottom", 2, False, None),
            ("trousers_06_stone-gingham", "bottom", 2, True, None),
            ("shoes_02_andre-tan-brogue", "shoe", 3, False, None),
            ("belts_03_oxford-arlen-tan", "belt", 4, False, None),
        ],
        "preconditions": [],
    },
]

# The complete wear history: two events, both from data/outfit-log.md, both
# referencing garments by id. Neither corresponds to one of the 18 seeded fits —
# they were ad-hoc combinations — so fit_id is None on both.
WEAR_EVENTS = [
    {
        "worn_on": "2026-08-26",
        "fit_id": None,  # "Moto & burgundy" is not one of the seeded fits
        "context": "Work (bank)",
        "temp_c": None,  # not recorded
        "rain": None,
        "rating": 7,
        "note": (
            "Works. Burgundy against black does what it should; the jacket sits "
            "correctly at the hip with clean shoulders; the Ecco disappears into the "
            "hem, which is correct behaviour for an all-black shoe. Reads current, not "
            "dated. Marked down for the jeans: too faded to sit under all that black, so "
            "the eye lands on the weakest garment, and the hem breaks and pools over the "
            "shoe."
        ),
        "tweak": None,
        "items": [
            ("outerwear_02_indindustrie-black-waxed-biker", False),
            ("polo-rl-burgundy-cashmere-crew", False),
            ("trousers_09_celio-indigo-jeans", False),
            ("shoes_03_ecco-black-nubuck", False),
            ("belts_11_black-classic-pin-buckle", False),
        ],
        # The second event in a row to include a garment that has never been
        # catalogued. This is why wear_event_items.item_id is nullable.
        "free_text_items": [("plain tee", True)],
        "photo_slug": "fit_moto_and_burgundy",
    },
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
        # The two photos are still embedded in the legacy Wardrobe_Manager.html
        # artifact and have not been extracted as files.
        "photo_slug": None,
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

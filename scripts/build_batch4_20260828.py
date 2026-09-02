"""Batch 4, 2026-08-28: the Hugo Boss three-piece wedding suit.

Jacket, waistcoat and trousers from the suit Max was married in, 2008. BOSS
"The Jam/Sharp", Super 120s wool, size 38R / EU 48 - a size below his other
Hugo Boss suit and still fitting.

The waistcoat goes into Tops (Max's decision 2026-08-28): it is a torso garment
worn over a shirt, same slot logic as a polo or knit. No new category.

Reads the batch-3 import file read-only and writes a NEW file.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\maxim\PycharmProjects\wardrobe-manager")
SRC = REPO / "data" / "wardrobe_2026-08-28_batch3.json"
DST = REPO / "data" / "wardrobe_2026-08-28_batch4.json"

SUIT = ("Part of the Hugo Boss three-piece Max was married in, 2008. BOSS 'The Jam/Sharp', "
        "Super 120s wool, DE/FR/UK/IT 48, US 38R - one size below his other Hugo Boss suit "
        "(trousers_12 / outerwear_11) and, eighteen years on, still fitting. Pieces: "
        "outerwear_13 jacket, tops_49 waistcoat, trousers_14 trouser.")

NEW = [
    {
        "id": "outerwear_13_hugo-boss-navy-wedding-suit-jacket",
        "slug": "outerwear_13_hugo-boss-navy-wedding-suit-jacket",
        "cat": "Outerwear",
        "name": "Hugo Boss navy wedding suit jacket",
        "colour": "Dark navy with a fine tonal stripe",
        "hex": "#202634",
        "role": "Anchor dark",
        "cut": "Two-button notch-lapel suit jacket, flap pockets, half-lined with contrast "
               "cream piping on the interior seams",
        "material": "Super 120s wool",
        "weight": "Mid",
        "formality": "Formal",
        "fit": "The best-fitting jacket in the wardrobe. Shoulders sit exactly right, real "
               "waist shape, clean line from shoulder to hem in the side view with no "
               "collapse. Length ends at mid-seat. Sleeves right",
        "condition": "Very good for its age",
        "verdict": "Keep",
        "verdictNote": "Eighteen years old and the sharpest tailored thing Max owns - what a "
                       "good cloth in the correct size does",
        "scope": "occasional",
        "worksAlone": True,
        "warmth": 2,
        "weatherproof": {"rain": False, "wind": False},
        "pairs": "trousers_14_hugo-boss-navy-wedding-suit-trouser and "
                 "tops_49_hugo-boss-navy-wedding-suit-waistcoat",
        "layer": "Outer layer. Over the waistcoat for the full three-piece, or without it for "
                 "the two-piece - the two-piece is the version with real-world use",
        "avoid": "Breaking it up as an odd jacket - the tonal stripe ties it to its trousers",
        "notes": SUIT + " Super 120s is a genuine step above the cloth in either of the other "
                 "two Hugo Boss suits, and the half-lining with cream piping is finishing you "
                 "do not get at the cheaper tiers. Notch lapels are slightly wide with a low "
                 "gorge - 2008 is visible if you look - but far closer to current than "
                 "outerwear_11, and nothing about it reads costume. Compared 2026-08-28: this "
                 "is a better navy suit than the glen check one. Render came out charcoal; "
                 "cloth is dark navy in every real frame - hex sampled from the photographs",
        "noPhoto": False,
        "photoRef": "Outerwear/outerwear_13_hugo-boss-navy-wedding-suit-jacket_* "
                    "(7 frames: 2 label, 3 worn-front, 2 worn-side)",
        "photoPrefix": "outerwear_13_hugo-boss-navy-wedding-suit-jacket",
        "retailPrefix": "outerwear_13_hugo-boss-navy-wedding-suit-jacket",
    },
    {
        "id": "tops_49_hugo-boss-navy-wedding-suit-waistcoat",
        "slug": "tops_49_hugo-boss-navy-wedding-suit-waistcoat",
        "cat": "Tops",
        "name": "Hugo Boss navy wedding suit waistcoat",
        "colour": "Dark navy with a fine tonal stripe",
        "hex": "#202634",
        "role": "Anchor dark",
        "cut": "Five-button suit waistcoat, welted pockets, satin back with rear adjuster. "
               "High neckline, narrow opening",
        "material": "Super 120s wool front, satin back",
        "weight": "Light to mid",
        "formality": "Formal",
        "fit": "Still fits. Closes cleanly with no strain across the buttons and keeps shape "
               "through the waist rather than going flat-fronted the way a tight one does",
        "condition": "Very good for its age",
        "verdict": "Keep",
        "verdictNote": "Third piece of the wedding suit, and it still does up - which is the "
                       "headline",
        "scope": "occasional",
        "worksAlone": False,
        "pairs": "outerwear_13_hugo-boss-navy-wedding-suit-jacket and "
                 "trousers_14_hugo-boss-navy-wedding-suit-trouser",
        "layer": "Over a dress shirt, under the suit jacket",
        "avoid": "Wearing it open-collared without the jacket - the high neckline and narrow "
                 "opening leave an awkward gap at the throat. It needs a tie, or the jacket on",
        "notes": SUIT + " Filed under Tops rather than Outerwear or a new Waistcoats category "
                 "(Max's call 2026-08-28): it is a torso garment worn over a shirt, so it "
                 "shares slot logic with a polo or a knit, and in a three-piece it is never "
                 "the outer layer. The high neckline and narrow opening are the 2008 detail - "
                 "modern waistcoats drop lower and open wider - and are why it reads slightly "
                 "formal-hire worn without the jacket",
        "noPhoto": False,
        "photoRef": "Shirts/tops_49_hugo-boss-navy-wedding-suit-waistcoat_* "
                    "(4 frames: 2 flat, 2 worn-front)",
        "photoPrefix": "tops_49_hugo-boss-navy-wedding-suit-waistcoat",
        "retailPrefix": "tops_49_hugo-boss-navy-wedding-suit-waistcoat",
    },
    {
        "id": "trousers_14_hugo-boss-navy-wedding-suit-trouser",
        "slug": "trousers_14_hugo-boss-navy-wedding-suit-trouser",
        "cat": "Trousers",
        "name": "Hugo Boss navy wedding suit trouser",
        "colour": "Dark navy with a fine tonal stripe",
        "hex": "#202634",
        "role": "Anchor dark",
        "cut": "Flat-front suit trouser, belt loops, moderately straight leg",
        "material": "Super 120s wool",
        "weight": "Mid",
        "formality": "Formal",
        "fit": "Still fits, and better cut than the 40R - narrower leg, better length, only a "
               "slight break. Snug through the seat and thigh: visible tension in the close "
               "frame, not straining but with no ease either",
        "condition": "Good - a few small marks on the leg",
        "verdict": "Keep",
        "verdictNote": "Better-cut of the two Hugo Boss suit trousers, and still wearable "
                       "eighteen years on",
        "scope": "occasional",
        "worksAlone": True,
        "pairs": "outerwear_13_hugo-boss-navy-wedding-suit-jacket and "
                 "tops_49_hugo-boss-navy-wedding-suit-waistcoat",
        "avoid": "Pairing with another jacket - the tonal stripe ties it to outerwear_13",
        "notes": SUIT + " Snug through the seat and thigh - worth knowing before committing to "
                 "wearing it all day at an event. Narrower leg, better length and no dated "
                 "glen check compared with trousers_12, so of the two Hugo Boss suits this is "
                 "the one closer to a navy suit that reads current. Render came out charcoal "
                 "with a fine vertical stripe; the cloth is dark navy with a tonal rib - hex "
                 "sampled from the photographs",
        "noPhoto": False,
        "photoRef": "Trousers/trousers_14_hugo-boss-navy-wedding-suit-trouser_* "
                    "(7 frames: label, detail, 5 worn-front)",
        "photoPrefix": "trousers_14_hugo-boss-navy-wedding-suit-trouser",
        "retailPrefix": "trousers_14_hugo-boss-navy-wedding-suit-trouser",
    },
]

payload = json.loads(SRC.read_text(encoding="utf-8"))
existing = {i["id"] for i in payload["items"]}

clashes = [i["id"] for i in NEW if i["id"] in existing]
if clashes:
    sys.exit(f"ABORT - these ids already exist: {clashes}")

payload["items"].extend(NEW)
payload["generated"] = "2026-08-28"

DST.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"source items : {len(existing)}")
for i in NEW:
    print(f"   + {i['id']}  ({i['verdict']})")
print(f"written      : {len(payload['items'])} -> {DST.name}")

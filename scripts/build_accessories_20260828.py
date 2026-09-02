"""Append the three 2026-08-28 scarves to a copy of the catalogue JSON.

Reads data/wardrobe.json read-only and writes a NEW file. The original is never
touched. The 113 existing items are carried through unchanged so the importer's
upsert is a no-op on them and only the three new ids are inserted.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\maxim\PycharmProjects\wardrobe-manager")
SRC = REPO / "data" / "wardrobe.json"
DST = REPO / "data" / "wardrobe_2026-08-28_accessories.json"

NEW = [
    {
        "id": "accessories_00_leopard-wool-silk-scarf",
        "slug": "accessories_00_leopard-wool-silk-scarf",
        "cat": "Accessories",
        "name": "Leopard-print wool-silk scarf",
        "colour": "Pale greige ground with muted plum-mauve leopard rosettes",
        "hex": "#C5B0AB",
        "role": "Pale neutral - the only patterned piece that sits at the face",
        "cut": "Long rectangle, approx 180-190cm, fine gauze with self-fringed ends. "
               "Long enough to double into a loop knot with tails to mid-torso",
        "material": "95% wool / 5% silk",
        "weight": "Fine",
        "formality": "Smart-casual",
        "fit": "Drapes softly; doubles into a loop knot without bulk at the throat",
        "condition": "Good - no pilling, holes or staining visible; self-fringe intact",
        "verdict": "Keep",
        "verdictNote": "The only patterned thing that sits near the face. Breaks up plain "
                       "knitwear and reads Parisian rather than banker",
        "scope": "occasional",
        "worksAlone": False,
        "pairs": "Burgundy RL cashmere crew (photographed together 2026-08-28, works - the "
                 "mauve is a desaturated relative of the burgundy and the greige ground picks "
                 "up the stone chino, so it bridges the outfit rather than sitting on top of "
                 "it). Also black, charcoal, navy and dark knits",
        "layer": "Over knitwear or a jacket, at the neck. Not tucked under a collar",
        "avoid": "Warm colours - camel, rust, olive, tan. The mauve is cool-toned and fights "
                 "them. Never over a patterned shirt",
        "notes": "Reads as a soft textured neutral at conversational distance; the leopard "
                 "rosettes only resolve close up. That scale and low saturation is what keeps "
                 "it wearable in the office. Wool, so despite the fine gauze it is a "
                 "three-season scarf, not a hot-weather one. Brand tag present but the script "
                 "lettering is not legible in either label frame - brand unknown. Hex sampled "
                 "from the macro frame, NOT from the render, which drifted pink",
        "careNote": "Dry clean only. Made in India",
        "noPhoto": False,
        "photoRef": "Accessories/accessories_00_leopard-wool-silk-scarf_* (5 frames: 2 label, "
                    "1 detail, 2 worn-front)",
        "photoPrefix": "accessories_00_leopard-wool-silk-scarf",
        "retailPrefix": "accessories_00_leopard-wool-silk-scarf",
    },
    {
        "id": "accessories_01_sage-print-gauze-scarf",
        "slug": "accessories_01_sage-print-gauze-scarf",
        "cat": "Accessories",
        "name": "Sage printed gauze scarf",
        "colour": "Pale sage-grey ground with washed-out charcoal print",
        "hex": "#BEC0B2",
        "role": "Pale neutral - too close in value to Max's hair to frame the face",
        "cut": "Large rectangle approx 220cm and wide enough to work as a light wrap. "
               "Crinkle finish, short self-fringe, semi-sheer",
        "material": None,
        "weight": "Fine",
        "formality": "Casual",
        "fit": "Very light and fluid; needs volume in the knot or it collapses",
        "condition": "Good - the mottling is the print, not soiling",
        "verdict": "Keep",
        "verdictNote": "Weakest of the three. Sits too close to Max's hair value, so it washes "
                       "the face out rather than framing it. Earns its place for warm-weather "
                       "and weekend wear only",
        "scope": "occasional",
        "worksAlone": False,
        "pairs": "Navy, charcoal, white linen, mid-blue denim",
        "avoid": "Burgundy and warm browns - the green fights them. Assessed over the burgundy "
                 "crew 2026-08-28 and it was the wrong pairing",
        "notes": "Abstract washed print, somewhere between a faded toile and a weathered map. "
                 "Large scale but so low in contrast it reads as mottling. IMPORTANT: hex is "
                 "sampled from the real frames, not the render - the render lost the green cast "
                 "entirely and came out warm oatmeal, which would invert the styling advice",
        "noPhoto": False,
        "unconfirmed": True,
        "photoRef": "Accessories/accessories_01_sage-print-gauze-scarf_* (3 frames: hanger, "
                    "detail, worn-front). No label frame - material unverified",
        "photoPrefix": "accessories_01_sage-print-gauze-scarf",
        "retailPrefix": "accessories_01_sage-print-gauze-scarf",
    },
    {
        "id": "accessories_02_charcoal-check-crinkle-scarf",
        "slug": "accessories_02_charcoal-check-crinkle-scarf",
        "cat": "Accessories",
        "name": "Charcoal check crinkle scarf",
        "colour": "Slate blue-grey with a tonal windowpane check",
        "hex": "#575D64",
        "role": "Anchor dark - the only scarf dark enough to frame the face",
        "cut": "Rectangle approx 200cm, crinkle-pleated gauze with a cut fringe",
        "material": None,
        "weight": "Light",
        "formality": "Smart-casual",
        "fit": "Holds a knot well; the pleating gives it body without bulk",
        "condition": "Good - fringe slightly tangled at one end",
        "verdict": "Keep",
        "verdictNote": "Most useful of the three and the least interesting. Dark enough to "
                       "create a real break at the collar, and the only one safe over a "
                       "patterned shirt",
        "scope": "occasional",
        "worksAlone": False,
        "pairs": "Burgundy, navy, black, charcoal, stone chino, denim. Widest range of the three",
        "layer": "Over knitwear. Undercuts a blazer - the crinkle texture is too casual for "
                 "tailoring",
        "avoid": "Anything sharp or formal",
        "notes": "The check is so close in value to the ground that at any distance it reads as "
                 "texture, not pattern - which is why this is the one that works over a "
                 "patterned shirt. The crinkle-pleat finish is the most dated thing in this "
                 "batch; that texture had its moment around 2008-2014 and carries a whiff of "
                 "it. Not enough to bin, but it is why this is a workhorse rather than a good "
                 "piece. IMPORTANT: the render blew the check out to high-contrast black bars "
                 "and gave it twisted tassels - the real garment has a subtle tonal check and a "
                 "cut fringe. Do not judge pattern intensity from the render",
        "noPhoto": False,
        "unconfirmed": True,
        "photoRef": "Accessories/accessories_02_charcoal-check-crinkle-scarf_* (4 frames: "
                    "hanger, detail, 2 worn-front). No label frame - material unverified",
        "photoPrefix": "accessories_02_charcoal-check-crinkle-scarf",
        "retailPrefix": "accessories_02_charcoal-check-crinkle-scarf",
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
print(f"new items    : {len(NEW)}")
print(f"written      : {len(payload['items'])} -> {DST.name}")
print(f"original data/wardrobe.json untouched: {SRC.stat().st_size} bytes")

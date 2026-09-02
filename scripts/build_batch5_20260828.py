"""Batch 5, 2026-08-28: the last three.

Paul Smith navy wool trouser (Keep, dry clean - surface mould bloom), and the
Christian Dior black suit, both pieces Bin.

The Dior is catalogued rather than simply discarded so there is a record of what
left and why - the same treatment the other 16 disposed garments get.
gone_at is app-owned state and cannot be set by the importer, so Max marks both
pieces gone in the app afterwards, exactly as he did for the previous twelve.

Reads the batch-4 import file read-only and writes a NEW file.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\maxim\PycharmProjects\wardrobe-manager")
SRC = REPO / "data" / "wardrobe_2026-08-28_batch4.json"
DST = REPO / "data" / "wardrobe_2026-08-28_batch5.json"

DIOR = ("Half of the Christian Dior black suit assessed and binned 2026-08-28. Christian Dior "
        "in this era was heavily licensed - the name is doing more work than the make. "
        "Catalogued rather than simply discarded so there is a record of what left and why.")

NEW = [
    {
        "id": "trousers_15_paul-smith-navy-wool-trouser",
        "slug": "trousers_15_paul-smith-navy-wool-trouser",
        "cat": "Trousers",
        "name": "Paul Smith navy wool trouser",
        "colour": "Very dark navy",
        "hex": "#1B1F2B",
        "role": "Anchor dark",
        "cut": "Flat-front tailored trouser, belt loops, straight leg",
        "material": "Wool suiting",
        "weight": "Mid",
        "formality": "Formal",
        "fit": "Decent - straight leg, slight break, waist fine. A touch loose through the "
               "thigh but nothing like the Hugo Boss 40R",
        "condition": "Surface mould bloom across the leg - white-pale specks sitting on the "
                     "weave, scattered rather than clustered, with no grey-brown halo and no "
                     "discolouration in the cloth beneath. Assessed 2026-08-28 as surface "
                     "mildew that has not fed into the fibre",
        "verdict": "Keep",
        "verdictNote": "Good tailoring tier, recoverable damage - the bloom should dry-clean "
                       "out completely",
        "scope": "occasional",
        "worksAlone": True,
        "pairs": "Dark knitwear, white or pale blue shirts",
        "avoid": "Storing in a plastic garment bag - see notes",
        "notes": "Paul Smith London, so a proper tailoring tier. MOULD: surface bloom, not "
                 "embedded. The embedded kind shows grey-brown staining with a tidemark edge "
                 "and cloth that goes thin and tears at stress points - none of that is "
                 "present. NOT YET CONFIRMED PHYSICALLY: the definitive test is to brush a "
                 "patch outdoors with a soft brush and check the bloom lifts cleanly leaving "
                 "unmarked cloth, and to check inside the waistband and pocket bags where it "
                 "goes deepest. If staining shows underneath, this verdict changes. LIKELY "
                 "CAUSE: the trousers were photographed inside a plastic dry-cleaning bag, "
                 "visible in the macro and label frames. Plastic bags trap moisture against "
                 "cloth and are one of the commonest causes of mould on stored tailoring - "
                 "which would mean the wardrobe itself is fine and the bag is the whole story. "
                 "Worth checking anything else stored in plastic. Render invented a pleated "
                 "front and a birdseye texture; the real trousers are flat-front and plain - "
                 "hex and cut are from the photographs",
        "actionRequired": "DRY CLEAN",
        "actionStatus": "pending",
        "actionNote": "Dry clean to remove surface mould bloom. Brush a test patch outdoors "
                      "first and check the cloth beneath is unmarked. Do not re-store in the "
                      "plastic bag. Flagged 2026-08-28",
        "noPhoto": False,
        "photoRef": "Trousers/trousers_15_paul-smith-navy-wool-trouser_* "
                    "(6 frames: 2 label, 1 damage-mould-bloom, 3 worn-front)",
        "photoPrefix": "trousers_15_paul-smith-navy-wool-trouser",
        "retailPrefix": "trousers_15_paul-smith-navy-wool-trouser",
    },
    {
        "id": "outerwear_14_christian-dior-black-three-button-suit-jacket",
        "slug": "outerwear_14_christian-dior-black-three-button-suit-jacket",
        "cat": "Outerwear",
        "name": "Christian Dior black three-button suit jacket",
        "colour": "Black",
        "hex": "#121212",
        "role": "Anchor dark",
        "cut": "Three-button single-breasted with a high stance, flap pockets, long body",
        "material": "Wool suiting",
        "weight": "Mid",
        "formality": "Formal",
        "fit": "Too large and the wrong decade. Shoulders overhang clearly past the natural "
               "shoulder with a visible drop below the seam. Boxy through the body with no "
               "waist suppression - it hangs straight. Long, covering the seat and running "
               "toward mid-thigh. Sleeves long",
        "condition": "Sound but dusty - black shows everything",
        "verdict": "Bin",
        "verdictNote": "Three-button high stance plus overhanging shoulders and a long boxy "
                       "body - dated and oversized at once, with no route back",
        "scope": "out",
        "worksAlone": True,
        "warmth": 2,
        "weatherproof": {"rain": False, "wind": False},
        "pairs": "trousers_16_christian-dior-black-pleated-suit-trouser - its matching half",
        "avoid": "Everything",
        "notes": DIOR + " Three-button single-breasted with a high stance is a hard marker for "
                 "roughly 1996-2005, and worn with the pleated trousers the suit reads its "
                 "decade from across a room. THE ONE GARMENT ASSESSED 2026-08-28 WITH NO ROUTE "
                 "BACK: every other problem piece had a fix (hem and taper the Hugo Boss 40R, "
                 "waist and sleeves on the Burberry). This would need new shoulders, a "
                 "shortened body, a re-cut lapel and stance, and a rebuilt trouser front to "
                 "lose the pleats - a new suit's worth of work. No gap to fill either: "
                 "outerwear_13, the wedding Hugo Boss, is better cloth, correct size, better "
                 "cut, and fits now. Binned by Max 2026-08-28",
        "noPhoto": False,
        "photoRef": "Outerwear/outerwear_14_christian-dior-black-three-button-suit-jacket_* "
                    "(9 frames: 2 label, hanger, 4 worn-front, worn-side, detail)",
        "photoPrefix": "outerwear_14_christian-dior-black-three-button-suit-jacket",
        "retailPrefix": "outerwear_14_christian-dior-black-three-button-suit-jacket",
    },
    {
        "id": "trousers_16_christian-dior-black-pleated-suit-trouser",
        "slug": "trousers_16_christian-dior-black-pleated-suit-trouser",
        "cat": "Trousers",
        "name": "Christian Dior black pleated suit trouser",
        "colour": "Black",
        "hex": "#121212",
        "role": "Anchor dark",
        "cut": "Double forward-pleated front, belt loops, wide straight leg, high rise",
        "material": "Wool suiting",
        "weight": "Mid",
        "formality": "Formal",
        "fit": "Baggy throughout. Very full through seat and thigh with no shape at all in the "
               "back view. High rise sitting well above the natural waist. Long, pooling at "
               "the ankle. Loose in the waist so they hang off rather than sit",
        "condition": "Sound",
        "verdict": "Bin",
        "verdictNote": "Pleated, full and high-rise - the pleats cannot be tailored out, which "
                       "is what puts this beyond rescue",
        "scope": "out",
        "worksAlone": True,
        "pairs": "outerwear_14_christian-dior-black-three-button-suit-jacket - its matching half",
        "avoid": "Everything",
        "notes": DIOR + " Double forward pleats are the single most dating detail in menswear "
                 "and, unlike length or leg width, CANNOT be tailored out - removing them means "
                 "rebuilding the entire front rise, which costs more than the trousers are "
                 "worth. Compare trousers_13, the Varce: same colour, same job, entirely "
                 "different decade. Binned by Max 2026-08-28",
        "noPhoto": False,
        "photoRef": "Trousers/trousers_16_christian-dior-black-pleated-suit-trouser_* "
                    "(5 frames: flat, 2 worn-front, worn-back, worn-side)",
        "photoPrefix": "trousers_16_christian-dior-black-pleated-suit-trouser",
        "retailPrefix": "trousers_16_christian-dior-black-pleated-suit-trouser",
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

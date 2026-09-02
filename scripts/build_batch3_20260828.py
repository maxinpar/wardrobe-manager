"""Batch 3, 2026-08-28: formalwear.

Six items — two suits (Hugo Boss navy check, Varce black tie), the orphaned
Burberry dinner jacket, and the bow tie.

Reads the batch-2 import file read-only and writes a NEW file. Nothing edited in
place. Only the six new ids should show as changes.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\maxim\PycharmProjects\wardrobe-manager")
SRC = REPO / "data" / "wardrobe_2026-08-28_batch2.json"
DST = REPO / "data" / "wardrobe_2026-08-28_batch3.json"

NEW = [
    {
        "id": "outerwear_10_burberry-prorsum-navy-dinner-jacket",
        "slug": "outerwear_10_burberry-prorsum-navy-dinner-jacket",
        "cat": "Outerwear",
        "name": "Burberry Prorsum navy dinner jacket",
        "colour": "Midnight navy with black satin facings",
        "hex": "#232838",
        "role": "Anchor dark",
        "cut": "Single-button dinner jacket. Satin-faced peak lapels, satin-jetted pockets, "
               "satin-covered cuff buttons, chain hanger loop",
        "material": "Wool suiting with satin lapel and pocket facings",
        "weight": "Mid",
        "formality": "Formal (black tie)",
        "fit": "Too large. Shoulders sit at or just past the natural shoulder point - "
               "borderline but acceptable, and the one thing a tailor cannot fix. Waist "
               "clearly loose, hangs straight with no shape through the middle. Sleeves run "
               "long, covering to the base of the thumb",
        "condition": "Excellent - no wear visible on any panel",
        "verdict": "Tailor",
        "verdictNote": "Best-quality garment in the wardrobe by a distance, in the wrong size "
                       "and with no matching trousers",
        "scope": "occasional",
        "worksAlone": True,
        "warmth": 2,
        "weatherproof": {"rain": False, "wind": False},
        "pairs": "Nothing that matches. See notes - this jacket is orphaned",
        "layer": "Outer layer",
        "avoid": "Daylight and smart-casual. NOT a blazer substitute - the satin facings read "
                 "as evening wear and give it away instantly. Photographed 2026-08-28 over the "
                 "burgundy crew with chinos and sneakers and it did not work",
        "notes": "Burberry Prorsum, made in Italy, size 52 (approx 42in chest; Max wears M). "
                 "Prorsum was Burberry's runway line, discontinued around 2016 - construction "
                 "confirms it (chain hanger loop, clean lapel roll, satin-covered buttons). "
                 "ORPHANED: no matching trousers. Max confirmed 2026-08-28 that none exist. "
                 "It can be worn over trousers_13_varce-black-slim-formal-trouser, but that is "
                 "a poly blend and the quality mismatch shows under evening light. "
                 "SUPERSEDED: the Varce dinner suit (outerwear_12 + trousers_13) is complete, "
                 "correctly fitted, and shawl-collared, which is more correct for black tie "
                 "than peak. So this jacket fills no gap. Before paying for alterations, "
                 "decide whether it is being kept to wear or kept because it is beautiful - "
                 "both are legitimate, but Prorsum holds resale value and this is superseded",
        "actionRequired": "TAILOR",
        "actionStatus": "pending",
        "actionNote": "Take in through the waist, shorten sleeves approx 1.5cm. Leave the "
                      "shoulders alone. Flagged 2026-08-28. HOLD - see notes; the Varce dinner "
                      "suit supersedes this and the alteration may not be worth doing",
        "noPhoto": False,
        "photoRef": "Outerwear/outerwear_10_burberry-prorsum-navy-dinner-jacket_* "
                    "(7 frames: 2 label, hanger, 4 worn-front)",
        "photoPrefix": "outerwear_10_burberry-prorsum-navy-dinner-jacket",
        "retailPrefix": "outerwear_10_burberry-prorsum-navy-dinner-jacket",
    },
    {
        "id": "outerwear_11_hugo-boss-navy-check-suit-jacket",
        "slug": "outerwear_11_hugo-boss-navy-check-suit-jacket",
        "cat": "Outerwear",
        "name": "Hugo Boss navy check suit jacket",
        "colour": "Dark navy with a tonal glen check",
        "hex": "#22283A",
        "role": "Anchor dark",
        "cut": "Two-button notch-lapel suit jacket, flap pockets, wide lapels with a low gorge",
        "material": "Wool suiting",
        "weight": "Mid",
        "formality": "Formal",
        "fit": "Problems are era, not size. Long - covers the seat entirely and runs toward "
               "mid-thigh where a current cut ends around mid-seat. Wide lapels with a low "
               "gorge. No waist suppression, hangs straight from the chest. Sleeves long, "
               "sitting at the knuckle",
        "condition": "Good",
        "verdict": "Keep",
        "verdictNote": "Good cloth in a 2000s silhouette. Fine as the obligation suit; not "
                       "worth rebuilding",
        "scope": "occasional",
        "worksAlone": True,
        "warmth": 2,
        "weatherproof": {"rain": False, "wind": False},
        "pairs": "trousers_12_hugo-boss-navy-check-suit-trouser - its matching half. Worn as a "
                 "full suit, not as separates",
        "layer": "Outer layer",
        "avoid": "Wearing it as an odd jacket - the check ties it to its trousers",
        "notes": "BOSS, made in Bulgaria - mainline, not the Italian-made tier. Matching half "
                 "of a two-piece with trousers_12. Only the sleeves are a genuine alteration; "
                 "shortening the body changes the pocket-to-hem proportion and narrowing the "
                 "lapels is a front rebuild. You cannot tailor a 2000s silhouette into a 2020s "
                 "one - you can only make a 2000s suit fit better. Recommendation 2026-08-28: "
                 "leave it, do the trousers, treat this as the funeral/formal-client suit. If "
                 "a current-looking suit is ever wanted, that is a purchase not an alteration. "
                 "Render came out mid-grey; the cloth is dark navy in every real frame - hex "
                 "sampled from the photographs",
        "noPhoto": False,
        "photoRef": "Outerwear/outerwear_11_hugo-boss-navy-check-suit-jacket_* "
                    "(7 frames: label, hanger, 2 detail, 3 worn)",
        "photoPrefix": "outerwear_11_hugo-boss-navy-check-suit-jacket",
        "retailPrefix": "outerwear_11_hugo-boss-navy-check-suit-jacket",
    },
    {
        "id": "outerwear_12_varce-black-shawl-dinner-jacket",
        "slug": "outerwear_12_varce-black-shawl-dinner-jacket",
        "cat": "Outerwear",
        "name": "Varce black shawl-collar dinner jacket",
        "colour": "Black with black satin shawl facings",
        "hex": "#131313",
        "role": "Anchor dark",
        "cut": "Single-button dinner jacket, satin shawl collar, satin-jetted pockets, "
               "satin-covered cuff buttons. Slim fit",
        "material": "Poly/wool blend with satin facings",
        "weight": "Mid",
        "formality": "Formal (black tie)",
        "fit": "Correct. Shoulders sit on the shoulder point, real waist suppression, length "
               "ends around mid-seat, sleeves right. The best-fitting tailored garment in the "
               "wardrobe",
        "condition": "Good - some lint on the lapel, nothing structural",
        "verdict": "Keep",
        "verdictNote": "The black tie outfit that actually works - complete, correctly fitted, "
                       "and shawl collar is more correct than peak",
        "scope": "occasional",
        "worksAlone": True,
        "warmth": 2,
        "weatherproof": {"rain": False, "wind": False},
        "pairs": "trousers_13_varce-black-slim-formal-trouser (its matching half) and "
                 "accessories_03_black-satin-bow-tie. Satin tie to satin lapel is the rule and "
                 "this kit follows it",
        "layer": "Outer layer",
        "avoid": "Anything but black tie. Shawl collar and satin make it unusable as a blazer",
        "notes": "Varce Italia, Slim Fit. Budget label - poly/wool blend, made in China - but "
                 "it fits properly and it is complete, which beats a better garment that does "
                 "not. Compare outerwear_10: the Burberry is the better garment and the worse "
                 "outfit. Together with trousers_13 and accessories_03 this is a full, "
                 "coherent black tie kit. Its render is the most faithful of the eleven "
                 "generated on 2026-08-28 - black and true neutrals survive the generator "
                 "where subtle colours (sage, navy) drift badly",
        "noPhoto": False,
        "photoRef": "Outerwear/outerwear_12_varce-black-shawl-dinner-jacket_* "
                    "(8 frames: label, hanger, 5 worn-front, detail)",
        "photoPrefix": "outerwear_12_varce-black-shawl-dinner-jacket",
        "retailPrefix": "outerwear_12_varce-black-shawl-dinner-jacket",
    },
    {
        "id": "trousers_12_hugo-boss-navy-check-suit-trouser",
        "slug": "trousers_12_hugo-boss-navy-check-suit-trouser",
        "cat": "Trousers",
        "name": "Hugo Boss navy check suit trouser",
        "colour": "Dark navy with a tonal glen check",
        "hex": "#22283A",
        "role": "Anchor dark",
        "cut": "Flat-front suit trouser, belt loops, straight untapered leg, high rise",
        "material": "Wool suiting",
        "weight": "Mid",
        "formality": "Formal",
        "fit": "Full through the thigh and knee, hanging dead straight with no taper. Long - "
               "heavy stack of fabric pooling at the ankle even barefoot. High rise, sitting "
               "well above the natural waist. Waist itself is about right",
        "condition": "Good - some lint on the leg, no wear visible",
        "verdict": "Tailor",
        "verdictNote": "Good cloth, most ageing silhouette in the wardrobe. Cheapest fix with "
                       "the biggest visible payoff",
        "scope": "occasional",
        "worksAlone": True,
        "pairs": "outerwear_11_hugo-boss-navy-check-suit-jacket - its matching half. Worn as a "
                 "full suit, not as separates",
        "avoid": "Pairing with any other jacket - the check ties it to outerwear_11",
        "notes": "BOSS 'The Grand/Central', US 40/R - suit-labelled, so sized to the jacket. "
                 "High + full + long is the single most ageing silhouette in menswear and runs "
                 "directly against the stated goal of not looking like a 50-year-old. All of "
                 "it is fixable: the waist is right, which is the fiddly part. Of the two "
                 "tailoring jobs flagged 2026-08-28 this is the one worth doing without "
                 "hesitation. Render came out mid-grey; cloth is dark navy in every real frame",
        "actionRequired": "TAILOR",
        "actionStatus": "pending",
        "actionNote": "Hem substantially and taper the leg from the knee down. Waist as-is. "
                      "Flagged 2026-08-28",
        "noPhoto": False,
        "photoRef": "Trousers/trousers_12_hugo-boss-navy-check-suit-trouser_* "
                    "(5 frames: label, 2 detail, worn-front, worn-side)",
        "photoPrefix": "trousers_12_hugo-boss-navy-check-suit-trouser",
        "retailPrefix": "trousers_12_hugo-boss-navy-check-suit-trouser",
    },
    {
        "id": "trousers_13_varce-black-slim-formal-trouser",
        "slug": "trousers_13_varce-black-slim-formal-trouser",
        "cat": "Trousers",
        "name": "Varce black slim formal trouser",
        "colour": "Black",
        "hex": "#141414",
        "role": "Anchor dark",
        "cut": "Flat-front formal trouser, belt loops, slim tapered leg. No satin side stripe",
        "material": "65% polyester / 35% wool, polyester lining",
        "weight": "Mid",
        "formality": "Formal (black tie)",
        "fit": "Slim through the leg, properly tapered, correct length with a slight break. "
               "The best-fitting formal trouser in the wardrobe",
        "condition": "Good",
        "verdict": "Keep",
        "verdictNote": "Cut is right, cloth is the weak half. Fits better than anything formal "
                       "Max owns",
        "scope": "occasional",
        "worksAlone": True,
        "pairs": "outerwear_12_varce-black-shawl-dinner-jacket (its matching half) and "
                 "accessories_03_black-satin-bow-tie",
        "avoid": "Nothing specific - but see notes on wearing these under the Burberry",
        "notes": "Varce Italia, SLIM-36R, colour 3208/BLACK, made in China, dry clean only. "
                 "65% polyester is the real limitation: against wool it reads flat and "
                 "slightly plasticky, and evening light is exactly where that shows. No satin "
                 "side stripe, so strictly these are black suit trousers rather than tuxedo "
                 "trousers - academic for most Australian black tie. These can be worn under "
                 "outerwear_10 (the Burberry) but it is a quality mismatch, not just a colour "
                 "one. A wool replacement is the real upgrade if this kit ever gets used often. "
                 "NOTE: these were uncatalogued until 2026-08-28 and their absence caused a "
                 "wrong conclusion that Max owned no black formal trousers - a live example of "
                 "the orders-and-gaps.md warning that the gap list is unreliable for "
                 "categories never catalogued",
        "noPhoto": False,
        "photoRef": "Trousers/trousers_13_varce-black-slim-formal-trouser_* "
                    "(3 frames: label, worn-front, worn-side)",
        "photoPrefix": "trousers_13_varce-black-slim-formal-trouser",
        "retailPrefix": "trousers_13_varce-black-slim-formal-trouser",
    },
    {
        "id": "accessories_03_black-satin-bow-tie",
        "slug": "accessories_03_black-satin-bow-tie",
        "cat": "Accessories",
        "name": "Black satin bow tie",
        "colour": "Black",
        "hex": "#0F0F0F",
        "role": "Anchor dark",
        "cut": "Pre-tied butterfly bow tie, adjustable neckband marked 15-19, metal hook and "
               "slide closure",
        "material": "Satin",
        "weight": "Fine",
        "formality": "Formal (black tie)",
        "fit": "Adjustable, fits",
        "condition": "Good",
        "verdict": "Keep",
        "verdictNote": "Completes the black tie kit, and correctly - satin tie to satin lapel",
        "scope": "occasional",
        "worksAlone": False,
        "pairs": "outerwear_12_varce-black-shawl-dinner-jacket and "
                 "trousers_13_varce-black-slim-formal-trouser",
        "layer": "At the collar, with a dress shirt",
        "avoid": "Anything that is not black tie",
        "notes": "Pre-tied rather than self-tie. Purists object because a self-tie has slight "
                 "asymmetry that reads as real, where pre-tied sits a fraction too perfect - "
                 "at a normal Australian black tie event nobody checks. A self-tie in the same "
                 "satin is inexpensive and is the single cheapest upgrade to the whole kit. "
                 "Matching the tie's finish to the lapel facing is the rule and this does",
        "noPhoto": False,
        "photoRef": "Accessories/accessories_03_black-satin-bow-tie_01_flat.jpg (1 frame)",
        "photoPrefix": "accessories_03_black-satin-bow-tie",
        "retailPrefix": "accessories_03_black-satin-bow-tie",
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
for i in NEW:
    print(f"   + {i['id']}  ({i['verdict']})")
print(f"written      : {len(payload['items'])} -> {DST.name}")

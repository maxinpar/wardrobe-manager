"""Batch 6, 2026-08-28: the last non-golf garment.

T.M. Lewin fitted shirt - Max's fit benchmark. Closes out the non-golf wardrobe.

Reads the batch-5 import file read-only and writes a NEW file.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\maxim\PycharmProjects\wardrobe-manager")
SRC = REPO / "data" / "wardrobe_2026-08-28_batch5.json"
DST = REPO / "data" / "wardrobe_2026-08-28_batch6.json"

NEW = [
    {
        "id": "tops_50_tm-lewin-lilac-stripe-fitted-shirt",
        "slug": "tops_50_tm-lewin-lilac-stripe-fitted-shirt",
        "cat": "Tops",
        "name": "T.M. Lewin lilac stripe fitted shirt",
        "colour": "Lilac with a fine white stripe",
        "hex": "#A88BB5",
        "role": "Mid colour",
        "neck": "collar",
        "cut": "Fitted body (John Francomb 'Rovereto'), 15in / 38cm collar, 34in sleeve",
        "material": "Cotton poplin",
        "weight": "Light",
        "formality": "Smart-casual",
        "fit": "Tight through the midsection - Max's own assessment 2026-08-28, wearing it. "
               "Chest, shoulders, collar and sleeves all sit correctly; it is the waist that "
               "is snug. NOTE: a first read from the photographs called this 'slight softness, "
               "no strain' and that was wrong - the wearer's account governs",
        "condition": "Good",
        "verdict": "Keep",
        "verdictNote": "Max's fit benchmark rather than a rotation shirt - kept for what it "
                       "measures, not for how often it goes on",
        "scope": "occasional",
        "worksAlone": True,
        "pairs": "Stone and sand chinos, worn open-collar. The lilac is a near-relative of the "
                 "mauve in accessories_00, so those two sit together well",
        "layer": "On its own, or under a plain dark knit",
        "avoid": "Under a suit with a tie - lilac-with-white-stripe on a fitted T.M. Lewin body "
                 "is very specifically mid-2000s City finance, and that register brings it "
                 "straight back. Open collar with chinos is what keeps it current",
        "notes": "T.M. Lewin, John Francomb 'Fitted Rovereto'. THE BENCHMARK SHIRT: Max keeps "
                 "this as his reference for fit - it dates from when he was at his slimmest and "
                 "he measures against it. As of 2026-08-28 it is tight around the middle. That "
                 "is the whole point of the garment and the reason it stays in the catalogue; "
                 "it is a measuring stick, not a rotation piece. The colour genuinely works - "
                 "enough saturation to put colour into the face, unlike the sage scarf "
                 "(accessories_01) which sits too close to his hair value. Last non-golf "
                 "garment catalogued; golf apparel is deliberately deferred",
        "noPhoto": False,
        "photoRef": "Shirts/tops_50_tm-lewin-lilac-stripe-fitted-shirt_* "
                    "(6 frames: label, 2 worn-front, 2 worn-side, detail)",
        "photoPrefix": "tops_50_tm-lewin-lilac-stripe-fitted-shirt",
        "retailPrefix": "tops_50_tm-lewin-lilac-stripe-fitted-shirt",
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

"""Batch 2, 2026-08-28: the Prodigy fleece, plus the 'no label exists' correction
on the two scarves whose material could not be confirmed.

Reads the accessories import file read-only and writes a NEW file. Nothing is
edited in place. Only the three touched ids should show as changes.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\maxim\PycharmProjects\wardrobe-manager")
SRC = REPO / "data" / "wardrobe_2026-08-28_accessories.json"
DST = REPO / "data" / "wardrobe_2026-08-28_batch2.json"

NEW = [
    {
        "id": "outerwear_09_prodigy-navy-sherpa-fleece",
        "slug": "outerwear_09_prodigy-navy-sherpa-fleece",
        "cat": "Outerwear",
        "name": "Prodigy navy sherpa-lined fleece",
        "colour": "Navy with a cream sherpa lining",
        "hex": "#3D4450",
        "role": "Anchor dark",
        "cut": "Full-zip polar fleece, sherpa-lined body, stand collar, two zip pockets, "
               "elasticated cuffs, hip length. Pale blue piping across the chest and "
               "shoulder seams",
        "material": "Polar fleece with sherpa-lined body",
        "weight": "Mid-Heavy",
        "formality": "Casual",
        "fit": "Sits well - hits at the hip, sleeves the right length, less boxy than it "
               "looks on the hanger",
        "condition": "Good - no pilling, lining clean",
        "verdict": "Keep",
        "verdictNote": "Fills the one outerwear gap: warm, casual, zip-front and sleeved. "
                       "Everything else is smart, bike-specific or sleeveless",
        "scope": "core",
        "worksAlone": True,
        "warmth": 4,
        "weatherproof": {"rain": False, "wind": False},
        "pairs": "Stone chino, denim, grey. Over a tee or a plain knit",
        "layer": "Outer layer. Nothing goes over it",
        "avoid": "The office, and anything smart. The pale blue piping and elasticated cuffs "
                 "undercut tailoring. Not a bike layer - not weatherproof, and the bomber and "
                 "waxed biker already cover that",
        "notes": "Assessed 2026-08-28 against the other seven outerwear pieces: three blazers, "
                 "a leather bomber, a waxed biker, a wool overcoat and a puffer gilet. Every "
                 "one of those is smart, bike-specific or sleeveless, so this is the only warm "
                 "casual sleeved layer in the wardrobe - the cold Saturday morning and golf "
                 "club car park garment. Second warmest thing after the INDACO overcoat. The "
                 "pale blue piping is the dated detail; it is mid-2000s outdoor-brand styling "
                 "and it is what keeps this useful rather than good. Catalogued in the same "
                 "session as a Westpac-branded JB's Wear fleece that was binned - the "
                 "difference is that this one carries no third-party branding, is navy rather "
                 "than greying black, and fills a gap instead of duplicating one. Standing "
                 "rule agreed from that comparison: no third-party logos in the work wardrobe. "
                 "The first render came back black; a regen fixed it. Hex is sampled from the "
                 "real frames",
        "careNote": "Prodigy Clothing Co, size M, made in China",
        "noPhoto": False,
        "photoRef": "Outerwear/outerwear_09_prodigy-navy-sherpa-fleece_* (4 frames: label, "
                    "hanger, worn-front, worn-side)",
        "photoPrefix": "outerwear_09_prodigy-navy-sherpa-fleece",
        "retailPrefix": "outerwear_09_prodigy-navy-sherpa-fleece",
    },
]

# Confirmed by Max 2026-08-28: these two genuinely have no care label. Recording it
# so nobody re-shoots them looking for one, the way the lost belt photos are
# recorded in photo-filing-guide.md.
NO_LABEL_NOTE = (
    " CONFIRMED 2026-08-28: this garment has no care label at all - it is not that the "
    "label frame is missing, it is that no tag exists. Material cannot be recovered from "
    "the garment. Do not re-shoot looking for one."
)
AMEND = {
    "accessories_01_sage-print-gauze-scarf": NO_LABEL_NOTE,
    "accessories_02_charcoal-check-crinkle-scarf": NO_LABEL_NOTE,
}

payload = json.loads(SRC.read_text(encoding="utf-8"))
by_id = {i["id"]: i for i in payload["items"]}

clashes = [i["id"] for i in NEW if i["id"] in by_id]
if clashes:
    sys.exit(f"ABORT - these ids already exist: {clashes}")

missing = [k for k in AMEND if k not in by_id]
if missing:
    sys.exit(f"ABORT - cannot amend ids that are not present: {missing}")

for item_id, suffix in AMEND.items():
    item = by_id[item_id]
    if suffix.strip() in (item.get("notes") or ""):
        sys.exit(f"ABORT - {item_id} already carries the no-label note")
    item["notes"] = (item.get("notes") or "").rstrip(". ") + "." + suffix

payload["items"].extend(NEW)
payload["generated"] = "2026-08-28"

DST.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"source items : {len(by_id)}")
print(f"new items    : {len(NEW)}")
print(f"amended      : {len(AMEND)}  ({', '.join(sorted(AMEND))})")
print(f"written      : {len(payload['items'])} -> {DST.name}")

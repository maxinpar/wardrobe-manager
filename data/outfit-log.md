# Outfit Log — worn fits (newest first)

_The complete wear history. Two entries as of 2026-08-26. These become `wear_events`._

Filing convention for photos in `G:\My Drive\Claude stuff\Wardrobe Photos\Fits`:
- worn photos: `fit_<slug>_NN_<angle>.jpg`
- generated renders: `fit_<slug>_render.<ext>` — **a render is not evidence a fit was worn**

---

## Wear event 2 — Tue 26 Aug 2026
- **fit:** "Moto & burgundy" · **context:** work (bank) · **rating:** 7/10
- **weather:** not recorded
- **items worn (by id):**
  - `outerwear_02_indindustrie-black-waxed-biker`
  - `polo-rl-burgundy-cashmere-crew`
  - `trousers_09_celio-indigo-jeans`
  - `shoes_03_ecco-black-nubuck`
  - `belts_11_black-classic-pin-buckle`
  - _plain tee, base layer_ — **NOT IN CATALOGUE.** Free-text item; no id exists. This is the
    second wear event to include one, and the reason the schema must allow an unmatched item.
- **photos:** `Fits/fit_moto_and_burgundy_01_worn-front.jpg` (1, worn front, mirror)
- **generated render:** `Fits/Gemini_Generated_Image_x9dcv4x9dcv4x9dc.jpeg` — awaiting rename to
  `fit_moto_and_burgundy_render.jpeg`. Flag as generated, never as a worn photo.
- **note:** Works. Burgundy against black does what it should; the jacket sits correctly at the hip
  with clean shoulders; the Ecco disappears into the hem, which is correct behaviour for an all-black
  shoe. Reads current, not dated. Marked down for the jeans: too faded to sit under all that black,
  so the eye lands on the weakest garment, and the hem breaks and pools over the shoe.
- **corrections this wear produced:**
  - `outerwear_02` condition note was wrong — see the patch script.
  - `trousers_09` was never hemmed — see the patch script.

## Wear event 1 — Mon 17 Aug 2026
- **fit:** "Burgundy & denim" · **context:** work (bank) · **rating:** 8/10
- **weather:** cold, light rain
- **items worn (by id):**
  - `polo-rl-burgundy-cashmere-crew`
  - `trousers_09_celio-indigo-jeans`
  - `shoes_02_andre-tan-brogue`
  - `belts_04_distressed-brown-everyday`
  - _plain neutral tee, base layer_ — **NOT IN CATALOGUE.** Free-text item.
- **photos:** 2 (front + side), cropped head-to-shoes. Currently embedded in the legacy
  `Wardrobe_Manager.html` artifact only — not yet extracted as standalone files.
- **note:** Works — warm, cohesive burgundy/tan/blue, trim, current, smart-casual-right for a cold
  casual work day. Brogues correct with denim; rubber sole good in the wet.
- **tweak:** jeans read mid-blue with some fade (leans weekend); a darker/cleaner indigo or the
  black jean lifts it for the office.

---

## Cross-entry signal
Both wear events independently flag **the same jeans** for **the same reason** — too faded, leans
weekend. Two assessments a week apart reaching the same conclusion is a signal, not noise.
`trousers_09` is the wardrobe's most-used bottom and its weakest link.

Consequences for the shopping list: "spare dark-wash jeans" should move from priority 2 to
priority 1.

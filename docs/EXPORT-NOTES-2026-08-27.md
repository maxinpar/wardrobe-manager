# Export for Claude Code — 2026-08-27

Two files, both in this folder:

| file | what it is |
|---|---|
| `wardrobe.json` | the canonical catalogue, **113 items**. Same schema as before, appended to. |
| `fits.json` | **35 fits** as structured data — ordered slots keyed by `items[].id`. New. |

`wardrobe.json` supersedes `data/wardrobe.json` referenced in `db-port-brief.md`. Everything below
is what changed since that brief was written, and what will break if you import against its numbers.

---

## 1. The reconciliation numbers in the brief are stale — do not assert against them

`db-port-brief.md` §2 and §10 tell the importer to stop if counts don't match 69 items /
Keep 45 · Tailor 10 · Bin 8 · Replace 6 / core 65 · out 4 / 13 without photos.
**Those were correct on 2026-08-25 and are wrong now.** Current truth:

| | brief (69 items) | now (113 items) |
|---|---|---|
| Knitwear | 18 | 18 |
| Trousers | 12 | **11** |
| Shoes | 12 | 12 |
| Belts | 11 | 11 |
| Tops | 10 | **53** |
| Outerwear | 6 | **8** |
| Keep | 45 | **79** |
| Tailor | 10 | **11** |
| Bin | 8 | **17** |
| Replace | 6 | 6 |
| scope core | 65 | **103** |
| scope out | 4 | **6** |
| scope occasional | — | **4** ← new value |
| noPhoto | 13 | **7** |

The Tops jump (10 → 53) is three weeks of shirt cataloguing. The Trousers drop (12 → 11) is a
correction, not a loss.

**Update the assertion to the right-hand column** — or better, make the importer print the counts
and compare against a value it reads from the file rather than a hardcoded one, because this will
go stale again next week.

## 2. Schema changes you must handle

**`scope` now has three values, not two.** The brief says `core | out`. There is now
**`occasional`** on four items: `tops_14_souleiado-terracotta-print-shirt`,
`tops_16_hm-cream-orchid-floral-shirt`, `tops_19_baubridge-kay-white-twill-shirt`,
`tops_20_christian-lacroix-geometric-print-shirt`. Semantics: wearable and in scope, but not part
of the daily rotation. If `scope` became a Postgres enum this is a migration; if it became a lookup
table (which the brief recommends) it is one INSERT.

**Four fields exist that the brief's field list does not mention. All must be nullable.**

- `unconfirmed` (bool) — on the five tees `tees_01`…`tees_05`. Their colours and hexes were
  assumed from a verbal list, never photographed. Surface this in the UI; don't let a guessed hex
  look authoritative.
- `actionRequired` (text), `actionStatus` (text), `actionNote` (text) — currently only on
  `outerwear_07_jules-pale-grey-linen-blazer` (`DRY CLEAN` / `pending`). This is the beginning of a
  proper task model. Suggest a small `item_actions` table rather than three columns, since several
  more items need one (see §5).

**Nine items have an empty `retailPrefix`.** All nine are `Bin`. That is deliberate and correct —
binned items get no catalogue render. Empty string, not null; normalise if you care.

## 3. New folder: `Fits`

`db-port-brief.md` §5 lists the Drive subfolders as Knitwear, Shirts, Trousers, Shoes, Belts,
Outerwear, Retail. There is now an eighth:

```
G:\My Drive\Claude stuff\Wardrobe Photos\Fits\
```

28 fit renders, named `fit_<code>_<slug>_render.<ext>`. Extensions are a **mix of `.png` and
`.jpg`** and the values in `fits.json` are exact — do not assume one.

Two files in that folder are **not** fit renders and should be skipped by any glob:
`fit_moto_and_burgundy_01_worn-front.jpg` (a real worn photo) and
`Gemini_Generated_Image_x9dcv4x9dcv4x9dc.jpeg` (unidentified, awaiting Max).

Fit renders are **generated images, not photographs of Max wearing the clothes.** Same rule as
§3 of the brief: the app must never present a render as a photo of the real thing.

## 4. `fits.json` — read this before importing it

35 fits. They map onto the `outfits` + `outfit_items(role, position)` model in brief §3.
Roles used: `outer`, `top`, `base` (a tee worn under a V-neck), `bottom`, `shoe`, `belt`.

- **27 have full compositions keyed by `items[].id`.** Verified: every `itemId` resolves to exactly
  one item in `wardrobe.json`, none references a `Bin`, `Replace` or `out`-of-scope item, and every
  `render` filename exists in the Drive folder. No fuzzy matching needed anywhere.
- **8 have `"items": null` and `"compositionKnown": false`.** Codes C7, C8, W7, W8, K7, K8, S3, S4.
  **The renders are real and correct; the garment lists are genuinely lost** — they were designed in
  a session whose context was compacted before they were written to a doc. Import the render and the
  code, leave `outfit_items` empty, flag them in the UI as *composition to confirm*, and let Max read
  the garments off the render. **Do not infer the items from the filename slug.** A slug like
  `navy-blazer-and-blue-stripe` narrows it to maybe three candidates per slot; a guess written into
  the database would be indistinguishable from a fact six months from now.
- **The 10 vetted looks in `work-outfits.md` are deliberately NOT in this file.** They reference
  items by display name, names are not unique, and brief §4 already specifies the hand-mapping
  approach with an assertion that each name resolves to exactly one item. Seed those from
  `work-outfits.md` as the brief says. Nothing here duplicates them.

Categories on the 35: cold 9 · warm 9 · casual 11 · smart 6.

## 5. Open items that need a decision, not code

1. **`tops_19_baubridge-kay-white-twill-shirt`** — verdict is provisional, pending an oxalic-acid
   test on rust marks. Import as-is; it may flip to Bin.
2. **`tops_23_enzo-di-milano-navy-diagonal-stripe-shirt`** — collar turning to be quoted by the
   tailor. Verdict `Tailor` is correct but the work isn't booked.
3. **`polo-rl-burgundy-cashmere-crew`** — carries a correction made in a Claude session that never
   reached the old DB. The JSON is authoritative here; if an older row disagrees, the JSON wins.
4. **Five items need collar treatment** (enzyme / oxygen bleach): `tops_19`, `tops_22`, `tops_26`,
   `tops_27`, `tops_33`. None carries `actionRequired` yet — only `outerwear_07` does. If you build
   the `item_actions` table in §2, these are its first rows.
5. **The trouser verdicts.** Brief §4 flags that all trousers were tailored 2026-08-20 and are
   wearable, but their `verdict` still says `Tailor`. **Still unresolved in this export.** Report it
   and ask Max before flipping. Knitwear `Tailor` items are separately unconfirmed — leave alone.

## 6. Unchanged

`Shirts` folder still maps to the `Tops` category. Item ids are unchanged and were never renumbered.
Photo matching is still "filename starts with `photoPrefix`". Renders are still
`<retailPrefix>_retail.<ext>`. Nothing in the Drive folder was modified to produce this export —
files were read and renamed in place only within `Shirts` and `Retail`, per Max's own instruction,
and no file was moved, copied or deleted.

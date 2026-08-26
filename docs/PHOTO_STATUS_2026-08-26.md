# Drop for Claude Code — 2026-08-26 (final, rev 4)

Supersedes every earlier drop. Unzip into the port folder, overwriting.

| File | Goes to | What it is |
|---|---|---|
| `patch_wardrobe_20260826.py` | repo root or `scripts/` | **Run this first.** Rev 3. Corrects, deletes and adds items. |
| `data/killer-looks.md` | `data/` | 7 fits, items by id |
| `data/fits-batch-2.md` | `data/` | **20 new fits**, items by id, + retail filenames per fit |
| `data/outfit-log.md` | `data/` (replaces) | Both wear events, items by id |
| `data/style-drafts.md` | `data/` | `style` suggestions — drafts, not authored values |

## 1. Run the patch

```
python patch_wardrobe_20260826.py data/wardrobe.json           # dry run
python patch_wardrobe_20260826.py data/wardrobe.json --commit  # writes .new, backs up .bak
```

Idempotent (verified: 54 changes from a clean original, 0 on a second run). Never edits in place.
Exits non-zero rather than committing if the counts don't reconcile:

```
items 73 | noPhoto 7 | Keep 50, Tailor 9, Bin 8, Replace 6 | core 69, out 4
```

### What it does

**Adds 5 crew tees.** `tees_01_white-crew` … `tees_05_red-crew`. **These must exist before
`fits-batch-2.md` imports** — nine of the twenty fits reference them and would fail on unresolved
references. ⚠️ **RENDER-ONLY ITEMS — a distinction the app needs to make.** Generated retail renders now exist
for white, grey and black (`Retail\tees_0{1,2,3}_*-crew_retail.jpeg`), but **no photograph of any
actual tee exists**. So `noPhoto` stays `true` and `unconfirmed` stays `true`: colour is now measured
from the renders, but fit, condition and material are still guesses.

This is the same distinction as the group-shot shoes: "has an image" is not "has been photographed".
Three states worth badging separately — photographed, render-only, nothing.

`tees_02_grey-crew` hex corrected to **`#A6A6A6`** (measured from its render — a heather marl,
lighter and more neutral than the `#8E9095` first assumed). White and black were near-exact.

**Deletes `trousers_00_decathlon-stone`** — a phantom duplicate of `trousers_01_decathlon-beige`.
Max physically counted and confirmed he owns one beige/stone Decathlon chino, not two. Caught when
he re-sent photos of the supposedly unphotographed pair and they were byte-identical to
`trousers_01`'s label and flatlay. The label reads **US W33 L33**; `trousers_01` was recorded as
"US W31 L33" — that transcription error was the only field separating the two records.

**Corrects `shoes_08b`, twice.** Not a penny loafer (the vamp is a single unbroken panel — no strap,
no keyhole; it's a plain-vamp venetian moccasin) and not tan (dark chocolate brown, pebbled). The id
and `photoPrefix` keep the `-tan-loafer` stem because photos are filed under it.

**Gives five shoes individual prefixes.** `shoes_08a/b/c` shared one stem and `shoes_09a/b` shared
another — that is exactly why none of them ever rendered individually. **This orphans two files:**
`Shoes/shoes_08_loafers-group_reference.webp` and `Shoes/shoes_09_nike-trainers-group_reference.webp`.
Park them, don't delete.

**Identifies `belts_11` as H&M** — size M, 85-95, article 304970, read off the underside stamp the
catalogue had recorded as illegible.

**Flags `belts_05` and `belts_10` as not located, NOT deleted.** Neither appeared when Max gathered
every belt he owns; both were already `Replace`. Absence is weaker evidence than the proof that
removed `trousers_00`. Confirm with Max before removing.

**Corrects `outerwear_02`** — the "coating faded/dusty" note came from hanger shots and is wrong on
the body.

**Flags `trousers_09` as never tailored** — the 2026-08-20 batch covered `Tailor` items; this pair is
`Keep` so it was skipped despite its own record saying "~2cm too long". Check any other `Keep`
trouser with a length note.

## 2. Import the fits — 37 total

| Source | Count | Item refs |
|---|---|---|
| `work-outfits.md` | 10 | **by display name — ambiguous**, needs a hand-written mapping table |
| `killer-looks.md` | 7 | by id |
| `fits-batch-2.md` | 20 | by id |

`fits-batch-2.md` categories: Office warm 6 · Office cold 6 · Casual/Friday 6 · Smart 2. Smart is
capped at 2 deliberately — one blazer, one wool trouser, one smart shoe means a third would be the
same skeleton with a different knit.

Each fit carries: register, `formality_rank`, `temp_bands`, `rain_safe`, `good_for`, `bad_for`,
`commentary`, `catch`, plus `precondition` and alternate slots where they apply. See
`fits-requirements.md` (sent earlier) for the entity spec.

**`bad_for` is populated on the id-referenced fits and empty on the 10 from `work-outfits.md`** —
those genuinely have no recorded negatives. Don't derive them.

## 3. Images — all on Drive, nothing to send

`G:\My Drive\Claude stuff\Wardrobe Photos\` — read-only, as the main brief says.

- **Every one of the 73 items has a source photo** except the 5 tees and 2 missing belts.
- **~60 retail renders** in `Retail\`, named `<retailPrefix>.<ext>`. Any doc claiming only one exists
  is stale. **Add `Retail` to `build_app.py`'s scan list** and decide whether the app prefers the
  retail render over the source photo when both exist.
- **20 fit renders** in `Fits\`, named `fit_<code>_<slug>_render.png` (e.g.
  `fit_c5_oatmeal-and-cobalt_render.png`). One per fit in `fits-batch-2.md`. The code prefix sorts
  them into category order.
- **1 real worn photo**: `Fits/fit_moto_and_burgundy_01_worn-front.jpg`.

⚠️ **Fit renders are generated illustrations, not photographs.** Flag them as such and never present
one as evidence a fit was worn. The 10 vetted looks and 7 killer looks have no renders yet.

⚠️ **`photoPrefix` is still not guaranteed unique** in older data — warn rather than assume.

## 4. Known data-quality notes, not applied

- **`tops_02_brioni-white-blue-collar-polo`** — the contrast is on the **placket**, not the collar.
  Cosmetic naming error; id stays.
- **`shoes_08c_megis-driving-moc`** is scoped `out` (holiday only), set before there was a decent
  photo. The individual shots show it in good condition. Max's call, unchanged.
- **Three retail renders drift darker/duller than their recorded hex** —
  `polo-rl-burgundy-cashmere-crew` (renders near-black, recorded `#6E2233`),
  `trousers_07_oxford-sage` and `tops_05_sage-pique-polo`. Fits inherit the drift faithfully. The
  blazer had the same fault until it was regenerated.

## 5. Still unlogged

**Dress shirts, shorts, socks, golf apparel, accessories** — zero items each. Golf apparel is
deliberately deferred (Max's call). Both wear events include a plain tee with no id, so free-text
items on a wear event are the current normal, not an edge case.

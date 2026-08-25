# Owner profile, styling rules, and photo layout

Extracted from the Claude Project docs (`CLAUDE.md`, `PROJECT_NOTES.md`, `work-outfits.md`,
`data-integration-brief.md`, `photo-filing-guide.md`) so the app doesn't have to re-derive them.
Everything here is hand-written knowledge, not generated — treat it as the spec for the picker.

---

## 1. Owner profile

- Max, 48, French, works in a bank, lives in Sydney (timezone Australia/Sydney).
- **The office is genuinely relaxed/casual — NOT formal, not even strict smart-casual.** Devs in
  t-shirts and jeans, polos, puffer vests, sneakers. Nothing casual stands out there.
- Goal: look respectable and current — not dated, not "like a 50-year-old" — **relative to a
  genuinely low bar**. This is not about out-dressing the room. The smartest available option is
  *not* automatically the right answer (a full wool overcoat reads overdressed for daily wear).
  But looking smart is welcome — so the model is **two registers, picked by mood/occasion**, not
  one default.
- Daily uniform: trousers/jeans + shoes/sneakers + a top layer (jumper or polo). A puffer vest or
  casual jacket on top all winter is completely normal.
- Sizes: tops M (some XXL Asian sizing ≈ M); trousers ~W33–34 / EU44; shoes ~EU44 / 10.5;
  belts ~34–36in.
- Hard preference: **dislikes roll-necks.** The roll-neck look is hidden by default in the picker.

## 2. Outfit-construction rules (the rule engine)

Global rules, in rough priority order:

1. Pale tops need a dark bottom — pale-on-pale washes out.
2. Belt colour tracks shoe colour. Brown belt ↔ brown shoes; black belt ↔ black shoes. Never crossed.
3. Formality is matched across the outfit (don't put a dress trouser with a running shoe).
4. Borderline-golf items are excluded from work outfits (Vuori polo, Cuater belt).
5. A roll-neck is worn alone — no collar underneath.
6. `worksAlone: false` means the item needs a tee or shirt under it. **Max owns no tees**, so every
   `worksAlone: false` item is currently unwearable in a generated outfit. This is why the 10 vetted
   looks all use polos or crews. The picker must respect this or it will produce impossible outfits.
7. The cardigan is *the* layer — it goes over, never under.
8. One statement colour per outfit; everything else neutral.
9. A pale item needs a dark counterpart or the outfit washes out.
10. Navy and black knitwear clash.
11. No two items from the same colour family (red + burgundy; the three mid-blues).
12. Badged/crested items read as uniform → casual only (Lyle & Scott club V-neck).
13. Suede and nubuck stay home in the rain.
14. `scope: "out"` items never appear in outfits (gym fleece, formal Zegna monks, holiday mocs,
    running trainers).
15. Verdict `Bin` items should never be suggested. `Replace` = wearable but on the way out.
    `Tailor` = owned but blocked until altered (**note: all trousers came back from the tailor
    2026-08-20 and are wearable as-is — their verdicts in wardrobe.json are stale**).

Per-item rules live in each record's `pairs` / `layer` / `avoid` free-text fields — 69 hand-written
pairing rules. These are the most valuable and least obvious asset in the dataset. Parse them into a
compatibility matrix and most of the engine writes itself, but keep the original text visible in the
UI so Max can see *why* something was excluded.

## 3. The existing picker logic (`WardrobeKit.pick()`, to be ported)

The current JS picker **chooses among the vetted looks** rather than generating new combinations —
that's deliberate, it keeps the styling rules intact. Scoring:

- weather band match: `tempC` < 14 cold / 14–22 mild / > 22 warm
- rain-safety: rain drops suede and nubuck items
- Friday bonus for the cardigan look
- bonus for wear-as-is over needs-tailoring
- a stable per-day rotation — `pick()` is **deterministic per calendar day** (same outfit all day,
  different tomorrow, no `Math.random`, no flicker on re-render)
- roll-neck look excluded unless `allowDisliked: true`

Options it accepts: `tempC`, `rain`, `allowTailoring`, `allowDisliked`, `date`, `exclude`.

Keep the "pick from vetted looks" model as the default in the new app. Free combinatorial generation
can be a second mode later, but the vetted looks are also the correctness check: **if a generated
engine can't reproduce these 10 looks, it's wrong.**

## 4. Weather

There is no weather source wired up today. Sydney weather is the input the picker wants
(`tempC`, `rain`). Manual entry is acceptable for v1; a free API can come later.

## 5. Photos — where they are and how they're matched

- Root on Max's laptop: `G:\My Drive\Claude stuff\Wardrobe Photos\` (Google Drive, synced locally).
- Subfolders by category: `Knitwear`, `Shirts` (= the Tops category), `Trousers`, `Shoes`, `Belts`,
  `Outerwear`. **`Shirts` maps to `cat = "Tops"` — the folder name and the category name differ.**
- Matching rule used by the old `build_app.py`: **filename prefix == the item's `photoPrefix`**.
  Any suffix after the prefix works (`_01`, `_worn-front`, etc.).
- Shot convention per garment: label → hanger → worn-front → worn-side → worn-back → worn-closed
  (4–8 frames). Belts: buckle → full → underside stamp (2–3 frames).
- Generated "retail" catalogue renders (invisible-mannequin, white background, square) go to
  `Wardrobe Photos\Retail` named `<photoPrefix>_retail.<ext>`. These are **illustrations, not
  photographs of the actual garment** — the app should flag them as such, never present them as
  real photos of the item.
- Current coverage: Knitwear 85 files / all 18 items · Shirts 46 / all 10 · Trousers 52 / 10 of 12 ·
  Shoes 35 / 7 of 12 · Belts 13 / 5 of 11 · Outerwear 35 / all 6.
- **13 items have no photo anywhere** (`noPhoto: true` in the JSON) — 6 belts, 5 shoes, 2 trousers.
  Those photos are permanently lost, not misplaced. Don't go looking for them; the app should just
  fall back to the colour swatch (`hex`) and show a "needs reshoot" flag.

## 6. Known data-quality issues to carry into the DB

- Trouser verdicts still say `Tailor`; they were all tailored on 2026-08-20 and are wearable.
  Fix during or right after the import.
- `formality` is free text with parenthetical variants (`Casual (club crest)`,
  `Smart (formal)`, `Casual / smart-casual`). Needs normalising to an ordinal 1–5 **plus** keeping
  the parenthetical as a note — the parenthetical carries the reason it's capped.
- No `occasions` field exists (work / casual / golf / formal / gym). Golf-ness is prose in `notes`.
  This is the single most useful field the data is missing.
- No pattern field. The wardrobe is ~entirely plain; the exceptions are the Lyle & Scott crest, the
  Manfinity navy tipping, the Manfinity mustard tipping, and a gingham waistband facing.
- `name` is **not unique** (two "Zara Man V-neck", three "Decathlon chino"). `id` is the only key.
- Older docs say "67 items"; the current file has **69** (tops_09 and tops_10 were added later).
- No laundry / availability state exists at all. Every item is implicitly always available.

## 7. Gap analysis / shopping priorities (as of 2026-08-24)

1. Now: charcoal/grey trousers · white + grey crew tees · pale-blue OCBD · a dark polo.
2. Soon: white OCBD · spare dark-wash jeans · a black sneaker.
3. Later: smart-casual dark boot (to replace the black Chelsea) · one quality neutral crew knit.

The crew tees are the highest-leverage buy: they unlock five V-neck knits that currently can't be
worn at all.

## 8. Categories not yet logged

No t-shirts, no shirts/OCBDs, no suits, no shorts, no socks. The schema should not assume the six
current categories are the final list — adding a category must not require a migration.

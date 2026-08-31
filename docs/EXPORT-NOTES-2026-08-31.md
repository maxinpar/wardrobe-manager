# Export for Claude Design — 2026-08-31 (the golf question)

Answers to the three questions asked before the export, then what changed in the file.

| file | what it is |
|---|---|
| `data/wardrobe.json` | the catalogue, **265 items** (239 live, 26 binned). Regenerated from the DB. |
| `data/photos-manifest.json` | **240** item id → retail render filename. New. |

The last file the design read was `data/wardrobe.json` @ main — **73 items, 2026-08-26**. That is
three weeks stale. The jump to 265 is 39+9 golf polos, 40 hats, 20 shorts, 11 golf shoes and the
tee batch, not a schema change.

---

## 1. Category — golf is an occasion tag, not a category

There is **no golf category**. Golf garments are filed under the ordinary categories and carry a
`golf` **occasion tag**. This export adds that tag list to every item as `occasions`.

```js
const golf = items.filter(i => !i.gone && i.occasions.includes("golf"));
```

106 live golf items: **Tops 51 · Hats 25 · Shorts 17 · Shoes 11 · Trousers 1 · Belts 1.**

`occasions` values: `casual` · `work` · `golf` · `weekend` · `formal` · `gym`. An item can hold
several; an empty array means untagged, which is a real answer, not missing data.

**`scope` is not golf and never was.** It is `core` / `out` / `occasional` — whether the picker may
use the item at all. All 106 golf items are `core` except one.

**Filter `gone`.** 26 items carry `"gone": true`; they are in the bin and must not be shown as
wearable. They are exported so a rebuild doesn't lose the bin.

## 2. Crest — prose, in a new `formalityNote` field

No boolean. The crest fact was written per garment, from the photographs, into `formality_note`,
and this export now carries it as **`formalityNote`**. The vocabulary is regular:

| `formalityNote` starts with | means |
|---|---|
| `Royal Sydney - home club…` / `Woollahra - home club…` | home club crest |
| a club name in CAPS, e.g. `BARNBOUGLE LOST FARM - another club's crest…` | another club's crest |
| `Brand polo, no club` / `Brand cap, no club` / `No club crest` | branded, no club crest |
| `…could not be read` / `not legible` / `NOT read at full resolution` | a mark is there and was **not** identified — do not assert either way |

Four polos are in that last row: `tops_70`, `tops_71`, `tops_80`, `tops_89`.

**Max's rule, as the DB actually holds it:** another club's crest is *fine* at his own clubs — that
restriction was an inference and migration 051 removed it. The only surviving caution is wearing a
club's crest as a guest **at that club** (the Bonville and NSWGC caps, `hats_20`–`hats_23`).

30 golf items have no `formalityNote` — the shorts, shoes and belt, where crest was never a question.

## 3. Hats — the category exists

`Hats` was added by migration 044, `sort_order` 65, between Outerwear and Accessories. **40 items,
34 live, 25 golf-tagged** (14 club caps and visors, 8 Titleist/FootJoy brand pieces, 3 slogan caps).
All 25 have a render.

---

## 4. Known bad data — the crossover tags on polos `tops_61`–`tops_99`

**Do not trust `casual`/`weekend` on the batch-2 polos.** Migration `050_golf_crossover_pass` strips
`casual` and `weekend` from any golf garment carrying a club crest, technical fabric or sport
styling. `050_golf_polos_batch_2` shares its number and sorts after it, so those 39 polos were
inserted *after* the rule ran and never had it applied. Every one of them carries
`casual, golf, weekend` regardless — including ~14 crested Royal Sydney and Woollahra polos that the
rule would make golf-only.

The batch-1 polos (`tops_51`–`tops_60`), the shorts and the hats **are** correct.

Flagged, not fixed: re-deciding 39 garments is Max's call, not a migration written to make a tab
look consistent. Until it lands, treat `golf` as reliable and `casual`/`weekend` on `tops_61`+ as
unset rather than false.

## 5. Photos

Renders are `<retailPrefix>.<ext>` — the extension is a **mix of `.jpeg`, `.jpg` and `.png`** and is
in `data/photos-manifest.json`; do not assume one. 102 of the 106 golf items have a render. The four
without: `tops_69`, `tops_70`, `tops_71`, `tops_77`.

The image files themselves are not in git (`photos/` is ignored — 253 MB at full resolution). Max is
sharing the folder separately.

## 6. Still open

- `shorts_02_blush-poly` was excluded from the golf tags on instruction, but its own note reads
  "reads as a golf or performance short". Migration 044 left this as a question. Still open.
- `data/fits.json` was not regenerated in this pass; the fits in the DB are ahead of it.

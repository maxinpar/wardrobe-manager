# Drop for Claude Code — 2026-08-26

Answers the three blockers, plus two corrections you couldn't have known about.

| File | Goes to | What it is |
|---|---|---|
| `data/killer-looks.md` | `data/` | **Blocker 1.** The 7 killer fits. References items **by id** — no mapping table needed. |
| `data/outfit-log.md` | `data/` (replaces) | **Blocker 2.** Both wear events, items by id. Supersedes the 1-entry version. |
| `patch_wardrobe_20260826.py` | repo root or `scripts/` | **Blocker 3.** See below — a patch, not a new `wardrobe.json`. |
| `data/style-drafts.md` | `data/` | `style` suggestions. Drafts, not authored values. |

## On blocker 3 — why a patch and not a new wardrobe.json

Your copy is stale in exactly one structural way (`trousers_11` / the 13-vs-12 count) plus a handful
of note corrections. Hand-transcribing all 69 items to regenerate the file risked silently corrupting
the single source of truth — which ground rule 1 exists to prevent. So instead:

```
python patch_wardrobe_20260826.py data/wardrobe.json           # dry run, prints every change
python patch_wardrobe_20260826.py data/wardrobe.json --commit  # writes .new, backs up .bak
```

- **Idempotent** — verified by running twice against a 69-item fixture; second run reports 0 changes.
- **Never edits in place.** Writes `wardrobe.json.new`, copies the original to `.bak`. Review the
  diff and move it into place yourself.
- **Self-verifying.** Reconciles to 69 items / 12 noPhoto / Keep 45, Tailor 10, Bin 8, Replace 6 /
  core 65, out 4 and **exits non-zero rather than committing** if anything mismatches.

**Baseline moves from 13 to 12.** `trousers_11_black-coated-jeans` was filed 2026-08-25.

## Two corrections you couldn't have known about

**1. `noPhoto` means "no INDIVIDUAL photo", not "no image at all".** The catalogue claims for all
five group-shot shoes that "the referenced group photo is not on Drive - this item has no image
file." **That is false.** Both group photos exist and are legible:

```
Shoes/shoes_08_loafers-group_reference.webp        340 KB — all 3 loafers, assessable
Shoes/shoes_09_nike-trainers-group_reference.webp  315 KB — both Nikes, assessable
```

The patch fixes the false note and points `photoRef` at the real files, and **deliberately leaves
`noPhoto: true`** on those five, because they still need individual shots. The dry-run output splits
the 12 into "shared group shot" (5 shoes) and "NO IMAGE AT ALL" (6 belts + 1 trouser) so the
distinction is visible. Worth surfacing differently in the UI — a "needs individual shot" badge is
not the same as "no image".

**2. `trousers_09_celio-indigo-jeans` was never tailored.** The 2026-08-20 "all trousers tailored"
batch covered verdict `Tailor` items; this pair is verdict `Keep`, so it was skipped — despite its
own `fit` field reading "~2cm too long". Confirmed from a worn photo. **Check any other `Keep`
trouser carrying a length note for the same trap.**

## On your good_for / bad_for deviation

Your call is better than the spec and it should stay. A join table against the `occasions` lookup
with a foreign key is what makes the "work fit containing a gym-only item" check possible; `text[]`
never could. Fold the extension (`client`, `dinner`, `weekend`, `riding`) back into the shared
vocabulary.

**But `bad_for` doesn't have to stay empty.** You were right not to derive it — a derived negative
invents warnings nobody made. `killer-looks.md` carries **explicit** ones per fit, hand-written:

```
1. The Shawl              bad_for: client, formal
2. Oatmeal & Navy Wool    bad_for: casual, weekend, gym
5. Navy Knit & Stone      bad_for: gym          (+ catch: never over navy bottoms)
7. Sage & Tan             bad_for: client, formal  (+ catch: nothing olive)
```

Import those as stated. Leave `bad_for` empty on the 10 from `work-outfits.md` — those genuinely
have no recorded negatives, and inventing them would be the thing you correctly refused to do.

## Also in `killer-looks.md` that the schema wants

- **`precondition`** on fits 2 and 4 (repair the Fedeli cuff; whiten-wash the Brioni). Actions, not
  warnings — they belong in `fit_preconditions`, not `catch`.
- **`alternate`** slots on fits 1, 3, 4, 5, 7 — marked `_alternate:` with the role they substitute.
- **`catch`** on all 7, distinct from `commentary`.

## Not blocking, but worth knowing

- `trousers_00_decathlon-stone` has a retail render and **no source photograph** — generated from a
  written description, never verified against the garment. Flagged in the patch notes.
- 5 retail renders exist for items that can never appear in a fit (`shoes_01` Replace, `shoes_05`
  Bin, `shoes_06` out, `anko-black-quarterzip-fleece` out, `belts_01` Replace). Harmless.
- 50 retail renders now exist. Any doc saying "only the brogue has been generated" is stale.

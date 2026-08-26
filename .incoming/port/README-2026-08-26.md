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

**Baseline moves from 13 to 11 items without an individual photo, and the catalogue drops from
69 items to 68.** Two separate reasons:
- `trousers_11_black-coated-jeans` was filed 2026-08-25 (13 -> 12).
- `trousers_00_decathlon-stone` is deleted as a phantom (12 -> 11, and 69 -> 68). See below.

New expected counts, enforced by the script:

```
items 68 | noPhoto 11 | Keep 45, Tailor 9, Bin 8, Replace 6 | core 64, out 4
Trousers category: 12 -> 11
```

## The deletion — read this before running --commit

`trousers_00_decathlon-stone` **is not a real garment.** Max physically counted on 2026-08-26 and
confirmed he owns ONE beige/stone Decathlon chino, not two. It was the same pair logged twice.

How it was caught: he re-sent photos of what he thought was the unphotographed pair. They turned out
to be byte-identical to `trousers_01_decathlon-beige_label.jpg` and `_flatlay.jpg`, already on Drive
since 5 August. The label reads **US W33 L33** — but `trousers_01` was recorded as *"US W31 L33"*.
That W31 was a transcription error, and the size was the *only* field distinguishing the two records.

Everything else lines up: same brand, same 98% cotton / 2% elastane, same L33. `trousers_00` never
had a photograph in its life, and its retail render was generated from a written description with no
visual reference. The verdict conflict (`Tailor` "4–5cm too long" vs `Keep` "length correct") is one
garment logged either side of the 2026-08-20 hemming.

The patch deletes it, fixes `trousers_01`'s size, and reports one orphaned file:

```
Retail/trousers_00_decathlon-stone_retail.jpeg   <- park it, don't silently delete
```

**Side benefit for your name-mapping table:** there are now only TWO items called "Decathlon chino"
(`trousers_01` beige, `trousers_03` cobalt), not three. Neither `work-outfits.md` nor
`killer-looks.md` references `trousers_00`, so nothing downstream breaks.

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

## Unlogged categories — not blocking, don't wait for them

Zero items exist in the catalogue for: **t-shirts, dress shirts, shorts, socks, golf apparel,
accessories.** Two consequences worth building for:

- **Both wear events include a plain tee with no id.** Free-text item on the wear event is not an
  edge case, it's the current normal.
- **Golf apparel is deliberately deferred** — Max's call, 2026-08-26. He owns at least one Callaway
  golf polo that isn't logged. Don't model a `golf` split beyond the existing `occasions` value;
  when it lands it's just more rows.

Tees are the one that matters: 9 V-neck knits are unwearable without one, which is why not a single
one of the 17 fits uses a V-neck.

---

# REV 2 — 2026-08-26, after the belt and shoe reshoots

`patch_wardrobe_20260826.py` has been **replaced with a rev-2 superset**. It is idempotent and safe
to run whether or not you already applied rev 1 — already-applied edits are skipped. 49 changes from
a clean original; 0 on a second run. Verified against a 69-item fixture.

## The catalogue is now photo-complete

Every one of the 68 items has both a source photograph and a retail render, except two belts that no
longer physically exist. New reconciliation target:

```
items 68 | noPhoto 2 | Keep 45, Tailor 9, Bin 8, Replace 6 | core 64, out 4
```

## What rev 2 adds

**Four belts photographed and rendered** — `belts_06`, `belts_07`, `belts_09`, `belts_11` all flip to
`noPhoto: false` with real `photoRef` values.

**`belts_11` brand identified.** The underside stamp, recorded as "gone faint / unreadable", reads
**H&M, size M, 85-95, article 304970**.

**Five shoes get individual prefixes.** `shoes_08a/b/c` all shared `shoes_08_loafers-group_reference`
and `shoes_09a/b` shared `shoes_09_nike-trainers-group_reference` — that shared stem is precisely why
none of them ever rendered individually. Each now has its own `photoPrefix` and `retailPrefix` and
its own frames. **This orphans the two group `.webp` files** — park them, don't delete.

**🔴 `shoes_08b` had two record errors**, both corrected:
- It is **not a penny loafer.** The vamp is a single unbroken panel — no strap, no saddle band, no
  keyhole. It's a plain-vamp venetian slip-on moccasin with a hand-stitched apron seam and a small
  raised tab at the throat.
- It is **not tan.** Dark chocolate brown, pebbled. `colour` and `hex` corrected.

The id and `photoPrefix` deliberately keep the `-tan-loafer` stem: the photos are already filed under
it, and ids are never renumbered.

**Two belts marked not located, NOT deleted.** `belts_05` and `belts_10` did not appear when Max
gathered every belt he owns. Both were already `Replace`. Absence is weaker evidence than the proof
that removed `trousers_00`, so they stay in the catalogue with a note. Confirm with Max before
removing them.

## Two observations for Max, not applied

- **`shoes_08c` may be wrongly scoped.** Its `scope='out'` (holiday only) was set from a group photo.
  The individual shots show deep even nap, clean cream stitching, a barely-worn sole. A navy suede
  driving moc is not obviously wrong for a casual office. Left unchanged — his call.
- **`shoes_09b` was shot and rendered without being cleaned.** Grey scuffing on the toe and midsole
  is in both the photo and the render. Honest, but unflattering for a Keep/core shoe.

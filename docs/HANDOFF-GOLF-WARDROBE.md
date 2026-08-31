# The golf wardrobe — built 2026-08-31

Implements `design_handoff_golf_wardrobe` (the global Everyday / Golf switch) in the Flask app.
This records what was built, where it deliberately departs from the handoff, and what is still open.

## The model

One setting, `wardrobe.mode` in `app_settings`, flips the whole app. It is a **mode, not a filter**:
it changes which garments the closet lists, which fits exist, what Today picks from, and the anatomy
of the builder. There is deliberately **no Golf tab and no dress-code checker** — both were rejected
in the handoff, and neither was built.

Membership is derived, never stored as a second flag (`wardrobe/wardrobes.py`):

```
golf      the item carries the `golf` occasion
everyday  the item carries any occasion that is NOT `golf`
```

The sets overlap on purpose. Live counts today: **107 golf · 186 everyday · 56 in both**; filtered to
`verdict = Keep`, the numbers on the switch are **Golf 105 · Everyday 170**.

A **fit** is golf when it carries the `golf` occasion, or — as a safety net for fits saved before any
of the tagging existed — when it contains a garment that is both golf-tagged and crested. A plain
golf polo is not enough on its own: half the golf wardrobe is deliberately wearable off the course,
so treating those as proof would drag everyday fits across.

## Departures from the handoff, and why

1. **Crest comes from `formality_note`, not a regex on names.** The handoff derives crestedness with
   a regex over name + notes + cut and calls it a stopgap. It does not need to be one: migrations
   044–051 already wrote the crest fact per garment, from the photographs, in a regular vocabulary
   ("Royal Sydney - home club", "Brand polo, no club", "another club's crest"). `wardrobes.crest_state()`
   reads that vocabulary and returns **crested · plain · unread · unknown**. It finds 43 crested
   garments against the regex's 39, and — unlike the regex — it will not fire on the next club shirt
   just because the club is in its name.

   The three `unread` polos (`tops_70`, `tops_71`, `tops_80`) carry a mark that was photographed and
   never identified. They are not crested and not plain, and nothing asserts either.

2. **Golf fits save with `register = everyday`, not `casual`.** `casual` is the prototype's
   vocabulary; this database's `registers` table holds `everyday` and `sharp` and nothing else, so
   writing `casual` is a foreign key violation — it failed on the first save. It is also unnecessary:
   register says how dressed-up a fit is, and the `golf` occasion is what makes a fit a golf fit.

3. **The golf occasion is forced on save, and recorded as `manual`.** `fit_derive.good_for()` is an
   intersection, so the moment the knit slot borrows a casual layer the fit loses its golf tag and
   would vanish from the wardrobe it was built in. When the tag has to be forced, `good_for`'s source
   is written as `manual` rather than `derived`: it came from which wardrobe Max was in, not from the
   garments, and an import must not quietly derive it away.

4. **All 107 golf garments have a render.** The handoff lists four without (`tops_69`, `tops_70`,
   `tops_71`, `tops_77`); they were generated after that bundle was cut. The hex-swatch fallback is
   still there and still required — it is what lets a render-less garment appear at all.

5. **The everyday `bottom` slot now offers Shorts as well as Trousers**, per the handoff's slot table.

## What the builder does now

| | Everyday | Golf |
|---|---|---|
| Slots | Outer, Layer, Top, Knit, Bottom, Shoe, Belt | Hat 25 · Polo 50 · Knit or outerwear 16 · Belt 2 · Shorts or trousers 17 · Shoes 11 |
| Optional | Outer, Layer, Knit | Knit or outerwear, Belt |

**No cap on options** — the old `LIMIT 10` equivalent is gone, and it was the single reason the
wardrobe felt invisible. **No render required** — a garment without one falls back to its hex swatch
rather than disappearing. The count note under the switch is computed from the same pools the slots
render, so the note and the slot cannot disagree.

Nothing in Knitwear or Outerwear is golf-tagged, so that slot **borrows** casual layers of
`warmth <= 3` and says so on the slot. Tag the real golf knits and the fallback stops firing by
itself.

The **hat slot saves as role `accessory`** — the fit schema has no hat role. See the open items.

## Empty states

The golf wardrobe has **zero fits**, so these are load-bearing, not an edge case. On both Fits and
Today the surrounding chrome is suppressed entirely — chips, summary line, grid, hero, base strip,
week strip. Rendering them around nothing produced "All 0, Everyday 0, Sharp 0…" above blank space,
which reads as broken rather than as empty. Today distinguishes *no fits in this wardrobe* from
*every fit blocked today*; they are different nothings and need different words.

## Open

1. **`items.crested` as a real column.** `crest_state()` reading `formality_note` is honest and
   accurate today, but it is still prose-parsing. A column set at import, seeded from this function,
   is the end state. Max declined it once (2026-08-31) in favour of exporting the prose — worth
   revisiting now that the app reads it too.
2. **Nothing in Knitwear or Outerwear is tagged golf.** 16 casual layers are borrowed. Which knits
   does Max actually play in?
3. **A `hat` role in the fit schema**, instead of mapping hats onto `accessory`.
4. **Two golf legs are excluded from the builder** by the `Keep`/`Tailor` filter:
   `shorts_08_decathlon-cream-twill` (Replace) and `trousers_17_inesis-navy` (Tailor). Correct
   behaviour — but Max may not know they are sidelined.
5. **The crossover tags on polos `tops_61`–`tops_99` are still wrong.**
   `050_golf_polos_batch_2.sql` sorts after `050_golf_crossover_pass.sql`, so the crossover rule
   never reached those 39 polos and every one still claims `casual` and `weekend`. That is why the
   everyday builder shows 22 crest dots: crested Royal Sydney and Woollahra polos are appearing in
   the everyday wardrobe. Flagged on 2026-08-31 and left for Max to decide; migration 052 would fix it.

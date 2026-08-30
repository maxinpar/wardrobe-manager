# Change pack — 2026-08-30

Addendum to `README.md`. Four changes to the **Fits** and **Closet** screens, all in
`Fits.dc.html` (the single prototype file). Everything else in the handoff still stands —
tokens, copy, the base-plus-top model, Laundry/Log disabled.

Read this as a diff against the original handoff. Where a value here conflicts with
`README.md`, **this document wins**.

---

## 1. Filter bar: grouped into labelled clusters

**Was:** one flat row of 13 pills on the Fits screen. Users couldn't tell which pills were
mutually exclusive, which were toggles, or what any of them would do.

**Now:** five labelled groups, left to right, on one wrapping row.

| Group label | Chips | Behaviour |
|---|---|---|
| REGISTER | All · Everyday · Sharp · Casual | radio — exactly one active, `All` is the default |
| AVAILABILITY | Wearable now · Blocked · Killers | independent toggles; Wearable now and Blocked are mutually exclusive of each other |
| WEATHER | Cold · Mild · Warm | radio-ish — clicking the active one clears it (back to no band filter) |
| OCCASION | Client · Dinner | radio-ish, same clear-on-reclick |
| DISLIKED | Roll-necks hidden / Roll-necks shown | single toggle, label changes with state |

### Markup and style

Group wrapper: `display: flex; flex-direction: column; gap: 8px`. Groups sit in a
`display: flex; align-items: flex-end; gap: 22px; flex-wrap: wrap` row with page padding
`20px 28px 10px`. The Details/Renders segmented control stays right-aligned
(`margin-left: auto`) on the same row.

Group label: IBM Plex Mono, `9.5px`, `letter-spacing: 0.14em`, uppercase, `#A9A08F`.

Chip: `border-radius: 999px; padding: 8px 15px; font-size: 12.5px`, 1px border.
- inactive — `background: transparent`, text `#5C554B`, border `#DCD5C7`
- active — `background: #1A1815`, text `#F4F1EA`, border `#1A1815`

### Counts on every chip (important)

Each chip carries a count to its right: IBM Plex Mono `10px`, `letter-spacing: 0.06em`,
colour `#A9A08F` inactive / `rgba(244,241,234,0.62)` active. Chip content is a
`display: flex; gap: 7px; white-space: nowrap` of label + count.

Counts are computed over the **currently visible fit set** (i.e. respecting the roll-neck
toggle) and are *not* narrowed by the other active filters — they answer "how many fits
would this chip show me", not "how many match everything at once".

- REGISTER counts: total visible; per `register` value
- AVAILABILITY: wearable = fits with no problems *and* no open jobs; blocked = the
  complement; killers = fits flagged killer
- WEATHER: fits whose derived/imported band list includes that band
- OCCASION: fits whose `good_for` includes that occasion
- DISLIKED: `"+1"` — the number of `hidden` fits the toggle would add, always shown with
  the `+` prefix

**Why this matters:** the old roll-neck pill looked broken. Exactly one fit in the data is
`hidden: true` (*The sharp one*), so toggling it appended a single card to the end of a
37-card grid — invisible from the top of the page. The state label plus the `+1` count make
both the state and the effect legible without scrolling. Keep both.

---

## 2. Fits gallery: four cards per row

Both view modes go from 3 to 4 columns.

- Renders mode: `repeat(4, minmax(0, 1fr))`, `gap: 18px` (was 3 cols / 20px)
- Details mode: `repeat(4, minmax(0, 1fr))`, `gap: 16px` (was 3 cols / 16px)

Page padding unchanged (`0 28px 60px`). Card internals unchanged.

This is deliberate and paired with change 3: the grid card is now clearly *smaller* than
the render in the detail view, so opening a fit is a step up in size rather than down.

---

## 3. Fit detail: right-hand drawer → centred modal

**Was:** a fixed 540px `aside` pinned to the right edge. It sat on top of the third grid
column while the grid behind it kept scrolling — a column of fits was silently covered.

**Now:** a centred modal over a dimmed backdrop.

### Shell

- Backdrop: `position: fixed; inset: 0; background: rgba(26,24,21,0.46); z-index: 30`,
  flex-centred, `padding: 26px`. **Clicking the backdrop closes.**
- Panel: `width: min(1200px, 96vw); height: min(900px, 93vh)`, `background: #FFFFFF`,
  `border-radius: 24px`, `overflow: hidden`,
  `box-shadow: 0 34px 90px rgba(26,24,21,0.3)`.
  Click inside must **not** close (stop propagation).
- Panel grid: `grid-template-rows: auto minmax(0, 1fr)` — header, then body.
- Header: the editable fit-name input + mono subhead + round × button,
  `padding: 20px 26px 16px`, `border-bottom: 1px solid #F0EBE0`. Spans the full width.
- Body: `grid-template-columns: minmax(0, 50%) minmax(0, 1fr); min-height: 0`.
  The two columns scroll **independently**.

### Left column — the render, and only the render

The fit render is the star of this screen; it gets half the modal at full panel height.

- Column: `display: flex; flex-direction: column; min-height: 0`,
  `border-right: 1px solid #F0EBE0`, `background: #FCFAF5`.
- Image frame: `flex: 1 1 0; min-height: 0; position: relative; margin: 18px 18px 0`,
  1px `#EEE8DB` border, `border-radius: 16px`, white background. **No fixed aspect
  ratio** — the frame takes the available height and the image is
  `position: absolute; inset: 0; object-fit: contain`, so portrait 5:8 renders show head
  to feet at maximum size.
- Fallback when a fit has no render: the piece photos laid out side by side inside the
  same frame (unchanged logic).
- Caption below the frame: `padding: 10px 20px 16px`, `11.5px`, `#776E60`.
- Nothing else lives in this column.

### Right column — everything else

`overflow-y: auto; padding: 0 2px 44px`, sections keeping their own `24px` horizontal
padding. Order, top to bottom:

1. Problems banner (if any) → catch box → commentary paragraph *(moved here from the left
   column)*
2. The pieces
3. Three numbers, kept apart (your score / worn rating / picker rank)
4. Killer toggle + characterisation field
5. When to wear it
6. Jobs blocking it (conditional)
7. Worn — log entries + "log a wearing" form
8. The rules disclosure

Section styling, copy and controls are all unchanged from the original handoff.

---

## 4. Piece rows are links into the Closet

In the modal's **The pieces** list, each row is now a control, not static text.

- Row gets `cursor: pointer` and a transparent 1px border that becomes `#D9D1C0` on hover,
  with the background going to `#FFFFFF` (from `#F6F3EC` primary / `#FAF8F3` alternate).
- A `→` glyph sits at the row's right end, after the state label: `13px`, `#BEB6A4`.
- Clicking navigates: **close the fit modal, switch to the Closet tab, open that garment's
  detail modal.** In the prototype that's one state change
  (`sel: null, tab: "closet", garmentSel: id`); in Flask this is a link to the garment's
  closet URL, e.g. `/closet?garment=<id>`, so it's back-button friendly.

The reverse link already existed and stays: the garment modal's "in n fits" strip opens a
fit.

---

## 5. Closet garment detail: same modal treatment

The garment drawer had the identical covered-column problem and gets the identical
structure, with two differences from the fit modal:

- Panel: `width: min(1140px, 96vw); height: min(860px, 93vh)`, `z-index: 32` (above the
  fit modal, since a fit can open a garment).
- Body columns: `minmax(0, 46%) minmax(0, 1fr)` — slightly narrower left column, since
  garment photos are 4:5 rather than 5:8.
- Left column is `padding: 18px` all round; the photo frame fills it
  (`flex: 1 1 0; min-height: 0`), background `{{ garment.bg }}` (the swatch colour when
  there's no photo), and the swatch note pill stays bottom-left inside the frame at
  `left: 12px; bottom: 12px`.
- Right column: state segmented control → verdict chips → "in n fits" strip → written
  notes, verbatim → specs table → bin/undo block. Unchanged content.
- Backdrop click closes, same as the fit modal.

---

## Acceptance checks

- [ ] Filter chips render in five labelled groups; every chip shows a count; the roll-neck
      chip reads "hidden"/"shown" and shows `+1`.
- [ ] Register chips are exclusive; availability chips toggle; clicking an active weather
      or occasion chip clears it.
- [ ] Fits gallery is 4 across in both Details and Renders.
- [ ] Opening a fit dims the page and centres a modal; no gallery column is covered.
- [ ] The render in the modal is visibly larger than a gallery card.
- [ ] The modal's two columns scroll independently; the header does not scroll.
- [ ] Backdrop click and × both close; clicking inside the panel does not.
- [ ] Clicking a piece row lands on that garment in the Closet with its modal open.
- [ ] Closet garment detail is a modal, photo on the left at full height.

## Not changed

Today screen, the week strip, the closet grid and filters, the fit builder drawer (still a
right-hand `aside` — it's a form, not a browse-and-compare surface), all tokens, all copy
outside the strings quoted above, Laundry and Log still disabled.

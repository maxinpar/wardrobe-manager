# Handoff: golf fits — two looks, collapsible categories, recategorising, garment render upload

## Overview

Four pieces of work on the `/fits` and `/closet` surfaces of the Wardrobe Manager
(`maxinpar/wardrobe-manager`, branch `main`, synced at commit `3245fb56` + the
`export_fits.py` commit on 2026-09-02):

1. **Two looks per fit.** A fit with an optional layer (quarter-zip, long-sleeve,
   vest) has two renders — without the layer and with it. One switch flips between
   them, on the card and in the fit pane, sharing a single state.
2. **Collapsible category sections** in the fits grid, wherever fits carry a
   `category`. Golf sections come from the nine authored golf categories; everyday
   sections from `smart / casual / warm / cold / formal`; anything without a
   category falls into a trailing "Not in a category yet" section.
3. **Recategorising a golf fit** from the fit pane — a ten-chip picker (nine golf
   categories + None), with the user's choice marked as theirs and persisted.
4. **Uploading a render for a closet garment** — file picker or drag-and-drop on
   the garment panel, with the upload replacing the catalogue render everywhere the
   garment is drawn.

Everything reads from the app's own exports: `data/fits.json` (via
`scripts/export_fits.py`) and `data/wardrobe.json`. No design-side data invention.

## About the design files

The files in this bundle are **design references created in HTML** — a working
prototype showing intended look and behaviour, not production code to copy. The
task is to **recreate these designs in the app's existing environment**: Flask +
Jinja templates (`wardrobe/templates/`) and `wardrobe/static/app.css`, using the
patterns already there (`_fit_macros.html`, `_fit_modal.html`, `_renders.html`,
`fits.html`, `catalogue.html`, `item.html`).

Note the prototype is a single-file design component with inline styles and
browser-local state. In the real app several of these behaviours should be
**server-side and persisted in Postgres**, not in `localStorage` — see
"State & persistence" below for which is which.

## Fidelity

**High fidelity.** Final colours, type, spacing and interaction. Recreate closely,
but express it through `app.css` rather than transplanting inline styles.

## What already exists server-side

Relevant work that is already committed and does **not** need rebuilding:

- `migrations/063_fits_golf_batch_1.sql` — the 12 golf fits, the nine
  `fit_categories` rows, slots, occasions, temp bands, seasons, one precondition.
- `migrations/064_fit_layered_render.sql` — `fits.layered_image_path` and
  `fits.layered_thumb_path`, with `hero_image_path` deliberately the WITHOUT-layer
  render.
- `wardrobe/wardrobes.py` — the everyday/golf derivation and the two builder
  anatomies.
- `wardrobe/fits_json.py` + `scripts/export_fits.py` — the export this design reads.
- `fit.has_two_looks` and the `pill-looks` "2 looks" pill in `_fit_macros.html`
  and `_renders.html` — **superseded by this design** (see below).

## Screens / views

### 1. Fits grid (`/fits`, list view) — `templates/fits.html`

**Purpose.** Browse every fit in the current wardrobe.

**Layout.** A 4-column CSS grid, `gap: 16px`, page padding `0 28px 60px`. Each
card is a grid cell. Section headers are grid items spanning the full row
(`grid-column: 1 / -1`).

**Card.** `background #FFFFFF`, `border-radius 20px`, `padding 14px`, a
transparent-white 1px border that becomes `#E0BE84` on hover, contents in a
column flex with `gap: 12px`:

- **Image**, `aspect-ratio 5 / 8`, `border-radius 13px`, `border 1px solid #EEE8DB`,
  `object-fit: cover`, `loading="lazy"`. On image error, fall back to a strip of
  the fit's garment renders (`object-fit: contain`, up to 5).
- **Layer switch** (only when the fit has two looks) — absolutely positioned
  `left 8px / bottom 8px`. A single `<button>`: `background rgba(26,24,21,0.86)`
  (hover `0.96`), `border-radius 999px`, `padding 5px 10px`, `display:flex`,
  `gap 8px`. Inside: the label `Layer off` / `Layer on` in IBM Plex Mono 8.5px,
  `letter-spacing 0.12em`, uppercase, `#EFE7D6`; then a track `22×12px`,
  `border-radius 999px`, background `rgba(239,231,214,0.32)` when off and
  `#E0BE84` when on, holding a `10×10px` white knob at `left: 1px` / `left: 11px`,
  `transition: left 120ms ease`.
  **One click toggles.** It must not be two buttons — the user explicitly rejected
  a segmented control, because the target moves and going back means chasing it.
  The click must `stopPropagation` so it does not open the fit.
- **"Your photo" badge** — same position and pill styling as the switch, text
  `Your photo`, shown only when the hero is a user upload. There is **no**
  "Generated · never worn" badge on cards any more (see "Provenance" below).
- **State badge** — `right 8px / top 8px`, mono 8.5px uppercase,
  `padding 4px 8px`, `border-radius 6px`. Wearable: `rgba(255,255,255,0.92)` on
  `#5C554B`. Blocked: `rgba(140,59,34,0.9)` on `#FBF0EC`. Copy:
  `wearable now` / `blocked on a job` / `not wearable`.
- **Name** 17px/600, `letter-spacing -0.02em`; **score** on the same baseline,
  mono 9.5px uppercase `#776E60`.
- **Badges row**, `flex-wrap`, `gap 5px`, each `border-radius 6px`,
  `padding 4px 8px`, mono 9px uppercase. The first badge is the fit's **category
  label**, falling back to its setting/register.
- **Meta line** 12.5px `#7D7565`: bands · formality · good-for.
- **Catch** (if any): `background #FBF3E4`, `border-radius 10px`,
  `padding 10px 11px`, a mono `CATCH` label `#A07A2C` beside 12.5px `#5C4A22`.
- **Job** (if any): a top border `#F0EBE0`, a "Mark done" pill, and the job text.
- **Actions**: gold `Log worn` (`#E0BE84` on `#241C0C`, hover `#EFD3A2`) and an
  outlined `Open`.

**Section header** (a full-row grid item). A `<button>`, transparent, with
`border-bottom: 1px solid #E4DED0` (`#EFE9DD` when the section is collapsed,
`#E0BE84` on hover), `padding 16px 2px 10px`, `margin-top 8px`, contents baseline-
aligned with `gap 12px`:

- a mono 13px `–` / `+` mark in a 12px-wide box (`–` open, `+` collapsed),
- the category label at 17px/600 — **with the leading `Golf · ` stripped**, since
  the wardrobe toggle already says Golf,
- the fit count, mono 9.5px uppercase `#A9A08F`, e.g. `4 fits` / `1 fit`.

Clicking anywhere on the header collapses or expands the section. A collapsed
section renders no cards.

**Sectioning rules** (important):

- Group by category. Sections appear in **authored order** (the nine golf
  categories in Max's order, then Smart, Casual, Warm weather, Cold weather,
  Formal) — *not* first-seen order, so a fit moved between categories lands where
  that category belongs.
- Fits with no category go to a trailing section labelled
  **"Not in a category yet"**. They are never hidden — this was a real bug the
  user caught.
- If *no* fit in the current wardrobe has a category, render the old flat grid
  with no headers at all.
- Empty categories are not rendered (the six unused golf categories do not appear
  in the grid, but they are all offered in the picker).

**Golf sections today.** I want to be SEEN 4 · Is he a pro? 4 · Old school 4 ·
Not in a category yet 8.

### 2. Fit pane (`templates/_fit_modal.html`)

Two columns, `minmax(0, 50%) minmax(0, 1fr)`, inside a `min(1140px, 96vw)` ×
`min(860px, 93vh)` sheet, `border-radius 24px`.

**Left column** — the hero, `flex: 1 1 0`, `margin 18px 18px 0`,
`border-radius 16px`, `object-fit: contain`, still accepting a dropped image to
set the fit's render.

**Layer row** (only for two-look fits), directly under the hero,
`padding 12px 20px 0`, `align-items: center`, `gap 10px`, and — this matters —
**`min-height: 58px`**, with the note beside it at **`min-height: 32px`**:

- The switch: a white pill, `border 1px solid #E2DCCE` (hover `#1A1815`),
  `border-radius 999px`, `padding 8px 14px`, label `Layer off` / `Layer on` at
  12.5px/500, then a `32×18px` track (`#DCD5C7` off, `#E0BE84` on) with a
  `14×14px` white knob at `left 2px` / `left 17px`, `transition: left 130ms ease`.
- The note, 11.5px `#776E60`: `Without the <layer garment name> — it comes off at
  the range.` / `With the <layer garment name> on.`

**Why the fixed heights:** the two notes are different lengths, so the row grew
and shrank between states and visibly resized the hero above it. The row now
reserves its space and the copy is kept short enough to wrap the same either way.
The hero box must be **pixel-identical** in both states — verify it.

**Hero caption**, `padding 10px 20px 6px`, 11.5px `#776E60`, in priority order:

1. upload made in this session → `Your uploaded render.`
2. an `images.upload` from the export → `Your own picture, uploaded in the app.`
3. a generated render → `Generated illustration — not a photo of this fit being worn.`
4. nothing → `The pieces, as shot. No render of the whole fit yet.`

**Category block** (golf wardrobe only), below the commentary in the right column:
`border 1px solid #EFE9DD`, `border-radius 16px`, `padding 14px 15px`, white.

- Header row: mono 9px `letter-spacing 0.16em` uppercase `#776E60` reading
  `Category`; the current label at 13px/500 (`not in a category yet` when unset);
  and, when the value is the user's own override, a badge `moved here · yours` —
  mono 8.5px uppercase `#8A6320` on `#FBF3E4`, `border-radius 5px`,
  `padding 3px 7px`.
- Chip row, `flex-wrap`, `gap 6px`, `margin-top 12px`. Ten chips:
  `I want to be SEEN`, `Is he a pro?`, `Old school`, `Modern`, `Winter golf`,
  `Club day`, `Away day`, `The 19th`, `Wet & windy`, `None`. Selected chip is
  `#1A1815` on `#F4F1EA` with a matching border; unselected is transparent,
  `#5C554B`, `border 1px solid #DCD5C7`, hover border `#1A1815`.
  `border-radius 999px`, `padding 7px 13px`, 12px.
- One click moves the fit and the grid re-sections immediately.

**Server-side note.** In the app this should write `fits.category_code` (values
are the `fit_categories.code` rows migration 063 already inserts) and record
provenance in `fit_field_sources` as `manual` — which is exactly what migration
063 does for the authored ones. The "moved here · yours" badge should then be
driven by that provenance row, not by a client-side diff.

### 3. Garment panel (`templates/item.html`) — render upload

Left column of the garment sheet, `padding 18px`, image pane `flex: 1 1 0`,
`border-radius 16px`, border `1px solid #EEE8DB` — **`#E0BE84` while a file is
dragged over it**. The whole pane is a drop target (`dragover` / `dragleave` /
`drop`). While dragging: an overlay `rgba(250,247,240,0.92)` centred with mono
10.5px uppercase `#8A6A1E` reading `Drop to set this render`.

Corner badge at `left 12px / bottom 12px`, mono 9px uppercase,
`background rgba(26,24,21,0.78)`, `#F4F1EA`, `padding 6px 10px`,
`border-radius 7px`:

- `Your render` when the garment shows an uploaded render;
- otherwise the existing swatch note (`Render pending — colour field stands in`,
  or `No photo anywhere — colour field stands in` when `noPhoto`).

Control row below the pane, `padding 14px 2px 0`, `gap 12px`, wrapping:

- A pill button `border 1px solid #DCD5C7` on white, `padding 8px 15px`, 12px
  `#3E382F`, hover border `#1A1815`. Label: `Upload a render` when the garment has
  no render at all, `Upload your own render` when it has a catalogue one,
  `Replace this render` when an upload is already in place.
- `Back to the catalogue one` — an underlined text button `#9A9184` — shown only
  when an upload exists.
- A mono 9.5px uppercase `#A8A093` hint reading
  `no render yet — or drop an image on the panel`, shown only when there is no
  render.
- A hidden `<input type="file" accept="image/*">`.

**The upload replaces the catalogue render everywhere that garment is drawn** —
closet tiles, fit piece strips, Today's pieces, the builder's tiles. It resolves
ahead of `photos-manifest`, so filling in one of the 61 renderless garments
improves every screen at once. In the app this belongs in the existing photo
store / `scripts/import_photos.py` path with a per-item upload, not in the
browser.

## Interactions & behaviour

- **Layer switch** — single click flips the hero between `heroThumb` and
  `layeredThumb`. State is keyed by fit id and **shared between the card and the
  pane**: flip it on a card, open the fit, it opens flipped. In the prototype this
  is session state; persisting it is optional and low value.
- **Section collapse** — click the header. Keyed by category label.
- **Category chip** — one click, no confirm, no save button.
- **Render upload** — file picker or drop. The image is downscaled before storage:
  **1000px** longest edge for a fit render, **700px** for a garment render, JPEG
  quality 0.84.
- **Wardrobe toggle** (existing) — switching clears the builder draft and any open
  selection, and re-derives the grid, the closet, Today and the builder anatomy.
- No animations beyond the two knob transitions and existing hover borders.

## State & persistence

Prototype state, and where each belongs in the real app:

| State | Prototype | Real app |
| --- | --- | --- |
| `layerOn[fitId]` | component state | client-side is fine (view state) |
| `catClosed[categoryLabel]` | component state | client-side (view state) |
| `fitCat[fitId]` | `localStorage: wardrobe.fitCategory` | **Postgres** — `fits.category_code` + `fit_field_sources` |
| `itemUploads[itemId]` | `localStorage: wardrobe.itemRenders` (downscaled data URLs) | **photo store** — a per-item uploaded render, like `fits.render_upload_path` (migration 016) |
| `uploads[fitId]` | `localStorage: wardrobe.fitRenders` | already exists as `fits.render_upload_path` |

Storage keys are read on mount and written on every change; a quota failure
degrades to session-only rather than throwing.

## Provenance rules (keep these)

- A generated render is **never** presented as a photograph of the clothes being
  worn. The fit pane says so in words.
- The card-level `Generated · never worn` badge was **removed on purpose**: with
  every golf render carrying identical provenance it was noise twelve times over.
  The rule is now inverted — silence means generated, and a card is badged only
  when the image is the user's own upload. Keep the sentence in the pane.
- An `images.upload` **outranks** a render and carries **no** provenance label:
  the export does not record whether the user's picture is a photograph or a
  render of their own, so the design must not assert either.
- The base (no-layer) render stays the hero for two-look fits. The batch rule is
  that the fit must stand up without the layer.
- Score, killer and style stay the user's: the design never writes them.

## Data contract

`data/fits.json` — 90 fits, 89 live, 20 golf, 12 two-look, 10 with uploads.
Per fit, the fields this design uses:

- `id`, `code`, `name`, `source`, `commentary`, `catch`, `style`
- `wardrobe` — `everyday` | `golf`. **Authoritative.** The design no longer runs
  its own crest regex; the export derives membership the same way `/fits` does
  (the golf occasion, or a crested club garment).
- `category` — `golf_seen` | `golf_pro` | `golf_oldschool` | `golf_modern` |
  `golf_winter` | `golf_club` | `golf_away` | `golf_19th` | `golf_wet` |
  `smart` | `casual` | `warm` | `cold` | `formal` | `null`
- `temp` (bands), `rainSafe`, `formalityRank`, `goodFor`, `badFor`
- `items[]` — `{ role, position, itemId, isAlternate?, note? }`; roles are
  `outer, layer, top, base, bottom, shoe, belt, accessory`
- `preconditions[]` — `{ text, itemId, done }` → the card's job row
- `hiddenByDefault`, `gone`, `vetted`, `score`, `sortOrder`
- `images` — `{ display, hero, heroThumb, heroIsGenerated, layered, layeredThumb,
  upload, looks }`. `looks === 2` means a base/layered pair should be offered as a
  pair; `display` is what a screen should draw by default.

**The optional layer** is the item row whose `note` starts with `optional` (falling
back to the `layer` row, then `outer`). Its garment name is what the layer note
names, so the copy is data-driven rather than hardcoded.

## Design tokens

Colours
- paper `#F4F1EA` · card `#FFFFFF` · panel `#FCFAF5` · sunken `#F6F3EC`
- ink `#1A1815` · body `#3E382F` · secondary `#5C554B` · muted `#6E6659` /
  `#776E60` · faint `#A9A08F` / `#A8A093`
- rules `#E4DED0` · card lines `#EFE9DD` / `#EEE8DB` / `#F0EBE0` · chip line `#DCD5C7`
- gold `#E0BE84`, gold hover `#EFD3A2`, gold ink `#241C0C`, gold deep `#8A6320`
- caution `#FBF3E4` bg / `#A07A2C` label / `#5C4A22` text
- alarm `#FBF0EC` bg / `#8C3B22` text · blocked pill `rgba(140,59,34,0.9)`
- overlays `rgba(26,24,21,0.86)` (badges) · `rgba(26,24,21,0.46)` (scrim) ·
  `rgba(250,247,240,0.92)` (drop)

Type
- Space Grotesk 400/500/600/700 — 46px hero, 25px empty-state, 17–18px card
  titles, 15.5px lede, 13.5px body, 12.5px controls, 11.5px captions
- IBM Plex Mono 400/500 — 8–10.5px, `letter-spacing 0.1–0.18em`, uppercase, for
  labels, counts, states and ids

Radius `999px` pills · `24px` sheets · `20px` cards · `16px` panels ·
`13px` card image · `10px` catch · `6px` badges
Spacing 2 / 4 / 6 / 8 / 10 / 12 / 14 / 16 / 18 / 20 / 24 / 28 / 34 px
Motion `left 120–130ms ease` on the switch knobs only

## Assets

- `photos/fits/thumbs/` — 92 fit render thumbnails (500px-ish JPEG), including
  `<fit_id>_layered_render.jpg` for the 12 two-look fits.
- `photos/fits/uploads/` — 11 pictures the user uploaded in the app.
- `photos/Retail/` — 235 garment renders (500×500 q82).
- All of these come from the repo, unchanged. Full-size fit renders
  (`photos/fits/*.jpeg`, 1.6–1.9 MB each) were deliberately **not** pulled into
  the prototype; the thumbs are what a grid should load.

## Known gaps

- 13 garments used by the 12 authored golf fits have **no** render yet — the seven
  golf knits/zips, the Peter Millar reversible vest, the white ratchet belt, both
  Puma belts, the Inesis strawberry trouser, the Glenmuir cream mercerised polo.
  They fall back to colour swatches in the piece strips. The new garment upload is
  the way to close this.
- Six of the nine golf categories have no fits.
- Eight of the user's own golf fits have no category.

## Files

- `Fits.dc.html` — the whole design: Today, Fits (list + gallery), Closet,
  Hospital, Gaps, the fit pane, the garment panel and the builder.
- `fits-export.js` — `window.FITS_ALL`, generated from `data/fits.json`.
- `data/fits.json` — the source export, for reference.
- `wardrobe-data.js` — `window.WARDROBE`, 297 garments from `data/wardrobe.json`.
- `photos-manifest.js` — `window.PHOTOS`, garment renders by id.
- `fits-data.js` — legacy fits **plus** `window.WEAR_EVENTS` and
  `window.STYLING_RULES`, which are still used.
- `fits-batch2.js` — legacy fits plus `window.WORN_PHOTO`.
- `hospital-gaps-data.js` — `window.HOSPITAL`, `window.GAPS` (gaps are
  placeholder data; the shape is final).
- `support.js` — the prototype runtime. Not part of the design; do not port.

Open `Fits.dc.html` in a browser to see the design running. Image paths are
relative, so the `photos/` folders must sit alongside it.

# Handoff: Fits (gallery, detail, builder)

## Overview

A redesign of the Fits area of `maxinpar/wardrobe-manager` (branch `main`, synced 2026-08-26).
Three views: a **fits gallery**, a **fit detail drawer**, and a **build-a-fit drawer**. It replaces
the current Jinja templates `wardrobe/templates/fits.html` and `wardrobe/templates/fit.html`,
and adds a builder that has no current equivalent.

Also bundled: the earlier catalogue/today design (`Wardrobe.dc.html`) and the three explored
visual directions (`Wardrobe Directions.dc.html`) for context. **`Fits.dc.html` is the approved
direction.** Match it.

## About the design files

The `.dc.html` files are **design references written as HTML prototypes** — they show intended
look and behaviour. They are not production code and should not be shipped or copied wholesale.
The task is to **recreate these designs inside the existing Flask + Jinja + `app.css` codebase**,
using its established patterns (server-rendered templates, POST-form actions, `url_for('photo', …)`
for renders). Where a view needs client-side state that Jinja can't express (the builder's live
derived metadata), add the smallest possible progressive-enhancement script rather than
introducing a SPA framework.

The prototypes use a small runtime (`support.js`) so they render standalone in a browser; it is
irrelevant to the implementation. Ignore it.

## Fidelity

**High-fidelity.** Colours, type, spacing, radii and copy are final. Recreate pixel-for-pixel
using `app.css` (extend it; don't add a second styling system). The one thing deliberately left
open is responsive behaviour below ~1200px — see *Responsive*.

---

## Design tokens

Colours

| Token | Hex | Use |
| --- | --- | --- |
| Page | `#F4F1EA` | app background |
| Surface | `#FFFFFF` | cards, drawers, photo grounds |
| Surface muted | `#FAF8F3` | builder summary panel, alternate rows |
| Row | `#F6F3EC` | primary piece rows in detail |
| Ink | `#1A1815` | primary text, active chips, primary button |
| Ink hover | `#3B352C` | primary button hover |
| Body | `#3E382F` | commentary prose |
| Secondary | `#5C554B` | chip text, secondary labels |
| Muted | `#7D7565` | card meta text |
| Faint | `#A9A192` | mono labels, placeholders, "unscored" |
| Line | `#E4DED0` | header/drawer borders |
| Line light | `#EFE9DD` / `#F2EDE3` / `#EEE8DB` | card inner borders, table dividers |
| Chip fill | `#EAE5DA` / `#F1ECE1` | weather chips, badges |
| Brass | `#E0BE84` | accent fill: logo mark, primary "Log worn", save |
| Brass hover | `#EFD3A2` | |
| Brass text | `#8A6320` | links, accent text on light |
| Brass deep | `#241C0C` | text on brass fill |
| Catch bg / text | `#FBF3E4` / `#5C4A22`, label `#A07A2C` | the fit's catch block |
| Problem bg / text | `#FBF0EC` / `#8C3B22` | not-wearable states |

Type — `Space Grotesk` (400/500/600/700) for UI, `IBM Plex Mono` (400/500) for labels and numbers.
Mono labels are uppercase with `letter-spacing: 0.1–0.18em` at 8.5–10.5px. Body sizes: 11.5, 12,
12.5, 13, 13.5px. Headings: card title 17px/600/`-0.02em`; drawer title 24px/600/`-0.03em`.

Radii — pill `999px`; card `20px`; drawer panels `14–16px`; photo ground `12–13px`; thumbs `8px`;
badges `5–6px`. No shadows anywhere. Borders do the work.

Spacing — page padding `28px`; card padding `14px`, internal gap `12px`; grid gap `16px`;
drawer padding `24px`; section gap `22–24px`.

---

## Screens

### 1. Fits gallery

**Purpose** — browse the 18 hand-reasoned fits, see at a glance which are wearable today, and
act (log worn, clear a blocking job) without opening anything.

**Layout** — full-width column:

1. **Header** (`padding: 18px 28px`, `border-bottom: 1px solid #E4DED0`): brass 26px rounded
   square + "Wardrobe" (15px/700/`-0.02em`); pill nav `Today · Fits · Closet · Laundry · Log`
   (13px, active = ink fill, white text, 500); right side two read-only chips (`16°C · mild`,
   `Dry`) and a `Build a fit` ink pill button.
2. **Filter row** (`padding: 22px 28px 10px`, flex wrap, gap 10): pill buttons, 12.5px,
   `padding: 8px 15px`, `1px` border. Inactive: border `#DCD5C7`, text `#5C554B`, transparent
   fill. Active: ink fill + border, `#F4F1EA` text. Order: `All`, `Everyday`, `Sharp`,
   `Killer only`, `Wearable now`, `Blocked`, `Cold`, `Mild`, `Warm`, `Good for client`,
   `Good for dinner`, `Show roll-neck`. Register chips are mutually exclusive; `Wearable now`
   and `Blocked` clear each other; band and occasion chips toggle off on re-click.
3. **Count line** — mono 10.5px uppercase `#8A8272`:
   `18 fits · 14 wearable now · 4 blocked · showing 18`.
4. **Card grid** — `grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px`.

**Fit card** — white, `border-radius: 20px`, `padding: 14px`, `1px` transparent border that turns
brass on hover; flex column, `gap: 12px`; whole card is clickable (opens detail).

- **Photo ground** — 208px tall, white, `1px solid #EEE8DB`, radius 13px, `overflow: hidden`.
  - If the fit has a generated full-look render: `object-fit: cover`, plus a bottom-left pill
    (mono 8.5px, `rgba(26,24,21,0.86)` on `#EFE7D6`) reading **"Generated · never worn"**. This
    label is non-negotiable — `fits.hero_is_generated` means it must never imply a wearing.
  - Otherwise: the fit's primary garment renders laid side by side, `flex: 1 1 0`,
    `object-fit: contain`, `padding: 12px`, `gap: 2px`. **Skip any garment with no render** —
    do not emit an empty slot (19 of 69 garments are unshot).
  - Top-right status pill (mono 8.5px, radius 6px): `wearable now` on `rgba(255,255,255,0.92)` /
    `#5C554B`; `blocked on a job` or `not wearable` on `rgba(140,59,34,0.9)` / `#FBF0EC`.
- **Title row** — name (17px/600) left, score right (mono 9.5px uppercase `#A9A192`):
  `7/10` or `unscored`.
- **Badges** — mono 9px uppercase, radius 6px, `padding: 4px 8px`: `killer` (ink fill, brass
  text) when set; `hidden by default`; register (`everyday`/`sharp`); `dry days only` when not
  rain-safe (`#F5EEE4`/`#8A6320`); `authored` for the killer-looks fits.
- **Meta** — 12.5px `#7D7565`: bands · `formality n/5` · `good for work, client`.
- **Catch block** — only when the fit has one: `#FBF3E4`, radius 10px, `padding: 10px 11px`,
  mono `CATCH` label in `#A07A2C` beside the text in `#5C4A22`.
- **Job row** — only when a precondition is open: `Mark done` outline pill + the job text.
  Clicking must not open the detail (`stopPropagation`).
- **Footer** — two buttons, equal width: `Log worn` (brass fill, 600) — becomes `Worn 2×` once
  logged — and `Open` (outline).

### 2. Fit detail drawer

Fixed right panel, **540px**, white, `border-left: 1px solid #E4DED0`, own scroll, above the
grid. Order matters — it goes from *what is it* to *what do I do with it* to *provenance*:

1. **Header** — the name as an inline editable input (24px/600/`-0.03em`, transparent border,
   brass border on focus — renaming is expected, so no separate edit mode). Below: mono subhead
   `register · formality n/5 · rain-safe · work-outfits.md 2026-08-24`. Round `×` close at right.
2. **Hero** — 300px, `1px solid #EEE8DB`, radius 14px. Generated render `cover`, else the
   primary pieces `contain` in a row. Caption below in 11.5px `#A9A192`:
   "Generated illustration — not a photo of this fit being worn." or
   "The pieces, as shot. No render of the whole fit yet."
3. **Problems** — when blocked: `#FBF0EC` block, 12.5px `#8C3B22`,
   "Not wearable right now — Grey piqué polo is in the wash."
4. **Catch** — same treatment as the card, one step larger (13px).
5. **Commentary** — 13.5px/1.6 `#3E382F`, `text-wrap: pretty`. Verbatim from the data. This prose
   is the point of a fit; never truncate it here.
6. **The pieces** — one row per `fit_items` row, sorted by role
   (`outer, layer, top, base, bottom, shoe, belt, accessory`): 42×50 thumb (white ground, or the
   garment's `hex` when unshot), mono role label (`TOP`, or `TOP · ALTERNATE`), name, optional
   note (`"clean the coating first"`), and the laundry state right-aligned — `clean` in `#A9A192`,
   anything else in `#8C3B22`. Alternates sit on `#FAF8F3`, primaries on `#F6F3EC`.
7. **"Three numbers, kept apart"** — a bordered 14px-radius group, one row each, in this order:
   - **Your score** — number input 1–10, hint "Yours — nothing in the app ever writes this".
   - **Worn rating** — `7.5/10 over 2` or `never worn and rated yet`, hint "How the wearings went
     — never merged into your score".
   - **Picker rank** — value `not stored`, hint "Computed per day on Today; never stored".
   Then a row with the **killer toggle** (`Mark as killer` outline → `Killer ✓` ink+brass) and the
   **style field** (pill input) with a mono tag beside it: `draft` (`#A9A192`) until edited, then
   `yours` (`#8A6320`).
8. **When to wear it** — 5 rows, `108px 1fr auto` grid: `Temperature` (band labels
   "Cold (under 14°)" etc.), `Rain`, `Season`, `Good for`, `Bad for`. Each row carries a
   provenance tag: `imported`, `derived`, `browsing only` (season), or `—` when nothing was
   authored. Season's value copy must keep the "browsing label only" meaning — the picker never
   reads it.
9. **Jobs blocking it** — `Mark done` / `Reopen` per precondition; done text goes `#A9A192`.
10. **Worn** — history entries (date, rating in brass mono, context, note), then a
    **Log a wearing** panel: 10 rating buttons (32px wide, mono, ink fill when picked), a note
    input, and an ink `Log it · 8/10` button. Empty state: "Never logged. The log holds two ad-hoc
    fits that were never saved as one."
11. **Rules** — full-width outline toggle → numbered list of `STYLING_RULES` with the caveat
    "Reference only — not enforced in v1. The fits were hand-checked."

### 3. Build a fit drawer

Fixed right panel, **680px**, same chrome. New capability; mirrors `wardrobe/fit_derive.py`.

1. Title `Build a fit`, mono subhead "Pick a piece per role · metadata derives as you go".
2. **Summary panel** (`#FAF8F3`, radius 16, `1px solid #EFE9DD`): name input + brass `Save fit`;
   below, a 4-cell strip (white cells, 1px gutters) showing **Temperature / Rain / Formality /
   Season** derived live from the current picks, `—` until enough is chosen; footnote:
   "Everything above is a first guess, recorded as derived. Your edits win and are never
   overwritten by an import."
3. **Role rows** — `Outer · optional`, `Layer · optional`, `Top`, `Bottom`, `Shoe`, `Belt`. Each:
   mono role label left, chosen garment name right (`nothing picked` when empty), then a
   horizontally scrolling strip of 96px candidate cards (78px render, 10.5px name, radius 12).
   Selected: brass border + `#FAF6EC` fill. Re-clicking clears the slot.
4. `Save fit` requires ≥3 picks, then the fit appears in the gallery and its detail opens.

---

## Interactions & behaviour

- Filters are pure client/query-side; they never mutate a fit.
- Card click → detail. `Mark done` and `Log worn` inside a card must stop propagation.
- Rename, score, style, killer and job-done are optimistic writes; in the Flask app they map to
  the existing POST routes (`fit_score`, `fit_killer`, `fit_style`, `precondition_done`) — add a
  `fit_rename` route for the name.
- Logging a wearing writes a `wear_events` row for `fit_id` with today's date, the rating and the
  note; the drawer's Worn list and the card's `Worn n×` label reflect it immediately.
- Hover: cards get a brass border; outline buttons darken border and text to ink; brass buttons go
  `#EFD3A2`; ink buttons go `#3B352C`. No transforms, no shadows, no motion beyond colour.
- Focus: inputs take a brass border, `outline: none`.
- No loading skeletons are designed — the Flask app renders server-side. If you fetch the builder
  candidates asynchronously, hold the strip at its height rather than collapsing it.

## State

Gallery: `register`, `killerOnly`, `wearableOnly`, `blockedOnly`, `band`, `occasion`,
`showHidden`. Detail: `selectedFitId`, `showRules`, `logRating`, `logNote`. Builder: `draft`
(role → item id), `draftName`. Persisted server-side: score, killer, style, name, job done,
wear events, laundry state.

## Derivation rules (must match `wardrobe/fit_derive.py`)

- **Bands** — 2+ layer-role pieces (`top|layer|outer|base`) → `cold`; single layer with
  `warmth ≥ 4` → `cold`; single `Tops` piece with `warmth ≤ 3` → `warm`; else `mild`. Then always
  add `mild`.
- **Rain-safe** — false if any primary piece is suede, nubuck or mesh.
- **Formality** — mean of the pieces' 1–5 ranks, rounded, clamped. Items in this dataset carry
  formality as prose, so the prototype maps `formal|business → 4`, `smart → 3`, `casual → 2`,
  else 3 **and labels the result "derived"**. If the real items table gains a rank column, use it.
- **Season** — `cold → winter`, `mild → autumn, spring`, `warm → summer`. Browsing label only.
- **Never derive** `score`, `killer`, `style`, `bad_for`. The design has no affordance that
  writes them from data.
- **Authored fits** (`killer-looks.md`, `authored: true` in the data file) keep their bands, rain,
  formality and good/bad-for exactly as written — badge them `imported`, never re-derive.

## Assets

- Garment renders: `photos/Retail/<item_id>_retail.{png,jpeg}`, mapped in `photos-manifest.js`
  (50 of 69 present). All shot on white — which is why every photo ground in this design is pure
  white; any tinted ground shows the render's box.
- Full-look renders: `photos/Looks/<slug>_look.jpeg`. Only
  `leather-jacket-dressed-down_look.jpeg` exists; it is AI-generated, hence the
  "Generated · never worn" flag.
- Fonts: Space Grotesk + IBM Plex Mono (Google Fonts).
- No icons. The only glyphs are `×` and `⚠`-free text labels.

## Responsive

Designed at 1440px. Below ~1200px the grid should go 2-up, then 1-up under ~820px; the drawers
should become full-width sheets. Not specified further — treat as implementer's judgement.

## Files in this bundle

| File | What it is |
| --- | --- |
| `Fits.dc.html` | **The approved design.** Gallery + detail + builder. |
| `fits-data.js` | All 18 fits lifted from `wardrobe/seed_data.py`, plus the wear log and styling rules. Reference for copy; the app reads the DB. |
| `wardrobe-data.js` | The 69 garments, exported from `data/wardrobe.json`. |
| `photos-manifest.js` | item id → render filename, and the one full-look render. |
| `Wardrobe.dc.html` | Earlier catalogue + today's-pick design (different, older visual direction). |
| `Wardrobe Directions.dc.html` | The three explored directions. Context only. |
| `support.js` | Prototype runtime. Ignore. |

Renders are **not** included in the zip — they already live in the repo's photo directory.

## Repo touchpoints

| Design | Repo |
| --- | --- |
| Gallery | `wardrobe/templates/fits.html`, `wardrobe/app.py` (`fits_view`) |
| Detail drawer | `wardrobe/templates/fit.html`, `migrations/003_fits.sql` |
| Builder | new; derivation from `wardrobe/fit_derive.py` |
| Styling | `wardrobe/static/app.css` |

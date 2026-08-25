# Brief for Claude Code — port the wardrobe catalogue to Postgres and build a local web app

You are picking up a project that has lived until now as JSON + markdown docs inside a Claude
Project, plus a 17 MB self-contained HTML file with photos base64'd into it. That has hit its
limit. Your job is to move the catalogue into Postgres and put a small, fast web front-end on
top of it, running locally, and to make the database the single source of truth from then on.

Everything you need is in this folder. Read all of it before writing code.

```
PROMPT.md                     ← this file
data/wardrobe.json            ← the canonical catalogue, 69 items. THE data.
data/work-outfits.md          ← 10 vetted outfits, hand-reasoned. Seed data + correctness check.
data/outfit-log.md            ← the entire wear history so far (one entry)
data/rules-and-context.md     ← owner profile, styling rules, picker logic, photo layout,
                                known data-quality issues. Read this one carefully — it is the
                                spec for the outfit picker.
```

---

## 0. Ground rules — read before touching anything

1. **Never destroy Max's data.** This project has a real incident behind it: about a year of
   uncommitted work was permanently lost to careless file and git operations. Copy before you
   change. Never `git reset --hard`, never force-push, never delete or overwrite originals,
   never `DROP` anything that isn't one of your own dev tables. Work on copies.
2. **`data/wardrobe.json` is read-only input.** Never edit it in place. The DB becomes the source
   of truth after the import; the JSON is the seed and the fallback.
3. **Photos are irreplaceable.** 13 items already have permanently lost photos. Any photo handling
   must copy, never move, and never write into the Google Drive folder. Treat
   `G:\My Drive\Claude stuff\Wardrobe Photos\` as read-only.
4. **Don't offload work onto Max that you can do yourself.** You have his GitHub, PyCharm and
   Postgres. If you need something from disk, go and get it. Ask him for *decisions*, not
   *labour*.
5. **Keep it simple.** Max's standing instruction for code is: keep things simple. Prefer boring,
   readable, few-dependency solutions over clever ones. No microservices, no queue, no ORM
   gymnastics, no front-end build step unless you can justify it in one sentence.

---

## 1. Ask Max these before you start

He has already decided:

- **Stack: your call.** Bias to Python end-to-end so it opens cleanly in PyCharm, with as little
  ceremony as possible. Recommend one, say why in two lines, then build it.
- **Photo storage: your call.** Same bias — simplest thing that works and doesn't recreate the
  17 MB-single-file problem. State the choice and the reason.
- **Scope for v1:** browse + filter the catalogue · outfit picker with the vetted looks ·
  one-tap wear log · laundry/availability state. **Item add/edit UI is explicitly NOT in v1** —
  the importer is the write path for catalogue data for now.
- **Hosting:** localhost, run from PyCharm. But build it so it can be reached from his phone later
  without a rewrite — config from env vars, no hardcoded absolute paths, no `localhost` baked into
  URLs, mobile-first responsive CSS, host/port configurable. No auth in v1; leave one obvious place
  to add it.

Ask him only about these:

1. **Which Postgres?** Existing local instance — new database (e.g. `wardrobe`) or a schema inside
   an existing one? Confirm connection details and whether there's a role you should use rather
   than superuser.
2. **Which GitHub repo?** New private repo (suggest a name) or an existing one? Confirm before you
   push anything.
3. **Where do the photos live on this machine right now**, and is the `G:\My Drive\...` path still
   correct? Confirm before you read from it.

If he doesn't answer within a reasonable window, pick the safest option (new database `wardrobe`,
new private repo, don't touch Drive) and tell him what you assumed.

---

## 2. The data you're importing

69 items. Categories: Knitwear 18 · Trousers 12 · Shoes 12 · Belts 11 · Tops 10 · Outerwear 6.
Verdicts: Keep 45 · Tailor 10 · Bin 8 · Replace 6. Scope: core 65 · out 4. 13 items have no photo.

Per-item fields as they exist in the JSON (not all items have all of them):

```
id / slug        stable string key, e.g. "polo-rl-burgundy-cashmere-crew". id is the ONLY unique key.
cat              Knitwear | Tops | Trousers | Shoes | Belts | Outerwear
name             display name — NOT unique
colour           free text
hex              "#B3C3CA" — present and reliable on every item
role             Pale neutral | Neutral | Mid tone | Anchor dark | Statement
neck             crew | v-neck | roll | shawl | cardigan | quarter-zip | button/mock | polo collar
cut              silhouette description (trousers/shoes/belts/outerwear)
material         "100% cashmere", "98% cotton / 2% elastane", …
weight           Fine | Light-Mid | Mid | Mid-Heavy | Chunky | ""
formality        free text — needs normalising, see below
fit              free-text assessment
condition        free-text assessment
verdict          Keep | Tailor | Replace | Bin
verdictNote      one-line justification
scope            core | out      ("out" = excluded from outfit building)
worksAlone       true | false | null   ← the layering primitive
pairs            free text: what it goes with
layer            free text: what goes under/over it
avoid            free text: what it must not go with
notes            free text
warmth           1–5   (outerwear only so far)
weatherproof     {rain: bool, wind: bool}   (outerwear only so far)
careNote         free text (outerwear only so far)
noPhoto          bool
photoRef         free text describing where the photos are
photoPrefix      filename prefix used to match photos on disk
retailPrefix     filename prefix for the generated catalogue render
```

Plus a top-level `profile` object (age, context, goal, workUniform) and a `generated` date.

---

## 3. Schema

Design it yourself, but hit these requirements:

- **`items.id` is the natural primary key** — the existing string slugs. Do not renumber them.
  Every downstream artefact, every photo filename, and every doc in the Claude Project references
  these ids. Changing them breaks the link to years of context.
- **Normalise the enum-ish fields** (`cat`, `role`, `verdict`, `scope`, `neck`, `weight`) into
  lookup tables or Postgres enums — your call, but adding a new category must not require a
  schema migration, because tees, shirts, shorts and socks are all still unlogged. Lookup tables
  are the safer bet for that reason.
- **Keep every free-text field.** `pairs`, `layer`, `avoid`, `notes`, `fit`, `condition`,
  `verdictNote` are hand-written knowledge accumulated over weeks. They are the rule engine. Never
  drop, truncate or "clean" them.
- **Add the derived columns the data has been missing.** Compute a first pass during import, then
  let Max correct them:
  - `formality_rank` smallint 1–5, normalised from the free-text `formality`, **and**
    `formality_note` for the parenthetical (`Casual (club crest)` → rank + "club crest"). The
    parenthetical explains why the item is capped — it matters.
  - `occasions` — work / casual / golf / formal / gym. Multi-valued. This is the field the data
    most needs and doesn't have; golf-ness is currently prose buried in `notes` (Vuori polo,
    Cuater belt). Seed it from the notes and the existing exclusion list in `work-outfits.md`.
  - `warmth` 1–5 for every item, not just outerwear — derive from `weight` + `material`.
  - `weatherproof_rain` / `weatherproof_wind` booleans for every item; default false, but set
    suede/nubuck to explicitly rain-unsafe (the picker needs this).
  - `pattern` — the wardrobe is ~entirely plain; a small exception list (Lyle & Scott crest,
    two Manfinity tipping details, a gingham waistband facing) covers it.
  Mark every derived value as derived (a `source` column or a `derived_fields` table), so a later
  hand-correction is visibly authoritative over the guess.
- **Photos are a separate table** — an item can have 1–8 frames. Store the angle
  (label / hanger / worn-front / worn-side / worn-back / worn-closed / detail / damage) where it's
  inferable from the filename, a sort order, and a flag for whether the image is a **generated
  catalogue render** rather than a real photograph of the garment. The app must never present a
  generated render as a photo of the actual item.
- **Outfits** are ordered slots, not a fixed four columns — a look can be
  top + trouser + shoe + belt + outer layer, and sometimes two tops (cardigan over polo). Model
  `outfits` + `outfit_items(role, position)`. Store the register (`everyday` | `sharp`), the
  rationale text, a `hidden_by_default` flag (the roll-neck look), and whether the look is vetted
  (hand-reasoned) or generated.
- **Wear log**: a `wear_events` table (date, context, weather temp/rain, rating 1–10, note, photos)
  plus the items worn, keyed by item id. It must be able to record an item that isn't in the
  catalogue (the 17 Aug entry includes a plain tee that has never been logged) — allow a free-text
  item alongside the FK, or don't enforce the FK on that column.
- **Item state**: `clean | worn | in_wash | at_tailor`, with a timestamp of the last change. This
  is app-owned state, not catalogue data — keep it in its own table so a re-import of the
  catalogue can never wipe it.
- Timestamps `created_at` / `updated_at` on everything. Timezone Australia/Sydney.
- Migrations as plain, numbered `.sql` files in the repo unless you have a strong reason for
  Alembic. Simple beats clever.

---

## 4. The importer

`scripts/import_wardrobe.py` (or the equivalent in whatever stack you choose):

- Reads `data/wardrobe.json`, writes to Postgres.
- **Idempotent.** Re-running it must not duplicate anything and must not clobber app-owned state
  (wear log, laundry status, any hand-corrections to derived fields). Upsert on `id`.
- **Dry-run mode by default**, `--commit` to actually write. Print what would change.
- Prints a verification report at the end: row counts per category, per verdict, per scope,
  items with no photo, items whose `photoPrefix` matched no file on disk, and any field it
  couldn't parse. Numbers must reconcile against section 2 above (69 / 18-12-12-11-10-6 /
  Keep 45, Tailor 10, Bin 8, Replace 6 / core 65, out 4 / 13 without photos). **If they don't
  reconcile, stop and say so — don't paper over it.**
- Separately seeds the 10 vetted outfits from `data/work-outfits.md` and the single wear event
  from `data/outfit-log.md`. Both reference items **by display name, and names are not unique** —
  two items are called "Zara Man V-neck", three are "Decathlon chino". Re-key them to ids by hand
  in a small explicit mapping table in the code, and assert that every reference resolves to
  exactly one item. Don't fuzzy-match this: get it wrong and the picker recommends the wrong
  garment forever.

**One data fix to apply during the import:** all trousers were tailored on 2026-08-20 and are
wearable as-is, but their `verdict` still says `Tailor` in the JSON. Flag them in the report and
ask Max to confirm before flipping them to `Keep`. Knitwear items marked `Tailor` are unconfirmed —
leave those alone.

---

## 5. Photos

- Source: `G:\My Drive\Claude stuff\Wardrobe Photos\` with subfolders `Knitwear`, `Shirts`,
  `Trousers`, `Shoes`, `Belts`, `Outerwear`, `Retail`. **`Shirts` maps to the `Tops` category** —
  the folder name and the category name differ.
- Matching rule: **filename starts with the item's `photoPrefix`**; any suffix works. Generated
  renders are `<photoPrefix>_retail.<ext>` in `Retail`.
- Copy them into the app's own storage — read-only from Drive, never write back, never move.
- Generate thumbnails once at import (Pillow); serve thumbs in the grid, full size on the detail
  view. The old app was 17 MB because it inlined full-size images as base64 — don't recreate that.
- Items with `noPhoto: true` fall back to a colour swatch from `hex` and show a small
  "needs reshoot" badge. Those photos are gone for good; the app should state that plainly rather
  than looking broken.

---

## 6. The app

Mobile-first, fast, no build step if you can avoid it. Screens:

**Catalogue** — grid of item cards (thumbnail or hex swatch, name, category, verdict badge).
Filter by category, verdict, scope, colour role, formality rank, occasion, and current
laundry state. Free-text search across name, colour, material and notes. Clicking a card opens the
detail view with every field, all the photos, and the `pairs` / `layer` / `avoid` text shown as
written — that prose is the point, don't summarise it away.

**Today** — the outfit picker. See section 7.

**Outfits** — the 10 vetted looks, grouped by register (Everyday / Sharp), each showing its items
with thumbnails, its rationale, and whether it's wearable right now given laundry state. The
roll-neck look is hidden behind a toggle.

**Wear log** — reverse-chronological list of what was worn, with rating and note. Logging must be
genuinely one tap from the Today screen: "wore this" → marks the outfit worn today, sets those
items to `worn`, and opens an optional rating/note field. The whole reason the current log has one
entry is that logging was a manual markdown edit.

**Laundry** — a simple board or list to flip items between `clean` / `worn` / `in_wash` /
`at_tailor`. Bulk actions: "all worn → in wash", "all in wash → clean". Two taps, not twenty.

---

## 7. The outfit picker

Port the existing logic — don't invent a new one. It's specified in `data/rules-and-context.md`
§3, and the 10 looks in `data/work-outfits.md` are both the seed data and the correctness check.

Key behaviours to preserve:

- It **picks among the vetted looks**, it does not generate new combinations. That's deliberate:
  it keeps the hand-reasoned styling rules intact.
- Scoring: weather band (`tempC` < 14 cold / 14–22 mild / > 22 warm), rain-safety (rain rules out
  suede and nubuck), a Friday bonus for the cardigan look, a bonus for wear-as-is over
  needs-tailoring, plus a stable per-day rotation.
- **Deterministic per calendar day** — same outfit all day, different tomorrow. No `random()`.
  Seed the rotation from the date.
- The roll-neck look is excluded unless explicitly allowed. Max dislikes roll-necks.
- **New in this version:** skip looks whose items aren't `clean`, and say why ("Friday layer is out
  — the grey polo is in the wash"). That's the whole point of adding laundry state.
- Weather input is manual for v1 (a temp field and a rain toggle that remember their last value).
  Leave a clean seam for a weather API later — Sydney.

Validation: the picker must be able to return each of the 10 vetted looks under some
weather/day/state combination. If it can't, the port is wrong.

Free combinatorial generation from the `pairs`/`avoid` rules is **not** v1. Note it as a follow-up.

---

## 8. Keep the Claude Project in sync

Max works on this wardrobe in Claude sessions that read `wardrobe.json` from the Claude Project.
Once the DB is canonical, that file goes stale immediately and those sessions start giving wrong
advice. So build the round-trip:

`scripts/export_wardrobe.py` → regenerates `wardrobe.json` from the DB, byte-for-byte compatible
with the current schema (same field names, same shape, `generated` bumped to today), so Max can
drop it straight back into the Claude Project. Run it at the end of the port and confirm the
output round-trips: export → re-import into a scratch database → identical row counts and field
values.

---

## 9. Repo hygiene

- Private GitHub repo, confirmed with Max first.
- `.env` for the DB connection, `.env.example` committed, `.env` gitignored. No credentials in
  code, in migrations, or in commit messages.
- Photos and thumbnails gitignored — the repo stays small.
- `README.md`: how to create the DB, run migrations, run the import, start the app, and run the
  export. Assume Max is coming back to this in three months having forgotten everything.
- Small, frequent commits with real messages. Branch, don't commit to `main` directly, and don't
  push until he's confirmed the repo.

---

## 10. Definition of done

- [ ] Postgres database exists with the schema; migrations are in the repo and run clean from
      scratch on an empty database.
- [ ] All 69 items imported, counts reconcile exactly against section 2.
- [ ] The 10 vetted outfits and the 1 wear event are seeded, every item reference resolved to a
      unique id.
- [ ] Photos linked, thumbnails generated, the 13 photo-less items degrade gracefully.
- [ ] The app runs from PyCharm with one command and works on a phone-sized viewport.
- [ ] Catalogue browse + filter, Today picker, Outfits, Wear log, Laundry all functional.
- [ ] The picker reproduces all 10 vetted looks and respects laundry state, rain, temperature,
      Friday, and the roll-neck exclusion.
- [ ] `export_wardrobe.py` round-trips cleanly.
- [ ] Import is idempotent — verified by running it twice and diffing.
- [ ] README written.
- [ ] Nothing in `G:\My Drive\Claude stuff\Wardrobe Photos\` was modified. Verify this.

## 11. Explicitly out of scope for v1

Item add/edit UI · free combinatorial outfit generation · weather API · auth · deployment ·
shopping-list features · the SVG illustration set (`wardrobe-kit.js`) · migrating the old 17 MB
`Wardrobe_Manager.html` (it's superseded; leave the file alone, don't delete it) · logging the
missing categories (tees, shirts, shorts, socks — that's Max's work, not yours).

Note them in the README as follow-ups. Don't build them.

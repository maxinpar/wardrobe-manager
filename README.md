# Wardrobe Manager

The wardrobe catalogue in Postgres, with a small local web app on top. It
replaces the 17 MB `Wardrobe_Manager.html` and the JSON/markdown/spreadsheet
copies that had drifted apart.

**The database is the source of truth.** `data/wardrobe.json` is the seed and
the fallback; once the import has run, regenerate it with
`scripts/export_wardrobe.py` and drop that file back into the Claude Project so
those sessions don't go stale.

Stack: Python 3.11 · Flask · psycopg3 · Jinja templates · plain CSS. No ORM, no
JS framework, no build step.

---

## Getting set up

Assumes PostgreSQL 15 on `localhost:5432` (the instance that also holds
`scoringDB`). Everything below is run from the repo root.

### 1. Create the database

```
psql -U postgres -h localhost -p 5432 -f scripts/bootstrap_db.sql
```

It prompts for a password for a new `wardrobe_app` role, then creates the
`wardrobe` database owned by it. The password never lands in the repo or in
shell history. Nothing else on the server is touched.

### 2. Configure

```
cp .env.example .env
```

Edit `.env` and put the password you just chose into `DATABASE_URL`. Check
`PHOTO_SOURCE_ROOT` still points at the Drive folder.

### 3. Install the dependencies

```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

In PyCharm: File ▸ Settings ▸ Project ▸ Python Interpreter ▸ add `.venv`.

### 4. Create the schema

```
.venv\Scripts\python scripts/migrate.py
```

Plain numbered `.sql` files in `migrations/`, applied once each and recorded in
`schema_migrations`. They run clean from scratch on an empty database.

### 5. Import the catalogue

```
.venv\Scripts\python scripts/import_wardrobe.py
.venv\Scripts\python scripts/import_wardrobe.py --commit
```

The first form is a dry run — it prints every change it would make and writes
nothing. The second one commits. It also seeds the 10 vetted looks (plus the
hidden roll-neck one) and the single wear event.

The importer prints a verification report: counts per category, verdict and
scope, items with no photo, `photoPrefix` values that matched no file on disk,
and anything it couldn't parse. If the numbers don't reconcile against the
known-good baseline (69 items · Knitwear 18 / Trousers 12 / Shoes 12 / Belts 11
/ Tops 10 / Outerwear 6 · Keep 45, Tailor 10, Bin 8, Replace 6 · core 65, out 4
· 13 without photos) it stops rather than papering over it.

Re-running it is safe: it upserts on `items.id`, and it never touches laundry
state, the wear log, or any field you've corrected by hand.

### 6. Copy the photos in

```
.venv\Scripts\python scripts/import_photos.py --commit
```

Copies from `G:\My Drive\Claude stuff\Wardrobe Photos\` into `photos/` and
generates thumbnails. Drive is **read-only**: files are copied, never moved, and
the script snapshots the source folder before and after and reports any
difference. `photos/` is gitignored, so the repo stays small.

### 7. Run the app

```
.venv\Scripts\python run.py
```

Then open http://127.0.0.1:5005. In PyCharm: right-click `run.py` ▸ Run.

To reach it from your phone on the same wifi, set `APP_HOST=0.0.0.0` in `.env`
and browse to your laptop's LAN address on the same port. There is no auth —
see `require_login()` in `wardrobe/app.py`, which is the one obvious place to
add it.

---

## The screens

- **Today** — the picker. Enter the temperature and whether it's raining (both
  remembered), and it picks one of the vetted looks for today. One tap on
  "Wore this" logs it and marks those garments worn.
- **Catalogue** — every item, filterable by category, verdict, scope, colour
  role, formality, occasion and laundry state, plus free-text search across
  name, colour, material and notes. The detail view shows every field, all the
  photos, and the `pairs` / `layer` / `avoid` prose exactly as written.
- **Outfits** — the vetted looks by register, each showing whether it's wearable
  right now. The roll-neck look is behind a toggle.
- **Log** — what was worn, newest first, with rating and note.
- **Laundry** — flip items between clean / worn / in the wash / at the tailor,
  with two bulk moves.

## The picker

Ported from `WardrobeKit.pick()`, not reinvented. It **chooses among the vetted
looks** rather than generating new combinations — that keeps the hand-reasoned
styling rules intact. It scores on weather band (cold < 14 °C, mild 14–22, warm
> 22), rain safety (suede and nubuck stay home), a Friday bonus for the cardigan
look, a bonus for wear-as-is over needs-tailoring, and a stable per-day
rotation. It is deterministic per calendar day — no `random()` anywhere, so the
same day always gives the same look.

New in this version: a look whose garments aren't clean is skipped and says why
("Friday layer is out — the grey polo is in the wash"). Where the look offers an
alternate for that slot, the alternate is substituted instead of dropping the
look.

```
.venv\Scripts\python -m pytest tests          # picker behaviour, offline
.venv\Scripts\python scripts/validate_picker.py   # every vetted look is reachable
```

`validate_picker.py` sweeps a year of dates against six temperatures and both
rain states and fails if any vetted look can never be picked — that's the
correctness check for the port.

## Keeping the Claude Project in sync

```
.venv\Scripts\python scripts/export_wardrobe.py --compare data/wardrobe.json
```

Regenerates `wardrobe.json` from the database into `export/wardrobe.json`, in
the same shape and formatting as the hand-maintained file, with `generated`
bumped to today. `--compare` verifies field by field against the original. The
one deliberate difference: key order within each item is canonicalised (the
source file had six different orders from months of editing; the values are
identical).

```
.venv\Scripts\python scripts/roundtrip_check.py
```

Full round-trip proof: export → build a scratch database → migrate → re-import →
re-export → compare both JSON files and every table count. It drops only the
scratch database it created.

## Derived fields

The catalogue never had `formality_rank`, `occasions`, per-item `warmth`,
`weatherproof`, or `pattern`. The importer computes a first pass and records
each one in `item_field_sources` as `derived`. Correct any of them by hand and
mark the row `manual`, and the importer will never overwrite it again — a
hand-correction is permanently authoritative over the guess. The item detail
page shows which is which.

## Safety rules this repo follows

- `data/wardrobe.json` is opened read-only and never rewritten.
- `G:\My Drive\Claude stuff\Wardrobe Photos\` is read-only. Photos are copied,
  never moved, and the copy is verified not to have changed the source.
- Nothing drops or truncates anything except the scratch database that
  `roundtrip_check.py` creates for itself.
- `items.id` — the existing string slugs — is never renumbered. Photo filenames
  and years of Claude Project context depend on those ids.
- Laundry state and the wear log live in their own tables so re-importing the
  catalogue can never wipe them.
- Secrets live in `.env` only, which is gitignored.

## Known state and follow-ups

- **Trouser verdicts.** The trousers came back from the tailor on 2026-08-20
  and are wearable, but `wardrobe.json` still says `Tailor` for 6 of them.
  Imported as-is, by request; the importer prints them, and the exact SQL to
  flip them, on every run. Marking `verdict_code` as `manual` in
  `item_field_sources` is what makes the correction stick — the importer never
  overwrites a manual value. Knitwear `Tailor` items are unconfirmed and
  untouched.
- **13 items have no photo** (6 belts, 5 shoes, 2 trousers) and those photos are
  gone for good. The app falls back to the colour swatch and shows a "needs
  reshoot" badge with the prefix to reuse.
- **Generated catalogue renders** (`Retail/`) are the preferred image
  everywhere: the catalogue grid, the outfit chips and the top of the item
  detail page all lead with the render where one exists, falling back to a real
  photo, then to the colour swatch. They are flagged `is_render` and labelled
  "illustration" wherever they appear, so they are never presented as photos of
  the actual garment. Current coverage: **39 of 69 items have a render**, 17
  more show a real photo, 13 show a swatch. The 30 core items still without one
  are listed by `scripts/missing_renders.py`.

Out of scope for v1, deliberately, and not built:

- item add/edit UI — the importer is the write path for catalogue data
- free combinatorial outfit generation from the `pairs` / `avoid` rules
- a weather API (Sydney) — the picker takes manual input, with a clean seam
- auth, deployment, shopping-list features
- the SVG illustration set (`wardrobe-kit.js`)
- migrating the old 17 MB `Wardrobe_Manager.html` — superseded, left alone
- logging the missing categories: tees, shirts, shorts, socks

## Layout

```
migrations/     numbered .sql, applied by scripts/migrate.py
scripts/        bootstrap, migrate, import, export, round-trip, picker validation
wardrobe/       config, db, derive, picker, seed_data, the Flask app, templates
data/           the seed JSON and the hand-written docs it came with
docs/BRIEF.md   the original brief for this port
tests/          offline picker tests
```

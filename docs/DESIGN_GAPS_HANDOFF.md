# Handoff: Gaps tab

## Overview

A new **Gaps** view for `wardrobe-manager` — the shopping/replacement list. There is no current
equivalent: no `gaps.html` template, no `/gaps` route, no tables. This is additive.

Bundled with this doc:

| File | What it is |
|---|---|
| `Gaps.dc.html` | the approved design prototype — match it |
| `data/gaps.json` | **the content**: 14 authored gaps, final copy, ready to seed |
| `wardrobe/static/gaps/g01–g14.svg` | one image per gap — **placeholders**, see below |
| `claude/gaps.md` | the reasoning behind each gap, for reference; not needed to build |

Follow the conventions already set in `DESIGN_FITS_HANDOFF.md`: server-rendered Jinja, extend
`app.css` rather than adding a second styling system, POST-form actions, smallest possible
progressive enhancement where Jinja can't express client state.

---

## Decision 1 — gaps live in Postgres, not in the JSON

`data/gaps.json` is **seed data, not the runtime store.** The cards carry state the user changes:
status (open / bought / not a gap), and candidate links pasted into the card. That has to persist,
so it belongs in the database, imported the same way items and fits are.

This mirrors the existing rule from `fits-requirements.md`: **the importer is the write path, and
the app never overwrites a field the user set.** Specifically:

- `status`, `status_changed_at` and any user-pasted candidate are **app-owned**. A re-import must
  never reset them.
- `title`, `rationale`, `unlocks`, `spec`, `size`, `budget`, `priority` are **authored** and the
  importer refreshes them.
- `unlocks` is **authored prose, never computed.** It is a claim about the closet made at authoring
  time. Do not derive it from `fit_items` at render time — it will drift and be wrong.

## Decision 2 — schema

Migration `015_gaps.sql` (note: `014` is already used twice, start at 015).

```sql
CREATE TABLE gaps (
  id                text PRIMARY KEY,          -- 'g01'
  category          text NOT NULL,             -- Trousers | Tops | Shoes | Belts | Knitwear
  priority          text NOT NULL,             -- high | medium | low
  status            text NOT NULL DEFAULT 'open',   -- open | bought | not_a_gap
  status_changed_at timestamptz,
  title             text NOT NULL,
  rationale         text,
  unlocks           text,
  spec              text,
  size              text,
  budget            text,
  image_path        text,
  image_is_placeholder boolean NOT NULL DEFAULT true,
  replaces_item_id  text REFERENCES items(id),  -- nullable; a gap that retires something owned
  sort_order        smallint NOT NULL DEFAULT 100,
  created_at        timestamptz NOT NULL DEFAULT now(),
  updated_at        timestamptz NOT NULL DEFAULT now(),
  CHECK (priority IN ('high','medium','low')),
  CHECK (status  IN ('open','bought','not_a_gap'))
);

CREATE TABLE gap_buy_at (       -- the 'BUY AT' line: retailer names, ordered
  gap_id     text REFERENCES gaps(id) ON DELETE CASCADE,
  retailer   text NOT NULL,
  sort_order smallint NOT NULL DEFAULT 0,
  PRIMARY KEY (gap_id, retailer)
);

CREATE TABLE gap_candidates (   -- specific products; seeded AND user-added
  id         bigserial PRIMARY KEY,
  gap_id     text REFERENCES gaps(id) ON DELETE CASCADE,
  name       text NOT NULL,
  source     text,              -- 'meermin.es', 'Oxford, in store'
  url        text,
  price      text,              -- text, not numeric: 'A$195', or NULL when unverified
  added_by   text NOT NULL DEFAULT 'import',   -- import | user
  created_at timestamptz NOT NULL DEFAULT now()
);
```

`price` is deliberately text and frequently NULL — the seed data does not carry verified prices and
must not invent them. Render an empty price as blank, not as `$0`.

`gap_candidates.added_by = 'user'` rows are **never touched by the importer.**

## Decision 3 — importer

`scripts/import_gaps.py`, same shape as the other two: dry run by default, `--commit` to write,
prints what would change. Upsert on `gaps.id`. Reconcile nothing (there is no baseline for gaps).

Rules it must honour:
- Never write `status` or `status_changed_at` on an existing row.
- Never delete a `gap_candidates` row with `added_by = 'user'`.
- A gap present in the DB but absent from the JSON is left alone, not deleted — same conservatism as
  the item importer, and for the same reason.

---

## The view

Route `/gaps` → `wardrobe/templates/gaps.html`, plus nav entry in `base.html`.

**Header:** `N OPEN GAPS · N HIGH · N BOUGHT`, then filter chips: Open / High / Medium / Low /
Bought / Not a gap, each with a count. Chips filter, they don't navigate.

**Card**, in the order the prototype shows:

1. category label (mono, uppercase) + priority badge, top row
2. title
3. rationale paragraph
4. `UNLOCKS` bar — tinted, full width
5. definition rows: `SPEC`, `SIZE`, `BUDGET`, `BUY AT`
6. `CANDIDATES` — list of name · source · price, then a "Paste a link" input
7. actions: `Bought it`, `Not a gap`

When a gap has no candidates, the prototype shows `NO CANDIDATE FOUND YET` above the input. Keep
that.

**Actions** are POST forms: `POST /gaps/<id>/status` with `bought` or `not_a_gap`, and
`POST /gaps/<id>/candidate` with a URL. Both redirect back to `/gaps` preserving the active filter.
Setting a status writes `status_changed_at`. A bought or dismissed gap stays visible under its
filter chip — never delete it.

**Image.** The `gNN.svg` files are flat spec illustrations — correct garment type and colour, and
nothing else. `image_is_placeholder` is true on all 14. Render them, but badge or dim them so
nobody mistakes a drawing for a product. Real product photos replace them later; the field and the
flag are what makes that swap a data change rather than a code change.

---

## Definition of done

- [ ] 14 gaps seeded from `data/gaps.json`, every `replaces_item_id` resolving to a real item.
- [ ] Marking a gap `bought`, re-running `import_gaps.py --commit`, and confirming it is **still**
      `bought`. This is the test that matters — it is the exact failure the fits importer was
      designed to avoid.
- [ ] A user-pasted candidate survives a re-import.
- [ ] Filter chip counts match the rows shown.
- [ ] A gap with no candidates renders `NO CANDIDATE FOUND YET` and an empty input, not a blank box.
- [ ] Placeholder images are visibly marked as placeholders.
- [ ] Nothing on this screen is computed from the closet at render time — `unlocks` is authored text.

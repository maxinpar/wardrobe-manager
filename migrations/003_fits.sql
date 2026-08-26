-- 003_fits.sql — outfits become "fits": a managed entity with their own
-- metadata, score, photo and history. Per the fits addendum (2026-08-26).
--
-- They are fits, not outfits, everywhere: table, column, UI.
--
-- The old outfits/outfit_items tables held nothing but seed data, so they are
-- copied across and then dropped. wear_events holds real user data and is only
-- ALTERed — its outfit_id is migrated to fit_id, never dropped with data in it.
--
-- Three numbers are kept apart and must never overwrite each other:
--   fits.score          Max's own 1-10 opinion. Manual. The app never computes it.
--   the picker's rank   computed per request, never stored.
--   wear_events.rating  how one wearing went; aggregated for display only.

-- ------------------------------------------------------- new lookups --

CREATE TABLE temp_bands (
  code       text PRIMARY KEY,          -- cold | mild | warm
  label      text NOT NULL,
  sort_order smallint NOT NULL DEFAULT 100
);

INSERT INTO temp_bands (code, label, sort_order) VALUES
  ('cold', 'Cold (under 14°)', 10),
  ('mild', 'Mild (14–22°)',    20),
  ('warm', 'Warm (over 22°)',  30);

CREATE TABLE seasons (
  code       text PRIMARY KEY,
  label      text NOT NULL,
  sort_order smallint NOT NULL DEFAULT 100
);

INSERT INTO seasons (code, label, sort_order) VALUES
  ('summer', 'Summer', 10),
  ('autumn', 'Autumn', 20),
  ('winter', 'Winter', 30),
  ('spring', 'Spring', 40);

-- good_for / bad_for share the item occasion vocabulary, so that a work fit
-- containing a gym-only item is a detectable contradiction later. Extending the
-- shared list, not starting a parallel one.
INSERT INTO occasions (code, label, sort_order) VALUES
  ('client',  'Client day', 15),
  ('dinner',  'Dinner',     25),
  ('weekend', 'Weekend',    35),
  ('riding',  'Riding',     45);

-- ---------------------------------------------------------------- fits --

CREATE TABLE fits (
  id                text PRIMARY KEY,   -- stable slug, e.g. fit_the_shawl. Never renumbered.
  name              text NOT NULL,      -- display name; NOT unique-safe, never key on it
  register_code     text NOT NULL REFERENCES registers(code),

  killer            boolean NOT NULL DEFAULT false,  -- Max-set. Never computed or overwritten.
  vetted            boolean NOT NULL DEFAULT true,   -- hand-reasoned by a human
  hidden_by_default boolean NOT NULL DEFAULT false,  -- the roll-neck look

  style             text,               -- short characterisation, Max's field
  commentary        text,               -- why it works
  catch             text,               -- what goes wrong: a wear-time warning,
                                        -- surfaced when choosing, not buried

  score             smallint CHECK (score BETWEEN 1 AND 10),  -- Max's 1-10 opinion, manual
  formality_rank    smallint CHECK (formality_rank BETWEEN 1 AND 5),  -- same scale as items
  rain_safe         boolean NOT NULL DEFAULT true,   -- derived from items, overridable

  source            text,               -- which pass produced it, e.g. 'work-outfits.md 2026-08-24'
  sort_order        smallint NOT NULL DEFAULT 100,

  -- A generated render illustrating the fit. Max may never have worn it, so it
  -- is flagged wherever it appears and never shown where it implies a wearing.
  hero_image_path   text,
  hero_thumb_path   text,
  hero_is_generated boolean NOT NULL DEFAULT true,

  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TRIGGER fits_updated_at BEFORE UPDATE ON fits
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE INDEX fits_register_idx ON fits (register_code);
CREATE INDEX fits_killer_idx   ON fits (killer);

-- Ordered slots. A fit is 3-6 pieces and sometimes doubles up (cardigan over
-- polo; knit under a vest under a jacket), so this is rows, not columns.
CREATE TABLE fit_items (
  id            bigserial PRIMARY KEY,
  fit_id        text NOT NULL REFERENCES fits(id) ON DELETE CASCADE,
  item_id       text NOT NULL REFERENCES items(id),
  role          text NOT NULL,          -- outer|layer|top|base|bottom|shoe|belt|accessory
  position      smallint NOT NULL,      -- ordering within a role, outermost first
  is_alternate  boolean NOT NULL DEFAULT false,
  alternate_for bigint REFERENCES fit_items(id) ON DELETE CASCADE,
  note          text,                   -- "or the black jean if the coating shows"
  UNIQUE (fit_id, item_id, role)
);

CREATE INDEX fit_items_fit_idx  ON fit_items (fit_id, position);
CREATE INDEX fit_items_item_idx ON fit_items (item_id);

-- Multi-valued, and what actually drives the picker.
CREATE TABLE fit_temp_bands (
  fit_id    text NOT NULL REFERENCES fits(id) ON DELETE CASCADE,
  band_code text NOT NULL REFERENCES temp_bands(code),
  PRIMARY KEY (fit_id, band_code)
);

-- Browsing label ONLY. Nothing in the picker may read this table.
CREATE TABLE fit_seasons (
  fit_id      text NOT NULL REFERENCES fits(id) ON DELETE CASCADE,
  season_code text NOT NULL REFERENCES seasons(code),
  PRIMARY KEY (fit_id, season_code)
);

-- good_for / bad_for against the shared occasion vocabulary.
CREATE TABLE fit_occasions (
  fit_id        text NOT NULL REFERENCES fits(id) ON DELETE CASCADE,
  occasion_code text NOT NULL REFERENCES occasions(code),
  kind          text NOT NULL CHECK (kind IN ('good', 'bad')),
  PRIMARY KEY (fit_id, occasion_code, kind)
);

-- A one-off job blocking a fit — not laundry, not a verdict. "Repair the cuff"
-- is a precondition; "wear the blazer open" is a catch and lives on the fit.
CREATE TABLE fit_preconditions (
  id         bigserial PRIMARY KEY,
  fit_id     text NOT NULL REFERENCES fits(id) ON DELETE CASCADE,
  text       text NOT NULL,
  item_id    text REFERENCES items(id),
  done       boolean NOT NULL DEFAULT false,
  done_at    timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX fit_preconditions_fit_idx ON fit_preconditions (fit_id) WHERE NOT done;

-- Same provenance rule as items: the importer refreshes 'derived' values and
-- never overwrites one Max has corrected by hand.
CREATE TABLE fit_field_sources (
  fit_id     text NOT NULL REFERENCES fits(id) ON DELETE CASCADE,
  field_name text NOT NULL,
  source     text NOT NULL CHECK (source IN ('imported', 'derived', 'manual')),
  note       text,
  updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (fit_id, field_name)
);

-- ------------------------------------------- migrate the old outfits --

-- Carry the seeded looks across, keyed by a stable text id built from the slug.
INSERT INTO fits (id, name, register_code, vetted, hidden_by_default, commentary,
                  sort_order, source, created_at)
SELECT 'fit_' || replace(o.slug, '-', '_'),
       o.name, o.register_code, o.vetted, o.hidden_by_default, o.rationale,
       o.sort_order, 'work-outfits.md 2026-08-24', o.created_at
FROM outfits o;

INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note)
SELECT 'fit_' || replace(o.slug, '-', '_'),
       oi.item_id,
       CASE oi.slot_role
         WHEN 'trouser'   THEN 'bottom'
         WHEN 'mid-layer' THEN 'layer'
         ELSE oi.slot_role
       END,
       oi.position, oi.is_alternate, oi.note
FROM outfit_items oi
JOIN outfits o ON o.id = oi.outfit_id;

-- wear_events holds real user data: migrate the reference, never the rows.
ALTER TABLE wear_events ADD COLUMN fit_id text REFERENCES fits(id);

UPDATE wear_events w
   SET fit_id = 'fit_' || replace(o.slug, '-', '_')
  FROM outfits o
 WHERE o.id = w.outfit_id;

ALTER TABLE wear_events DROP COLUMN outfit_id;

DROP TABLE outfit_items;
DROP TABLE outfits;

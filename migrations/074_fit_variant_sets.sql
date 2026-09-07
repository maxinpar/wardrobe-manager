-- 074_fit_variant_sets.sql — a base fit with swappable tops.
--
-- Source: brief-fit-variant-sets.md (2026-09-07).
--
-- Max does not change his whole outfit every day. Shoes, trousers, belt and the
-- outer layer stay put all week and only the top changes. This models that: a
-- *set* of fits that share a base, tagged by two nullable columns.
--
-- WHY A FULL FIT ROW PER VARIANT, and not a fit_variants table or
-- fit_items.is_alternate. The picker, the wear log, the laundry check, the fits
-- list and scripts/import_photos.py all key off fit_id. Under this design not
-- one of them learns a new concept: the importer files all five renders with no
-- code change, and the wear log already records WHICH variant was worn, which is
-- the entire reason for the feature. Compare migration 064's layered renders,
-- where a smaller idea still needed an importer special-case.
--
-- The accepted cost is duplication: the four base garments are written five
-- times, so changing the base shoe later means changing five rows. Deliberate.
-- A set is a seasonal thing you rebuild, not something you edit piecemeal.
--
-- Nullable is correct — the large majority of fits are not in a set and never
-- will be, and they must behave exactly as they do today.

ALTER TABLE fits ADD COLUMN variant_set text;
ALTER TABLE fits ADD COLUMN variant_position smallint;

COMMENT ON COLUMN fits.variant_set IS
  'The set this fit is a variant of, e.g. black_canvas. NULL for the ordinary '
  'fits, which are the large majority. Members of a set share every garment '
  'except the top.';

COMMENT ON COLUMN fits.variant_position IS
  '1-based order within the set. The picker rotates through these by date, so '
  'the position is the rotation order, not a ranking.';

-- Two positions cannot collide inside one set. Partial, because NULL is the
-- normal state and hundreds of fits share it.
CREATE UNIQUE INDEX fits_variant_set_position_idx
  ON fits (variant_set, variant_position)
  WHERE variant_set IS NOT NULL;

-- Half-tagged is meaningless: a set key with no position has no place in the
-- rotation, and a position with no set belongs to nothing.
ALTER TABLE fits ADD CONSTRAINT fits_variant_both_or_neither CHECK (
  (variant_set IS NULL AND variant_position IS NULL)
  OR (variant_set IS NOT NULL AND variant_position IS NOT NULL)
);

-- --------------------------------------------------------- black_canvas --
--
-- The first set. Base, identical and locked in all five:
--   outer   Anko slate puffer gilet
--   bottom  black coated straight jeans
--   belt    black classic pin-buckle
--   shoe    Ecco black nubuck
--
-- Position 4 is NOT inserted here. fit_c6_pale-blue-vest-and-black is already
-- exactly this outfit — same gilet, same jeans, same belt, same Ecco, pale blue
-- piqué polo — so it is tagged into the set at the bottom of this file rather
-- than duplicated. A sixth row for an outfit that already exists would show up
-- twice in the gallery and split its own wear history.

INSERT INTO fits (id, name, register_code, category_code, vetted, source, sort_order,
                  variant_set, variant_position) VALUES
('fit_bc_charcoal-shirt', 'Charcoal shirt & the gilet', 'everyday', 'cold', true,
 'brief-fit-variant-sets.md', 59, 'black_canvas', 1),
('fit_bc_burgundy-crew',  'Burgundy crew & the gilet',  'everyday', 'cold', true,
 'brief-fit-variant-sets.md', 60, 'black_canvas', 2),
('fit_bc_sage-polo',      'Sage polo & the gilet',      'everyday', 'cold', true,
 'brief-fit-variant-sets.md', 61, 'black_canvas', 3),
('fit_bc_grey-henley',    'Grey henley & the gilet',    'everyday', 'cold', true,
 'brief-fit-variant-sets.md', 62, 'black_canvas', 5);

INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note) VALUES
('fit_bc_charcoal-shirt','outerwear_06_anko-slate-puffer-vest','outer',1,false,NULL),
('fit_bc_charcoal-shirt','tops_31_zara-charcoal-textured-shirt','top',1,false,NULL),
('fit_bc_charcoal-shirt','trousers_11_black-coated-jeans','bottom',1,false,NULL),
('fit_bc_charcoal-shirt','shoes_03_ecco-black-nubuck','shoe',1,false,NULL),
('fit_bc_charcoal-shirt','belts_11_black-classic-pin-buckle','belt',1,false,NULL),

('fit_bc_burgundy-crew','outerwear_06_anko-slate-puffer-vest','outer',1,false,NULL),
('fit_bc_burgundy-crew','polo-rl-burgundy-cashmere-crew','top',1,false,NULL),
('fit_bc_burgundy-crew','trousers_11_black-coated-jeans','bottom',1,false,NULL),
('fit_bc_burgundy-crew','shoes_03_ecco-black-nubuck','shoe',1,false,NULL),
('fit_bc_burgundy-crew','belts_11_black-classic-pin-buckle','belt',1,false,NULL),

('fit_bc_sage-polo','outerwear_06_anko-slate-puffer-vest','outer',1,false,NULL),
('fit_bc_sage-polo','tops_05_sage-pique-polo','top',1,false,NULL),
('fit_bc_sage-polo','trousers_11_black-coated-jeans','bottom',1,false,NULL),
('fit_bc_sage-polo','shoes_03_ecco-black-nubuck','shoe',1,false,NULL),
('fit_bc_sage-polo','belts_11_black-classic-pin-buckle','belt',1,false,NULL),

('fit_bc_grey-henley','outerwear_06_anko-slate-puffer-vest','outer',1,false,NULL),
('fit_bc_grey-henley','tees_15_adidas-grey-henley','top',1,false,NULL),
('fit_bc_grey-henley','trousers_11_black-coated-jeans','bottom',1,false,NULL),
('fit_bc_grey-henley','shoes_03_ecco-black-nubuck','shoe',1,false,NULL),
('fit_bc_grey-henley','belts_11_black-classic-pin-buckle','belt',1,false,NULL);

-- The derived metadata below was computed by running wardrobe/fit_derive.py over
-- these exact garment lists — the same functions the app runs when Max saves a
-- fit in the builder — and the results written out as literals so this file
-- still runs clean on an empty database. Every value is `derived`, so a later
-- hand-correction outranks it and an import never overwrites it.
--
-- All four land on cold/mild and formality 3. Only the henley differs on
-- occasion: it is casual and not work, which is what its own occasion tags say.

INSERT INTO fit_temp_bands (fit_id, band_code)
SELECT f.id, b.band FROM (VALUES
  ('fit_bc_charcoal-shirt'),('fit_bc_burgundy-crew'),
  ('fit_bc_sage-polo'),('fit_bc_grey-henley')) AS f(id),
  (VALUES ('cold'),('mild')) AS b(band);

INSERT INTO fit_seasons (fit_id, season_code)
SELECT f.id, s.season FROM (VALUES
  ('fit_bc_charcoal-shirt'),('fit_bc_burgundy-crew'),
  ('fit_bc_sage-polo'),('fit_bc_grey-henley')) AS f(id),
  (VALUES ('winter'),('autumn'),('spring')) AS s(season);

INSERT INTO fit_occasions (fit_id, occasion_code, kind) VALUES
('fit_bc_charcoal-shirt','work','good'),
('fit_bc_charcoal-shirt','casual','good'),
('fit_bc_burgundy-crew','work','good'),
('fit_bc_burgundy-crew','casual','good'),
('fit_bc_sage-polo','work','good'),
('fit_bc_sage-polo','casual','good'),
-- The henley is casual only. Its garment record does not carry `work`, and
-- inventing one here would put a long-sleeve jersey henley into the office
-- rotation on the strength of nothing.
('fit_bc_grey-henley','casual','good');

-- rain_safe is false across the set for one reason: the Ecco is nubuck, and
-- nubuck stays home in the rain (rules-and-context.md §2 rule 13).
UPDATE fits SET rain_safe = false, formality_rank = 3
 WHERE id IN ('fit_bc_charcoal-shirt','fit_bc_burgundy-crew',
              'fit_bc_sage-polo','fit_bc_grey-henley');

INSERT INTO fit_field_sources (fit_id, field_name, source, note)
SELECT f.id, v.field, 'derived', 'brief-fit-variant-sets.md 2026-09-07'
FROM (VALUES
  ('fit_bc_charcoal-shirt'),('fit_bc_burgundy-crew'),
  ('fit_bc_sage-polo'),('fit_bc_grey-henley')) AS f(id),
  (VALUES ('temp_bands'),('seasons'),('good_for'),('rain_safe'),('formality_rank'))
    AS v(field);

-- ------------------------------------------------- position 4, in place --
--
-- Tagged, and nothing else about it touched: not its name, not its source, not
-- its wear history. It was already this outfit before the set existed.
UPDATE fits
   SET variant_set = 'black_canvas', variant_position = 4
 WHERE id = 'fit_c6_pale-blue-vest-and-black';

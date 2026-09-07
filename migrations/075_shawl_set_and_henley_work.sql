-- 075_shawl_set_and_henley_work.sql — the_shawl variant set, and the henley at work.
--
-- Source: brief-shawl-set-and-henley.md (2026-09-07). Follows 074, which added
-- fits.variant_set / variant_position and built black_canvas.

-- ------------------------------------------------ the henley at the office --
--
-- tees_15_adidas-grey-henley derived as casual-only, which made black_canvas
-- four deep on an office day rather than five: the rotation reached position 5
-- and found a fit that could not go to work.
--
-- `manual`, not `derived`. Max says he wears it to the office, and a statement
-- from the owner has to outrank a derivation from the catalogue — otherwise the
-- next import quietly reverts it and the henley disappears from the rotation
-- again with nothing to show why.

INSERT INTO item_occasions (item_id, occasion_code)
VALUES ('tees_15_adidas-grey-henley', 'work')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note)
VALUES ('tees_15_adidas-grey-henley', 'occasions', 'manual',
        'Max confirmed he wears it to the office — brief-shawl-set-and-henley.md 2026-09-07')
ON CONFLICT (item_id, field_name) DO UPDATE
   SET source = EXCLUDED.source, note = EXCLUDED.note, updated_at = now();

-- ------------------------------------------------------------ the_shawl --
--
-- The second variant set, and it varies a DIFFERENT SLOT from the first. In
-- black_canvas the gilet-and-jeans base holds and the top changes. Here the
-- shawl IS the top and what changes is the garment underneath it, which the
-- schema calls `base` — the same convention as fit_k13_bomber-and-burgundy.
--
-- That difference is the reason the variant code no longer reads a role
-- anywhere: the varying garment is defined as the item a member has that its
-- siblings do not, which is true of both sets and of any set built later.
--
-- Base, identical in all five:
--   top     Ben Sherman aubergine shawl-collar
--   bottom  black coated straight jeans
--   belt    black classic pin-buckle
--   shoe    Ecco black nubuck

INSERT INTO fits (id, name, register_code, category_code, vetted, source, sort_order,
                  variant_set, variant_position) VALUES
('fit_sh_grey-tee',       'The Shawl, grey tee',       'everyday', 'casual', true,
 'brief-shawl-set-and-henley.md', 63, 'the_shawl', 2),
('fit_sh_black-tee',      'The Shawl, black tee',      'everyday', 'casual', true,
 'brief-shawl-set-and-henley.md', 64, 'the_shawl', 3),
('fit_sh_white-polo',     'The Shawl, white polo',     'everyday', 'casual', true,
 'brief-shawl-set-and-henley.md', 65, 'the_shawl', 4),
('fit_sh_pale-blue-polo', 'The Shawl, pale blue polo', 'everyday', 'casual', true,
 'brief-shawl-set-and-henley.md', 66, 'the_shawl', 5);

INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note) VALUES
('fit_sh_grey-tee','ben-sherman-aubergine-shawl','top',1,false,NULL),
('fit_sh_grey-tee','tees_02_grey-crew','base',1,false,NULL),
('fit_sh_grey-tee','trousers_11_black-coated-jeans','bottom',1,false,NULL),
('fit_sh_grey-tee','shoes_03_ecco-black-nubuck','shoe',1,false,NULL),
('fit_sh_grey-tee','belts_11_black-classic-pin-buckle','belt',1,false,NULL),

('fit_sh_black-tee','ben-sherman-aubergine-shawl','top',1,false,NULL),
('fit_sh_black-tee','tees_03_black-crew','base',1,false,NULL),
('fit_sh_black-tee','trousers_11_black-coated-jeans','bottom',1,false,NULL),
('fit_sh_black-tee','shoes_03_ecco-black-nubuck','shoe',1,false,NULL),
('fit_sh_black-tee','belts_11_black-classic-pin-buckle','belt',1,false,NULL),

('fit_sh_white-polo','ben-sherman-aubergine-shawl','top',1,false,NULL),
('fit_sh_white-polo','tops_09_white-pique-polo','base',1,false,NULL),
('fit_sh_white-polo','trousers_11_black-coated-jeans','bottom',1,false,NULL),
('fit_sh_white-polo','shoes_03_ecco-black-nubuck','shoe',1,false,NULL),
('fit_sh_white-polo','belts_11_black-classic-pin-buckle','belt',1,false,NULL),

('fit_sh_pale-blue-polo','ben-sherman-aubergine-shawl','top',1,false,NULL),
('fit_sh_pale-blue-polo','tops_01_pale-blue-pique-polo','base',1,false,NULL),
('fit_sh_pale-blue-polo','trousers_11_black-coated-jeans','bottom',1,false,NULL),
('fit_sh_pale-blue-polo','shoes_03_ecco-black-nubuck','shoe',1,false,NULL),
('fit_sh_pale-blue-polo','belts_11_black-classic-pin-buckle','belt',1,false,NULL);

-- Derived by running wardrobe/fit_derive.py over these exact garment lists — the
-- same functions the builder runs on save — and written out as literals so this
-- file still runs clean on an empty database. All five land identically:
-- cold/mild, work and casual, formality 3, and not rain-safe because the Ecco is
-- nubuck (rules-and-context.md §2 rule 13).

INSERT INTO fit_temp_bands (fit_id, band_code)
SELECT f.id, b.band FROM (VALUES
  ('fit_sh_grey-tee'),('fit_sh_black-tee'),
  ('fit_sh_white-polo'),('fit_sh_pale-blue-polo')) AS f(id),
  (VALUES ('cold'),('mild')) AS b(band);

INSERT INTO fit_seasons (fit_id, season_code)
SELECT f.id, s.season FROM (VALUES
  ('fit_sh_grey-tee'),('fit_sh_black-tee'),
  ('fit_sh_white-polo'),('fit_sh_pale-blue-polo')) AS f(id),
  (VALUES ('winter'),('autumn'),('spring')) AS s(season);

INSERT INTO fit_occasions (fit_id, occasion_code, kind)
SELECT f.id, o.occ, 'good' FROM (VALUES
  ('fit_sh_grey-tee'),('fit_sh_black-tee'),
  ('fit_sh_white-polo'),('fit_sh_pale-blue-polo')) AS f(id),
  (VALUES ('work'),('casual')) AS o(occ);

UPDATE fits SET rain_safe = false, formality_rank = 3
 WHERE id IN ('fit_sh_grey-tee','fit_sh_black-tee',
              'fit_sh_white-polo','fit_sh_pale-blue-polo');

INSERT INTO fit_field_sources (fit_id, field_name, source, note)
SELECT f.id, v.field, 'derived', 'brief-shawl-set-and-henley.md 2026-09-07'
FROM (VALUES
  ('fit_sh_grey-tee'),('fit_sh_black-tee'),
  ('fit_sh_white-polo'),('fit_sh_pale-blue-polo')) AS f(id),
  (VALUES ('temp_bands'),('seasons'),('good_for'),('rain_safe'),('formality_rank'))
    AS v(field);

-- ---------------------------------------------- position 1, folded in --
--
-- fit_the_shawl is the same outfit and has been since killer-looks.md, except
-- that nothing was ever logged UNDER the shawl. Adding the white crew tee makes
-- it position 1 rather than a sixth near-duplicate that would split the fit's
-- wear history in two.
--
-- This CHANGES A VETTED FIT'S COMPOSITION, which the fit_c6 case in the last
-- brief did not, so it is recorded: the garment list is now manual, and this
-- document says why.
--
-- Its optional waxed biker stays where it is and is NOT copied to the other
-- four. An optional outer belongs to the fit that offers it; five copies of it
-- would be five alternates nobody asked for.

INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note)
VALUES ('fit_the_shawl','tees_01_white-crew','base',1,false,
        'The tee under the shawl — logged 2026-09-07, it was always worn with one');

UPDATE fits
   SET variant_set = 'the_shawl', variant_position = 1
 WHERE id = 'fit_the_shawl';

INSERT INTO fit_field_sources (fit_id, field_name, source, note)
VALUES ('fit_the_shawl', 'composition', 'manual',
        'White crew tee added under the shawl as position 1 of the set — '
        'brief-shawl-set-and-henley.md 2026-09-07')
ON CONFLICT (fit_id, field_name) DO UPDATE
   SET source = EXCLUDED.source, note = EXCLUDED.note;

-- 079_stone_brown_and_beige_blue.sql — sets four and five, plus one crest read.
--
-- Source: brief-w5-w3-sets.md (2026-09-08).
--
-- Both sets have the same shape as the_shawl: a knit holds the `top` slot in all
-- five positions and what changes is the shirt or tee UNDER it, which is `base`.
-- No new code was needed for that — the varying garment has been defined as the
-- item unique to one member since 078, not as a fixed role.
--
-- Both knits are wool-family (Zara 100% cashmere; Tissaia 30% wool / 5%
-- cashmere), and every position of both sets carries a base, so the invariant in
-- tests/test_no_wool_next_to_skin.py holds without any special handling here.
-- That is the test doing its job quietly rather than the rule being remembered.

-- ---------------------------------------------------------- stone_brown --
--
-- Brown cashmere V over stone gingham. Position 4 is
-- fit_w5_brown-cashmere-and-gingham, which already has this exact composition,
-- so it is retagged and nothing else about it changes.

INSERT INTO fits (id, name, register_code, category_code, vetted, source, sort_order,
                  variant_set, variant_position) VALUES
('fit_sb_brown-stripe',    'Brown stripe under the brown V',    'everyday', 'warm', true,
 'brief-w5-w3-sets.md', 100, 'stone_brown', 1),
('fit_sb_pale-blue-twill', 'Pale blue twill under the brown V', 'everyday', 'warm', true,
 'brief-w5-w3-sets.md', 101, 'stone_brown', 2),
('fit_sb_pink-stripe',     'Pink stripe under the brown V',     'everyday', 'warm', true,
 'brief-w5-w3-sets.md', 102, 'stone_brown', 3),
('fit_sb_grey-tee',        'Grey tee under the brown V',        'everyday', 'warm', true,
 'brief-w5-w3-sets.md', 103, 'stone_brown', 5);

INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note) VALUES
('fit_sb_brown-stripe','zara-brown-cashmere-vneck','top',1,false,NULL),
('fit_sb_brown-stripe','tops_34_tm-lewin-brown-tan-multistripe-shirt','base',1,false,NULL),
('fit_sb_brown-stripe','trousers_06_stone-gingham','bottom',1,false,NULL),
('fit_sb_brown-stripe','shoes_04_churchs-apron-derby','shoe',1,false,NULL),
('fit_sb_brown-stripe','belts_02_tan-vera-pelle','belt',1,false,NULL),

('fit_sb_pale-blue-twill','zara-brown-cashmere-vneck','top',1,false,NULL),
('fit_sb_pale-blue-twill','tops_47_tm-lewin-blue-twill-shirt','base',1,false,NULL),
('fit_sb_pale-blue-twill','trousers_06_stone-gingham','bottom',1,false,NULL),
('fit_sb_pale-blue-twill','shoes_04_churchs-apron-derby','shoe',1,false,NULL),
('fit_sb_pale-blue-twill','belts_02_tan-vera-pelle','belt',1,false,NULL),

('fit_sb_pink-stripe','zara-brown-cashmere-vneck','top',1,false,NULL),
('fit_sb_pink-stripe','tops_12_paul-smith-pink-stripe-shirt','base',1,false,NULL),
('fit_sb_pink-stripe','trousers_06_stone-gingham','bottom',1,false,NULL),
('fit_sb_pink-stripe','shoes_04_churchs-apron-derby','shoe',1,false,NULL),
('fit_sb_pink-stripe','belts_02_tan-vera-pelle','belt',1,false,NULL),

('fit_sb_grey-tee','zara-brown-cashmere-vneck','top',1,false,NULL),
('fit_sb_grey-tee','tees_02_grey-crew','base',1,false,NULL),
('fit_sb_grey-tee','trousers_06_stone-gingham','bottom',1,false,NULL),
('fit_sb_grey-tee','shoes_04_churchs-apron-derby','shoe',1,false,NULL),
('fit_sb_grey-tee','belts_02_tan-vera-pelle','belt',1,false,NULL);

UPDATE fits SET variant_set = 'stone_brown', variant_position = 4
 WHERE id = 'fit_w5_brown-cashmere-and-gingham';

-- ----------------------------------------------------------- beige_blue --
--
-- Blue V over beige chino. The id prefix is fit_bb2_, because fit_bb_ already
-- belongs to beige_brown from 078 and two sets sharing a prefix would make
-- every LIKE 'fit_bb_%' query in a future migration quietly wrong.
--
-- Position 1 is fit_w3_blue-vneck-and-beige: same composition already, retag
-- only.

INSERT INTO fits (id, name, register_code, category_code, vetted, source, sort_order,
                  variant_set, variant_position) VALUES
('fit_bb2_grey-tee',    'Grey tee under the blue V',       'everyday', 'warm', true,
 'brief-w5-w3-sets.md', 104, 'beige_blue', 2),
('fit_bb2_pink-stripe', 'Pink stripe under the blue V',    'everyday', 'warm', true,
 'brief-w5-w3-sets.md', 105, 'beige_blue', 3),
('fit_bb2_provencal',   'Provencal print under the blue V','everyday', 'warm', true,
 'brief-w5-w3-sets.md', 106, 'beige_blue', 4),
('fit_bb2_red-tee',     'Red tee under the blue V',        'everyday', 'warm', true,
 'brief-w5-w3-sets.md', 107, 'beige_blue', 5);

INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note) VALUES
('fit_bb2_grey-tee','tissaia-blue-vneck','top',1,false,NULL),
('fit_bb2_grey-tee','tees_02_grey-crew','base',1,false,NULL),
('fit_bb2_grey-tee','trousers_01_decathlon-beige','bottom',1,false,NULL),
('fit_bb2_grey-tee','shoes_02_andre-tan-brogue','shoe',1,false,NULL),
('fit_bb2_grey-tee','belts_03_oxford-arlen-tan','belt',1,false,NULL),

('fit_bb2_pink-stripe','tissaia-blue-vneck','top',1,false,NULL),
('fit_bb2_pink-stripe','tops_12_paul-smith-pink-stripe-shirt','base',1,false,NULL),
('fit_bb2_pink-stripe','trousers_01_decathlon-beige','bottom',1,false,NULL),
('fit_bb2_pink-stripe','shoes_02_andre-tan-brogue','shoe',1,false,NULL),
('fit_bb2_pink-stripe','belts_03_oxford-arlen-tan','belt',1,false,NULL),

('fit_bb2_provencal','tissaia-blue-vneck','top',1,false,NULL),
('fit_bb2_provencal','tops_48_souleiado-cream-navy-geometric-print-shirt','base',1,false,NULL),
('fit_bb2_provencal','trousers_01_decathlon-beige','bottom',1,false,NULL),
('fit_bb2_provencal','shoes_02_andre-tan-brogue','shoe',1,false,NULL),
('fit_bb2_provencal','belts_03_oxford-arlen-tan','belt',1,false,NULL),

('fit_bb2_red-tee','tissaia-blue-vneck','top',1,false,NULL),
('fit_bb2_red-tee','tees_05_red-crew','base',1,false,NULL),
('fit_bb2_red-tee','trousers_01_decathlon-beige','bottom',1,false,NULL),
('fit_bb2_red-tee','shoes_02_andre-tan-brogue','shoe',1,false,NULL),
('fit_bb2_red-tee','belts_03_oxford-arlen-tan','belt',1,false,NULL);

UPDATE fits SET variant_set = 'beige_blue', variant_position = 1
 WHERE id = 'fit_w3_blue-vneck-and-beige';

-- --------------------------------------------------- derived metadata --
--
-- Derived with wardrobe/fit_derive.py over these exact garment lists and written
-- out as literals so this file runs clean on an empty database. Uniform within
-- each set: cold/mild, work and casual, rain-safe (leather soles, no nubuck).
-- Formality differs BETWEEN the sets — 4 for the Church's derby, 3 for the
-- Andre brogue — which is the shoe talking and is left alone.

INSERT INTO fit_temp_bands (fit_id, band_code)
SELECT f.id, b.band FROM (VALUES
  ('fit_sb_brown-stripe'),('fit_sb_pale-blue-twill'),('fit_sb_pink-stripe'),('fit_sb_grey-tee'),
  ('fit_bb2_grey-tee'),('fit_bb2_pink-stripe'),('fit_bb2_provencal'),('fit_bb2_red-tee')
) AS f(id), (VALUES ('cold'),('mild')) AS b(band);

INSERT INTO fit_seasons (fit_id, season_code)
SELECT f.id, s.season FROM (VALUES
  ('fit_sb_brown-stripe'),('fit_sb_pale-blue-twill'),('fit_sb_pink-stripe'),('fit_sb_grey-tee'),
  ('fit_bb2_grey-tee'),('fit_bb2_pink-stripe'),('fit_bb2_provencal'),('fit_bb2_red-tee')
) AS f(id), (VALUES ('winter'),('autumn'),('spring')) AS s(season);

INSERT INTO fit_occasions (fit_id, occasion_code, kind)
SELECT f.id, o.occ, 'good' FROM (VALUES
  ('fit_sb_brown-stripe'),('fit_sb_pale-blue-twill'),('fit_sb_pink-stripe'),('fit_sb_grey-tee'),
  ('fit_bb2_grey-tee'),('fit_bb2_pink-stripe'),('fit_bb2_provencal'),('fit_bb2_red-tee')
) AS f(id), (VALUES ('work'),('casual')) AS o(occ);

UPDATE fits SET rain_safe = true, formality_rank = 4
 WHERE id IN ('fit_sb_brown-stripe','fit_sb_pale-blue-twill','fit_sb_pink-stripe','fit_sb_grey-tee');

UPDATE fits SET rain_safe = true, formality_rank = 3
 WHERE id IN ('fit_bb2_grey-tee','fit_bb2_pink-stripe','fit_bb2_provencal','fit_bb2_red-tee');

INSERT INTO fit_field_sources (fit_id, field_name, source, note)
SELECT f.id, v.field, 'derived', 'brief-w5-w3-sets.md 2026-09-08'
FROM (VALUES
  ('fit_sb_brown-stripe'),('fit_sb_pale-blue-twill'),('fit_sb_pink-stripe'),('fit_sb_grey-tee'),
  ('fit_bb2_grey-tee'),('fit_bb2_pink-stripe'),('fit_bb2_provencal'),('fit_bb2_red-tee')
) AS f(id),
  (VALUES ('temp_bands'),('seasons'),('good_for'),('rain_safe'),('formality_rank')) AS v(field);

-- ------------------------------------------------ the crest, read properly --
--
-- `pattern` said "Club crest", derived, which is what the importer could tell
-- from a photograph. Max has now read the crest: it is Royal County Down. That
-- is an observation, not a derivation, so it goes in as manual and outranks
-- anything a later import would infer.
--
-- The other correction in the brief needs no migration and is recorded here so
-- nobody undoes it: tops_12_paul-smith-pink-stripe-shirt's card says "fine pink
-- and black stripe on white" and is CORRECT. The retail render shows only the
-- pink because the dark stripe is too fine to render. Do not regenerate it.
--
-- Likewise the five c10 renders (set stone_navy, if it is ever built) carry a
-- red-and-gold crest that is not the Royal County Down design — generated
-- against the old Retail file. Max has accepted them. Do not regenerate them.

UPDATE items
   SET pattern = 'Small red-and-gold club crest at the left chest, about 6cm — '
                 'red crown above a gold harp, flanked by crossed golf clubs and '
                 'gold-and-red ribbon banners. Royal County Down Golf Club.',
       updated_at = now()
 WHERE id = 'lyle-scott-club-navy-vneck';

INSERT INTO item_field_sources (item_id, field_name, source, note)
VALUES ('lyle-scott-club-navy-vneck', 'pattern', 'manual',
        'Crest read off the garment by Max — Royal County Down. '
        'brief-w5-w3-sets.md 2026-09-08')
ON CONFLICT (item_id, field_name) DO UPDATE
   SET source = EXCLUDED.source, note = EXCLUDED.note, updated_at = now();

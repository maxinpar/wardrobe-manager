-- 078_beige_brown_set.sql — the third variant set.
--
-- Source: brief-beige-brown-set.md (2026-09-07).
--
-- Unlayered: beige chino, distressed brown belt, brown Chelsea boot, and the
-- top changes. No outer at all, which the first two sets both had.
--
-- THIS SET IS THE ONE THAT BROKE THE VARIANT DETECTION, and it is worth writing
-- down why. Positions 2 and 5 are knitwear, so under the no-wool-next-to-skin
-- rule (077) they each carry a white crew tee as `base`. That makes the white
-- tee appear in TWO members — so "the item this member has that its siblings do
-- not" returns two candidates for each of them, the knit and the tee.
--
-- The strip label survived that by luck of ordering. The week rotation did not:
-- it would have rotated over seven entries for five looks, with the white tee
-- turning up twice as though it were a day of its own. The definition is now
-- "appears in exactly one member of the set", which is right for all three sets
-- and for any set built later.
--
-- Bands are NOT uniform across this set, unlike black_canvas and the_shawl: the
-- two knits derive cold/mild and the shirt and polo derive mild/warm. That is a
-- real difference and it is left alone — a set is five fits, not one fit with a
-- costume change, and the picker scores whichever variant is on today.

INSERT INTO fits (id, name, register_code, category_code, vetted, source, sort_order,
                  variant_set, variant_position) VALUES
('fit_bb_burgundy-crew', 'Burgundy crew & beige',  'everyday', 'casual', true,
 'brief-beige-brown-set.md', 90, 'beige_brown', 2),
('fit_bb_charcoal-shirt','Charcoal shirt & beige', 'everyday', 'casual', true,
 'brief-beige-brown-set.md', 91, 'beige_brown', 3),
('fit_bb_sage-polo',     'Sage polo & beige',      'everyday', 'casual', true,
 'brief-beige-brown-set.md', 92, 'beige_brown', 4),
('fit_bb_brown-vneck',   'Brown V-neck & beige',   'everyday', 'casual', true,
 'brief-beige-brown-set.md', 93, 'beige_brown', 5);

INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note) VALUES
-- Position 2: cashmere, so it takes a tee (077).
('fit_bb_burgundy-crew','polo-rl-burgundy-cashmere-crew','top',1,false,NULL),
('fit_bb_burgundy-crew','tees_01_white-crew','base',1,false,'No wool next to skin'),
('fit_bb_burgundy-crew','trousers_01_decathlon-beige','bottom',1,false,NULL),
('fit_bb_burgundy-crew','shoes_07_oxford-brown-chelsea','shoe',1,false,NULL),
('fit_bb_burgundy-crew','belts_04_distressed-brown-everyday','belt',1,false,NULL),

('fit_bb_charcoal-shirt','tops_31_zara-charcoal-textured-shirt','top',1,false,NULL),
('fit_bb_charcoal-shirt','trousers_01_decathlon-beige','bottom',1,false,NULL),
('fit_bb_charcoal-shirt','shoes_07_oxford-brown-chelsea','shoe',1,false,NULL),
('fit_bb_charcoal-shirt','belts_04_distressed-brown-everyday','belt',1,false,NULL),

('fit_bb_sage-polo','tops_05_sage-pique-polo','top',1,false,NULL),
('fit_bb_sage-polo','trousers_01_decathlon-beige','bottom',1,false,NULL),
('fit_bb_sage-polo','shoes_07_oxford-brown-chelsea','shoe',1,false,NULL),
('fit_bb_sage-polo','belts_04_distressed-brown-everyday','belt',1,false,NULL),

-- Position 5: cashmere again, same reason.
('fit_bb_brown-vneck','zara-brown-cashmere-vneck','top',1,false,NULL),
('fit_bb_brown-vneck','tees_01_white-crew','base',1,false,'No wool next to skin'),
('fit_bb_brown-vneck','trousers_01_decathlon-beige','bottom',1,false,NULL),
('fit_bb_brown-vneck','shoes_07_oxford-brown-chelsea','shoe',1,false,NULL),
('fit_bb_brown-vneck','belts_04_distressed-brown-everyday','belt',1,false,NULL);

-- Derived with wardrobe/fit_derive.py over these exact garment lists and written
-- out as literals, so this file still runs clean on an empty database.

INSERT INTO fit_temp_bands (fit_id, band_code) VALUES
('fit_bb_burgundy-crew','cold'), ('fit_bb_burgundy-crew','mild'),
('fit_bb_brown-vneck','cold'),   ('fit_bb_brown-vneck','mild'),
('fit_bb_charcoal-shirt','mild'),('fit_bb_charcoal-shirt','warm'),
('fit_bb_sage-polo','mild'),     ('fit_bb_sage-polo','warm');

INSERT INTO fit_seasons (fit_id, season_code) VALUES
('fit_bb_burgundy-crew','winter'), ('fit_bb_burgundy-crew','autumn'), ('fit_bb_burgundy-crew','spring'),
('fit_bb_brown-vneck','winter'),   ('fit_bb_brown-vneck','autumn'),   ('fit_bb_brown-vneck','spring'),
('fit_bb_charcoal-shirt','autumn'),('fit_bb_charcoal-shirt','spring'),('fit_bb_charcoal-shirt','summer'),
('fit_bb_sage-polo','autumn'),     ('fit_bb_sage-polo','spring'),     ('fit_bb_sage-polo','summer');

INSERT INTO fit_occasions (fit_id, occasion_code, kind)
SELECT f.id, o.occ, 'good' FROM (VALUES
  ('fit_bb_burgundy-crew'),('fit_bb_charcoal-shirt'),
  ('fit_bb_sage-polo'),('fit_bb_brown-vneck')) AS f(id),
  (VALUES ('work'),('casual')) AS o(occ);

-- Rain-safe, unlike the first two sets: the Chelsea boot is leather, not the
-- Ecco nubuck.
UPDATE fits SET rain_safe = true, formality_rank = 3
 WHERE id IN ('fit_bb_burgundy-crew','fit_bb_charcoal-shirt',
              'fit_bb_sage-polo','fit_bb_brown-vneck');

INSERT INTO fit_field_sources (fit_id, field_name, source, note)
SELECT f.id, v.field, 'derived', 'brief-beige-brown-set.md 2026-09-07'
FROM (VALUES
  ('fit_bb_burgundy-crew'),('fit_bb_charcoal-shirt'),
  ('fit_bb_sage-polo'),('fit_bb_brown-vneck')) AS f(id),
  (VALUES ('temp_bands'),('seasons'),('good_for'),('rain_safe'),('formality_rank'))
    AS v(field);

-- ------------------------------------------- position 1, a pure retag --
--
-- fit_k4_navy-knit-and-beige already has exactly this composition. Nothing else
-- about it changes: no new fit_items, no rename, no re-source. Its navy knit
-- polo is categorised Tops and is not wool, so 077 does not touch it either.
UPDATE fits
   SET variant_set = 'beige_brown', variant_position = 1
 WHERE id = 'fit_k4_navy-knit-and-beige';

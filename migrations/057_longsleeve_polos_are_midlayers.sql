-- 057_longsleeve_polos_are_midlayers.sql
-- 2026-09-01. Reverts the CATEGORY half of migration 056. Keeps the neckline correction.
--
--   tops_100_footjoy-charcoal-purple-stripe-polo -> footjoy-charcoal-purple-stripe-longsleeve
--   tops_101_footjoy-pale-blue-polo              -> footjoy-pale-blue-longsleeve
--   Tops -> Knitwear, in both cases.
--
-- WHY. Migration 056 established that both garments have a spread polo collar and a two-button
-- placket rather than a quarter-zip. That much is right and stands. It then moved both to Tops on
-- the reasoning that a polo belongs with the polos. Max corrected that: he wears both ON TOP of a
-- short-sleeve polo, because Sydney is warm enough that a long-sleeve polo is never the base
-- layer. Their ROLE is mid-layer, so Knitwear is where the picker should find them - the same
-- reasoning that already puts anko-black-quarterzip-fleece in Knitwear rather than with the tops.
--
-- Construction says polo; use says mid-layer; the catalogue is organised for use. Migration 056
-- read the construction and stopped there.
--
-- The ids no longer claim a closure either way. They said "quarterzip" (wrong), then "polo"
-- (right about construction, misleading about role). "longsleeve" is accurate on both counts and
-- is the final name - the neckline is recorded in neck_raw and cut, where it belongs.
--
-- Photo and render files have been moved back on Drive from \Shirts to \Knitwear and renamed.
-- Delete-and-reinsert again, for the same reason as 054 and 056; both guarded below.

DO $$
DECLARE ids text[] := ARRAY['tops_100_footjoy-charcoal-purple-stripe-polo','tops_101_footjoy-pale-blue-polo'];
BEGIN
  IF EXISTS (SELECT 1 FROM fit_items WHERE item_id = ANY(ids))
  OR EXISTS (SELECT 1 FROM wear_event_items WHERE item_id = ANY(ids))
  OR EXISTS (SELECT 1 FROM week_days WHERE top_item_id = ANY(ids))
  OR EXISTS (SELECT 1 FROM gap_replaces WHERE item_id = ANY(ids))
  OR EXISTS (SELECT 1 FROM fit_preconditions WHERE item_id = ANY(ids))
  THEN RAISE EXCEPTION 'dependency appeared - repoint, do not delete';
  END IF;
END $$;

DELETE FROM items WHERE id IN ('tops_100_footjoy-charcoal-purple-stripe-polo','tops_101_footjoy-pale-blue-polo');

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, neck_code, neck_raw, cut,
                   material, weight_code, formality_raw, formality_rank, formality_note, fit,
                   condition, verdict_code, verdict_note, scope_code, works_alone, pairs, layer,
                   avoid, notes, no_photo, photo_prefix, retail_prefix, warmth, rain_unsafe,
                   pattern, unconfirmed) VALUES

('footjoy-charcoal-purple-stripe-longsleeve','footjoy-charcoal-purple-stripe-longsleeve','Knitwear',
 'FootJoy charcoal purple-stripe long-sleeve','Charcoal with a fine purple stripe','#3B3E50',
 'Anchor dark','polo collar','polo collar',
 'LONG-SLEEVE POLO worn as a mid-layer - spread collar, two-button placket, fine allover stripe',
 'Technical jersey','Light','Casual',3,'Tonal purple crowned RSGC crest on the left chest',
 'Size S - correct for FootJoy','Good from the flat-lay','Keep',
 'Dark and quiet; the purple only shows up close, which is what makes it wearable.',
 'core',false,'Navy, stone, charcoal, white',
 'Goes OVER a short-sleeve polo. In Sydney it is never the base layer - Max confirmed 2026-09-01',
 'Purple or charcoal bottoms',
 'FOOTJOY, size S. Long-sleeve polo with a spread collar and a two-button placket, worn as a mid-layer over a short-sleeve polo. Fine purple stripe on charcoal.',
 false,'footjoy-charcoal-purple-stripe-longsleeve','footjoy-charcoal-purple-stripe-longsleeve_retail',
 2,false,'Fine stripe',false),

('footjoy-pale-blue-longsleeve','footjoy-pale-blue-longsleeve','Knitwear',
 'FootJoy pale blue long-sleeve','Pale blue','#C0D6F1','Pale blue','polo collar','polo collar',
 'LONG-SLEEVE POLO worn as a mid-layer - spread collar, two-button placket, plain body',
 'Technical jersey','Light','Casual',3,'Small tonal white crowned RSGC crest on the left chest',
 'Size M. FootJoy fits Max at S, so this runs a size large','Good from the flat-lay','Keep',
 'Plain and pale, and the only light blue long-sleeve he owns. The crest is tonal and quiet.',
 'core',false,'Navy, stone, charcoal, white',
 'Goes OVER a short-sleeve polo - see footjoy-charcoal-purple-stripe-longsleeve',
 'Pale blue bottoms',
 'FOOTJOY, size M. Long-sleeve polo with a spread collar and a two-button placket, worn as a mid-layer.',
 false,'footjoy-pale-blue-longsleeve','footjoy-pale-blue-longsleeve_retail',
 2,false,'Plain',true);

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('footjoy-charcoal-purple-stripe-longsleeve','golf'),
('footjoy-pale-blue-longsleeve','golf')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('footjoy-charcoal-purple-stripe-longsleeve','hex','derived','MEASURED against the white table in the same frame, 2026-09-01, migration 050 method.'),
('footjoy-pale-blue-longsleeve','hex','derived','MEASURED against the white table in the same frame, 2026-09-01, migration 050 method.'),
('footjoy-charcoal-purple-stripe-longsleeve','neck_raw','manual','Spread polo collar with a two-button placket, NOT a quarter-zip. Migration 053 called it a quarter-zip from a 440px contact sheet, where an open polo placket and an open quarter-zip placket look the same. Corrected off the full-resolution neck shot in migration 056.'),
('footjoy-charcoal-purple-stripe-longsleeve','cat_code','manual','Knitwear, not Tops. Migration 056 moved it to Tops because it is constructed as a polo. Max corrected that on 2026-09-01: he wears it OVER a short-sleeve polo - Sydney is warm enough that a long-sleeve polo is never his base layer - so its role is mid-layer and the picker should find it with the knits, as anko-black-quarterzip-fleece already is. Lesson: this catalogue is organised by how a garment is USED, not by how it is cut. Ask what goes under it before choosing a category.'),
('footjoy-pale-blue-longsleeve','neck_raw','manual','Spread polo collar with a two-button placket, not a quarter-zip. See footjoy-charcoal-purple-stripe-longsleeve.'),
('footjoy-pale-blue-longsleeve','cat_code','manual','Knitwear, not Tops. See footjoy-charcoal-purple-stripe-longsleeve.')
ON CONFLICT DO NOTHING;

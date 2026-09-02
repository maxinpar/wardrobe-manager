-- 056_two_golf_polos_miscatalogued_as_quarterzips.sql
-- 2026-09-01. Two garments in migration 053 are long-sleeve POLOS, not quarter-zips.
--
--   footjoy-charcoal-purple-stripe-quarterzip  ->  tops_100_footjoy-charcoal-purple-stripe-polo
--   footjoy-pale-blue-quarterzip               ->  tops_101_footjoy-pale-blue-polo
--
-- WHAT HAPPENED. Both were read off a contact sheet at 440px, where an open polo placket and an
-- open quarter-zip placket look identical. Both garments in fact have a spread polo collar and a
-- two-button placket, unmistakable at full resolution in PXL_20260831_071840016 and _072137293.
--
-- CAUGHT BY THE RENDERS AGAIN. Both retail renders came back with polo collars and buttons. I
-- zoomed the original neck shots intending to show the renders were wrong. They were right. That
-- is the fourth time in this batch a render was correct and the catalogue row was not, after
-- outerwear_16 (rain jacket read as a windshirt), outerwear_18 (jacket read as a vest) and
-- outerwear_19/20 (a crest recorded as absent).
--
-- THE STANDING LESSON, now four times over: a 440px contact sheet is enough to COUNT garments and
-- to cluster a shoot. It is not enough to assert neckline, sleeve count, closure or chest
-- embroidery. Those need the frame at full resolution, or a question to Max. Cheap to check,
-- expensive to get wrong - each of these took a migration to undo.
--
-- CATEGORY MOVES TOO. These are golf polos and belong with the other forty-odd in Tops, on the
-- tops_NN convention, not in Knitwear on the slug convention. Photo files have been moved on
-- Drive from Wardrobe Photos\Knitwear to \Shirts and renamed to the new prefixes; both renders
-- are filed. As in migration 054 there is no ON UPDATE CASCADE on items.id, so each row is
-- deleted and re-inserted. Both were created today and neither appears in a fit, wear event,
-- week plan or gap - guarded below.

DO $$
DECLARE ids text[] := ARRAY['footjoy-charcoal-purple-stripe-quarterzip','footjoy-pale-blue-quarterzip'];
BEGIN
  IF EXISTS (SELECT 1 FROM fit_items WHERE item_id = ANY(ids))
  OR EXISTS (SELECT 1 FROM wear_event_items WHERE item_id = ANY(ids))
  OR EXISTS (SELECT 1 FROM week_days WHERE top_item_id = ANY(ids))
  OR EXISTS (SELECT 1 FROM gap_replaces WHERE item_id = ANY(ids))
  OR EXISTS (SELECT 1 FROM fit_preconditions WHERE item_id = ANY(ids))
  THEN RAISE EXCEPTION 'one of the two polos now has a dependency - repoint, do not delete';
  END IF;
END $$;

DELETE FROM items WHERE id IN ('footjoy-charcoal-purple-stripe-quarterzip','footjoy-pale-blue-quarterzip');

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, neck_code, neck_raw, cut,
                   material, weight_code, formality_raw, formality_rank, formality_note, fit,
                   condition, verdict_code, verdict_note, scope_code, works_alone, pairs, layer,
                   avoid, notes, no_photo, photo_prefix, retail_prefix, warmth, rain_unsafe,
                   pattern, unconfirmed) VALUES

('tops_100_footjoy-charcoal-purple-stripe-polo','footjoy-charcoal-purple-stripe-polo','Tops',
 'FootJoy charcoal purple-stripe long-sleeve polo','Charcoal with a fine purple stripe','#3B3E50',
 'Anchor dark','polo collar','polo collar',
 'LONG-SLEEVE POLO - spread collar, two-button placket, fine allover stripe',
 'Technical jersey','Light','Casual',3,'Tonal purple crowned RSGC crest on the left chest',
 'Size S - correct for FootJoy','Good from the flat-lay','Keep',
 'Dark and quiet; the purple only shows up close, which is what makes it wearable. Catalogued in migration 053 as a quarter-zip - it is a polo.',
 'core',true,'Navy, stone, charcoal, white','Under a knit or a vest','Purple or charcoal bottoms',
 'FOOTJOY, size S. Long-sleeve polo with a two-button placket. Fine purple stripe on charcoal.',
 false,'tops_100_footjoy-charcoal-purple-stripe-polo','tops_100_footjoy-charcoal-purple-stripe-polo_retail',
 2,false,'Fine stripe',false),

('tops_101_footjoy-pale-blue-polo','footjoy-pale-blue-polo','Tops',
 'FootJoy pale blue long-sleeve polo','Pale blue','#C0D6F1','Pale blue','polo collar','polo collar',
 'LONG-SLEEVE POLO - spread collar, two-button placket, plain body',
 'Technical jersey','Light','Casual',3,'Small tonal white crowned RSGC crest on the left chest',
 'Size M. FootJoy fits Max at S, so this runs a size large','Good from the flat-lay','Keep',
 'Plain and pale, and the only light blue long-sleeve polo he owns. The crest is tonal and quiet. Catalogued in migration 053 as a quarter-zip - it is a polo.',
 'core',true,'Navy, stone, charcoal, white','Under a knit or a vest','Pale blue bottoms',
 'FOOTJOY, size M. Long-sleeve polo with a two-button placket, plain pale blue body.',
 false,'tops_101_footjoy-pale-blue-polo','tops_101_footjoy-pale-blue-polo_retail',
 2,false,'Plain',true);

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('tops_100_footjoy-charcoal-purple-stripe-polo','golf'),
('tops_101_footjoy-pale-blue-polo','golf')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('tops_100_footjoy-charcoal-purple-stripe-polo','hex','derived','MEASURED against the white table in the same frame, 2026-09-01, migration 050 method.'),
('tops_101_footjoy-pale-blue-polo','hex','derived','MEASURED against the white table in the same frame, 2026-09-01, migration 050 method.'),
('tops_100_footjoy-charcoal-purple-stripe-polo','neck_raw','manual','CLOSURE CORRECTED 2026-09-01. Catalogued in migration 053 as a quarter-zip in Knitwear, read from a 440px contact sheet where an open polo placket and an open quarter-zip placket are indistinguishable. It is a long-sleeve polo with a spread collar and a two-button placket, plain at full resolution. Re-filed to Tops as tops_100; photos moved from Wardrobe Photos\Knitwear to \Shirts.'),
('tops_101_footjoy-pale-blue-polo','neck_raw','manual','CLOSURE CORRECTED 2026-09-01. As tops_100 - a long-sleeve polo, not a quarter-zip. Re-filed to Tops as tops_101.')
ON CONFLICT DO NOTHING;

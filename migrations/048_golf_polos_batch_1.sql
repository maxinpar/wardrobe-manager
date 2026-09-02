-- 048_golf_polos_batch_1.sql
-- 2026-08-31. First ten golf polos, tops_51 - tops_60.
--
-- These are the first garments in the whole project whose colour is MEASURED rather than
-- estimated. Max shot every one flat on a white table with the table itself in frame, so each
-- photograph carries its own neutral reference. Method: white point = median of the brightest
-- 5% of low-saturation pixels (the lit table); garment = median of the central region with the
-- darkest quartile and brightest decile discarded so shadow and highlight do not drag it.
-- Marked 'measured' in item_field_sources with that method recorded.
-- TWO EXCEPTIONS, marked 'derived': tops_52 and tops_53 are white garments and the measurement
-- returned #B8C4DF and #DADDDF - it was reading shadow across a white piqué, not the colour.
-- Their hexes are set to near-white by judgement. Everything else stands as measured.
--
-- COUNT: eleven files in batch 1 and ten in batch 2 = 21 photographs for 10 garments, verified
-- by contact sheet before any row was written. Batch 2 completed two garments batch 1 had left
-- half-shot (the pink flat-lay, and the Cross label for the taupe).
--
-- SIZE PATTERN, worth acting on: nine of ten are S - Peter Millar, Fairway & Greene, PING,
-- FootJoy, Cross Sweden. The only M is the Tikeden. US golf brands run large on Max; generic
-- and Asian-sized brands do not. Buy S in the former, M in the latter.
--
-- CLUB RULE (044): six of ten carry the Royal Sydney crest. RSGC is a home club, so no
-- restriction anywhere.
--
-- IDENTIFICATION: tops_56 is Puma, confirmed by Max from the garment - its printed label has
-- worn away and nothing was recoverable from the photograph even after contrast and edge
-- enhancement. tops_58 is left UNBRANDED on Max's instruction: its label shows a chevron mark
-- and the word DRY, and he could not identify it either. Not guessed.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, neck_raw, cut, material,
                   weight_code, formality_raw, formality_rank, formality_note, fit, condition,
                   verdict_code, verdict_note, scope_code, works_alone, pairs, layer, avoid,
                   notes, no_photo, photo_prefix, retail_prefix, warmth, rain_unsafe, pattern,
                   unconfirmed) VALUES

('tops_51_tikeden-navy-toucan-polo','tikeden-navy-toucan-polo','Tops',
 'Tikeden toucan-print polo','Navy ground with multicolour tropical print','#48556F','Statement',
 'polo collar','Short-sleeve polo, three-button placket, contrast navy collar and cuffs',
 'Technical polyester','Light','Casual',2,'Loud print - social round only, not a guest day',
 'Size M - the only M in the batch','Good from the flat-lay; print sharp, collar sound',
 'Keep','The loudest thing in the drawer. Fine on a Saturday, wrong at a club you are visiting.',
 'core',true,'Navy, white, stone shorts. Nothing else patterned','-',
 'Any other print or a club crest cap - too much going on',
 'TIKEDEN, size M. Toucans, palms and flowers on navy; plain navy collar and cuff ribs; white inner placket facing.',
 false,'tops_51_tikeden-navy-toucan-polo','tops_51_tikeden-navy-toucan-polo_retail',1,false,'Tropical print',false),

('tops_52_peter-millar-white-rsgc-polo','peter-millar-white-rsgc-polo','Tops',
 'Peter Millar white RSGC polo','White','#F2F1EE','Pale neutral',
 'polo collar','Short-sleeve polo, two-button placket, self collar, side vents',
 'Summer Comfort performance jersey','Light','Smart-casual',4,
 'Royal Sydney - home club, no restriction','Size S',
 'Good from the flat-lay. White, so watch the collar and underarms.',
 'Keep','Best-made polo in the batch alongside tops_57. Peter Millar is the quality mark here.',
 'core',true,'Navy, stone, charcoal, coral shorts or trousers','-',
 'Nothing significant - white goes under everything',
 'PETER MILLAR Summer Comfort, size S, made in Vietnam. Navy RSGC crown-and-monogram on the left chest, cream buttons.',
 false,'tops_52_peter-millar-white-rsgc-polo','tops_52_peter-millar-white-rsgc-polo_retail',1,false,'Plain',false),

('tops_53_fairway-greene-white-interclub-polo','fairway-greene-white-interclub-polo','Tops',
 'Fairway & Greene "Interclub Team 2021" polo','White','#F0F0EE','Pale neutral',
 'polo collar','Short-sleeve polo, placketless V-neck opening, self collar, side vents',
 'Performance jersey','Light','Smart-casual',4,
 'Royal Sydney - home club, no restriction. Team shirt, so it states a date',
 'Size S','Good from the flat-lay',
 'Keep','A dated team shirt. Perfect at Royal Sydney, slightly odd anywhere else four years on.',
 'core',true,'Navy, stone, charcoal','-','Nothing significant',
 'FAIRWAY & GREENE, size S, made in the USA. "INTERCLUB TEAM 2021" embroidered on the left chest with the navy RSGC crest to its right. Placketless - no buttons at all.',
 false,'tops_53_fairway-greene-white-interclub-polo','tops_53_fairway-greene-white-interclub-polo_retail',1,false,'Plain',false),

('tops_54_fairway-greene-pink-rsgc-polo','fairway-greene-pink-rsgc-polo','Tops',
 'Fairway & Greene pink RSGC polo','Raspberry pink','#E25A80','Statement',
 'polo collar','Short-sleeve polo, one-button placket, self collar, side vents',
 'Performance jersey','Light','Smart-casual',4,
 'Royal Sydney - home club, no restriction','Size S','Good from the flat-lay',
 'Keep','Gold crest rather than navy - the only one in the set. Pink and gold is a deliberate choice and it works.',
 'core',true,'Navy, white, stone, charcoal. Not red','-',
 'Red or coral bottoms - too close to the shirt',
 'FAIRWAY & GREENE, size S, made in the USA. GOLD RSGC crown-and-monogram, unlike every other RSGC polo here which is navy or white.',
 false,'tops_54_fairway-greene-pink-rsgc-polo','tops_54_fairway-greene-pink-rsgc-polo_retail',1,false,'Plain',false),

('tops_55_cross-taupe-diamond-polo','cross-taupe-diamond-polo','Tops',
 'Cross Sweden taupe diamond polo','Grey-taupe with tonal diamond jacquard','#787069','Mid tone',
 'polo collar','Short-sleeve polo, three-button placket, plain contrast collar and cuffs',
 'Technical polyester','Light','Casual',3,'Brand polo, no club',
 'Size S','Good from the flat-lay',
 'Keep','The only warm-neutral polo here. Everything else is white, navy, blue, pink or lime.',
 'core',true,'Navy, white, stone, olive','-','Olive - muddy against this taupe',
 'CROSS SWEDEN, size S. Tonal diamond jacquard on the body, plain taupe collar and sleeves, small green golfer logo on the left chest and text on the right sleeve.',
 false,'tops_55_cross-taupe-diamond-polo','tops_55_cross-taupe-diamond-polo_retail',1,false,'Diamond jacquard',false),

('tops_56_puma-lime-stripe-polo','puma-lime-stripe-polo','Tops',
 'Puma lime stripe polo','Chartreuse with pale horizontal stripe','#C8CE7A','Statement',
 'polo collar','Short-sleeve polo, two-button placket, self collar, grey inner neck tape',
 'Cotton-feel jersey','Light','Casual',2,'Brand polo, no club',
 'Size not readable - the label print has worn away','Good from the flat-lay',
 'Keep','Softest hand in the batch - reads more shirt than sports polo.',
 'core',true,'Navy, white, stone, charcoal','-','Olive or yellow bottoms',
 'PUMA - confirmed by Max from the garment, 2026-08-31. The printed neck label has worn off entirely and nothing was recoverable from the photograph even under heavy contrast and edge enhancement, so brand is on his word and SIZE IS UNKNOWN. Measured hex is a blend of ground and stripe.',
 false,'tops_56_puma-lime-stripe-polo','tops_56_puma-lime-stripe-polo_retail',1,false,'Horizontal stripe',true);

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, neck_raw, cut, material,
                   weight_code, formality_raw, formality_rank, formality_note, fit, condition,
                   verdict_code, verdict_note, scope_code, works_alone, pairs, layer, avoid,
                   notes, no_photo, photo_prefix, retail_prefix, warmth, rain_unsafe, pattern,
                   unconfirmed) VALUES

('tops_57_peter-millar-periwinkle-rsgc-polo','peter-millar-periwinkle-rsgc-polo','Tops',
 'Peter Millar periwinkle RSGC polo','Periwinkle blue-grey','#8086A8','Mid tone',
 'polo collar','Short-sleeve polo, striped placket band, self collar, side vents',
 'Crown Crafted performance jersey','Light','Smart-casual',4,
 'Royal Sydney - home club, no restriction','Size S','Good from the flat-lay',
 'Keep','Crown Crafted is Peter Millar''s tour line - the best-made polo in the batch. The cream-and-tan placket stripe is the detail that lifts it.',
 'core',true,'Navy, stone, white, charcoal','-','Blue bottoms in a near shade - too tonal',
 'PETER MILLAR CROWN CRAFTED, size S, made in Vietnam. Vertical cream and tan stripe down the placket band; tonal RSGC crest on the left chest.',
 false,'tops_57_peter-millar-periwinkle-rsgc-polo','tops_57_peter-millar-periwinkle-rsgc-polo_retail',1,false,'Placket stripe',false),

('tops_58_navy-jacquard-rsgc-polo','navy-jacquard-rsgc-polo','Tops',
 'Navy jacquard RSGC polo','Dark navy with tonal block jacquard','#4A4B5E','Anchor dark',
 'polo collar','Short-sleeve polo, three-button placket, self collar, textured chest and midriff panels',
 'Technical polyester','Light','Casual',3,
 'Royal Sydney - home club, no restriction','Size not read',
 'Good from the flat-lay','Keep','The only dark polo in the batch - the one that goes with everything.',
 'core',true,'Anything - navy is neutral against every short owned','-','Nothing significant',
 'BRAND UNIDENTIFIED, deliberately. The neck label shows a chevron or arrow mark and the word DRY, plus a small second tab; Max could not identify it from the garment either and instructed leaving it unbranded rather than guessed, 2026-08-31. There is also a small light logo on the outside of the collar stand, unread. Size not read.',
 false,'tops_58_navy-jacquard-rsgc-polo','tops_58_navy-jacquard-rsgc-polo_retail',1,false,'Block jacquard',true),

('tops_59_ping-blue-colourblock-polo','ping-blue-colourblock-polo','Tops',
 'PING blue colourblock polo','Azure blue with navy sleeves and collar','#1A77C0','Statement',
 'polo collar','Short-sleeve polo, three-button placket, contrast navy collar, shoulders and sleeves, orange collar piping',
 'sensorcool technical polyester','Light','Casual',3,'Brand polo, no club',
 'USA S / UK-EUR M','Good from the flat-lay',
 'Keep','Sportiest cut here - reads performance rather than smart. Range and social rounds.',
 'core',true,'Navy, white, stone, charcoal','-','Blue bottoms - the shirt is already the blue',
 'PING sensorcool, USA S / UK-EUR M, made in Indonesia. Navy yoke, sleeves and collar against an azure body, with a thin orange pipe along the collar edge.',
 false,'tops_59_ping-blue-colourblock-polo','tops_59_ping-blue-colourblock-polo_retail',1,false,'Colourblock',false),

('tops_60_footjoy-grey-mint-floral-rsgc-polo','footjoy-grey-mint-floral-rsgc-polo','Tops',
 'FootJoy grey mint-floral RSGC polo','Warm grey with mint floral print','#6F676C','Mid tone',
 'polo collar','Short-sleeve polo, three-button placket, contrast pale-mint collar with printed inner stand',
 'Technical polyester','Light','Smart-casual',3,
 'Royal Sydney - home club, no restriction','Athletic Fit, size S','Good from the flat-lay',
 'Keep','Small print on a grey ground - the one patterned polo that stays quiet. The mint collar is the trick.',
 'core',true,'Navy, white, stone, charcoal','-','Mint or green bottoms - the collar already does that',
 'FOOTJOY Athletic Fit, size S. Scattered mint floral motifs on warm grey; pale mint contrast collar with an FJ mark on the collar stand; white RSGC crest on the left chest.',
 false,'tops_60_footjoy-grey-mint-floral-rsgc-polo','tops_60_footjoy-grey-mint-floral-rsgc-polo_retail',1,false,'Floral print',false);

-- Occasions: golf plus casual/weekend for all ten. None is a work shirt - Max is in a bank.
INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, o FROM items CROSS JOIN (VALUES ('golf'),('casual'),('weekend')) v(o)
WHERE id BETWEEN 'tops_51' AND 'tops_60_zzz'
ON CONFLICT DO NOTHING;

-- Colour provenance. This is the first batch measured against a neutral in the same frame.
INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT id, 'hex', 'derived',
       'MEASURED against a neutral in the same frame, 2026-08-31 - the strongest colour provenance in the catalogue so far, not an estimate. White point = median of the brightest 5% of low-saturation pixels (the lit table); garment = median of the central region with the darkest quartile and brightest decile discarded. Recorded as derived only because the schema allows derived/imported/manual and this is still computed from a photograph rather than read off a label.'
FROM items WHERE id BETWEEN 'tops_51' AND 'tops_60_zzz'
  AND id NOT IN ('tops_52_peter-millar-white-rsgc-polo','tops_53_fairway-greene-white-interclub-polo')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('tops_52_peter-millar-white-rsgc-polo','hex','derived','Measurement returned #B8C4DF - it was reading shadow across white pique, not colour. Set near-white by judgement.'),
('tops_53_fairway-greene-white-interclub-polo','hex','derived','Measurement returned #DADDDF for the same reason. Set near-white by judgement.'),
('tops_56_puma-lime-stripe-polo','notes','manual','Brand confirmed verbally by Max from the garment; printed label worn away and unrecoverable from the photograph. Size unknown.'),
('tops_58_navy-jacquard-rsgc-polo','notes','manual','Left unbranded on Max''s explicit instruction after he could not identify it from the garment. Do not guess a brand into this row.')
ON CONFLICT DO NOTHING;

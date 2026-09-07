-- 069_brown_polo_and_three_sunglasses.sql
-- 2026-09-06. Four garments: one polo and the first three pairs of sunglasses in the catalogue.
--
-- NAMES are Max's, taken verbatim from the folders he filed: "Good Good Brown polo",
-- "Fat Sunnies", "French Sunnies Light", "French Sunnies Dark".
--
-- SUNGLASSES go to Accessories at his instruction, continuing accessories_00 - _03. They are
-- the first non-textile items in the catalogue, so several columns do not apply: neck, layer
-- and rain are left null or false and weight is recorded as Fine to keep the sort sane.
--
-- COLOUR, measured off each render with white excluded:
--   accessories_04  #5E5B5C, blue-minus-red -2   - neutral near-black. Black frames.
--   accessories_05  #7E786A, blue-minus-red -20  - warm mid brown. Light tortoiseshell.
--   accessories_06  #70695B, blue-minus-red -21  - the same warm hue, darker.
-- 05 and 06 share a hue and differ mainly in depth, which is consistent with one French frame
-- in two lens tints rather than two unrelated pairs. Recorded as a LIKELY pair, not asserted -
-- the frames were never examined.
--
-- ⚠️ tops_101 HAS NO RENDER. "GG Brown Render.jpeg" measures #9D9B99, blue-minus-red -4,
-- red-minus-green +2 - dead neutral grey, with dominant bands #A8A8A8 and #C0C0C0. There is no
-- brown in it. This is the exact failure documented in CLAUDE.md under RENDERS, so the file was
-- NOT filed to Retail and retail_prefix is left null. Regenerate it before the next app build.
--
-- ⚠️ ONE tops_101 SOURCE FRAME LOOKS WRONG. PXL_20260906_010704667, filed as _02_label,
-- measures #426FA7, blue-minus-red +101 - overwhelmingly saturated blue, unlike anything else
-- in the set. It may be a mis-sorted frame or a screen. Filed as shot; check it.
--
-- WHAT HAS NOT BEEN READ. None of the seventeen source frames were opened - they are on the
-- laptop and were filed by name and timestamp order only. Brand, size, material, frame markings
-- and lens type are therefore UNKNOWN for all four rows and are not asserted. Every row is
-- unconfirmed = true.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, neck_raw, cut, material,
                   weight_code, formality_raw, formality_rank, formality_note, fit, condition,
                   verdict_code, verdict_note, scope_code, works_alone, pairs, layer, avoid,
                   notes, no_photo, photo_prefix, retail_prefix, warmth, rain_unsafe, pattern,
                   unconfirmed) VALUES

('tops_101_goodgood-brown-polo','tops_101_goodgood-brown-polo','Tops','Good Good Brown polo',
 'Brown - not measured, the render came out neutral',NULL,'Warm neutral','polo',
 'Short-sleeve polo','NOT READ - label frame not examined','Light','Casual',3,
 'Good Good is a young golf-media brand, no club crest',
 'NOT READ - label frame not examined. The other Good Good piece, goodgood-green-stripe-quarterzip, is a MEDIUM',
 'Not assessed - source frames not examined','Keep',
 'Filed on Max''s naming only. No render and no measured colour yet.',
 'core',true,'Navy, stone, white or charcoal bottoms','Under a quarter-zip or a knit',
 'Brown or tan bottoms',
 'RENDER REJECTED: "GG Brown Render.jpeg" measures dead neutral grey (#9D9B99) with no brown in it, so it was not filed. Regenerate. Also check source frame _02_label - it measures a saturated blue (#426FA7) unlike the rest of the set and may be mis-sorted. Same brand as goodgood-green-stripe-quarterzip.',
 false,'tops_101_goodgood-brown-polo',NULL,1,false,'Plain',true),

('accessories_04_fat-sunglasses','accessories_04_fat-sunglasses','Accessories','Fat Sunnies',
 'Black','#5E5B5C','Anchor dark',NULL,
 'Sunglasses - heavy/chunky frame, hence Max''s name for them','NOT READ - frames not examined',
 'Fine','Casual',3,'No branding read',
 'NOT READ','Not assessed - source frames not examined','Keep',
 'Filed on Max''s naming and the render. Five source frames, none opened.',
 'core',true,'Anything - a black frame is the neutral of the three','Worn, not layered',NULL,
 'MEASURED near-neutral off the render: #5E5B5C, blue-minus-red -2. Brand, lens type and frame material all unread. The chunkiest of the three pairs by Max''s name for them.',
 false,'accessories_04_fat-sunglasses','accessories_04_fat-sunglasses_retail',1,false,'Plain',true),

('accessories_05_french-sunglasses-light','accessories_05_french-sunglasses-light','Accessories','French Sunnies Light',
 'Warm mid brown - light tortoiseshell','#7E786A','Warm neutral',NULL,
 'Sunglasses - lighter lens of what looks like a matched French pair','NOT READ - frames not examined',
 'Fine','Casual',3,'No branding read',
 'NOT READ','Not assessed - source frames not examined','Keep',
 'Filed on Max''s naming and the render. Four source frames, none opened.',
 'core',true,'Brown, tan, stone, navy','Worn, not layered',NULL,
 'MEASURED #7E786A, blue-minus-red -20 - a warm brown. LIKELY the same frame as accessories_06 in a lighter lens: same hue, different depth. Not confirmed - the frames were never examined.',
 false,'accessories_05_french-sunglasses-light','accessories_05_french-sunglasses-light_retail',1,false,'Plain',true),

('accessories_06_french-sunglasses-dark','accessories_06_french-sunglasses-dark','Accessories','French Sunnies Dark',
 'Warm brown, darker - dark tortoiseshell','#70695B','Warm neutral',NULL,
 'Sunglasses - darker lens of what looks like a matched French pair','NOT READ - frames not examined',
 'Fine','Casual',3,'No branding read',
 'NOT READ','Not assessed - source frames not examined','Keep',
 'Filed on Max''s naming and the render. Four source frames, none opened.',
 'core',true,'Brown, tan, stone, navy','Worn, not layered',NULL,
 'MEASURED #70695B, blue-minus-red -21 - the same warm hue as accessories_05, darker. LIKELY the same frame in a darker lens. Not confirmed.',
 false,'accessories_06_french-sunglasses-dark','accessories_06_french-sunglasses-dark_retail',1,false,'Plain',true);

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('tops_101_goodgood-brown-polo','golf'),
('tops_101_goodgood-brown-polo','casual'),
('accessories_04_fat-sunglasses','casual'),
('accessories_04_fat-sunglasses','weekend'),
('accessories_04_fat-sunglasses','golf'),
('accessories_05_french-sunglasses-light','casual'),
('accessories_05_french-sunglasses-light','weekend'),
('accessories_05_french-sunglasses-light','golf'),
('accessories_06_french-sunglasses-dark','casual'),
('accessories_06_french-sunglasses-dark','weekend'),
('accessories_06_french-sunglasses-dark','golf');

INSERT INTO item_actions (item_id, required, status, note) VALUES
('tops_101_goodgood-brown-polo','Regenerate the retail render','pending',
 'The 2026-09-06 render came back neutral grey (#9D9B99), no brown. Not filed.'),
('tops_101_goodgood-brown-polo','Check source frame _02_label','pending',
 'Measures #426FA7, a saturated blue unlike the rest of the set. Possibly mis-sorted.');

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('tops_101_goodgood-brown-polo','name','manual','Named by Max, 2026-09-06.'),
('tops_101_goodgood-brown-polo','hex','derived','Left null - the only render available measures neutral grey.'),
('accessories_04_fat-sunglasses','name','manual','Named by Max, 2026-09-06.'),
('accessories_04_fat-sunglasses','hex','derived','Measured off the render, white excluded.'),
('accessories_05_french-sunglasses-light','name','manual','Named by Max, 2026-09-06.'),
('accessories_05_french-sunglasses-light','hex','derived','Measured off the render, white excluded.'),
('accessories_06_french-sunglasses-dark','name','manual','Named by Max, 2026-09-06.'),
('accessories_06_french-sunglasses-dark','hex','derived','Measured off the render, white excluded.');

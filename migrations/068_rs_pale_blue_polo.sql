-- 068_rs_pale_blue_polo.sql
-- 2026-09-06. One garment: the RS Pale Blue polo. First item to cross into tops_100.
--
-- NAME. "RS Pale Blue polo", given by Max. RS = Royal Sydney, his home club.
--
-- COLOUR. Measured off the render, white background excluded: mean #AFB8DD, dominant band
-- #A8A8D8, blue-minus-red +46 with green-minus-red only +9. A pale blue with a clear violet
-- cast - periwinkle, not sky blue.
--
-- NOT A DUPLICATE OF tops_57. tops_57_peter-millar-periwinkle-rsgc-polo measures #8086A8, a
-- mid periwinkle blue-grey. This one is materially paler and more violet. Separate garment.
--
-- WHAT HAS NOT BEEN READ. The three source frames (flat-lay, back-neck label, chest crest)
-- were filed without being examined - they are on the laptop and were never opened. So brand,
-- label size, material, collar and placket detail, and the exact crest are all UNKNOWN and are
-- not asserted here. Size is left blank rather than assumed from the club-polo pattern, even
-- though every other RSGC polo in the catalogue is a size S. Row is unconfirmed = true until
-- someone reads the label frame.
--
-- USE. Golf, on the club-polo pattern, but not yet confirmed by Max. Occasion tag is golf only.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, neck_raw, cut, material,
                   weight_code, formality_raw, formality_rank, formality_note, fit, condition,
                   verdict_code, verdict_note, scope_code, works_alone, pairs, layer, avoid,
                   notes, no_photo, photo_prefix, retail_prefix, warmth, rain_unsafe, pattern,
                   unconfirmed) VALUES

('tops_100_rs-pale-blue-polo','tops_100_rs-pale-blue-polo','Tops','RS Pale Blue polo',
 'Pale periwinkle blue','#A8A8D8','Pale blue','polo',
 'Short-sleeve polo',
 'NOT READ - label frame not examined','Light','Smart-casual',4,
 'Royal Sydney club polo - home club, no restriction',
 'NOT READ - label frame not examined. Every other RSGC polo in the catalogue is a size S',
 'Not assessed - source frames not examined','Keep',
 'Filed on Max''s naming and the render only. Verdict provisional: nothing has been read off the garment itself.',
 'core',true,'Navy, stone, white or charcoal bottoms','Under a quarter-zip or a knit',
 'Blue or lilac bottoms',
 'BRAND NOT READ. Three source frames filed 2026-09-06 - flat-lay, back-neck label, chest crest - none opened. Colour measured off the render. Distinct from tops_57_peter-millar-periwinkle-rsgc-polo, which is a darker periwinkle.',
 false,'tops_100_rs-pale-blue-polo','tops_100_rs-pale-blue-polo_retail',1,false,'Plain',true);

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('tops_100_rs-pale-blue-polo','golf');

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('tops_100_rs-pale-blue-polo','name','manual','Named "RS Pale Blue polo" by Max, 2026-09-06.'),
('tops_100_rs-pale-blue-polo','hex','derived','Measured off the render, white excluded: #A8A8D8, blue-minus-red +46.'),
('tops_100_rs-pale-blue-polo','material','derived','Placeholder - label frame not examined.'),
('tops_100_rs-pale-blue-polo','fit','derived','Placeholder - label frame not examined.');

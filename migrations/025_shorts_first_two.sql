-- 025_shorts_first_two.sql
-- The first two entries in the new Shorts category, 2026-08-30. These are the pair Max
-- photographed to test whether shorts could be rendered at all; round 4 of the prompt work
-- produced house-style renders, so they go into the catalogue proper.
--
-- Everything below is read off the garment photos and the sewn care labels. Nothing about
-- how often he wears them, what he wears them for, or how he feels about them has been
-- established yet, so both rows are unconfirmed = true and the verdict notes say so rather
-- than inventing a judgement from a photo. Confirm usage, then rewrite verdict_note / pairs /
-- avoid and clear the flag.

INSERT INTO items (id, slug, cat_code, name, colour, hex, material, cut, formality_raw,
                   formality_rank, fit, condition, verdict_code, verdict_note, scope_code,
                   works_alone, pairs, layer, avoid, notes, no_photo, photo_prefix,
                   retail_prefix, rain_unsafe, pattern, unconfirmed) VALUES

('shorts_01_zara-tan-chino','zara-tan-chino','Shorts','Zara tan chino short',
 'Mustard tan','#C08F45','Cotton twill','Chino, flat front','Casual',2,'EUR44 / US34',
 'Used - softly faded, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photos and label only; verdict pending.',
 'core',true,'To confirm.','-','To confirm.',
 'BASIC ZARA MAN, EUR44 / USA34 / MEX34, made in Turkey. Flat front, belt loops, zip fly with a dark metal shank button, slash side pockets, plain hem, no turn-up. Bermuda length. Waist matches his usual W33-34.',
 false,'shorts_01_zara-tan-chino','shorts_01_zara-tan-chino',false,'Plain',true),

('shorts_02_blush-poly','blush-poly','Shorts','Blush technical short',
 'Pale blush / sandy pink-beige','#D8C4B8','100% polyester','Flat front','Casual',2,'38',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Reads as a golf or performance short - technical polyester, contrast striped inner waistband - but that is inference from construction, not from Max. Verdict pending. Also note the size.',
 'core',true,'To confirm.','-','To confirm.',
 'No brand label photographed - only the care label: 100% polyester, made in China, size 38. Flat front, belt loops, zip fly, single button, slash side pockets, plain hem. Inner waistband facing striped green / orange-red / black. SIZE FLAG: 38 is two sizes above his usual W33-34 - confirm whether these actually fit or are loose.',
 false,'shorts_02_blush-poly','shorts_02_blush-poly',false,'Plain',true);

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('shorts_01_zara-tan-chino','weekend'),
('shorts_01_zara-tan-chino','casual'),
('shorts_02_blush-poly','weekend'),
('shorts_02_blush-poly','casual')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_01_zara-tan-chino','notes','manual','Brand, size and country read off the sewn waistband label, 2026-08-30.'),
('shorts_02_blush-poly','notes','manual','Size and fibre content read off the sewn care label, 2026-08-30. No brand label was photographed - brand deliberately left blank rather than guessed.'),
('shorts_02_blush-poly','occasions','manual','Golf NOT tagged: construction suggests it, Max has not said so. Add once confirmed.')
ON CONFLICT DO NOTHING;

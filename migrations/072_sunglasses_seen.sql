-- 072_sunglasses_seen.sql
-- 2026-09-06. Adds accessories_07 and corrects 04, 05 and 06 now that all four have been LOOKED AT.
--
-- Migration 069 catalogued the first three pairs from pixel statistics without opening a single
-- frame. Every one of the three colour descriptions was wrong, in the same way: the whole-image
-- mean blends frame and lens into one number, and sunglasses are two materials. Corrected here
-- from the renders and, for 07, the source frames as well.
--
-- THE THREE FRENCH PAIRS ARE ONE FRAME IN THREE FINISHES. Same round keyhole panto shape, same
-- keyhole bridge, same temple profile:
--     05  blond / light tortoiseshell   + dark green lenses
--     06  dark, richer tortoiseshell    + dark green lenses
--     07  translucent honey acetate front, tortoiseshell temples + PALE AMBER lenses
-- Migration 069 guessed 05 and 06 were "one frame in two lens tints". Half right: the lenses are
-- the same, the FRAME colour differs. 07 is the one that actually differs by lens - Max's name
-- for it, "super light", is about the tint, and it is the only pair here you can see eyes through.
--
-- 04 IS NOT BLACK. It is a chunky flat-top square in a dark woodgrain-effect brown-grey, with
-- dark grey lenses and a brand plaque on the temple. #5E5B5C measured near-neutral because the
-- woodgrain is a dark warm grey, not because the frame is black.
--
-- BRANDS STILL NOT READ on any of the four. No maker mark is legible in any frame. Not asserted.
-- Everything else here was seen, so the unconfirmed flags come off.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, neck_raw, cut, material,
                   weight_code, formality_raw, formality_rank, formality_note, fit, condition,
                   verdict_code, verdict_note, scope_code, works_alone, pairs, layer, avoid,
                   notes, no_photo, photo_prefix, retail_prefix, warmth, rain_unsafe, pattern,
                   unconfirmed) VALUES

('accessories_07_french-sunglasses-super-light','accessories_07_french-sunglasses-super-light','Accessories','French Sunnies Super Light',
 'Translucent honey acetate front with tortoiseshell temples, pale amber lenses','#C9AB87','Warm neutral',NULL,
 'Round keyhole panto sunglasses - the same frame shape as accessories_05 and _06','Acetate',
 'Fine','Casual',3,'No maker mark legible in any frame',
 'NOT READ','Good - frames clean, lenses unscratched in all four frames','Keep',
 'The only pair of the three French frames with a light tint, so the only one that works indoors, at dusk, or anywhere someone needs to see his eyes. That is a real difference from 05 and 06, not a third version of the same thing.',
 'core',true,'Warm neutrals - tan, stone, olive, brown. Also fine with navy','Worn, not layered',
 'Nothing - a translucent honey frame is quiet enough for anything',
 'MEASURED off the render, white excluded: #C9AB87, red-minus-green +30, blue-minus-red -66 - a clear warm amber. Translucent honey acetate front, tortoiseshell temples with amber and yellow flecks, pale amber lenses. Same round keyhole panto shape as accessories_05 and _06. Four source frames read 2026-09-06; no brand mark visible on the frame front, temples or bridge. Render checks out against the frames, though it renders the lenses a shade more yellow than the photos do.',
 false,'accessories_07_french-sunglasses-super-light','accessories_07_french-sunglasses-super-light_retail',1,false,'Tortoiseshell',false);

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('accessories_07_french-sunglasses-super-light','casual'),
('accessories_07_french-sunglasses-super-light','weekend'),
('accessories_07_french-sunglasses-super-light','golf');

UPDATE items SET
    colour = 'Dark woodgrain-effect brown-grey with dark grey lenses',
    cut = 'Chunky flat-top square sunglasses - much heavier than the three French panto frames',
    pattern = 'Woodgrain effect',
    notes = 'MEASURED #5E5B5C off the render. NOT BLACK: migration 069 called it black on that near-neutral reading alone. Looked at 2026-09-06 - the frame is a dark woodgrain-effect brown-grey, flat-top square, with dark grey lenses and a brand plaque on the temple. Brand still not legible. The heavy one, hence Max''s name for it.',
    verdict_note = 'The only non-panto pair. Its weight and flat top make it the outlier of the four, and the one that reads most like a statement.',
    unconfirmed = false
WHERE id = 'accessories_04_fat-sunglasses';

UPDATE items SET
    colour = 'Blond / light tortoiseshell with dark green lenses',
    cut = 'Round keyhole panto sunglasses - the same frame shape as accessories_06 and _07',
    pattern = 'Tortoiseshell',
    notes = 'Blond, light tortoiseshell acetate with DARK GREEN lenses. Migration 069 called this "warm mid brown" from a whole-image mean, which averaged the tortoiseshell frame with the green lens. Looked at 2026-09-06. Same frame shape as accessories_06 (darker tortoiseshell, same green lens) and accessories_07 (honey front, amber lens). Brand not legible.',
    unconfirmed = false
WHERE id = 'accessories_05_french-sunglasses-light';

UPDATE items SET
    colour = 'Dark tortoiseshell with dark green lenses',
    cut = 'Round keyhole panto sunglasses - the same frame shape as accessories_05 and _07',
    pattern = 'Tortoiseshell',
    notes = 'Dark, richly mottled tortoiseshell acetate with DARK GREEN lenses - the same lens as accessories_05, a darker frame. Migration 069 guessed these two were one frame in two lens tints; it is the other way round. Looked at 2026-09-06. Brand not legible.',
    unconfirmed = false
WHERE id = 'accessories_06_french-sunglasses-dark';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('accessories_07_french-sunglasses-super-light','name','manual','Named "French Sunnies Super Light" by Max, 2026-09-06.'),
('accessories_07_french-sunglasses-super-light','hex','derived','Measured off the render, white excluded: #C9AB87.'),
('accessories_07_french-sunglasses-super-light','colour','imported','Read from the four source frames and the render, 2026-09-06.');

UPDATE item_field_sources SET source = 'imported',
    note = 'Corrected 2026-09-06 after looking at the render. The 069 value came from a whole-image mean that blended frame and lens.'
WHERE item_id IN ('accessories_04_fat-sunglasses','accessories_05_french-sunglasses-light','accessories_06_french-sunglasses-dark')
  AND field_name = 'hex';

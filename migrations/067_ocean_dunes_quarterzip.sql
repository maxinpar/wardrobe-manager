-- 067_ocean_dunes_quarterzip.sql
-- 2026-09-06. One garment: the adidas ClimaWarm Ocean Dunes quarter-zip.
--
-- SOURCE. Four frames sent by Max into the chat on 2026-09-06: hanger flat-lay, back-neck
-- label, left-chest embroidery close-up, left-sleeve adidas mark. They are chat-only captures
-- and are NOT yet on Drive - see claude/photo-status.md. Photos rows are added by
-- import_photos.py once the frames and the render are filed, not here.
--
-- IDENTITY. adidas ClimaWarm, adidasgolf.com, size S/P read off the back-neck label. Slate blue
-- body with a cream shoulder yoke and chest panel, quarter-zip stand collar. Embroidered
-- "Ocean Dunes / King Island" with a gold flag-and-dunes device on the left chest; adidas
-- performance mark on the right chest and a rubberised adidas mark on the left sleeve.
--
-- COLOUR. Measured off the hanger frame against the white table: body #333F59, blue-minus-red
-- +38, so a real slate blue and not a neutral. The yoke reads cream / ecru.
--
-- SIZING. S/P is CORRECT, not small. The batch-053 rule holds: US golf brands fit Max at S.
-- Calvin Klein Golf S/P sits in the same category on the same rule.
--
-- NAME. Max named it "Ocean Dunes quarterzip" - the app name is his, keep it. Ocean Dunes is
-- at Cape Wickham, King Island: a visiting club, so a souvenir crest. Under the migration 050
-- crossover test a visiting-club crest keeps the garment on the course; that decides occasion
-- tags only and is not a bin test.
--
-- USE. Confirmed by Max, not inferred: he wears it for golf. Golf occasion only.
--
-- SECOND OCEAN DUNES PIECE. tops_96_adidas-ocean-dunes-white-polo is the same club, a separate
-- garment, no link between the rows.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, neck_raw, cut, material,
                   weight_code, formality_raw, formality_rank, formality_note, fit, condition,
                   verdict_code, verdict_note, scope_code, works_alone, pairs, layer, avoid,
                   notes, no_photo, photo_prefix, retail_prefix, warmth, rain_unsafe, pattern,
                   unconfirmed) VALUES

('adidas-ocean-dunes-quarterzip','adidas-ocean-dunes-quarterzip','Knitwear','Ocean Dunes quarterzip',
 'Slate blue with a cream shoulder yoke','#333F59','Anchor dark','quarter-zip',
 'Long-sleeve quarter-zip, cream contrast shoulder yoke and chest panel, stand collar, brushed back',
 'adidas ClimaWarm brushed-back technical jersey','Mid','Casual',2,
 'Ocean Dunes King Island crest, left chest - a visiting club, so a souvenir piece. On the course only.',
 'Size S/P. adidas Golf is a US golf brand and fits Max at S, so this is the correct size',
 'Good from the flat-lay','Keep',
 'Golf mid-layer, worn as such - confirmed by Max. Warmer than the plain quarter-zips thanks to the brushed ClimaWarm back, so it is the one to reach for on a cold morning round.',
 'core',true,'Navy, stone, white or charcoal bottoms','Over a golf polo',
 'Cream, stone or pale-blue bottoms - too close to the yoke',
 'adidas ClimaWarm, adidasgolf.com, size S/P. Cream yoke across the shoulders and upper chest. Embroidered Ocean Dunes / King Island with a gold flag device, left chest; adidas mark right chest and rubberised adidas mark on the left sleeve. Same club as tops_96_adidas-ocean-dunes-white-polo, separate garment.',
 false,'adidas-ocean-dunes-quarterzip','adidas-ocean-dunes-quarterzip_retail',4,false,'Colourblock',false);

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('adidas-ocean-dunes-quarterzip','golf');

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('adidas-ocean-dunes-quarterzip','name','manual','Named "Ocean Dunes quarterzip" by Max, 2026-09-06.'),
('adidas-ocean-dunes-quarterzip','verdict_note','manual','Max stated he wears it for golf, 2026-09-06.'),
('adidas-ocean-dunes-quarterzip','hex','derived','Sampled from the hanger frame, blue-minus-red +38.'),
('adidas-ocean-dunes-quarterzip','fit','derived','Batch-053 sizing rule: US golf brands fit Max at S.');

-- 060_golf_belts.sql
-- 2026-09-01. Golf belts. 4 garments, belts_13 - belts_16, 11 photographs and 4 retail renders.
--
-- COUNT. 11 frames shot 06:26-06:28 UTC in the belt pattern from photo-filing-guide.md - buckle,
-- full strap, underside stamp. Four belts: 3 + 4 + 2 + 2 frames. Both Pumas got an extra frame.
--
-- RENDERS ARRIVED WITH THE PHOTOGRAPHS and all four are accurate: correct buckle, correct strap,
-- correct underside stamp, correct colour family. Checked against the originals before filing,
-- which is now standing practice after the outerwear batch. A fifth file in the render folder,
-- Gemini_Generated_Image_63knax63knax63kn.jpeg, is BYTE-IDENTICAL to Teal Puma.jpeg (same md5)
-- and was not filed - one file per prefix.
--
-- COLOUR. Measured with the flat-lay method fixed in migration 059: white reference = median of
-- the brightest 3% of the whole frame, no saturation filter. Belts are narrow, so the garment
-- sample is the top 45% most-saturated pixels inside a hand-set box on the strap rather than a
-- central patch - a centre crop on a belt frame is mostly table.
--
-- TWO MEASUREMENT NOTES, both recorded rather than smoothed over:
--   belts_13 read #30344A off the shadowed coil and #444963 off the top surface in good light.
--   The value kept is the lit one. Either way it is an INDIGO VIOLET, hue 230, and it is bluer
--   than its own render, which leans purple. The render is close enough to file; the hex is not
--   taken from it.
--   belts_15 read a washed-out #FF9455 in the frame whose white point measured strongly blue
--   (147,187,217), and #FF9528 in the frame lit neutrally. The neutral frame is kept.
--
-- SIZES. Both Pumas are stamped L / 100 cm, Genuine Leather, Made in China. 100cm is about 39in
-- against Max's 34-36in, but these are plate-buckle belts, made to be cut to length - not
-- recorded as oversized without checking whether they have already been trimmed.
--
-- ONE THING TO CONFIRM, NOT ASSUMED. belts_15 has a GREY REFLECTIVE STRIPE down the centre of the
-- webbing. That is a hi-vis feature, and Max rides a motorbike (see outerwear_02). It was sent in
-- a folder called "Golf belts" so it is tagged golf, but if it is actually bike kit the occasion
-- tags are one migration away from correct. Flagged, not decided - the 2026-08-24 outerwear
-- session is the precedent for asking rather than reading purpose off an object.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, cut, material, weight_code,
                   formality_raw, formality_rank, formality_note, fit, condition, verdict_code,
                   verdict_note, scope_code, works_alone, pairs, layer, avoid, notes, no_photo,
                   photo_prefix, retail_prefix, warmth, rain_unsafe, pattern, unconfirmed) VALUES

('belts_13_puma-indigo-violet','puma-indigo-violet','Belts','Puma indigo-violet golf belt',
 'Indigo violet','#444963','Anchor dark',
 'Leather belt with a rectangular Puma plate buckle; violet face, brown reverse','Genuine leather',
 'Mid','Casual',2,'Large Puma cat plate buckle - a logo buckle, which is sport styling',
 'Stamped L / 100 cm','Good from the photographs','Keep',
 'One of a pair of Puma plate-buckle belts, this one and belts_14. Colour is a muted indigo violet rather than a true purple.',
 'core',true,'Navy, stone, white, grey trousers','-','Brown leather - this is a cool-toned belt',
 'PUMA. Underside stamped "L / 100 cm, Genuine Leather, MADE IN CHINA" with the Puma cat. Brown leather reverse. MEASURED #444963 off the lit top surface; the shadowed coil reads #30344A. Hue 230 - bluer than its own render, which leans purple.',
 false,'belts_13_puma-indigo-violet','belts_13_puma-indigo-violet_retail',1,false,'Plain',false),

('belts_14_puma-teal','puma-teal','Belts','Puma teal golf belt','Teal','#207F9A','Statement',
 'Leather belt with a shield-shaped ribbed Puma plate buckle; teal face, brown reverse',
 'Genuine leather','Mid','Casual',2,'Large Puma cat plate buckle - sport styling',
 'Stamped L / 100 cm','Good from the photographs','Keep',
 'The better of the two Pumas to look at - the teal is a real colour rather than a muddy one, and the shield buckle is less blunt than the rectangular plate on belts_13.',
 'core',true,'Navy, stone, white, grey trousers','-','Teal or green trousers',
 'PUMA. Underside stamped "L / 100 cm, Genuine Leather, MADE IN CHINA" with the Puma cat. Brown leather reverse. MEASURED #207F9A, hue 193.',
 false,'belts_14_puma-teal','belts_14_puma-teal_retail',1,false,'Plain',false),

('belts_15_orange-reflective-webbing','orange-reflective-webbing','Belts',
 'Orange reflective webbing belt','Orange with a grey reflective centre stripe','#FF9528','Statement',
 'Woven webbing belt, eyeleted, gunmetal frame buckle with a black leather tab',
 'Synthetic webbing with a reflective stripe','Light','Casual',2,
 'No brand mark anywhere. Woven webbing, which per migration 050 is not in itself a golf signal',
 'Eyeleted webbing - adjustable','Good from the photographs','Keep',
 'The only one of the four with no logo on it. Bright, but a webbing belt is a webbing belt - the same reasoning that let belts_08 cross over.',
 'core',true,'Navy, stone, white, charcoal trousers','-','Orange or red trousers',
 'BRAND UNKNOWN and deliberately blank - no maker mark in either frame. A GREY REFLECTIVE STRIPE runs down the centre of the webbing. That is a hi-vis feature and Max rides a motorbike; it arrived in a folder marked golf belts and is tagged accordingly, but the purpose is worth confirming.',
 false,'belts_15_orange-reflective-webbing','belts_15_orange-reflective-webbing_retail',1,false,'Stripe',true),

('belts_16_purple-plastic','purple-plastic','Belts','Purple plastic golf belt','Purple','#6D4172',
 'Statement','Moulded plastic/rubber belt with a matching translucent plastic pin buckle',
 'Moulded plastic or rubber','Light','Casual',1,
 'No brand mark. A moulded plastic belt reads as sport or novelty rather than town',
 'Punched holes - adjustable','Good from the photographs','Keep',
 'The most disposable thing in the batch, and the only belt in the wardrobe that is not leather or webbing. Fine on a course, wrong everywhere else.',
 'core',true,'Navy, stone, white, grey trousers','-','Purple or burgundy trousers',
 'BRAND UNKNOWN and deliberately blank - no maker mark in either frame. Moulded plastic strap and buckle in the same purple. MEASURED #6D4172, hue 294.',
 false,'belts_16_purple-plastic','belts_16_purple-plastic_retail',1,false,'Plain',true)

ON CONFLICT (id) DO NOTHING;

-- Occasions. All four are golf.
INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, 'golf' FROM items WHERE id BETWEEN 'belts_13' AND 'belts_16_zzz'
ON CONFLICT DO NOTHING;

-- One crosses over. belts_15 carries no logo at all, and migration 050 already established with
-- belts_08 that woven webbing is not a golf signal. Orange is loud, but loud is not sport.
-- The two Pumas keep golf only: a large cat plate buckle is a logo monogram, which is sport
-- styling under the migration 050 test. belts_16 keeps golf only on the same test - a moulded
-- plastic belt reads as sport wherever it is worn.
INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, o FROM items CROSS JOIN (VALUES ('casual'),('weekend')) v(o)
WHERE id = 'belts_15_orange-reflective-webbing'
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT id, 'hex', 'derived',
       'MEASURED 2026-09-01, migration 059 method: white reference = median of the brightest 3 percent of the whole frame, no saturation filter. Belt sample = the top 45 percent most-saturated pixels inside a hand-set box on the strap, because a centre crop on a belt frame is mostly table.'
FROM items WHERE id BETWEEN 'belts_13' AND 'belts_16_zzz'
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('belts_13_puma-indigo-violet','hex','manual','Two readings from the same belt: #30344A off the shadowed coil, #444963 off the lit top surface. The lit one is kept. Both give hue 230, an indigo violet - measurably BLUER than this item''s own retail render, which leans purple. The render was still filed: buckle, strap and underside stamp are all correct and the difference is a shade, not an identity. The hex is not taken from the render.'),
('belts_15_orange-reflective-webbing','hex','manual','Read #FF9455 in the frame whose white point measured strongly blue (147,187,217) and #FF9528 in the neutrally lit frame. The neutral frame is kept. A blue-cast white reference over-corrects a warm colour - worth remembering as the counterpart to migration 059, where the same cast made a grey read white.'),
('belts_15_orange-reflective-webbing','notes','manual','GREY REFLECTIVE STRIPE down the centre of the webbing. Hi-vis, and Max rides a motorbike (outerwear_02, outerwear_05). It arrived in a folder called "Golf belts" and is tagged golf on that basis alone. If it is actually bike kit, the occasion tags are one migration from correct. Flagged rather than decided - purpose was not read off the object.'),
('belts_15_orange-reflective-webbing','notes','manual','BRAND UNKNOWN and deliberately blank. No maker mark appears in either frame. Do not guess one in.'),
('belts_16_purple-plastic','notes','manual','BRAND UNKNOWN and deliberately blank. No maker mark appears in either frame.'),
('belts_13_puma-indigo-violet','fit','manual','Stamped L / 100 cm, about 39in against Max''s 34-36in. Plate-buckle belts of this type are sold long and cut to length, so this is NOT recorded as oversized - it may already have been trimmed. Confirm before acting on it.'),
('belts_14_puma-teal','fit','manual','Stamped L / 100 cm. See belts_13.')
ON CONFLICT DO NOTHING;

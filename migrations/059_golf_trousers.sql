-- 059_golf_trousers.sql
-- 2026-09-01. Golf trousers. 6 garments, trousers_18 - trousers_23, 18 photographs.
--
-- SHOT TWICE. Flat-lays in Downloads\Golf-trousers 06:22-06:25 UTC, then a second set of
-- close-ups at 06:38-06:40 after the first set proved unmeasurable. Chronological order is
-- identical across both shoots, confirmed by perceptual hash rather than assumed.
--
-- COLOUR — WHY THE FIRST PASS FAILED, AND THE FIX. On the first flat-lays the standard method
-- returned a near-white grey, an electric-cyan green and a hot-pink red. Two causes, both mine:
--   1. The white reference was taken from LOW-SATURATION pixels. In these frames the white table
--      itself carries a colour cast strong enough to measure 10-25% saturated, so the filter threw
--      the table away and kept dimmer neutral clutter - white points landed between 81 and 132
--      where the frame's own 99th-percentile luminance was 200-229.
--   2. On the pale grey pair the garment IS the low-saturation majority, so it became its own
--      white reference. That is the migration 048 failure repeating in a new place.
-- THE FIX, used here: take the white reference as the median of the BRIGHTEST 3% OF THE WHOLE
-- FRAME, with no saturation filter at all. On a flat-lay it is always the table, because every
-- garment photographed is darker than the surface under it. White points then came in at 180-233
-- across all six, consistent and all cool by +22 to +46 blue-minus-red, which is this room.
-- Nothing here was set by judgement; nothing was guessed after the measurement disagreed.
--
-- THE THREE FOOTJOYS ARE THE SAME NAVY. trousers_18 #404455, _20 #3C3E4F, _23 #3E4155 - within
-- four points of each other on every channel, and indistinguishable side by side. The first pass
-- called _23 "blue-grey" from a flat-lay under different light. It is not a different colour; it
-- is a different WEAVE, a fine horizontal pique against the smooth twill of the other two.
--
-- SIZES, all read at full resolution. Max is W33-34 / EU44.
--   trousers_18 W36/L32 - two up      trousers_19 EU44 / US M - correct
--   trousers_20 W32/L32 - the slim one, and the one he wears
--   trousers_21 EU44 / US M - correct  trousers_22 36/34 - two up in both waist and leg
--   trousers_23 W36/L32 - two up
-- Max, unprompted and before any of this was catalogued: "the last two are fairly large cuts,
-- one of the blue ones is a slim fit". Both statements check out exactly against the labels.
--
-- OWNER VERDICTS, stated 2026-09-01 and taken as given:
--   trousers_19 and trousers_21 are his favourites - "very thin fabric, perfect for Sydney
--   winters or mid seasons, and they rock". Both are DECATHLON/INESIS, the same house as
--   trousers_17 - the one golf garment in the wardrobe that already carries work + casual +
--   weekend + golf, and the model case in golf-crossover.md. The two he reaches for are from the
--   line that already proved itself off the course; the three he is lukewarm on are the technical
--   FootJoys. That is the crossover buying rule confirming itself from the other direction.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, cut, material, weight_code,
                   formality_raw, formality_rank, formality_note, fit, condition, verdict_code,
                   verdict_note, scope_code, works_alone, pairs, layer, avoid, notes, no_photo,
                   photo_prefix, retail_prefix, warmth, rain_unsafe, pattern, unconfirmed) VALUES

('trousers_18_footjoy-navy','footjoy-navy','Trousers','FootJoy navy golf trouser','Navy','#404455',
 'Anchor dark','Flat-front golf trouser, smooth twill, straight leg','Technical stretch twill','Light',
 'Casual',3,'No crest. Small FJ tab at the waistband','W36/L32 - two sizes up on his W33-34',
 'Good from the flat-lay','Keep',
 'One of three near-identical navy FootJoys. This one and trousers_23 are both W36; trousers_20 is the W32 he actually wears. Keep at most one of the two large pairs.',
 'core',true,'Any polo; white, stone, pale blue tops','-','The other two navy FootJoys',
 'FOOTJOY, W36/L32. Smooth twill. Same navy as trousers_20 and trousers_23 within four points.',
 false,'trousers_18_footjoy-navy','trousers_18_footjoy-navy_retail',2,false,'Plain',true),

('trousers_19_inesis-grey','inesis-grey','Trousers','Inesis pale grey golf trouser','Pale grey','#9B9EA0',
 'Mid neutral','Flat-front golf trouser, straight leg, welt back pockets','Thin technical twill','Light',
 'Casual',3,'No crest, no logo beyond a small tonal tab','EU44 / US M / 180-88A - correct size',
 'Good from the flat-lay','Keep',
 'A FAVOURITE, stated by Max: very thin fabric, ideal for Sydney winters and mid-seasons. Same house as trousers_17, the model crossover case. Correct size, no crest, matte - the strongest crossover candidate in this batch.',
 'core',true,'Navy, white, pale blue, burgundy tops','-','Grey tops - too close',
 'DECATHLON / INESIS, EU44, US M, 180/88A. Measures a true neutral grey, saturation 3 percent.',
 false,'trousers_19_inesis-grey','trousers_19_inesis-grey_retail',1,false,'Plain',false),

('trousers_20_footjoy-navy-slim','footjoy-navy-slim','Trousers','FootJoy navy slim golf trouser','Navy','#3C3E4F',
 'Anchor dark','Flat-front golf trouser, SLIM cut, smooth twill','Technical stretch twill','Light',
 'Casual',3,'No crest. Small FJ tab at the waistband','W32/L32 - the slim pair, and the one that fits',
 'Good from the flat-lay','Keep',
 'The navy FootJoy worth keeping. Max identified it as the slim fit before it was catalogued, and the label confirms W32 against W36 on the other two.',
 'core',true,'Any polo; white, stone, pale blue tops','-','The two W36 FootJoys',
 'FOOTJOY, W32/L32. Smooth twill, slim cut. Same navy as trousers_18 and trousers_23.',
 false,'trousers_20_footjoy-navy-slim','trousers_20_footjoy-navy-slim_retail',2,false,'Plain',false),

('trousers_21_inesis-strawberry','inesis-strawberry','Trousers','Inesis strawberry golf trouser','Strawberry red','#EE253F',
 'Statement','Flat-front golf trouser, straight leg, welt back pockets','Thin technical twill','Light',
 'Casual',3,'No crest. Small grey Inesis triangle at the pocket','EU44 / US M / 180-88A - correct size',
 'Good from the flat-lay','Keep',
 'A FAVOURITE, stated by Max, alongside trousers_19: very thin fabric, ideal for Sydney winters and mid-seasons, and in his words they rock. Loud, but it is a golf course.',
 'core',true,'Navy, white, stone, pale grey tops','-','Red or pink tops - the trouser is the colour',
 'DECATHLON / INESIS, EU44, US M, 180/88A. Measured #EE253F, hue 352 - a true red with a pink lean, which is what strawberry means here.',
 false,'trousers_21_inesis-strawberry','trousers_21_inesis-strawberry_retail',1,false,'Plain',false),

('trousers_22_under-armour-green','under-armour-green','Trousers','Under Armour green golf trouser','Emerald green','#27A271',
 'Statement','Flat-front golf trouser, straight leg, relaxed cut','Technical twill','Light',
 'Casual',2,'No crest. Tonal UA logo at the pocket','36/34 - two sizes up in the waist AND two in the leg',
 'Good from the flat-lay','Keep',
 'The loosest garment in the batch: 36 waist and a 34 leg against his W33-34/L32. One of the two Max named as fairly large cuts, before any of this was measured.',
 'core',true,'Navy, white, stone tops','-','Green tops',
 'UNDER ARMOUR, 36/34. Measured emerald green, hue 156.',
 false,'trousers_22_under-armour-green','trousers_22_under-armour-green_retail',2,false,'Plain',true),

('trousers_23_footjoy-navy-pique','footjoy-navy-pique','Trousers','FootJoy navy pique golf trouser','Navy','#3E4155',
 'Anchor dark','Flat-front golf trouser, FINE HORIZONTAL PIQUE weave, straight leg','Technical pique twill','Light',
 'Casual',3,'No crest. Woven FJ tab on the waistband','W36/L32 - two sizes up',
 'Good from the flat-lay','Keep',
 'The second of the two large cuts Max named. Same navy as trousers_18 and trousers_20; the only thing that separates it is the textured weave.',
 'core',true,'Any polo; white, stone, pale blue tops','-','The other two navy FootJoys',
 'FOOTJOY, W36/L32. Fine horizontal pique weave, unlike the smooth twill of trousers_18 and trousers_20. Catalogued on the first pass as blue-grey from a flat-lay under different light; it is the same navy as the other two, measured within four points on every channel.',
 false,'trousers_23_footjoy-navy-pique','trousers_23_footjoy-navy-pique_retail',2,false,'Textured',true)

ON CONFLICT (id) DO NOTHING;

-- Occasions. All six are golf. Crossover per the migration 050 test, which decides only whether a
-- garment leaves the course and is not a verdict.
INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, 'golf' FROM items WHERE id BETWEEN 'trousers_18' AND 'trousers_23_zzz'
ON CONFLICT DO NOTHING;

-- The two Inesis pairs cross over, and they are the two Max actually reaches for. Matte, no crest,
-- no colourblock, no logo beyond a small tonal tab - the same profile as trousers_17, which is the
-- model case in golf-crossover.md. The strawberry gets casual and weekend but NOT work: the colour
-- is the point of it, and a bright red trouser is a weekend garment even in a relaxed office.
INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, o FROM items CROSS JOIN (VALUES ('casual'),('weekend')) v(o)
WHERE id IN ('trousers_19_inesis-grey','trousers_21_inesis-strawberry')
ON CONFLICT DO NOTHING;

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('trousers_19_inesis-grey','work')
ON CONFLICT DO NOTHING;

-- The three FootJoys and the Under Armour stay golf-only: technical stretch twill, and in the
-- FootJoys' case a branded waistband tab that reads as sport off the course.

INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT id, 'hex', 'derived',
       'MEASURED 2026-09-01 from the second flat-lay set. White reference = median of the brightest 3 percent of the whole frame, no saturation filter - on a flat-lay that is always the table, since every garment is darker than the surface under it. The standard low-saturation white point FAILED on this shoot: the table itself measures 10-25 percent saturated here, so the filter discarded it, and on the pale grey pair the garment became its own white reference.'
FROM items WHERE id BETWEEN 'trousers_18' AND 'trousers_23_zzz'
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('trousers_23_footjoy-navy-pique','hex','manual','Recorded as blue-grey on the first pass, from a flat-lay under different light. It is the same navy as trousers_18 and trousers_20 - #3E4155 against #404455 and #3C3E4F, within four points on every channel and indistinguishable side by side. What actually differs is the WEAVE: a fine horizontal pique against smooth twill. Lesson: a colour difference seen in one frame and not another is a lighting difference until measured.'),
('trousers_19_inesis-grey','verdict_code','manual','Owner-stated favourite, 2026-09-01, before the garment was catalogued: very thin fabric, perfect for Sydney winters and mid-seasons. Not inferred.'),
('trousers_21_inesis-strawberry','verdict_code','manual','Owner-stated favourite, 2026-09-01, alongside trousers_19. Same words: very thin fabric, perfect for Sydney winters and mid-seasons, and they rock.'),
('trousers_20_footjoy-navy-slim','fit','manual','Max identified this as the slim pair before the labels were read; W32/L32 confirms it against W36 on trousers_18 and trousers_23.'),
('trousers_22_under-armour-green','fit','manual','36/34. Max named this and trousers_23 as the two fairly large cuts before measurement; both check out - this one is two sizes up in the waist and two in the leg.')
ON CONFLICT DO NOTHING;

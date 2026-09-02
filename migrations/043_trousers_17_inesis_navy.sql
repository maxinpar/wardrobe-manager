-- 043_trousers_17_inesis_navy.sql
-- Inesis navy chino, found in the shorts drawer 2026-08-30 alongside a Zara olive chino.
-- The Zara was binned the same day (cloth-loss fraying at the pocket mouth and hem, plus a
-- collapsed seat) and never entered the catalogue - do not log it if it surfaces in an old photo.
--
-- Usage IS established: Max tried these on, they were photographed worn front/side/back, and he
-- confirmed in daylight that the cloth is matte with no technical sheen. So unconfirmed = false.
--
-- Two fields are DERIVED, not read, and are flagged as such in item_field_sources:
--   hex      - every photograph of this garment is badly lit. White-balanced against a neutral in
--              the same light, the sunlit half of the flat-lay gives #627BA9 and the dim mirror
--              shots give #0A192C. #2E3C55 is the midpoint and matches the eye, sitting between
--              trousers_08 (#232B45) and trousers_09 (#38455F). Reshoot in open shade to confirm.
--   material - Inesis chino construction plus the hand of the cloth. No composition label was
--              photographed.
-- Size is MISSING entirely - no size label was photographed.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, cut, material,
                   weight_code, formality_raw, formality_rank, formality_note, fit, condition,
                   verdict_code, verdict_note, scope_code, works_alone, pairs, layer, avoid,
                   notes, no_photo, photo_prefix, retail_prefix, warmth, weatherproof_rain,
                   weatherproof_wind, rain_unsafe, bike_safe, pattern, unconfirmed) VALUES

('trousers_17_inesis-navy','inesis-navy','Trousers','Inesis navy chino',
 'Dark slate navy','#2E3C55','Anchor dark',
 'Flat-front chino, belt loops, straight leg with mild taper, mid rise, two double-welt back pockets',
 'Cotton twill with stretch','Mid','Smart-casual',4,
 'Decathlon golf brand, but no technical finish and no logo visible in the front view',
 'Waist and seat correct, clean through the thigh; ~2-3cm too long, breaks on the shoe',
 'Good - no fading, no fraying, pockets and waistband sound',
 'Tailor','Hem ~2-3cm. Then it goes straight into work rotation.',
 'core',null,
 'Pale and mid tops: white, pale blue, pink, lilac, oatmeal, burgundy, grey',
 'Belt required, brown or black leather; black nubuck sneaker or brown chelsea',
 'Black knitwear - navy/black clash, same rule as trousers_08',
 'Found in the shorts drawer 2026-08-30, unworn for a long time. Decathlon golf brand but reads as a plain chino - matte, no technical sheen (confirmed by Max in daylight). Third dark bottom after trousers_08 and trousers_11, and the only dark bottom at formality rank 4: before this, dark meant either rank-5 suit wool or rank-2 denim. OPEN: no size label photographed. OPEN: the Inesis woven tab in the _02_label photo may sit on the OUTSIDE of a back pocket rather than an interior facing - the back view is too blown out to settle it, and it decides whether fit and retail render prompts may show visible branding.',
 false,'trousers_17_inesis-navy','trousers_17_inesis-navy_retail',
 3,false,false,false,true,'Plain',false);

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('trousers_17_inesis-navy','work'),
('trousers_17_inesis-navy','casual'),
('trousers_17_inesis-navy','weekend'),
('trousers_17_inesis-navy','golf')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('trousers_17_inesis-navy','hex','derived','Midpoint of two badly-lit photographs, white-balanced against a neutral in the same light: sunlit #627BA9, dim indoor #0A192C. Not measured off a shade shot. Reshoot to confirm.'),
('trousers_17_inesis-navy','material','derived','Inesis chino construction plus the hand of the cloth in the flat-lay. No composition label was photographed.'),
('trousers_17_inesis-navy','notes','manual','Brand read off the woven tab, 2026-08-30. Matte finish confirmed verbally by Max in daylight.')
ON CONFLICT DO NOTHING;

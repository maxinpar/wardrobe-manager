-- 065_fit_moto_and_burgundy.sql
-- 2026-09-02. Promote "Moto & burgundy" from a diary entry to a real fit.
--
-- It was worn to the bank on 2026-08-25 and rated 7/10 (wear_events.id = 3), and a render of
-- it has been sitting in Wardrobe Photos\Fits since 26 August under its raw Gemini filename,
-- unfilable because no fit of that name existed. The wear event already carried
-- fit_photo_slug = 'fit_moto_and_burgundy', so the name was decided; only the row was missing.
--
-- fits.score stays NULL on purpose. The 7 is wear_events.rating — how one wearing went — and
-- the two numbers must never be merged. score is Max's own opinion of the fit and only he sets it.
--
-- rain_safe = false: shoes_03 is nubuck.

INSERT INTO fits (id, name, register_code, category_code, formality_rank, rain_safe,
                  style, commentary, catch, source, sort_order, vetted) VALUES
('fit_moto_and_burgundy', 'Moto & burgundy', 'everyday', 'cold', 2, false,
 'Black on black, one warm note',
 'Burgundy against black does what it should. The jacket sits correctly at the hip with clean shoulders, and the Ecco disappears into the hem — correct behaviour for an all-black shoe. Reads current, not dated.',
 'The jeans are the weak point: too faded to sit under all that black, so the eye lands on the worst garment, and the hem breaks and pools over the shoe. Swap to the black coated jean.',
 'wear event 3, 2026-08-25 (Moto & burgundy)', 120, true);

INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note) VALUES
('fit_moto_and_burgundy','outerwear_02_indindustrie-black-waxed-biker','outer',1,false,NULL),
('fit_moto_and_burgundy','polo-rl-burgundy-cashmere-crew','top',1,false,NULL),
('fit_moto_and_burgundy','trousers_09_celio-indigo-jeans','bottom',1,false,
 'the faded pair actually worn on 25 Aug — see the catch'),
('fit_moto_and_burgundy','shoes_03_ecco-black-nubuck','shoe',1,false,NULL),
('fit_moto_and_burgundy','belts_11_black-classic-pin-buckle','belt',1,false,NULL);

-- The alternate that answers the catch. Seeded against the bottom slot's real row id rather
-- than a guessed one, so it survives however the sequence happens to number these.
INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, alternate_for, note)
SELECT 'fit_moto_and_burgundy', 'trousers_11_black-coated-jeans', 'bottom', 2, true, fi.id,
       'Swap for this when the indigo looks washed out — black coating under a black waxed biker is deliberate, not accidental.'
FROM fit_items fi
WHERE fi.fit_id = 'fit_moto_and_burgundy' AND fi.role = 'bottom' AND fi.is_alternate = false;

-- Connect the diary entry to the fit. fit_photo_slug is left alone: it is what attaches the
-- real worn photo (fit_moto_and_burgundy_01_worn-front.jpg) to the wearing, not to the fit.
UPDATE wear_events SET fit_id = 'fit_moto_and_burgundy'
WHERE id = 3 AND fit_photo_slug = 'fit_moto_and_burgundy' AND fit_id IS NULL;

INSERT INTO fit_occasions (fit_id, occasion_code, kind) VALUES
  ('fit_moto_and_burgundy','work','good'),
  ('fit_moto_and_burgundy','casual','good'),
  ('fit_moto_and_burgundy','formal','bad');

INSERT INTO fit_temp_bands (fit_id, band_code) VALUES
  ('fit_moto_and_burgundy','cold'),
  ('fit_moto_and_burgundy','mild');

INSERT INTO fit_seasons (fit_id, season_code) VALUES
  ('fit_moto_and_burgundy','autumn'),
  ('fit_moto_and_burgundy','winter');

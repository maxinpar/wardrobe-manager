-- 014_fits_bomber.sql
-- Two fits for outerwear_01_zara-brown-leather-bomber, which had zero fit uses until
-- Max noticed on 2026-08-29. Renders were generated and filed before this ran, per the
-- standing rule that a fit does not enter the database without one.
-- Both carry an explicit base-layer tee: the wear log shows Max wears a plain tee under
-- his crew knits, and the fits had never recorded it.
-- Safe to re-run: every insert is ON CONFLICT DO NOTHING.

INSERT INTO fits (id, name, register_code, category_code, formality_rank, rain_safe,
                  source, sort_order, catch) VALUES
('fit_k13_bomber-and-burgundy','Bomber & burgundy','everyday','casual',2,true,
 'session 2026-08-29 (bomber gap)',89,
 'Keep every piece of leather brown - the black belt and the Ecco are what turn a brown jacket into an accident. The tee under the crew is invisible; it is recorded for laundry, not for the look.'),
('fit_k14_bomber-navy-and-black','Bomber, navy knit & black jeans','everyday','casual',2,true,
 'session 2026-08-29 (bomber gap)',90,
 'Brown leather throughout. Coated jeans and boots make this the one that is actually rideable - nothing pale to ruin.')
ON CONFLICT (id) DO NOTHING;

INSERT INTO fit_temp_bands (fit_id, band_code) VALUES
('fit_k13_bomber-and-burgundy','mild'),('fit_k13_bomber-and-burgundy','cold'),
('fit_k14_bomber-navy-and-black','mild'),('fit_k14_bomber-navy-and-black','cold')
ON CONFLICT DO NOTHING;

INSERT INTO fit_seasons (fit_id, season_code) VALUES
('fit_k13_bomber-and-burgundy','autumn'),('fit_k13_bomber-and-burgundy','winter'),
('fit_k14_bomber-navy-and-black','autumn'),('fit_k14_bomber-navy-and-black','winter')
ON CONFLICT DO NOTHING;

INSERT INTO fit_occasions (fit_id, occasion_code, kind) VALUES
('fit_k13_bomber-and-burgundy','weekend','good'),('fit_k13_bomber-and-burgundy','casual','good'),
('fit_k13_bomber-and-burgundy','riding','good'),('fit_k13_bomber-and-burgundy','formal','bad'),
('fit_k14_bomber-navy-and-black','weekend','good'),('fit_k14_bomber-navy-and-black','casual','good'),
('fit_k14_bomber-navy-and-black','riding','good'),('fit_k14_bomber-navy-and-black','formal','bad'),
('fit_k14_bomber-navy-and-black','client','bad')
ON CONFLICT DO NOTHING;

INSERT INTO fit_items (fit_id, item_id, role, position, note) VALUES
('fit_k13_bomber-and-burgundy','outerwear_01_zara-brown-leather-bomber','outer',1,NULL),
('fit_k13_bomber-and-burgundy','polo-rl-burgundy-cashmere-crew','top',2,NULL),
('fit_k13_bomber-and-burgundy','tees_02_grey-crew','base',3,'Invisible under a crew - recorded for laundry and availability, not for the render.'),
('fit_k13_bomber-and-burgundy','trousers_01_decathlon-beige','bottom',4,NULL),
('fit_k13_bomber-and-burgundy','belts_04_distressed-brown-everyday','belt',5,NULL),
('fit_k13_bomber-and-burgundy','shoes_07_oxford-brown-chelsea','shoe',6,NULL),
('fit_k14_bomber-navy-and-black','outerwear_01_zara-brown-leather-bomber','outer',1,NULL),
('fit_k14_bomber-navy-and-black','topman-navy-crew','top',2,NULL),
('fit_k14_bomber-navy-and-black','tees_01_white-crew','base',3,'Invisible under a crew - recorded for laundry and availability, not for the render.'),
('fit_k14_bomber-navy-and-black','trousers_11_black-coated-jeans','bottom',4,NULL),
('fit_k14_bomber-navy-and-black','belts_04_distressed-brown-everyday','belt',5,NULL),
('fit_k14_bomber-navy-and-black','shoes_07_oxford-brown-chelsea','shoe',6,NULL)
ON CONFLICT (fit_id, item_id, role) DO NOTHING;

-- schema_migrations is written by scripts/migrate.py, not here.

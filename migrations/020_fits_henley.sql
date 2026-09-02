-- 020_fits_henley.sql
-- Two fits for tees_15_adidas-grey-henley, promoted to core by Max on 2026-08-30.
-- Renders were generated, QC'd and filed before this ran, per the standing rule.

INSERT INTO fits (id, name, register_code, category_code, formality_rank, rain_safe,
                  source, sort_order, catch) VALUES
('fit_k15_henley-and-black','Henley & black jeans','everyday','casual',2,false,
 'session 2026-08-30 (henley promoted to core)',91,
 'Sleeves pushed up, top of the placket undone. Buttoned to the throat with the sleeves down, a henley reads as thermal underwear. Nothing grey over the top - grey on grey collapses.'),
('fit_k16_henley-and-bomber','Henley & the bomber','everyday','casual',2,true,
 'session 2026-08-30 (henley promoted to core)',92,
 'Same placket and sleeve rule. Keep every piece of leather brown. The epaulettes and the bomber sit in the same register, which is why this pairing works better than the henley does alone.')
ON CONFLICT (id) DO NOTHING;

INSERT INTO fit_temp_bands (fit_id, band_code) VALUES
('fit_k15_henley-and-black','mild'),
('fit_k16_henley-and-bomber','cold'),('fit_k16_henley-and-bomber','mild')
ON CONFLICT DO NOTHING;

INSERT INTO fit_seasons (fit_id, season_code) VALUES
('fit_k15_henley-and-black','spring'),('fit_k15_henley-and-black','autumn'),
('fit_k16_henley-and-bomber','autumn'),('fit_k16_henley-and-bomber','winter')
ON CONFLICT DO NOTHING;

INSERT INTO fit_occasions (fit_id, occasion_code, kind) VALUES
('fit_k15_henley-and-black','weekend','good'),('fit_k15_henley-and-black','casual','good'),
('fit_k15_henley-and-black','work','bad'),('fit_k15_henley-and-black','formal','bad'),
('fit_k16_henley-and-bomber','weekend','good'),('fit_k16_henley-and-bomber','casual','good'),
('fit_k16_henley-and-bomber','riding','good'),('fit_k16_henley-and-bomber','formal','bad')
ON CONFLICT DO NOTHING;

INSERT INTO fit_items (fit_id, item_id, role, position, note) VALUES
('fit_k15_henley-and-black','tees_15_adidas-grey-henley','top',1,'Sleeves pushed up, placket open at the top.'),
('fit_k15_henley-and-black','trousers_11_black-coated-jeans','bottom',2,NULL),
('fit_k15_henley-and-black','belts_11_black-classic-pin-buckle','belt',3,NULL),
('fit_k15_henley-and-black','shoes_09b_nike-airmax-1','shoe',4,'The olive is the only colour in the fit.'),
('fit_k16_henley-and-bomber','outerwear_01_zara-brown-leather-bomber','outer',1,NULL),
('fit_k16_henley-and-bomber','tees_15_adidas-grey-henley','top',2,'Sleeves pushed up, placket open at the top.'),
('fit_k16_henley-and-bomber','trousers_09_celio-indigo-jeans','bottom',3,NULL),
('fit_k16_henley-and-bomber','belts_04_distressed-brown-everyday','belt',4,NULL),
('fit_k16_henley-and-bomber','shoes_07_oxford-brown-chelsea','shoe',5,NULL)
ON CONFLICT (fit_id, item_id, role) DO NOTHING;

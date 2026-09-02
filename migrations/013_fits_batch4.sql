-- 013_fits_batch4.sql
-- 1. Fills in the 8 batch-3 fits whose compositions were lost (read back off their renders).
-- 2. Adds the 14 batch-4 fits.
-- Safe to re-run: every insert is ON CONFLICT DO NOTHING.
-- Australia/Sydney. Written 2026-08-29.

-- ---------------------------------------------------------------- lookups
INSERT INTO fit_categories (code, label, sort_order) VALUES
  ('formal', 'Formal', 50)
ON CONFLICT (code) DO NOTHING;


-- ================================================================
-- PART 1 — the 8 recovered batch-3 compositions
-- Source: read off fit_*_render.* in Wardrobe Photos\Fits, 2026-08-28.
-- Three shirts were not decisive in the render; they are marked UNCERTAIN
-- and should be confirmed against the garment before being trusted.
-- ================================================================

INSERT INTO fit_items (fit_id, item_id, role, position) VALUES
-- C7 — navy blazer and blue stripe
('fit_c7_navy-blazer-and-blue-stripe','outerwear_08_zara-navy-blazer','outer',1),
('fit_c7_navy-blazer-and-blue-stripe','zara-brown-cashmere-vneck','layer',2),
('fit_c7_navy-blazer-and-blue-stripe','tops_42_tm-lewin-blue-navy-stripe-shirt','top',3),  -- UNCERTAIN: may be tops_22
('fit_c7_navy-blazer-and-blue-stripe','trousers_04_oxford-stone','bottom',4),
('fit_c7_navy-blazer-and-blue-stripe','belts_02_tan-vera-pelle','belt',5),
('fit_c7_navy-blazer-and-blue-stripe','shoes_07_oxford-brown-chelsea','shoe',6),
-- C8 — charcoal shirt and burgundy
('fit_c8_charcoal-shirt-and-burgundy','outerwear_06_anko-slate-puffer-vest','outer',1),
('fit_c8_charcoal-shirt-and-burgundy','polo-rl-burgundy-cashmere-crew','layer',2),
('fit_c8_charcoal-shirt-and-burgundy','tops_31_zara-charcoal-textured-shirt','top',3),
('fit_c8_charcoal-shirt-and-burgundy','trousers_01_decathlon-beige','bottom',4),
('fit_c8_charcoal-shirt-and-burgundy','belts_04_distressed-brown-everyday','belt',5),
('fit_c8_charcoal-shirt-and-burgundy','shoes_07_oxford-brown-chelsea','shoe',6),
-- K7 — paisley and black
('fit_k7_paisley-and-black','tops_35_atpco-teal-paisley-print-shirt','top',1),
('fit_k7_paisley-and-black','trousers_11_black-coated-jeans','bottom',2),
('fit_k7_paisley-and-black','belts_11_black-classic-pin-buckle','belt',3),
('fit_k7_paisley-and-black','shoes_03_ecco-black-nubuck','shoe',4),
-- K8 — thirty-year shirt and beige
('fit_k8_thirty-year-shirt-and-beige','tops_39_cornwell-black-pinstripe-short-sleeve-shirt','top',1),
('fit_k8_thirty-year-shirt-and-beige','trousers_01_decathlon-beige','bottom',2),
('fit_k8_thirty-year-shirt-and-beige','belts_04_distressed-brown-everyday','belt',3),
('fit_k8_thirty-year-shirt-and-beige','shoes_09b_nike-airmax-1','shoe',4),
-- S3 — grey blazer and pink stripe
('fit_s3_grey-blazer-and-pink-stripe','outerwear_03_grey-unbranded-blazer','outer',1),
('fit_s3_grey-blazer-and-pink-stripe','tops_12_paul-smith-pink-stripe-shirt','top',2),
('fit_s3_grey-blazer-and-pink-stripe','trousers_08_tyrwhitt-navy-wool','bottom',3),
('fit_s3_grey-blazer-and-pink-stripe','belts_02_tan-vera-pelle','belt',4),
('fit_s3_grey-blazer-and-pink-stripe','shoes_04_churchs-apron-derby','shoe',5),
-- S4 — overcoat over navy
('fit_s4_overcoat-over-navy','outerwear_04_indaco-brown-wool-overcoat','outer',1),
('fit_s4_overcoat-over-navy','outerwear_08_zara-navy-blazer','layer',2),
('fit_s4_overcoat-over-navy','tops_27_paul-smith-blue-hairline-stripe-shirt','top',3),  -- UNCERTAIN: may be tops_46
('fit_s4_overcoat-over-navy','trousers_07_oxford-sage','bottom',4),
('fit_s4_overcoat-over-navy','belts_04_distressed-brown-everyday','belt',5),
('fit_s4_overcoat-over-navy','shoes_07_oxford-brown-chelsea','shoe',6),
-- W7 — linen blazer and indigo
('fit_w7_linen-blazer-and-indigo','outerwear_07_jules-pale-grey-linen-blazer','outer',1),
('fit_w7_linen-blazer-and-indigo','tops_27_paul-smith-blue-hairline-stripe-shirt','top',2),  -- UNCERTAIN: may be tops_50
('fit_w7_linen-blazer-and-indigo','trousers_09_celio-indigo-jeans','bottom',3),
('fit_w7_linen-blazer-and-indigo','belts_02_tan-vera-pelle','belt',4),
('fit_w7_linen-blazer-and-indigo','shoes_08a_suede-penny-loafer','shoe',5),
-- W8 — bulls and beige
('fit_w8_bulls-and-beige','tops_37_souleiado-blue-bull-print-shirt','top',1),
('fit_w8_bulls-and-beige','trousers_01_decathlon-beige','bottom',2),
('fit_w8_bulls-and-beige','belts_04_distressed-brown-everyday','belt',3),
('fit_w8_bulls-and-beige','shoes_08a_suede-penny-loafer','shoe',4)
ON CONFLICT (fit_id, item_id, role) DO NOTHING;

-- the compositions are known now
UPDATE fits SET composition_known = true, updated_at = now()
WHERE id IN ('fit_c7_navy-blazer-and-blue-stripe','fit_c8_charcoal-shirt-and-burgundy',
             'fit_k7_paisley-and-black','fit_k8_thirty-year-shirt-and-beige',
             'fit_s3_grey-blazer-and-pink-stripe','fit_s4_overcoat-over-navy',
             'fit_w7_linen-blazer-and-indigo','fit_w8_bulls-and-beige');

-- rain_safe derived from the shoe (nubuck and suede are rain-unsafe)
UPDATE fits SET rain_safe = false, updated_at = now()
WHERE id IN ('fit_k7_paisley-and-black','fit_k8_thirty-year-shirt-and-beige',
             'fit_w7_linen-blazer-and-indigo','fit_w8_bulls-and-beige');

-- renders were refiled 2026-08-28/29 under the .jpg convention
UPDATE fits SET
  hero_image_path = 'fits/' || regexp_replace(id,'^fit_','fit_') || '_render.jpg',
  hero_thumb_path = 'fits/thumbs/' || id || '_render.jpg',
  hero_is_generated = true,
  updated_at = now()
WHERE id IN ('fit_c7_navy-blazer-and-blue-stripe','fit_c8_charcoal-shirt-and-burgundy',
             'fit_k7_paisley-and-black','fit_k8_thirty-year-shirt-and-beige',
             'fit_s3_grey-blazer-and-pink-stripe','fit_s4_overcoat-over-navy',
             'fit_w7_linen-blazer-and-indigo','fit_w8_bulls-and-beige');


-- ================================================================
-- PART 2 — the 14 batch-4 fits
-- Source: claude/fits-batch-4.md, 2026-08-28.
-- killer stays false on all of them: it is Max's flag, never the importer's.
-- score stays NULL: it is Max's number, the app never writes it.
-- ================================================================

INSERT INTO fits (id, name, register_code, category_code, formality_rank, rain_safe,
                  source, sort_order, catch, hero_image_path, hero_thumb_path, hero_is_generated) VALUES
('fit_s5_navy-blazer-and-pale-blue','Navy blazer & pale blue twill','sharp','smart',4,true,
 'fits-batch-4.md 2026-08-28',75,
 'Brown leather only. Black belt and black shoes flatten a navy blazer, and navy trousers under it are navy-on-navy. Shirt cuffs stay unrolled under a jacket.',
 'fits/fit_s5_navy-blazer-and-pale-blue_render.jpg','fits/thumbs/fit_s5_navy-blazer-and-pale-blue_render.jpg',true),

('fit_s6_grey-blazer-and-yellow-stripe','Grey blazer & the yellow stripe','sharp','smart',4,true,
 'fits-batch-4.md 2026-08-28',76,
 'Tan leather, not black - the yellow hairline in the shirt is what makes that the right call.',
 NULL,NULL,true),

('fit_s7_navy-two-piece','The navy two-piece','sharp','formal',5,true,
 'fits-batch-4.md 2026-08-28',77,
 'The two-piece is the version with real-world use - add the waistcoat only for an actual wedding, and never wear the waistcoat open-collared without the jacket. There is no smart dark-brown dress belt in the wardrobe; belts_02 is a casual tan and is the best available.',
 NULL,NULL,true),

('fit_c9_black-dobby-and-the-vest','Black dobby & the vest','everyday','cold',3,false,
 'fits-batch-4.md 2026-08-28',78,
 'Never black or charcoal trousers with this shirt - it disappears. Single-cuff shirt only under the vest; the double-cuff shirts and the vest argue.',
 'fits/fit_c9_black-dobby-and-the-vest_render.jpg','fits/thumbs/fit_c9_black-dobby-and-the-vest_render.jpg',true),

('fit_c10_navy-vneck-over-microprint','Navy V-neck over the micro-print','everyday','cold',3,true,
 'fits-batch-4.md 2026-08-28',79,
 'No tee under the V - the shirt is the layer that fills it. Collar out over the neckline, cuffs showing at the wrist.',
 'fits/fit_c10_navy-vneck-over-microprint_render.jpg','fits/thumbs/fit_c10_navy-vneck-over-microprint_render.jpg',true),

('fit_c11_brown-cashmere-over-brown-stripe','Brown cashmere over the brown stripe','everyday','cold',3,true,
 'fits-batch-4.md 2026-08-28',80,
 'No black leather anywhere near this one - the shirt''s camel and tan are the point. No tee under the V. Never over cool grey or navy bottoms.',
 'fits/fit_c11_brown-cashmere-over-brown-stripe_render.jpg','fits/thumbs/fit_c11_brown-cashmere-over-brown-stripe_render.jpg',true),

('fit_c12_leopard-scarf-and-burgundy','Leopard scarf & burgundy','everyday','cold',3,true,
 'fits-batch-4.md 2026-08-28',81,
 'The scarf is cool-toned - keep the leather to the darker brown, not the tan belt, and never wear it over a patterned shirt. Scarf over the knit at the neck, not tucked under a collar.',
 'fits/fit_c12_leopard-scarf-and-burgundy_render.jpg','fits/thumbs/fit_c12_leopard-scarf-and-burgundy_render.jpg',true),

('fit_c13_charcoal-shirt-and-check-scarf','Charcoal shirt, biker & check scarf','everyday','cold',2,false,
 'fits-batch-4.md 2026-08-28',82,
 'The crinkle scarf undercuts tailoring - never with a blazer. The charcoal shirt needs the pale trouser to read, and no charcoal or grey knit over it.',
 'fits/fit_c13_charcoal-shirt-and-check-scarf_render.jpg','fits/thumbs/fit_c13_charcoal-shirt-and-check-scarf_render.jpg',true),

('fit_w9_cobalt-linen-and-stone','Cobalt linen & stone','everyday','warm',3,false,
 'fits-batch-4.md 2026-08-28',83,
 'Nothing over it - linen bunches under a knit. Not rain-safe: suede loafer.',
 'fits/fit_w9_cobalt-linen-and-stone_render.jpg','fits/thumbs/fit_w9_cobalt-linen-and-stone_render.jpg',true),

('fit_w10_pale-grey-microprint-and-black','Pale grey micro-print & black jeans','everyday','warm',2,false,
 'fits-batch-4.md 2026-08-28',84,
 'Never a stone or pale grey bottom with this shirt - pale on pale. Worn open, nothing over the top.',
 'fits/fit_w10_pale-grey-microprint-and-black_render.jpg','fits/thumbs/fit_w10_pale-grey-microprint-and-black_render.jpg',true),

('fit_w11_terracotta-and-indigo','Terracotta & indigo','everyday','warm',2,false,
 'fits-batch-4.md 2026-08-28',85,
 'Never the beige or stone chino - terracotta over beige goes flat and warm. Nothing over it, nothing else patterned. Worn tucked.',
 'fits/fit_w11_terracotta-and-indigo_render.jpg','fits/thumbs/fit_w11_terracotta-and-indigo_render.jpg',true),

('fit_k9_floral-untucked','The floral, untucked','everyday','casual',2,false,
 'fits-batch-4.md 2026-08-28',86,
 'Never tucked - the hem and collar are built for it. Cream ground needs the dark bottom. Do not rotate in the same week as the terracotta or the Lacroix.',
 'fits/fit_k9_floral-untucked_render.jpg','fits/thumbs/fit_k9_floral-untucked_render.jpg',true),

('fit_k10_sherpa-and-stone','Sherpa & stone','everyday','casual',1,false,
 'fits-batch-4.md 2026-08-28',87,
 'Explicitly not an office fit - the pale blue piping and elasticated cuffs undercut anything smart. Not a bike layer either: not weatherproof.',
 'fits/fit_k10_sherpa-and-stone_render.jpg','fits/thumbs/fit_k10_sherpa-and-stone_render.jpg',true),

('fit_k12_pindot-and-black','Pin-dot, untucked, black jeans','everyday','casual',2,false,
 'fits-batch-4.md 2026-08-28',88,
 'Nothing else patterned. If tucked, the black belt has to show; if untucked, no belt.',
 'fits/fit_k12_pindot-and-black_render.jpg','fits/thumbs/fit_k12_pindot-and-black_render.jpg',true)
ON CONFLICT (id) DO NOTHING;


INSERT INTO fit_temp_bands (fit_id, band_code) VALUES
('fit_s5_navy-blazer-and-pale-blue','mild'),('fit_s5_navy-blazer-and-pale-blue','cold'),
('fit_s6_grey-blazer-and-yellow-stripe','mild'),
('fit_s7_navy-two-piece','mild'),('fit_s7_navy-two-piece','cold'),
('fit_c9_black-dobby-and-the-vest','cold'),
('fit_c10_navy-vneck-over-microprint','cold'),('fit_c10_navy-vneck-over-microprint','mild'),
('fit_c11_brown-cashmere-over-brown-stripe','cold'),
('fit_c12_leopard-scarf-and-burgundy','cold'),
('fit_c13_charcoal-shirt-and-check-scarf','cold'),
('fit_w9_cobalt-linen-and-stone','warm'),
('fit_w10_pale-grey-microprint-and-black','warm'),
('fit_w11_terracotta-and-indigo','warm'),
('fit_k9_floral-untucked','warm'),
('fit_k10_sherpa-and-stone','cold'),
('fit_k12_pindot-and-black','mild')
ON CONFLICT DO NOTHING;

-- seasons are a browsing label only and must not affect the picker
INSERT INTO fit_seasons (fit_id, season_code) VALUES
('fit_s5_navy-blazer-and-pale-blue','autumn'),('fit_s5_navy-blazer-and-pale-blue','spring'),
('fit_s6_grey-blazer-and-yellow-stripe','spring'),('fit_s6_grey-blazer-and-yellow-stripe','autumn'),
('fit_s7_navy-two-piece','autumn'),('fit_s7_navy-two-piece','winter'),('fit_s7_navy-two-piece','spring'),
('fit_c9_black-dobby-and-the-vest','winter'),
('fit_c10_navy-vneck-over-microprint','winter'),('fit_c10_navy-vneck-over-microprint','autumn'),
('fit_c11_brown-cashmere-over-brown-stripe','winter'),
('fit_c12_leopard-scarf-and-burgundy','winter'),('fit_c12_leopard-scarf-and-burgundy','autumn'),
('fit_c13_charcoal-shirt-and-check-scarf','winter'),
('fit_w9_cobalt-linen-and-stone','summer'),
('fit_w10_pale-grey-microprint-and-black','summer'),
('fit_w11_terracotta-and-indigo','summer'),
('fit_k9_floral-untucked','summer'),
('fit_k10_sherpa-and-stone','winter'),('fit_k10_sherpa-and-stone','autumn'),
('fit_k12_pindot-and-black','spring'),('fit_k12_pindot-and-black','autumn')
ON CONFLICT DO NOTHING;

INSERT INTO fit_occasions (fit_id, occasion_code, kind) VALUES
('fit_s5_navy-blazer-and-pale-blue','work','good'),('fit_s5_navy-blazer-and-pale-blue','client','good'),
('fit_s5_navy-blazer-and-pale-blue','gym','bad'),('fit_s5_navy-blazer-and-pale-blue','golf','bad'),
('fit_s6_grey-blazer-and-yellow-stripe','work','good'),('fit_s6_grey-blazer-and-yellow-stripe','client','good'),
('fit_s6_grey-blazer-and-yellow-stripe','gym','bad'),('fit_s6_grey-blazer-and-yellow-stripe','golf','bad'),
('fit_s7_navy-two-piece','formal','good'),('fit_s7_navy-two-piece','client','good'),('fit_s7_navy-two-piece','dinner','good'),
('fit_s7_navy-two-piece','casual','bad'),('fit_s7_navy-two-piece','gym','bad'),('fit_s7_navy-two-piece','golf','bad'),
('fit_c9_black-dobby-and-the-vest','work','good'),('fit_c9_black-dobby-and-the-vest','formal','bad'),('fit_c9_black-dobby-and-the-vest','gym','bad'),
('fit_c10_navy-vneck-over-microprint','work','good'),('fit_c10_navy-vneck-over-microprint','formal','bad'),('fit_c10_navy-vneck-over-microprint','gym','bad'),
('fit_c11_brown-cashmere-over-brown-stripe','work','good'),('fit_c11_brown-cashmere-over-brown-stripe','formal','bad'),('fit_c11_brown-cashmere-over-brown-stripe','gym','bad'),
('fit_c12_leopard-scarf-and-burgundy','work','good'),('fit_c12_leopard-scarf-and-burgundy','casual','good'),('fit_c12_leopard-scarf-and-burgundy','formal','bad'),
('fit_c13_charcoal-shirt-and-check-scarf','work','good'),('fit_c13_charcoal-shirt-and-check-scarf','riding','good'),('fit_c13_charcoal-shirt-and-check-scarf','formal','bad'),
('fit_w9_cobalt-linen-and-stone','work','good'),('fit_w9_cobalt-linen-and-stone','casual','good'),('fit_w9_cobalt-linen-and-stone','formal','bad'),
('fit_w10_pale-grey-microprint-and-black','work','good'),('fit_w10_pale-grey-microprint-and-black','casual','good'),
('fit_w10_pale-grey-microprint-and-black','formal','bad'),('fit_w10_pale-grey-microprint-and-black','client','bad'),
('fit_w11_terracotta-and-indigo','casual','good'),('fit_w11_terracotta-and-indigo','weekend','good'),
('fit_w11_terracotta-and-indigo','work','bad'),('fit_w11_terracotta-and-indigo','formal','bad'),
('fit_k9_floral-untucked','weekend','good'),('fit_k9_floral-untucked','casual','good'),
('fit_k9_floral-untucked','work','bad'),('fit_k9_floral-untucked','formal','bad'),
('fit_k10_sherpa-and-stone','weekend','good'),('fit_k10_sherpa-and-stone','work','bad'),
('fit_k10_sherpa-and-stone','formal','bad'),('fit_k10_sherpa-and-stone','client','bad'),
('fit_k12_pindot-and-black','work','good'),('fit_k12_pindot-and-black','casual','good'),('fit_k12_pindot-and-black','formal','bad')
ON CONFLICT DO NOTHING;


INSERT INTO fit_items (fit_id, item_id, role, position, note) VALUES
-- S5
('fit_s5_navy-blazer-and-pale-blue','outerwear_08_zara-navy-blazer','outer',1,NULL),
('fit_s5_navy-blazer-and-pale-blue','tops_47_tm-lewin-blue-twill-shirt','top',2,NULL),
('fit_s5_navy-blazer-and-pale-blue','trousers_01_decathlon-beige','bottom',3,NULL),
('fit_s5_navy-blazer-and-pale-blue','belts_02_tan-vera-pelle','belt',4,NULL),
('fit_s5_navy-blazer-and-pale-blue','shoes_04_churchs-apron-derby','shoe',5,NULL),
-- S6
('fit_s6_grey-blazer-and-yellow-stripe','outerwear_03_grey-unbranded-blazer','outer',1,NULL),
('fit_s6_grey-blazer-and-yellow-stripe','tops_45_tm-lewin-blue-yellow-stripe-shirt','top',2,NULL),
('fit_s6_grey-blazer-and-yellow-stripe','trousers_04_oxford-stone','bottom',3,NULL),
('fit_s6_grey-blazer-and-yellow-stripe','belts_03_oxford-arlen-tan','belt',4,NULL),
('fit_s6_grey-blazer-and-yellow-stripe','shoes_02_andre-tan-brogue','shoe',5,NULL),
-- S7
('fit_s7_navy-two-piece','outerwear_13_hugo-boss-navy-wedding-suit-jacket','outer',1,NULL),
('fit_s7_navy-two-piece','tops_49_hugo-boss-navy-wedding-suit-waistcoat','layer',2,'Three-piece only. Leave it off for the two-piece, which is the version with real-world use.'),
('fit_s7_navy-two-piece','tops_46_tm-lewin-blue-herringbone-shirt','top',3,NULL),
('fit_s7_navy-two-piece','trousers_14_hugo-boss-navy-wedding-suit-trouser','bottom',4,NULL),
('fit_s7_navy-two-piece','belts_02_tan-vera-pelle','belt',5,'Best available - there is no smart dark-brown dress belt in the wardrobe.'),
('fit_s7_navy-two-piece','shoes_04_churchs-apron-derby','shoe',6,NULL),
-- C9
('fit_c9_black-dobby-and-the-vest','outerwear_06_anko-slate-puffer-vest','outer',1,NULL),
('fit_c9_black-dobby-and-the-vest','tops_44_celio-black-dobby-shirt','top',2,NULL),
('fit_c9_black-dobby-and-the-vest','trousers_04_oxford-stone','bottom',3,NULL),
('fit_c9_black-dobby-and-the-vest','belts_11_black-classic-pin-buckle','belt',4,NULL),
('fit_c9_black-dobby-and-the-vest','shoes_03_ecco-black-nubuck','shoe',5,NULL),
-- C10
('fit_c10_navy-vneck-over-microprint','lyle-scott-club-navy-vneck','layer',1,NULL),
('fit_c10_navy-vneck-over-microprint','tops_26_tommy-hilfiger-pale-blue-micro-print-shirt','top',2,'Fills the V. No tee.'),
('fit_c10_navy-vneck-over-microprint','trousers_04_oxford-stone','bottom',3,NULL),
('fit_c10_navy-vneck-over-microprint','belts_06_argentina-perforated-brown','belt',4,NULL),
('fit_c10_navy-vneck-over-microprint','shoes_07_oxford-brown-chelsea','shoe',5,NULL),
-- C11
('fit_c11_brown-cashmere-over-brown-stripe','zara-brown-cashmere-vneck','layer',1,NULL),
('fit_c11_brown-cashmere-over-brown-stripe','tops_34_tm-lewin-brown-tan-multistripe-shirt','top',2,'Fills the V. No tee.'),
('fit_c11_brown-cashmere-over-brown-stripe','trousers_09_celio-indigo-jeans','bottom',3,NULL),
('fit_c11_brown-cashmere-over-brown-stripe','belts_04_distressed-brown-everyday','belt',4,NULL),
('fit_c11_brown-cashmere-over-brown-stripe','shoes_07_oxford-brown-chelsea','shoe',5,NULL),
-- C12
('fit_c12_leopard-scarf-and-burgundy','accessories_00_leopard-wool-silk-scarf','accessory',1,NULL),
('fit_c12_leopard-scarf-and-burgundy','polo-rl-burgundy-cashmere-crew','top',2,NULL),
('fit_c12_leopard-scarf-and-burgundy','trousers_00_decathlon-stone','bottom',3,NULL),
('fit_c12_leopard-scarf-and-burgundy','belts_04_distressed-brown-everyday','belt',4,NULL),
('fit_c12_leopard-scarf-and-burgundy','shoes_07_oxford-brown-chelsea','shoe',5,NULL),
-- C13
('fit_c13_charcoal-shirt-and-check-scarf','outerwear_02_indindustrie-black-waxed-biker','outer',1,NULL),
('fit_c13_charcoal-shirt-and-check-scarf','accessories_02_charcoal-check-crinkle-scarf','accessory',2,NULL),
('fit_c13_charcoal-shirt-and-check-scarf','tops_31_zara-charcoal-textured-shirt','top',3,NULL),
('fit_c13_charcoal-shirt-and-check-scarf','trousers_04_oxford-stone','bottom',4,NULL),
('fit_c13_charcoal-shirt-and-check-scarf','belts_11_black-classic-pin-buckle','belt',5,NULL),
('fit_c13_charcoal-shirt-and-check-scarf','shoes_03_ecco-black-nubuck','shoe',6,NULL),
-- W9
('fit_w9_cobalt-linen-and-stone','tops_17_purlin-cobalt-linen-shirt','top',1,NULL),
('fit_w9_cobalt-linen-and-stone','trousers_04_oxford-stone','bottom',2,NULL),
('fit_w9_cobalt-linen-and-stone','belts_03_oxford-arlen-tan','belt',3,NULL),
('fit_w9_cobalt-linen-and-stone','shoes_08a_suede-penny-loafer','shoe',4,NULL),
-- W10
('fit_w10_pale-grey-microprint-and-black','tops_40_celio-club-pale-grey-microprint-short-sleeve-shirt','top',1,'Worn open - the white collar band only shows that way.'),
('fit_w10_pale-grey-microprint-and-black','trousers_11_black-coated-jeans','bottom',2,NULL),
('fit_w10_pale-grey-microprint-and-black','belts_11_black-classic-pin-buckle','belt',3,NULL),
('fit_w10_pale-grey-microprint-and-black','shoes_09b_nike-airmax-1','shoe',4,NULL),
-- W11
('fit_w11_terracotta-and-indigo','tops_14_souleiado-terracotta-print-shirt','top',1,'Worn tucked.'),
('fit_w11_terracotta-and-indigo','trousers_09_celio-indigo-jeans','bottom',2,NULL),
('fit_w11_terracotta-and-indigo','belts_11_black-classic-pin-buckle','belt',3,NULL),
('fit_w11_terracotta-and-indigo','shoes_03_ecco-black-nubuck','shoe',4,NULL),
-- K9
('fit_k9_floral-untucked','tops_16_hm-cream-orchid-floral-shirt','top',1,'Untucked, always.'),
('fit_k9_floral-untucked','trousers_09_celio-indigo-jeans','bottom',2,NULL),
('fit_k9_floral-untucked','belts_04_distressed-brown-everyday','belt',3,NULL),
('fit_k9_floral-untucked','shoes_09b_nike-airmax-1','shoe',4,'Olive picks up the green in the print - this shoe, not the Ecco.'),
-- K10
('fit_k10_sherpa-and-stone','outerwear_09_prodigy-navy-sherpa-fleece','outer',1,NULL),
('fit_k10_sherpa-and-stone','tees_02_grey-crew','top',2,NULL),
('fit_k10_sherpa-and-stone','trousers_00_decathlon-stone','bottom',3,NULL),
('fit_k10_sherpa-and-stone','belts_08_cuater-grey-braided-stretch','belt',4,NULL),
('fit_k10_sherpa-and-stone','shoes_09b_nike-airmax-1','shoe',5,NULL),
-- K12
('fit_k12_pindot-and-black','tops_13_zara-white-navy-pindot-shirt','top',1,NULL),
('fit_k12_pindot-and-black','trousers_11_black-coated-jeans','bottom',2,NULL),
('fit_k12_pindot-and-black','belts_11_black-classic-pin-buckle','belt',3,'Only if tucked.'),
('fit_k12_pindot-and-black','shoes_09b_nike-airmax-1','shoe',4,NULL)
ON CONFLICT (fit_id, item_id, role) DO NOTHING;


-- provenance
INSERT INTO fit_field_sources (fit_id, field_name, source, note)
SELECT id, 'composition', 'manual',
       'Recovered by reading the fit render, 2026-08-28. Three shirt ids were not decisive and are marked UNCERTAIN in 013_fits_batch4.sql.'
FROM fits WHERE id IN ('fit_c7_navy-blazer-and-blue-stripe','fit_c8_charcoal-shirt-and-burgundy',
             'fit_k7_paisley-and-black','fit_k8_thirty-year-shirt-and-beige',
             'fit_s3_grey-blazer-and-pink-stripe','fit_s4_overcoat-over-navy',
             'fit_w7_linen-blazer-and-indigo','fit_w8_bulls-and-beige')
ON CONFLICT DO NOTHING;

-- schema_migrations is written by scripts/migrate.py, not here.

-- ---------------------------------------------------------------- verify
-- After running, expect: 60 fits, 0 without items, 0 composition_unknown, 0 unresolved refs.
--   SELECT (SELECT count(*) FROM fits) AS fits,
--          (SELECT count(*) FROM fit_items) AS fit_items,
--          (SELECT count(*) FROM fits f WHERE NOT EXISTS
--              (SELECT 1 FROM fit_items fi WHERE fi.fit_id = f.id)) AS fits_without_items,
--          (SELECT count(*) FROM fits WHERE NOT composition_known) AS composition_unknown,
--          (SELECT count(*) FROM fit_items fi LEFT JOIN items i ON i.id = fi.item_id
--            WHERE i.id IS NULL) AS unresolved_item_refs;

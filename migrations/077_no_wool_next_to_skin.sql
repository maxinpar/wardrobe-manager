-- 077_no_wool_next_to_skin.sql — a tee under every wool that would touch skin.
--
-- Max does not wear wool against skin. Thirteen fits put one there, mostly the
-- Polo Ralph Lauren cashmere crew, and the renders of several of them already
-- show a white tee at the neckline — the picture was right and the garment list
-- was wrong.
--
-- SCOPED BY MATERIAL, NOT BY CATEGORY. `Knitwear` catches cotton and acrylic
-- knits that are perfectly fine next to skin; what Max actually objects to is
-- wool, cashmere, merino, lambswool, alpaca and angora. The category was the
-- sloppy proxy and it would have put a tee under garments that never needed one.
--
-- SCOPED BY WHAT IS ACTUALLY INNERMOST. A `layer` sits OUTSIDE a `top` in this
-- schema's role order, so a wool V-neck over a shirt is not against skin and is
-- not in this list — fit_c10 already wears the micro-print under it. Reading
-- "any wool in top or layer with no base row" would have added a tee under
-- eleven garments that are already covered, including the golf quarter-zips
-- worn over a polo and the suit waistcoat worn over a shirt. The test added
-- alongside this migration encodes the innermost rule, not the loose one.
--
-- ROLL-NECKS ARE EXEMPT, by definition: one is worn alone, and a tee under it
-- is lumpy at the neck and wrong. fit_the_sharp_one keeps the Zara roll-neck
-- bare. This is the same exemption rules-and-context.md §2 rule 5 already makes.
--
-- THE SHAWL IS NOT EXEMPT. Its own catalogue card says a plain tee goes
-- underneath and the collar is the feature, so fit_s2_overcoat-over-shawl gets
-- one like the rest. (fit_the_shawl already has its tee — migration 075.)
--
-- `manual`, because this is Max's own statement about how he dresses and must
-- outrank anything the importer would derive from the garment lists.

INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note)
SELECT f.id, 'tees_01_white-crew', 'base', 1, false,
       'No wool next to skin — added 2026-09-08'
FROM (VALUES
  ('fit_bc_burgundy-crew'),
  ('fit_blazer_day'),
  ('fit_blazer_over_burgundy'),
  ('fit_c12_leopard-scarf-and-burgundy'),
  ('fit_c5_oatmeal-and-cobalt'),
  ('fit_cold_and_client'),
  ('fit_everyday_burgundy'),
  ('fit_fedeli_and_navy_chino'),
  ('fit_k1_burgundy-and-black'),
  ('fit_moto_and_burgundy'),
  ('fit_oatmeal_and_navy_wool'),
  ('fit_s2_overcoat-over-shawl'),
  ('fit_the_vest_done_right')
) AS f(id)
ON CONFLICT (fit_id, item_id, role) DO NOTHING;

INSERT INTO fit_field_sources (fit_id, field_name, source, note)
SELECT f.id, 'composition', 'manual',
       'White crew tee added under a wool garment that would otherwise sit '
       'against skin — brief-beige-brown-set.md 2026-09-08'
FROM (VALUES
  ('fit_bc_burgundy-crew'),
  ('fit_blazer_day'),
  ('fit_blazer_over_burgundy'),
  ('fit_c12_leopard-scarf-and-burgundy'),
  ('fit_c5_oatmeal-and-cobalt'),
  ('fit_cold_and_client'),
  ('fit_everyday_burgundy'),
  ('fit_fedeli_and_navy_chino'),
  ('fit_k1_burgundy-and-black'),
  ('fit_moto_and_burgundy'),
  ('fit_oatmeal_and_navy_wool'),
  ('fit_s2_overcoat-over-shawl'),
  ('fit_the_vest_done_right')
) AS f(id)
ON CONFLICT (fit_id, field_name) DO UPDATE
   SET source = EXCLUDED.source, note = EXCLUDED.note;

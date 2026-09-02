-- 012_accessories.sql — the Accessories category.
--
-- Three scarves catalogued 2026-08-28 are the first items that are neither worn
-- on the body nor hold anything up, so they need a category of their own. Per
-- the note in 002_lookups.sql, adding a category is an INSERT here rather than a
-- migration of the items table.
--
-- Scope is deliberately broad: scarves now, and later ties, pocket squares,
-- gloves and hats, rather than a category per accessory type. The distinction
-- between a scarf and a glove is carried by the fits layer, not by the taxonomy.
--
-- photo_folder matches the Drive folder created 2026-08-28. Note that
-- build_app.py still scans Knitwear/Trousers/Shoes only — until 'Accessories' is
-- added to both its scan list and CATS, anything filed there is invisible to the
-- app. Same outstanding fix as Shirts, Belts and Outerwear.

INSERT INTO categories (code, label, photo_folder, sort_order) VALUES
  ('Accessories', 'Accessories', 'Accessories', 70)
ON CONFLICT (code) DO NOTHING;

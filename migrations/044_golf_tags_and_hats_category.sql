-- 044_golf_tags_and_hats_category.sql
-- 2026-08-31. Two things, both prerequisites for the golf sub-wardrobe being usable at all.
--
-- PART 1 - tag the golf shorts.
-- Migration 025 deliberately withheld the golf tag: "construction suggests it, Max has not said
-- so." 026 followed the same rule for batch 1. Correct at the time, never revisited - so the
-- catalogue ended up with 10 golf-tagged shoes and nothing above the ankle, and the picker could
-- not assemble a single golf fit. Max confirmed the split on 2026-08-31.
--
-- Golf = all 20 shorts EXCEPT:
--   shorts_01_zara-tan-chino     cotton chino short, no technical content - casual only
--   shorts_02_blush-poly         technical, but Max excluded it. See the flag below.
--   shorts_17_chambray-linen-look  linen-look chambray - casual only
-- The weekend/casual tags stay: a golf short is still wearable off the course.

INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, 'golf' FROM items
WHERE cat_code = 'Shorts'
  AND id NOT IN ('shorts_01_zara-tan-chino',
                 'shorts_02_blush-poly',
                 'shorts_17_chambray-linen-look')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT id, 'occasions', 'manual',
       'Golf confirmed by Max 2026-08-31, releasing the hold placed in migration 025.'
FROM items
WHERE cat_code = 'Shorts'
  AND id NOT IN ('shorts_01_zara-tan-chino',
                 'shorts_02_blush-poly',
                 'shorts_17_chambray-linen-look')
ON CONFLICT DO NOTHING;

-- FLAG: shorts_02_blush-poly is excluded on instruction, but its own catalogue note reads
-- "technical polyester, contrast striped inner waistband - reads as a golf or performance
-- short". If that is simply a short Max does not take to the course, this is correct and the
-- note should be softened. If it was excluded because I hedged when I proposed the split, add
-- the tag. Left as a question rather than resolved by guess.

-- PART 2 - the Hats category.
-- A hat is part of every golf fit in Australia, so until this exists no golf fit can be
-- complete. fit_items.role is free text and position is ordered, so a hat slot needs no schema
-- change - only this row and the Drive folder.
-- sort_order 65 puts Hats between Outerwear (60) and Accessories (70).
-- photo_folder 'Hats' must exist under "Wardrobe Photos" or import_photos.py silently skips it.

INSERT INTO categories (code, label, photo_folder, sort_order)
VALUES ('Hats', 'Hats', 'Hats', 65)
ON CONFLICT (code) DO UPDATE
  SET label = EXCLUDED.label,
      photo_folder = EXCLUDED.photo_folder,
      sort_order = EXCLUDED.sort_order;

-- 024_shorts_category.sql
-- 2026-08-30: shorts get their own category. They were never going to sit sensibly
-- under Trousers - different season, different occasions, different fit rules - and
-- Max has a lot of them (golf bermudas plus casual chino shorts).
-- sort_order 35 puts them between Trousers (30) and Shoes (40).
-- photo_folder 'Shorts' must exist under "Wardrobe Photos" or import_photos.py skips it.

INSERT INTO categories (code, label, photo_folder, sort_order)
VALUES ('Shorts', 'Shorts', 'Shorts', 35)
ON CONFLICT (code) DO UPDATE
  SET label = EXCLUDED.label,
      photo_folder = EXCLUDED.photo_folder,
      sort_order = EXCLUDED.sort_order;

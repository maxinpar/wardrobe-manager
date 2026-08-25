-- 002_lookups.sql — the lookup rows.
--
-- Codes match the values in wardrobe.json exactly so the importer never has to
-- translate. Adding a category (tees, shirts, shorts, socks) is an INSERT here,
-- not a migration of the items table.

INSERT INTO categories (code, label, photo_folder, sort_order) VALUES
  ('Knitwear',  'Knitwear',  'Knitwear',  10),
  ('Tops',      'Tops',      'Shirts',    20),   -- folder name differs from the category
  ('Trousers',  'Trousers',  'Trousers',  30),
  ('Shoes',     'Shoes',     'Shoes',     40),
  ('Belts',     'Belts',     'Belts',     50),
  ('Outerwear', 'Outerwear', 'Outerwear', 60);

INSERT INTO colour_roles (code, label, sort_order) VALUES
  ('Pale neutral', 'Pale neutral', 10),
  ('Neutral',      'Neutral',      20),
  ('Mid tone',     'Mid tone',     30),
  ('Anchor dark',  'Anchor dark',  40),
  ('Statement',    'Statement',    50);

INSERT INTO verdicts (code, label, wearable, sort_order) VALUES
  ('Keep',    'Keep',    true,  10),
  ('Tailor',  'Tailor',  true,  20),   -- owned, blocked until altered
  ('Replace', 'Replace', true,  30),   -- wearable but on the way out
  ('Bin',     'Bin',     false, 40);   -- never suggested

INSERT INTO scopes (code, label) VALUES
  ('core', 'In the rotation'),
  ('out',  'Out of scope');

INSERT INTO necks (code, label, sort_order) VALUES
  ('crew',        'Crew',        10),
  ('v-neck',      'V-neck',      20),
  ('polo collar', 'Polo collar', 30),
  ('button/mock', 'Button/mock', 40),
  ('quarter-zip', 'Quarter-zip', 50),
  ('shawl',       'Shawl',       60),
  ('cardigan',    'Cardigan',    70),
  ('roll',        'Roll-neck',   80);

INSERT INTO weights (code, label, warmth_hint, sort_order) VALUES
  ('Fine',      'Fine',      2, 10),
  ('Light-Mid', 'Light-Mid', 2, 20),
  ('Mid',       'Mid',       3, 30),
  ('Mid-Heavy', 'Mid-Heavy', 4, 40),
  ('Chunky',    'Chunky',    5, 50);

INSERT INTO occasions (code, label, sort_order) VALUES
  ('work',   'Work',   10),
  ('casual', 'Casual', 20),
  ('golf',   'Golf',   30),
  ('formal', 'Formal', 40),
  ('gym',    'Gym',    50);

INSERT INTO registers (code, label, sort_order) VALUES
  ('everyday', 'Everyday', 10),
  ('sharp',    'Sharp',    20);

INSERT INTO laundry_states (code, label, available, sort_order) VALUES
  ('clean',     'Clean',        true,  10),
  ('worn',      'Worn',         false, 20),
  ('in_wash',   'In the wash',  false, 30),
  ('at_tailor', 'At the tailor', false, 40);

INSERT INTO photo_angles (code, label, sort_order) VALUES
  ('label',       'Label',        10),
  ('hanger',      'On the hanger', 20),
  ('worn-front',  'Worn — front',  30),
  ('worn-side',   'Worn — side',   40),
  ('worn-back',   'Worn — back',   50),
  ('worn-closed', 'Worn — closed', 60),
  ('buckle',      'Buckle',        70),
  ('full',        'Full length',   80),
  ('underside',   'Underside stamp', 90),
  ('detail',      'Detail',        100),
  ('damage',      'Damage',        110),
  ('render',      'Generated render', 120);

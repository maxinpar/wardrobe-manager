-- 011_role_raw.sql — `role` became prose, so it gets the `neck` treatment.
--
-- The 2026-08-27 export brought 40 shirts, and with them colour roles like
-- "Anchor dark - the only dark shirt in Tops" and "Pale blue - reads as a light
-- blue-white stripe at distance". That is a hand-written observation, not an
-- enum value, and 33 distinct ones would turn the lookup table into a list of
-- sentences.
--
-- So: keep the sentence in `role_raw`, normalise the leading term into
-- `role_code`, exactly as `neck_raw` / `neck_code` already work. The export
-- round-trips from `role_raw`, so nothing Max wrote is lost.

ALTER TABLE items ADD COLUMN role_raw text;

UPDATE items SET role_raw = role_code WHERE role_raw IS NULL;

COMMENT ON COLUMN items.role_raw IS
  'The colour role as written, which is often a sentence. role_code is the '
  'normalised leading term and may be null when nothing matches.';

-- The new base terms the shirts introduced. Still a short list, because only
-- the leading term is normalised.
INSERT INTO colour_roles (code, label, sort_order) VALUES
  ('Pale blue',    'Pale blue',    12),
  ('Pale warm',    'Pale warm',    14),
  ('Warm neutral', 'Warm neutral', 22),
  ('Mid neutral',  'Mid neutral',  24),
  ('Mid colour',   'Mid colour',   32),
  ('Pattern',      'Pattern',      60);

-- Shirt weights, and the collar the shirts are cut with.
INSERT INTO weights (code, label, warmth_hint, sort_order) VALUES
  ('Light',        'Light',        1, 5),
  ('Light to mid', 'Light to mid', 2, 15);

INSERT INTO necks (code, label, sort_order) VALUES
  ('collar', 'Shirt collar', 35);

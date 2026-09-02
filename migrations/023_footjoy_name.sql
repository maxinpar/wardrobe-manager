-- 023_footjoy_name.sql
-- 2026-08-30: shoes_16 was catalogued as an unbranded "spiked golf shoe, navy and lime"
-- because the raw photos did not show a legible logo. Max named its render file
-- "16-footjoys", i.e. these are his FootJoys. Name updated on his word.
-- Model not recorded: the render printed "HYPERFLEX" but that is the render's claim,
-- not his and not visible in the raw photos, so it is deliberately left out.

UPDATE items SET
  name = 'FootJoy spiked golf shoe, navy and lime',
  notes = coalesce(notes,'') || ' Brand: FootJoy, per Max 2026-08-30. Model not confirmed.',
  updated_at = now()
WHERE id = 'shoes_16_navy-lime-spiked';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shoes_16_navy-lime-spiked','name','manual','FootJoy identified by Max via render filename, 2026-08-30.')
ON CONFLICT DO NOTHING;

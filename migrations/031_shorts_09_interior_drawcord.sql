-- 031_shorts_09_interior_drawcord.sql
-- 2026-08-30. Max: the cord on shorts_09 is an INTERIOR drawcord, not visible when worn.
--
-- So the photograph and the general rule were both right and did not actually conflict: the cord
-- exists, and it is inside the waistband where a front view cannot see it. The render, which shows
-- no cord, is correct. Filed.
--
-- This closes the last of the batch-1 rejections. All five were mine; none were the model's.

UPDATE items SET
  cut = 'Flat front, interior drawcord',
  notes = 'NO BRAND FOUND. The only label is a size tab printed with the S / M / L / XL run and L marked, plus BODY: 90% Polyester 10% Elastane, exclusive of trim, made in China. Brand deliberately left blank. There is a dark grey flat drawcord INSIDE the waistband, threaded behind a grey elastic tape - it is not visible when the shorts are worn (Max, 2026-08-30), which is why the retail render correctly shows a plain waistband. SIZE FLAG: a letter size, not comparable to W33-34.'
WHERE id = 'shorts_09_white-sport-unbranded';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_09_white-sport-unbranded','cut','manual','Interior drawcord, hidden when worn - stated by Max 2026-08-30 after I queried the cord visible in photo 18. The cord is real; my error was assuming it showed on the outside.')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

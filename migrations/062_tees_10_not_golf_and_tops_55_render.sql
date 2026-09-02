-- 062_tees_10_not_golf_and_tops_55_render.sql
-- 2026-09-01. Two small corrections asked for by Max.
--
-- 1. tees_10 IS NOT GOLF APPAREL. It carried exactly one occasion tag, golf, presumably because
--    the print reads "GIVE ME BIRDIES OR GIVE ME DEATH". A slogan about golf is not golf kit.
--    Max's call, 2026-09-01.
--
--    Removing golf would have left the row with NO occasions at all, which makes it invisible to
--    the picker - tees_07 is already in that state and it is a bug, not a category. So it takes
--    casual instead, which is what every other graphic tee in the wardrobe carries: tees_06,
--    tees_11, tees_14, tees_16, tees_19, tees_20. If Max wants it genuinely untagged, that is one
--    line to undo - but an orphaned row was not what he asked for.
--
-- 2. tops_55 has a NEW RETAIL RENDER, supplied by Max and filed the same day. Identity confirmed
--    before it was written: Cross Sweden neck label, size S, tonal diamond jacquard across the
--    body, plain taupe collar and sleeves, green golfer logo at the chest, text on the right
--    sleeve - every detail already recorded in this item's notes. The superseded render was moved
--    out of the Drive tree rather than deleted, and one file remains under the prefix.
--
--    COLOUR DRIFT, RECORDED NOT FIXED. The new render's body reads #695B4A - hue 33, saturation
--    30 percent, a warm olive-brown. The garment measures #787069, saturation about 12 percent, a
--    grey-taupe. Same warm direction, roughly double the saturation. The render is the right
--    garment and was asked for, so it is filed; the item's hex is NOT changed, because the hex
--    comes from the photograph of the garment and never from a render. Same standing rule as
--    trousers_23 in migration 061.

DELETE FROM item_occasions
WHERE item_id = 'tees_10_coolgolf-red-badge' AND occasion_code = 'golf';

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('tees_10_coolgolf-red-badge','casual')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('tees_10_coolgolf-red-badge','notes','manual','NOT GOLF APPAREL. Max removed the golf tag on 2026-09-01. It is a graphic tee whose print happens to be a golf joke - "GIVE ME BIRDIES OR GIVE ME DEATH" - and it was tagged golf on the strength of the slogan alone. Retagged casual to match every other graphic tee rather than left with no occasions at all.'),
('tops_55_cross-taupe-diamond-polo','retail_prefix','manual','Render replaced 2026-09-01 with one supplied by Max. Identity verified against this item''s recorded details before writing: Cross Sweden label, size S, tonal diamond jacquard body, plain collar and sleeves, chest logo, right-sleeve text. The superseded render was moved out of the Drive tree, not deleted; one file remains under the prefix.'),
('tops_55_cross-taupe-diamond-polo','hex','manual','The 2026-09-01 render reads warmer and more saturated than the garment - #695B4A, hue 33, saturation 30 percent, against the measured #787069 at about 12 percent. The render is correct as to garment and was filed as asked, but the hex STANDS AS MEASURED FROM THE PHOTOGRAPH. Do not re-read this item''s colour off its render.')
ON CONFLICT DO NOTHING;

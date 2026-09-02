-- 034_shorts_fitting_07.sql
-- 2026-08-30 fitting. Max on shorts_07: "love it because it is a paler grey than the previous
-- pale grey. Easy fit."
--
-- Measured: hem 3.1 cm above the top of the kneecap - the fourth pair in a row to land within
-- 2 mm of 3 cm, and correct for a golf short. Seat is clean and well filled with no slack and no
-- pull; better through the seat than shorts_05 despite both being nominally oversized, which the
-- 88/12 stretch explains. Leg hangs straight, moderate opening, no flare.
--
-- The monogram print reads as a fine texture at conversational distance, not as a pattern, so it
-- behaves like a plain grey against a loud polo. That was the open question on this pair.
--
-- COLOUR NOT CHANGED, deliberately. Max says this is paler than shorts_05. Measured on matched
-- lit regions and white-balanced against the wall, the two come out at value 131 and 134 - the
-- same within noise - so the photographs cannot confirm or deny it and I am not overriding him
-- with a number I do not trust. The stored #E7E7E2 is very likely too pale regardless (it came
-- off the same over-exposed flat-lay that got shorts_05 wrong). Left alone pending one photograph
-- of the two pairs side by side in the same light, which settles both hexes at once.

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP AS IS. Max: "love it... easy fit." Fitted 2026-08-30: hem 3.1 cm above the kneecap, correct for golf. Seat clean and well filled - no slack, no pull lines - and better through the seat than shorts_05, which the 12% spandex explains. Waistband sits at the natural waist, leg hangs straight with a moderate opening. The all-over FJ monogram is fine enough to read as texture rather than pattern at any normal distance, so it pairs with a loud polo exactly like a plain grey would. The W36 being two sizes over his nominal W34 is a non-issue on the body. COLOUR UNRESOLVED: Max reads it as paler than shorts_05; photographic measurement cannot separate them and the stored hex is probably too pale. Needs one side-by-side shot.',
  pairs = 'Any loud polo - reads as a plain grey.',
  avoid = 'Nothing identified.'
WHERE id = 'shorts_07_footjoy-grey-monogram';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_07_footjoy-grey-monogram','verdict_code','manual','Keep, decided by Max at the 2026-08-30 fitting - "love it, easy fit".'),
('shorts_07_footjoy-grey-monogram','hex','manual','NOT VERIFIED. Max states this is paler than shorts_05; white-balanced measurement of both on matched lit regions gives 131 vs 134, indistinguishable. Stored value #E7E7E2 came from the same over-exposed flat-lay that made shorts_05 wrong and is probably too pale. Awaiting a side-by-side photograph.')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

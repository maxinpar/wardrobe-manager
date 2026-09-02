-- 038_shorts_fitting_close_out.sql
-- 2026-08-30. Max confirmed usage on the six remaining pairs in one pass:
--   14 "yes I wear" · 19 "yeah I wear it" · 04 "I love pink" · 09 "9 is new and yeah I wear it"
--   16 "I have a few yellow fits that require this. I wear it." · 02 "I wear"
--
-- TWO CLASSES OF ROW HERE, and the distinction matters:
--   shorts_14 and shorts_19 were NOT put on the body, but each is the identical model and size
--     of a pair that was, so their FIT is inherited and the source line says so.
--   shorts_04, shorts_09 and shorts_16 were never fitted at all and have no twin. Their verdicts
--     rest on Max's stated usage only. Their notes say the fit is unassessed rather than implying
--     a judgement that was never made.
--   shorts_02 was fitted; only the conditional was outstanding.

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP AS IS. Max wears it. FIT INHERITED, NOT FITTED: identical FootJoy model and identical W34 to shorts_03, which was measured on the body - hem 3.1 cm above the kneecap, waistband sitting at the natural waist with no gape, seat clean, and a leg on the wider side that hangs straight without flaring. Charcoal is a quiet neutral, so it does the same job as the navy under a loud polo, and unlike shorts_03 it carries no staining. If shorts_03 is eventually binned for its stain, this is the pair that absorbs its role.',
  pairs = 'Any loud polo.',
  avoid = 'Nothing identified.'
WHERE id = 'shorts_14_footjoy-charcoal';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP AS IS. Max wears it. FIT INHERITED, NOT FITTED: identical Cross Sportswear model and identical W34 to shorts_13, which was measured on the body - slim through hip, seat and thigh with no strain anywhere, welts flat, no pull lines, no creasing. Peach is his third loud short behind shorts_12 and shorts_13; that looked like surplus on paper, but all three get worn, so it earns its place. Same rule applies as to the others: when the shorts are the loud element the polo goes quiet.',
  pairs = 'White or grey tops - the shorts are the loud element.',
  avoid = 'A loud polo.'
WHERE id = 'shorts_19_crosssportswear-peach';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP. Max: "I love pink" - kept on affection and stated use, which is a perfectly good reason. FIT NOT ASSESSED: this pair was never put on for the fitting session and it has no identical twin to inherit from, so nothing is known about how it hangs, where the hem sits or how the seat sits. Its size is also still missing from the label. Worth one change at some point purely to close those two gaps - it is the only pair in the drawer with neither a fitting nor a readable size. Salmon pink is a loud short, so the same rule applies: quiet polo on top.',
  pairs = 'White or grey tops - the shorts are the loud element.',
  avoid = 'A loud polo, and specifically a pink one.'
WHERE id = 'shorts_04_tony-moro-pink';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP. Max: "9 is new and yeah I wear it." NEW GARMENT - condition is fresh and the earlier "used" note understates it. FIT NOT ASSESSED: never put on for the fitting session and no twin to inherit from. It is also a different class from everything else here - an athletic sport short with an elasticated waist and an interior drawcord, cut shorter than a bermuda - so none of the golf-short conclusions transfer to it. Bright white, which makes it a quiet base for a loud polo the same way shorts_20 is, though the sport cut means it reads more gym than course.',
  condition = 'New - little or no wear',
  pairs = 'Any loud polo. Casual and sport rather than a golf course.',
  avoid = 'Nothing identified.'
WHERE id = 'shorts_09_white-sport-unbranded';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP, and it has a specific job like shorts_18 does: Max has several yellow outfits that need it. That is what justifies a pale yellow short rather than general utility, and it should not be flagged as surplus later. FIT NOT ASSESSED: never put on for the fitting session and no twin to inherit from. Cotton twill with stretch, so on the pattern established across this drawer - every cotton pair fitted has been the weaker one - expect it to crease and to sit wider than the technical pairs. Worth confirming next time it comes out.',
  pairs = 'The yellow outfits it was bought for.',
  avoid = 'Cotton, so not a first-choice golf short.'
WHERE id = 'shorts_16_yellow-tartan-trim';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP, BUT ONLY UNDER A STRONG CONTRAST. Max wears it. Fitted 2026-08-30: hem 1.7 cm above the kneecap - one of the longer pairs, and fine for golf. The cut is good, better than the pale blue FootJoy: it hangs close to the leg with no flare and no tube. Waistband sits at the natural waist and stays up unbelted, so the size 38 on the label is meaningless on the body. Seat clean, no pull lines, no sag. THE COLOUR IS THE WHOLE LIMIT: blush sits only a few tones off his own leg colour, so at any distance the hem stops reading as a line and the boundary between short and leg blurs. Under a pink polo, as photographed, he becomes a single soft column from collar to knee - that is the one genuinely dated look produced in the whole session. Under navy, bottle green, crisp white or a saturated blue it is a good quiet base.',
  pairs = 'Navy, bottle green, white or saturated blue tops.',
  avoid = 'Pink, red, coral or any dusty pastel on top.'
WHERE id = 'shorts_02_blush-poly';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_14_footjoy-charcoal','verdict_code','manual','Keep, Max 2026-08-30: "yes I wear".'),
('shorts_14_footjoy-charcoal','fit','derived','FIT INHERITED from shorts_03 - identical FootJoy model, identical W34. Not put on the body.'),
('shorts_19_crosssportswear-peach','verdict_code','manual','Keep, Max 2026-08-30: "yeah I wear it".'),
('shorts_19_crosssportswear-peach','cut','derived','FIT INHERITED from shorts_13 - identical Cross Sportswear model, identical W34. Not put on the body.'),
('shorts_04_tony-moro-pink','verdict_code','manual','Keep, Max 2026-08-30: "I love pink". Verdict rests on stated usage alone - never fitted, no twin, size still unknown.'),
('shorts_09_white-sport-unbranded','verdict_code','manual','Keep, Max 2026-08-30: "9 is new and yeah I wear it". Never fitted, no twin.'),
('shorts_09_white-sport-unbranded','condition','manual','New, stated by Max 2026-08-30. Supersedes the "used - clean" read taken off the flat-lay.'),
('shorts_16_yellow-tartan-trim','verdict_code','manual','Keep, Max 2026-08-30: "I have a few yellow fits that require this. I wear it." Never fitted, no twin.'),
('shorts_02_blush-poly','verdict_code','manual','Keep with a contrast condition, Max 2026-08-30: "I wear".')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

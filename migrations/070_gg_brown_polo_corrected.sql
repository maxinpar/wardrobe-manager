-- 070_gg_brown_polo_corrected.sql
-- 2026-09-06. Corrects tops_101, which migration 069 got wrong in three ways.
--
-- 1. THE RENDER WAS NEVER BAD. Migration 069 rejected "GG Brown Render.jpeg" for measuring
--    #9D9B99, dead neutral. The measurement was right and the conclusion was wrong: the polo
--    carries a LARGE WHITE-AND-BLUE FLORAL PRINT over an olive-brown ground, and averaging the
--    whole garment mixes the white print into the ground until it reads neutral. The render is a
--    good likeness. It has now been filed to Retail and retail_prefix is restored.
--
--    THE LESSON, worth more than the row: the mean-channel colour test only works on PLAIN
--    garments. On a print, average the GROUND - the warm or saturated pixels - not the whole
--    garment. Measured that way, both renders agree: ground #605030 to #706040, red-minus-green
--    +16, red-minus-blue +32 to +48. A real olive-brown. See CLAUDE.md, RENDERS.
--
-- 2. THE "SUSPICIOUS BLUE FRAME" IS THE LABEL. Migration 069 flagged _02_label (#426FA7) as
--    possibly mis-sorted. It is the back-neck label, photographed against the polo's BLUE
--    CONTRAST COLLAR, which is why it measures blue. It reads, in full:
--        Good Good - FIGHTING FOR PAR - MEDIUM - GOODGOODGOLF.COM - 92% Polyester / 8% Spandex
--    So size and composition are now known and no longer NOT READ.
--
-- 3. IT IS NOT A PLAIN BROWN POLO. Olive-brown ground, all-over white flowers outlined in blue,
--    a blue contrast collar and placket, and a small red-orange embroidered mascot on the left
--    chest. Max's name for it stays "Good Good Brown polo" - his name, not a description.
--
-- A SECOND RENDER EXISTS and was not filed: "gg brrown render 2.jpeg". Same garment, but the
-- print is pushed much bluer and the collar brighter teal, so it sits further from the source
-- frames than the first render does. Kept in Downloads in case Max prefers it.
--
-- SIZING. MEDIUM is correct and not an outlier: goodgood-green-stripe-quarterzip is also a
-- MEDIUM, and batch 053 records Good Good as Korean-made and generously sized.

UPDATE items SET
    colour = 'Olive-brown with an all-over white and blue floral print, blue contrast collar',
    hex = '#665738',
    role_code = 'Pattern',
    pattern = 'Floral print',
    material = '92% polyester / 8% spandex',
    cut = 'Short-sleeve polo, blue contrast collar and placket, all-over floral print',
    fit = 'Size MEDIUM, read off the back-neck label. Correct - Good Good is Korean-made and sizes generously, and the Good Good quarter-zip is also a MEDIUM',
    condition = 'Good from the flat-lay and the two detail frames',
    verdict_note = 'A loud print, but the palette is quiet - olive and white with a blue collar, no bright colour anywhere. Closest thing in the wardrobe to the Good Good jade quarter-zip, which is the most current-looking golf piece Max owns.',
    formality_rank = 2,
    formality_note = 'Good Good is a young golf-media brand, no club crest. Large floral print - on the course, not the office',
    avoid = 'Anything else patterned, and olive or brown bottoms',
    notes = 'Good Good - FIGHTING FOR PAR, size MEDIUM, 92% polyester / 8% spandex, goodgoodgolf.com. Olive-brown ground with large white flowers outlined in blue; blue contrast collar and placket; small red-orange embroidered mascot on the left chest. GROUND MEASURED #605030 to #706040 on both renders. An earlier pass called this a plain brown polo with a failed grey render - both wrong, see migration 070.',
    retail_prefix = 'tops_101_goodgood-brown-polo_retail',
    unconfirmed = false
WHERE id = 'tops_101_goodgood-brown-polo';

UPDATE item_actions SET status = 'done', done_at = now(),
    note = note || ' RESOLVED 2026-09-06: the render is fine. The neutral reading was the white floral print averaging out the olive ground, not a failed render.'
WHERE item_id = 'tops_101_goodgood-brown-polo' AND required = 'Regenerate the retail render';

UPDATE item_actions SET status = 'done', done_at = now(),
    note = note || ' RESOLVED 2026-09-06: it is the back-neck label shot against the blue contrast collar. Correctly filed.'
WHERE item_id = 'tops_101_goodgood-brown-polo' AND required = 'Check source frame _02_label';

UPDATE item_field_sources SET source = 'derived',
    note = 'Ground measured on the warm pixels of both renders: #605030-#706040. Whole-garment mean is meaningless on a print.'
WHERE item_id = 'tops_101_goodgood-brown-polo' AND field_name = 'hex';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('tops_101_goodgood-brown-polo','fit','imported','Read off the back-neck label frame: MEDIUM.'),
('tops_101_goodgood-brown-polo','material','imported','Read off the back-neck label frame: 92% polyester / 8% spandex.');

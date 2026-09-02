-- 029_shorts_20_is_white.sql
-- 2026-08-30. Max corrected me: shorts_20 is WHITE, not the warm stone grey I measured.
--
-- Where the error came from: the hex on this row was the median of the garment centre in its
-- laid-flat photo, and that one photo was the odd one out in the shoot - taken on a dark
-- patterned rug in dimmer light rather than on the wooden floor like the other seventeen. The
-- measurement came back #C9C6C1 and I recorded a warm stone grey. I then rejected the Gemini
-- render for being "blown out to cool white" when the render was right and my number was wrong.
-- The render is now accepted and filed.
--
-- New hex #F0EFF4 is measured off the approved render at four points (both thighs, waistband,
-- lower leg), which agree to within two levels. Source is the render, not a photograph, and the
-- field source below says so.
--
-- The id, slug, photo_prefix and retail_prefix keep the word "stone" - the photos and the render
-- are already filed on Drive under those names and renaming would orphan them. Only the human
-- fields change.

UPDATE items SET
  name = 'Callaway white short',
  colour = 'White',
  hex = '#F0EFF4',
  notes = 'BRAND SOURCE: no sewn brand label in either photograph. Callaway is printed repeatedly along the black silicone shirt-gripper tape inside the waistband, between grey elastic bands - recorded on that basis and on no other. No size, no fibre and no country visible; all three left blank rather than guessed. Flat front, belt loops, zip fly, ecru pocketing. COLOUR: white, confirmed by Max on 2026-08-30. The earlier "stone grey" reading was an artefact of the only photograph of this pair being shot on a dark rug in poor light. The slug still says stone because the filed photo and render names depend on it.'
WHERE id = 'shorts_20_callaway-stone';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_20_callaway-stone','hex','manual','#F0EFF4 measured at four points on the approved render, after Max confirmed on 2026-08-30 that the garment is white. Supersedes #C9C6C1, which was measured off a photograph shot on a dark rug in poor light and was wrong.'),
('shorts_20_callaway-stone','colour','manual','White, stated by Max on 2026-08-30, correcting a measurement taken from a badly lit photograph.')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

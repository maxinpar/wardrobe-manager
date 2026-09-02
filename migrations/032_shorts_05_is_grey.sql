-- 032_shorts_05_is_grey.sql
-- 2026-08-30, fitting session. Max: "5 is a pale grey that I love wearing (as a colour)
-- because it goes with any LOUD colour top."
--
-- The catalogue had this as "Stone / warm off-white #E7DFD7" - measured off the flat-lay, which
-- was warm-lit and over-exposed. On the body it is plainly a neutral grey. Measured again from
-- the worn front photograph with a white-balance correction against the white wall in frame
-- (wall #CECAC6 normalised to neutral, then exposure-scaled): the cloth comes back #8E8E8A,
-- a near-neutral mid-pale grey with only a trace of warmth. Nothing like #E7DFD7.
--
-- SECOND-ORDER PROBLEM: the retail render inherited my wrong description - the prompt said
-- "warm stone off-white" - and came back a warm greige (#D0C7C0 measured). So the render is
-- wrong too, for the same reason shorts_20's was briefly rejected: the description, not the
-- model. Flagged in the notes; the render wants regenerating from the corrected colour.
--
-- This is the same class of error as shorts_20: a colour measured off one badly lit photograph.

UPDATE items SET
  colour = 'Pale-mid grey',
  hex = '#8E8E8A',
  notes = 'NO BRAND FOUND. Neither photograph shows a brand label or mark; brand deliberately left blank. Care label: 100% polyester, size 36, country partly legible only. Green / navy / red striped elastic inner waistband with orange piping down the fly facing, zip fly, belt loops. COLOUR: a near-neutral pale-mid grey, confirmed by Max on 2026-08-30 - he rates it his most useful short because it takes any loud polo. The earlier "stone / warm off-white" was measured off a warm-lit flat-lay and was wrong. RENDER NEEDS REGENERATING: the existing retail render inherited that wrong description and came back warm greige. SIZE FLAG: 36 is above his usual W33-34 and the fit photographs show it - roomy through the seat and thigh, though it stays up unbelted.'
WHERE id = 'shorts_05_stone-poly-webbing';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_05_stone-poly-webbing','colour','manual','Pale-mid grey, stated by Max at the 2026-08-30 fitting. Corrects a warm off-white read off an over-exposed flat-lay.'),
('shorts_05_stone-poly-webbing','hex','manual','#8E8E8A measured from the worn front photograph, white-balanced against the white wall in frame and exposure-corrected. Supersedes #E7DFD7.')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

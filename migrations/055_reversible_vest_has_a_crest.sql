-- 055_reversible_vest_has_a_crest.sql
-- 2026-09-01. The Peter Millar reversible vest DOES carry an RSGC crest. Both faces. My error.
--
-- Migration 053 recorded both rows as "NO CREST, NO LOGO" and built an argument on it: that the
-- blue face was "the one garment here that passes at the office" because it was unbranded. That
-- was wrong and it was not a close call - the crest is embroidered on the left chest of BOTH
-- faces, tonal on each: PINK crowned crest on the pale blue side, PALE BLUE-GREY crowned crest on
-- the pink side. It is plainly visible in PXL_20260831_072523044 and _072509028 at full
-- resolution. It was missed because both frames were only ever read at contact-sheet size, where
-- a tonal crest on its own ground disappears.
--
-- CAUGHT BY THE RENDER, not by me. The regenerated retail render for outerwear_20 came back
-- showing a pink crowned monogram on the chest. I went to the original frames intending to prove
-- the render had invented it. It had not. Third time in this batch that a render was right and
-- the catalogue row was wrong - see outerwear_16 (rain jacket read as a windshirt) and
-- outerwear_18 (jacket read as a vest).
--
-- ALSO CORRECTED: the two faces are not both quilted. The BLUE face is diamond-quilted; the PINK
-- face is a smooth softshell with no quilting. Migration 053 described both as quilted.
--
-- OCCASION TAGS ARE UNCHANGED, deliberately. Max's ruling of 2026-09-01 stands: a crest decides
-- only whether a garment leaves the course, and it is not a defect. A tonal crest on its own
-- ground is about as quiet as a club mark gets, so casual + weekend on both faces and work on the
-- blue face all still hold. What changes is the REASON recorded for them: quiet and tonal, not
-- unbranded. A claim that rested on a false premise does not get to keep its wording.

UPDATE items SET
  cut = 'Full-zip sleeveless quilted vest, diamond quilting, matte shell, contrast pink binding at the collar and armholes',
  formality_note = 'Tonal PINK crowned RSGC crest on the left chest. Quiet, but it is there',
  notes = 'PETER MILLAR, size M, made in Vietnam, polyurethane membrane - brand read at full resolution off the neck label. Same garment as outerwear_19 worn the other way out; entered separately at Max''s instruction and the two rows are not linked. The BLUE face is diamond-quilted and carries a pink crowned RSGC crest on the left chest.',
  verdict_note = 'The blue face of the reversible vest, and the most useful thing in this batch. Over a plain polo with the Inesis navy trousers it reads as a normal relaxed Friday rather than golf kit - the crest is tonal pink on pale blue and does not announce itself.'
WHERE id = 'outerwear_20_peter-millar-reversible-vest-blue';

UPDATE items SET
  cut = 'Full-zip sleeveless vest, SMOOTH softshell face with no quilting, matte finish, contrast pale blue binding at the collar and armholes',
  formality_note = 'Tonal PALE BLUE-GREY crowned RSGC crest on the left chest. Quiet, but it is there',
  notes = 'PETER MILLAR, size M, made in Vietnam, polyurethane membrane. REVERSIBLE - pink one way, pale blue the other, with the opposite colour showing as binding. This face is a smooth softshell; the blue face is diamond-quilted. Carries a pale blue-grey crowned RSGC crest on the left chest.',
  verdict_note = 'Still the best piece in the batch. Reversible: this row is the pink face, outerwear_20 is the blue. Entered as two independent rows at Max''s instruction, deliberately not linked.'
WHERE id = 'outerwear_19_peter-millar-reversible-vest-pink';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('outerwear_20_peter-millar-reversible-vest-blue','formality_note','manual','CREST CORRECTION 2026-09-01. Migration 053 recorded NO CREST, NO LOGO on this row and used it as the reason the garment works at the office. False: there is a pink crowned RSGC crest embroidered on the left chest, clearly visible in PXL_20260831_072523044 at full resolution. Missed because the frame was only read at contact-sheet size, where a tonal crest on its own ground vanishes. Lesson: check for chest embroidery at full resolution before asserting a garment is unbranded - a tonal crest is invisible in a thumbnail.'),
('outerwear_19_peter-millar-reversible-vest-pink','formality_note','manual','CREST CORRECTION 2026-09-01. As outerwear_20. This face carries a pale blue-grey crowned RSGC crest on the left chest, visible in PXL_20260831_072509028 at full resolution.'),
('outerwear_19_peter-millar-reversible-vest-pink','cut','manual','This face is a SMOOTH softshell, not quilted. Migration 053 described both faces as quilted; only the blue one is.')
ON CONFLICT DO NOTHING;

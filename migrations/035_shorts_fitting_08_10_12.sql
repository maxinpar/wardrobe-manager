-- 035_shorts_fitting_08_10_12.sql
-- 2026-08-30 fitting, third round.
--
-- shorts_08: Max - "let's flag as bin but I'll keep it for now as I decide." That is exactly what
-- the 'Replace' verdict is for: owned, still wearable, on the way out. Not 'Bin', which would stop
-- it being suggested at all while he is still deciding. Revisit once shorts_01 or shorts_17 has
-- been fitted as the harbourside pair.
--
-- shorts_10: Max - "the light blue one again is cotton. I rarely wear for golf because of this but
-- every now and then I do need a pale blue for a golf outfit and I'll wear it."
--
-- shorts_12: Max - "a GREAT fabric: mega super light and uncreasable. The colour is harder to
-- match but is loud and works with white or grey top and goes well with my decathlon strawberry
-- shoes."
--
-- Measured hems above the top of the kneecap: shorts_10 3.6 cm, shorts_12 3.0 cm. Both correct
-- for golf.

UPDATE items SET
  verdict_code = 'Replace',
  unconfirmed = false,
  verdict_note = 'FLAGGED FOR BIN, held while Max decides (2026-08-30). Barely worn, and never willingly for golf - he dislikes the roughish cotton hand on a course and reads the pair as a marina piece. The marina occasion is legitimate and he has it, but this garment does not serve it: at EU42 it is a size under and the fitting photographs show real strain - side pocket pulling open, diagonal drag lines from the hip across the thigh, seat stretched with the pocket welt distorted. Add the turn-up cuff piling bulk at the widest point of the leg, the longest hem in the drawer at 1.4 cm above the kneecap, and faint discolouration plus a dark line on cream cloth that bright harbour light will find. Fails on fit and condition, not on style. Decide against shorts_01 (Zara tan chino, his actual size) and shorts_17 (chambray linen-look) once those are fitted - if either lands, this goes with no gap left behind.'
WHERE id = 'shorts_08_decathlon-cream-twill';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP, but it is not really a golf short and Max does not treat it as one - cotton, and it creases badly, which is why it rarely goes on a course. He keeps it for the occasional round where the outfit needs a pale blue. Fitted 2026-08-30: hem 3.6 cm above the kneecap, the highest in the drawer and fine. Waist sits at the natural waist. The seat is roomy with visible slack and the leg openings are the widest of any pair fitted - the hems stand away from the leg rather than following it - so it reads relaxed and a little boxy next to the technical pairs. Not worth altering for a secondary short. ITS REAL HOME MAY BE HARBOURSIDE, not golf: a relaxed pale blue cotton short is exactly right for a marina, where the creasing is a feature and technical fabric would look like golf kit off the course. Fit it against shorts_08 and shorts_17 for that role. And if the stain lifts on shorts_03, that FootJoy is the better pale blue for actual golf and this one drops to weekend duty entirely.',
  pairs = 'Weekend and harbourside. On a course only when the outfit needs pale blue.',
  avoid = 'Not a first-choice golf short - it creases.'
WHERE id = 'shorts_10_decathlon-pale-blue';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP AS IS. One of the best-fitting pairs in the drawer and the fabric is the reason - Max rates it "mega super light and uncreasable", and the side and back photographs bear that out: not a single crease anywhere after being worn, clean drape, no slack. Fitted 2026-08-30: hem 3.0 cm above the kneecap, correct for golf. Seat clean and well shaped with no pull lines, leg hangs straight with a moderate opening. Colour is a loud saturated red-orange - Max notes it is harder to match, and that it works with a white or grey top and with his Decathlon strawberry shoes. That is the right instruction: this is the one case in the drawer where the SHORTS are the loud element, so the polo has to go quiet.',
  pairs = 'White or grey tops. Decathlon strawberry shoes.',
  avoid = 'A loud polo - the shorts are already the loud element here.'
WHERE id = 'shorts_12_decathlon-orange-tech';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_08_decathlon-cream-twill','verdict_code','manual','Replace - flagged for bin but held, on Max''s instruction 2026-08-30, pending a harbourside replacement from what he already owns.'),
('shorts_10_decathlon-pale-blue','verdict_code','manual','Keep, Max 2026-08-30: rarely worn for golf because of the cotton, kept for outfits that need a pale blue.'),
('shorts_12_decathlon-orange-tech','verdict_code','manual','Keep, Max 2026-08-30: rates the fabric highly, pairs it with white or grey tops and the Decathlon strawberry shoes.')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

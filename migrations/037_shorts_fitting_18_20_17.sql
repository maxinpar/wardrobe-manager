-- 037_shorts_fitting_18_20_17.sql
-- 2026-08-30 fitting, fifth round.
--
-- shorts_18, Max: "another ultra light weight tech but boring navy short. I like it I like the
--   fit. Only wear it when representing the team (navy bottoms)."
-- shorts_20, Max: "my white golf shorts, possibly a shade loose? I wore those today with this
--   shirt, banging combo I think. Ignore the stains, it just stains immediately after a day of
--   golf."
-- shorts_17, Max: "tight, for sure. weird jean blue hue. Defo not golf shorts I'd wear on the
--   course. Elsewhere though?"
--
-- Measured hems above the top of the kneecap: shorts_18 3.0 cm, shorts_20 2.2 cm, shorts_17
-- 2.7 cm. All correct for golf; shorts_17 is not a golf short regardless.
--
-- COLOUR: not touched on any of these. The white-balance trick that fixed shorts_05 needs a
-- clean neutral reference in frame and these three shots do not have one where the garment is.
-- shorts_17's hue is disputed by Max ("weird jean blue") and is added to the side-by-side colour
-- shoot already queued for the end of the fitting session.

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP AS IS, and it has a specific job: this is the pair Max wears when the team requires navy bottoms. That alone justifies it even though he owns two other navy-family shorts. Fitted 2026-08-30: hem 3.0 cm above the kneecap, correct for golf. Seat clean and well shaped, no slack, no pull lines, and no creasing after wear - the ultralight technical cloth Max rates, and the lightest thing he owns. He likes the fit and said so unprompted. Boring navy is the point, not a criticism: the colour lives in the polo.',
  pairs = 'Team days when navy bottoms are required. Any loud polo otherwise.',
  avoid = 'Nothing identified.'
WHERE id = 'shorts_18_navy-blue-lined';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP. Max asked "possibly a shade loose?" - yes, confirmed, and it is the loosest pair fitted alongside shorts_05. The back view shows real slack across the seat: the cloth hangs away from the body rather than following it, and the leg is on the wide side. Everything else is right - hem 2.2 cm above the kneecap, waistband sitting at the natural waist and staying put. OPTIONAL ALTERATION: taking roughly 2 cm out of the waist and seat, leaving the thigh alone so the swing keeps its room, would move this from fine to sharp for about $30-40. White shows silhouette more than any other colour in the drawer, so it is the pair where that money buys the most. Not urgent - his call. STAINING IS NOT A DEFECT HERE: Max reports white golf shorts mark within a single round, which is a property of the colour rather than damage to this garment. Do not let it drive a verdict. CONFIRMED COMBINATION: worn with the pink striped polo on 2026-08-30 and Max rates it - white shorts under a loud polo is exactly the formula this drawer is built on.',
  pairs = 'Any loud polo. Confirmed good with the pink striped polo.',
  avoid = 'Nothing identified.'
WHERE id = 'shorts_20_callaway-stone';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP, NON-GOLF ONLY - Max is explicit that it never goes on a course. Fitted 2026-08-30: hem 2.7 cm above the kneecap. It is at the tight end - the side view shows the pocket pulling slightly and a crease radiating from the hip - but it is nothing like the strain on shorts_08 and it is wearable. The real reservation is the colour, and it is his: a mid denim-teal that he calls a "weird jean blue hue", neither navy nor pale blue, and duller on the body than the stored hex suggests. NOT YET THE HARBOURSIDE ANSWER: shorts_01, the Zara tan chino in his actual size, should be fitted before this is assigned that role - tan is the more reliable marina colour and Max is ambivalent about this one. If shorts_01 lands, this and shorts_10 both become surplus casual shorts and one of them can go with shorts_08.',
  pairs = 'Weekend and casual only.',
  avoid = 'Never on a golf course - Max is explicit.'
WHERE id = 'shorts_17_chambray-linen-look';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_18_navy-blue-lined','verdict_code','manual','Keep, Max 2026-08-30: likes the fit, wears it for team navy-bottom days.'),
('shorts_20_callaway-stone','verdict_code','manual','Keep, Max 2026-08-30. He raised the looseness himself and it is confirmed in the back view; alteration offered, not imposed.'),
('shorts_17_chambray-linen-look','verdict_code','manual','Keep but non-golf, Max 2026-08-30: "tight, for sure. weird jean blue hue. Defo not golf shorts."')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

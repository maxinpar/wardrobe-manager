-- 039_shorts_01_fitted.sql
-- 2026-08-30, last fitting of the session. Max: "here is 1. I rarely wear this for golf."
--
-- Measured hem about 2.3 cm above the top of the kneecap - one of the longer pairs, in the same
-- band as shorts_13 and shorts_20. Per-pair precision is roughly +/-1 cm.
--
-- THIS CLOSES THE HARBOURSIDE QUESTION. Four candidates were in play - shorts_01, shorts_08,
-- shorts_10 and shorts_17 - and this is the best of them on every axis that matters for that
-- setting: cotton rather than technical, so it does not read as golf kit off the course; a warm
-- tan, which is the reliable colour there in a way that pale blue and denim-teal are not; and it
-- is the only one of the four in Max's actual size (EUR44 / US34), fitting cleanly at the waist
-- with no gape and no strain anywhere.
--
-- With this settled, shorts_08 has nothing left to be. Its verdict stays 'Replace' pending Max's
-- word, but the case for binning it is now complete rather than provisional.

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP - THIS IS THE HARBOURSIDE SHORT. Max rarely wears it for golf, which is right: it is cotton twill and creases like one, visibly so across the front and seat in the fitting photographs. That is a fault on a course and a virtue at a marina. Fitted 2026-08-30: hem about 2.3 cm above the kneecap, waistband sitting cleanly at the natural waist with no gape - the only one of the four casual candidates in his actual size - and a seat with only slight excess and no pull lines. Two qualifications, neither disqualifying: it wears a TURN-UP CUFF at the hem, which adds bulk at the widest point of the leg, and the leg is on the wider side. On a tan chino short a turn-up reads as a considered detail rather than a dated one, so leave it unless Max dislikes it; removing the cuffs is a cheap change if he ever does. Warm tobacco tan works well against his skin and sits comfortably under the pink polo he photographed it with.',
  pairs = 'Harbourside, weekend, lunch. Linen shirts and knit polos; loafers or boat shoes.',
  avoid = 'Not a golf short - it creases, and Max does not choose it for a course.'
WHERE id = 'shorts_01_zara-tan-chino';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_01_zara-tan-chino','verdict_code','manual','Keep and assigned the harbourside role, 2026-08-30, after fitting all four casual candidates. Max: "I rarely wear this for golf."')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

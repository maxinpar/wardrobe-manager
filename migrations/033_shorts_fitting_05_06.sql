-- 033_shorts_fitting_05_06.sql
-- 2026-08-30, shorts fitting session. Max: "we'll keep." Verdicts written for the two pairs
-- fitted in that round. unconfirmed cleared - a fitting is exactly the confirmation event the
-- flag was waiting for. Where something is still NOT established, the note says so rather than
-- the flag staying on forever.
--
-- Length was measured, not eyeballed: each front photograph was scaled so knee-to-floor matched,
-- kneecaps aligned, hems marked. shorts_05 sits 3.1 cm above the top of the kneecap, shorts_06
-- 2.9 cm. Both correct for a golf short - the category runs 9-11 inch inseams and is meant to
-- land at or just above the knee. An earlier call in this session that these were "too long"
-- applied a general menswear rule to a category with its own convention and was withdrawn.
--
-- shorts_05 name updated to match the corrected colour from migration 032. Slug, photo_prefix
-- and retail_prefix keep "stone" because the filed photos and render depend on them.

UPDATE items SET
  name = 'Pale grey technical short',
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP AS IS. Max''s most useful short and he knows it - a near-neutral pale-mid grey is the only thing in the drawer that takes a loud polo of any hue without a decision, which is the job his shorts have to do. Fitted 2026-08-30: hem 3.1 cm above the kneecap, correct for golf. Waistband sits at the natural waist and stays up unbelted despite the size 36. Leg hangs straight, no flare, moderate opening. The seat is the loosest of the pairs fitted - visible slack under it and some excess through the thigh - but that room is wanted for a swing, so no alteration. Revisit only if it slides while walking, in which case take 2 cm out of the waist.',
  pairs = 'Any loud polo - it is the neutral that never fights the top.',
  avoid = 'Nothing identified.'
WHERE id = 'shorts_05_stone-poly-webbing';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP AS IS. The best silhouette in the drawer. Max calls it his tightest-fitting pair; on the fitting photographs that is a virtue, not a fault - it is visibly narrower through the thigh and leg opening than the others and follows the leg instead of hanging off it, which is the single thing separating a current golf short from a dated one. Fitted 2026-08-30: hem 2.9 cm above the kneecap, correct for golf. No distress standing - no pull lines across the seat, pocket welts flat, no strain at the fly, no waistband roll, so the W32 genuinely fits. NOT ESTABLISHED: whether it binds in a squat or through a swing. Standing photographs cannot answer that and Max has not reported on it. If it ever does bind, this drops to occasional wear rather than a rotation piece.',
  pairs = 'Any polo. Navy is the workhorse neutral.',
  avoid = 'Nothing identified.'
WHERE id = 'shorts_06_footjoy-navy';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_05_stone-poly-webbing','verdict_code','manual','Keep, decided by Max at the 2026-08-30 fitting.'),
('shorts_06_footjoy-navy','verdict_code','manual','Keep, decided by Max at the 2026-08-30 fitting. Swing/squat comfort not tested.')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

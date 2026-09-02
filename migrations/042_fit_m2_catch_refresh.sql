-- 042_fit_m2_catch_refresh.sql
-- 2026-08-30, immediately after 041. Housekeeping: the catch on fit_m2 and the note on its shoe
-- row both still said the driving moc was "currently scope = out", which stopped being true one
-- migration ago. Stale warning text is worse than none - it sends the reader off to solve a
-- problem that is already solved.

UPDATE fits SET
  catch = 'Nothing blocking it. The navy suede driving moc this fit is built on used to be out of scope, marked holiday only; it was brought into the rotation on 2026-08-30 precisely so this fit could stand up. If it ever goes back out, the fallback is the brown suede loafer, and this fit then duplicates fit_m1_tan-and-cornflower.'
WHERE id = 'fit_m2_white-blue-and-burgundy';

UPDATE fit_items SET
  note = 'Sockless. Brought into the rotation on 2026-08-30 for this fit.'
WHERE fit_id = 'fit_m2_white-blue-and-burgundy'
  AND item_id = 'shoes_08c_megis-driving-moc';

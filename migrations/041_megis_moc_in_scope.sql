-- 041_megis_moc_in_scope.sql
-- 2026-08-30. Max: bring the Ateliers Megis navy suede driving moccasin into scope.
--
-- It was 'out', noted "holiday only". The marina fits are the argument that changed it: a navy
-- suede driving moc is the most correct shoe he owns for a harbourside setting, and Sydney gives
-- him that setting year-round rather than once a year on holiday.
--
-- This also closes the precondition on fit_m2_white-blue-and-burgundy, which existed solely to
-- record that this decision was outstanding. The fit is no longer blocked.

UPDATE items SET
  scope_code = 'core',
  verdict_note = 'KEEP, IN THE ROTATION. Brought into scope 2026-08-30 on Max''s instruction, from "holiday only - out of scope". The reasoning is the marina fits: a navy suede driving moccasin is the most correct shoe he owns for a harbourside setting, and living a short distance from Sydney''s marinas makes that an ordinary occasion rather than a once-a-year holiday one. It is the shoe fit_m2_white-blue-and-burgundy is built on, and without it that fit falls back to the brown suede loafer and duplicates fit_m1.'
WHERE id = 'shoes_08c_megis-driving-moc';

UPDATE fit_preconditions SET
  done = true,
  done_at = now()
WHERE fit_id = 'fit_m2_white-blue-and-burgundy'
  AND item_id = 'shoes_08c_megis-driving-moc'
  AND NOT done;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shoes_08c_megis-driving-moc','scope_code','manual','Moved from out to core on Max''s instruction, 2026-08-30, off the back of the marina fits.')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

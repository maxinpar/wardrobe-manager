-- 047_navy_chino_fit_prose.sql
-- 2026-08-31. Two jobs.
--
-- 1. Remove fit_test_fit, built in the app 2026-08-30 while trying the create-a-fit form.
--    Max confirmed it can go. fit_items first, then the fit, then the lookup tables that
--    reference it. Nothing else points at it - it has no wear events and no hero image.
--
-- 2. Fill style / commentary / catch on the two navy-chino fits Max built in the app on
--    2026-08-31. The items and the derived flags were already correct; only the prose was
--    missing, and per the port brief that prose is the rule engine, not decoration. The
--    reasoning below was worked out when the fits were designed and lives in
--    claude/trousers-17-inesis-navy.md - this migration moves it into the database so the
--    app shows it and a future session does not have to re-derive it.
--
-- Voice matched to the existing fits: commentary says why the combination works, catch says
-- what to do before wearing it. Both catches below name real, already-recorded conditions
-- rather than inventing new ones.

DELETE FROM fit_items      WHERE fit_id = 'fit_test_fit';
DELETE FROM fit_occasions  WHERE fit_id = 'fit_test_fit';
DELETE FROM fit_seasons    WHERE fit_id = 'fit_test_fit';
DELETE FROM fit_temp_bands WHERE fit_id = 'fit_test_fit';
DELETE FROM fit_preconditions WHERE fit_id = 'fit_test_fit';
DELETE FROM fit_field_sources WHERE fit_id = 'fit_test_fit';
DELETE FROM fits           WHERE id = 'fit_test_fit';

UPDATE fits SET
  style = 'French banker, no jacket',
  commentary = 'The shirt''s own catalogue card asks for this trouser by name - "beige/stone chino with a black belt, navy chino, dark denim, worn open-collar, no tie". Navy, dusty pink and cognac is as safe as this gets while still being a choice. It is also the only place tops_12 can go without a blazer: its one other fit is fit_s3, grey blazer over navy wool, and in a Sydney September a rank-5 shirt with no jacket had no rank-4 bottom to sit on until this trouser turned up.',
  catch = 'Hem the trouser first - it is 2-3cm long and breaks on the shoe. Shirt tucked, collar open, no tie. Do NOT add the Zara navy blazer: navy jacket on navy chino in two different cloths is the obvious way to wreck it. Swap the Church''s for the brown chelsea if it needs to read younger.'
WHERE id = 'fit_pink_stripe_and_navy_chino';

UPDATE fits SET
  style = 'best knit, off duty',
  commentary = 'The Fedeli is flagged "best piece owned" and "pale neutral, so it needs a dark bottom to read at all", and until now the only navy under it was suit wool - so the best garment in the wardrobe was locked to one dressed-up look, fit_oatmeal_and_navy_wool. Same colour logic, register he can actually wear on a Saturday. Olive is named in the knit''s own pairs line, which is what the Air Max brings.',
  catch = 'Repair the Fedeli cuff hole and the neck mark first. Clean the Air Max - the toes are grubby. Hem the trouser. Webbing belt rather than leather: with a sneaker there is no leather to match and navy/white keeps it tonal. Swap to the brown chelsea and the distressed brown belt if it needs to survive a nice lunch.'
WHERE id = 'fit_fedeli_and_navy_chino';

INSERT INTO fit_field_sources (fit_id, field_name, source, note) VALUES
('fit_pink_stripe_and_navy_chino','commentary','manual','Reasoning from claude/trousers-17-inesis-navy.md, written when the fit was designed 2026-08-30.'),
('fit_fedeli_and_navy_chino','commentary','manual','Reasoning from claude/trousers-17-inesis-navy.md, written when the fit was designed 2026-08-30.')
ON CONFLICT DO NOTHING;

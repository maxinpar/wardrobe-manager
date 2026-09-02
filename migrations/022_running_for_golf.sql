-- 022_running_for_golf.sql
-- Max, 2026-08-30: he plays golf in running shoes by choice, not by accident - cheaper than
-- golf shoes by a wide margin, better looking, and in his experience the performance matches
-- a $400 pair of FootJoys. Years of doing it, no regrets. So "running shoe" is not a reason
-- to exclude something from golf in this catalogue.
-- The Kalenji olive and the Nike trail pair are golf shoes in practice and are tagged as such.

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('shoes_14_kalenji-olive','golf'),
('shoes_20_nike-yellow-trail','golf')
ON CONFLICT DO NOTHING;

UPDATE items SET
  verdict_note = 'In golf rotation. A Kalenji running shoe by make, but Max plays in running shoes deliberately - see notes.',
  pairs = 'Golf, running, gym.',
  avoid = 'Smart wear.',
  notes = 'Kalenji (Decathlon running). Teal forefoot, dark grey heel, running tread. Used for golf: Max plays in running shoes by choice - cheaper, better looking, and performance he rates against any premium golf shoe.',
  updated_at = now()
WHERE id = 'shoes_14_kalenji-olive';

UPDATE items SET
  verdict_note = 'In golf rotation, but held back for now - Max is not ready to wreck them on a course yet.',
  pairs = 'Golf, running, gym.',
  avoid = 'Smart wear. Wet or chewed-up courses while he still wants them clean.',
  notes = 'Nike, style code FV3929-700, EUR44 / UK9 / US10. Black and yellow lugged trail outsole. Golf-eligible, but deliberately not yet played in.',
  updated_at = now()
WHERE id = 'shoes_20_nike-yellow-trail';

UPDATE items SET
  notes = coalesce(notes,'') || ' Note: running shoes are a legitimate golf choice in this wardrobe - this pair is out of golf on Max''s judgement of the sole, not because it is a running shoe.',
  updated_at = now()
WHERE id = 'shoes_19_inesis-jf100-1-grey';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shoes_14_kalenji-olive','occasions','manual','Golf added 2026-08-30. Max plays in running shoes by choice.'),
('shoes_20_nike-yellow-trail','occasions','manual','Golf added 2026-08-30, with a hold on actually wearing them on course.')
ON CONFLICT DO NOTHING;

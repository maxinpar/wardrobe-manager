-- 036_shorts_fitting_13_15_11.sql
-- 2026-08-30 fitting, fourth round.
--
-- shorts_13, Max: "by far the shortest of the shorts I own. And also very tight. I've worn them
-- maybe twice to golf. I think they're honestly a bit short and some golfers like that, its a
-- style, I'm not sure it's mine though. Could have other uses? Great condition."
-- shorts_15, Max: "tech fabric, mega ultra light, boring navy though."
--
-- MEASUREMENT vs PERCEPTION on shorts_13. Measured hem above the top of the kneecap: 2.3 cm,
-- against 2.7 for shorts_15 and 3.6 for shorts_10. By hem position it is one of the LONGER pairs
-- in the drawer, not the shortest - the opposite of how it reads to Max. Per-pair precision is
-- about +/-1 cm so the exact figure is soft, but not soft enough to make it the shortest.
-- The reconciliation is leg width, not length: this is the slimmest-cut pair fitted, and a leg
-- that follows the thigh always reads shorter than one that drapes over it at the same hem
-- height. Being tight, it may also genuinely ride up in motion, which standing photographs
-- cannot show. Recorded as an open question rather than resolved.
--
-- shorts_11 is written here WITHOUT being fitted: it is the same Decathlon model as shorts_15
-- (style ref 71332 / CC 313059) in the same size EU L, so the fit verdict transfers. Its
-- provenance line says so explicitly.

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP, but REASSIGNED away from golf. The garment is not the problem - it is the slimmest, cleanest-fitting pair in the drawer alongside shorts_06: close through the hip, seat and thigh with no strain anywhere, pocket welts flat, no pull lines, no creasing, and in great condition by Max''s own account. The problem is that he has worn it twice in its life and is not sure the slim short-reading style is his. It is also a second LOUD short competing with shorts_12, which has the better fabric and a pairing formula he already likes. So: weekend, holiday and summer wear, and the backup loud short when shorts_12 is in the wash. Worth one more round on a course now that he knows the leg is genuinely good rather than tight. If it is still unworn by the end of next season, bin it then - that is a preference call, not a fault. NOTE the length paradox: it measures 2.3 cm above the kneecap, one of the LONGER pairs he owns, and reads short only because it is the slimmest.',
  pairs = 'Weekend and holiday. White or grey tops if worn for golf - it is the loud element.',
  avoid = 'A loud polo. Not the first-choice loud short - shorts_12 is.'
WHERE id = 'shorts_13_crosssportswear-red';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP AS IS. Max calls it "mega ultra light, boring navy though" - and boring is the job. He wants the colour in the polo, so the short has to shut up, and a plain dark navy in an ultralight technical cloth is the most reliable way to do that. Fitted 2026-08-30: hem 2.7 cm above the kneecap, correct for golf. Seat clean and well shaped, no slack, no pull lines, no creasing after wear. Slightly roomier through the thigh than shorts_06 or shorts_13 but still following the leg rather than draping. A workhorse, and it should be treated as one.',
  pairs = 'Any loud polo. This is a base layer for colour.',
  avoid = 'Nothing identified.'
WHERE id = 'shorts_15_decathlon-navy-tech';

UPDATE items SET
  verdict_code = 'Keep',
  unconfirmed = false,
  verdict_note = 'KEEP AS IS - VERDICT INHERITED, NOT FITTED. This is the same Decathlon model as shorts_15 (style ref 71332 / CC 313059) in the same size EU L, differing only in colour, so its fit verdict transfers: hem correct for golf, clean seat, no slack, ultralight technical cloth that does not crease. Slate grey is if anything the more useful of the two colours under a loud polo. Max was deliberately not asked to change into this pair, on the basis that fitting its twin answered the same question. If it ever behaves differently on the body, this note is the thing to correct.',
  pairs = 'Any loud polo. Grey is the most forgiving neutral he owns.',
  avoid = 'Nothing identified.'
WHERE id = 'shorts_11_decathlon-slate-tech';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_13_crosssportswear-red','verdict_code','manual','Keep but reassigned off golf, 2026-08-30. Max: worn twice, unsure the style is his, great condition.'),
('shorts_15_decathlon-navy-tech','verdict_code','manual','Keep, Max 2026-08-30: rates the fabric, calls the colour boring - which is the point.'),
('shorts_11_decathlon-slate-tech','verdict_code','derived','INHERITED from shorts_15, its identical twin (ref 71332 / CC 313059, same size). NOT fitted on the body. Correct this if it ever wears differently.')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

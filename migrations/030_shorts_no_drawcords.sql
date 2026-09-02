-- 030_shorts_no_drawcords.sql
-- 2026-08-30. Max: "12 is solid. None of my shorts have draw cords, they are all tailored shorts."
--
-- Three of my construction descriptions were inference dressed up as observation, and I then
-- rejected three correct renders for not matching them:
--
--   shorts_13 and shorts_19 - I recorded "elasticated waist with drawcord, fully lined" for both.
--     No photograph of either pair shows a drawcord. What the photographs actually show is a black
--     woven tape inside the waistband with cross|sportswear repeated along it - an inner grip tape,
--     not an elasticated waist. I read swim-short construction into a tailored short.
--   shorts_12 - I recorded a grey side panel with a white stripe down each leg. That grey-and-white
--     is the inner facing, visible only because the waistband was held open for the label shot. The
--     outside of the garment is plain orange, as the render showed.
--
-- The renders for 12, 13 and 19 are correct and are now filed. Rows corrected here.
--
-- shorts_09 is deliberately NOT changed: its photograph shows a dark grey flat drawcord, knotted,
-- lying across the white cloth beside a grey elastic waistband tape. That contradicts the general
-- statement, so it is being put back to Max rather than edited on either of our say-so.

UPDATE items SET
  cut = 'Flat front, lined',
  material = '100% polyester shell, 100% polyester lining',
  notes = 'BRAND SOURCE: no conventional sewn brand label. The name is woven into the black inner waistband tape and printed on a small sewn tab reading cross|sportswear MENSWEAR, confirmed on the peach twin shorts_19. Care label: shell 100% polyester, lining 100% polyester. No size and no country visible on this pair. A TAILORED short with a conventional waistband - the black tape inside the waistband is a grip tape, not an elasticated waist, and there is no drawcord (Max, 2026-08-30). Tan lining, red topstitching. SAME MODEL as shorts_19 in peach.'
WHERE id = 'shorts_13_crosssportswear-red';

UPDATE items SET
  cut = 'Flat front, lined',
  material = '100% polyester shell, 100% polyester lining',
  notes = 'Brand tab reads cross|sportswear MENSWEAR. Grey size tab reads W34, from the clearer photograph Max took on 2026-08-30. Care label Swedish-first (SE YTTERTYG: POLYESTER 100%), wash 40: shell 100% polyester, lining 100% polyester. Country not legible. A TAILORED short with a conventional waistband - no drawcord and no elasticated waist (Max, 2026-08-30). Tan lining, orange topstitching. SAME MODEL as shorts_13 in red.'
WHERE id = 'shorts_19_crosssportswear-peach';

UPDATE items SET
  pattern = 'Plain',
  notes = 'Decathlon size label: ref 62495, CC 125541, Cm 100-104, CN 180/88A, EU 44, US M, plus the usual BR / RU / MX / IR run. Fibre content and country are not on the panel photographed. The garment is PLAIN ORANGE on the outside (Max, 2026-08-30). The grey panel and white stripe visible in the label photograph are the inner facing, seen only because the waistband was held open - they are not an exterior side panel. SIZE FLAG: EU 44 matches his usual EUR44 but the US mark is M.'
WHERE id = 'shorts_12_decathlon-orange-tech';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_13_crosssportswear-red','cut','manual','Tailored, no drawcord - stated by Max 2026-08-30, correcting a construction I inferred from the lining and the inner waistband tape rather than observed.'),
('shorts_19_crosssportswear-peach','cut','manual','Tailored, no drawcord - stated by Max 2026-08-30, correcting an inferred construction.'),
('shorts_12_decathlon-orange-tech','pattern','manual','Plain orange outside - stated by Max 2026-08-30. The grey-and-white I described as a side panel is the inner facing shown in the label photograph.')
ON CONFLICT (item_id, field_name) DO UPDATE
  SET source = EXCLUDED.source, note = EXCLUDED.note;

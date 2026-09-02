-- 027_shorts_18_19_corrections.sql
-- 2026-08-30, same session as 026. Two rows corrected after Max went and looked at the
-- garments himself.
--
-- shorts_18: the sewn tag is gone. Max could still make out that it is a Decathlon piece,
-- and says it is the lightest fabric he owns and definitely not cotton. Brand and material
-- are therefore recorded on HIS authority, not on a label - the field sources say so.
--
-- shorts_19: Max photographed the waistband again. The brand tab reads cross|sportswear
-- MENSWEAR, and the small grey size tab reads W34 - so the "W38-40 range" I read off the
-- first, thumb-obscured photograph was wrong and the size flag on this one is withdrawn.
-- The care label is Swedish-first (SE YTTERTYG: POLYESTER 100%), consistent with the brand.
-- shorts_13 is the same model, so its brand spelling is corrected to match.

UPDATE items SET
  name = 'Decathlon navy lightweight short',
  material = 'Very lightweight technical woven, not cotton',
  notes = 'LABEL GONE. The sewn tape inside the waistband has worn away and carries no readable brand, size, fibre or country. Brand recorded as Decathlon and the cloth described as extremely lightweight and not cotton ON MAX''S WORD, 2026-08-30, not from any label. Size and country remain unknown. Royal-blue lining and blue inner facing against a navy shell, zip fly, belt loops. Max notes this is the lightest fabric he owns.'
WHERE id = 'shorts_18_navy-blue-lined';

UPDATE items SET
  name = 'Cross Sportswear peach short',
  fit = 'W34',
  notes = 'Brand tab reads cross|sportswear MENSWEAR. Small grey size tab reads W34 - read off a second, clearer photograph Max took on 2026-08-30; the earlier reading of a W38-40 range was wrong and is withdrawn, so this size is NOT a flag. Care label is Swedish-first (SE YTTERTYG: POLYESTER 100%), wash 40: shell 100% polyester, lining 100% polyester. Country still not legible. Tan lining, orange topstitching, elasticated waist with drawcord. SAME MODEL as shorts_13 in red.'
WHERE id = 'shorts_19_crosssportswear-peach';

UPDATE items SET
  name = 'Cross Sportswear red short',
  notes = 'BRAND SOURCE: the name is woven into the black elastic inner waistband tape and printed on a small sewn tab reading cross|sportswear MENSWEAR - confirmed on the peach twin, shorts_19, 2026-08-30. Care label is the multilingual fibre panel only: shell 100% polyester, lining 100% polyester. No size and no country visible in any of the three photographs of this pair - shorts_19 carries its size on a small grey tab, so this one very likely has the same tab unphotographed. Tan lining, red topstitching. SAME MODEL as shorts_19 in peach.'
WHERE id = 'shorts_13_crosssportswear-red';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_18_navy-blue-lined','notes','manual','Brand (Decathlon) and material (very light, not cotton) supplied by Max on 2026-08-30 after inspecting the garment. The tag is gone; nothing here comes from a label.'),
('shorts_19_crosssportswear-peach','fit','manual','W34 read off the grey size tab in a second photograph Max supplied on 2026-08-30. Supersedes the earlier partial reading.'),
('shorts_19_crosssportswear-peach','notes','manual','Brand confirmed as cross|sportswear MENSWEAR from the sewn tab in Max''s second photograph, 2026-08-30.'),
('shorts_13_crosssportswear-red','notes','manual','Brand spelling corrected to Cross Sportswear from the clearer tab photographed on the peach twin, 2026-08-30.')
ON CONFLICT DO NOTHING;

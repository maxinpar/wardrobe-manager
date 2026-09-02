-- 028_shorts_source_notes_fix.sql
-- 2026-08-30. Housekeeping on 027: item_field_sources is keyed on (item_id, field_name), so
-- the three 'notes' rows in 027 hit the existing 026 rows and ON CONFLICT DO NOTHING silently
-- dropped them - leaving stale provenance behind ("brand deliberately unknown") on rows whose
-- brand Max has since supplied. Verified by the src counts not moving. Rewritten here.

UPDATE item_field_sources
SET source = 'manual',
    note = 'Sewn label worn away - nothing readable on the garment. Brand (Decathlon) and the description of the cloth as extremely light and not cotton were supplied by Max on 2026-08-30 after he inspected it, NOT read off a label. Size, fibre percentages and country remain genuinely unknown.'
WHERE item_id = 'shorts_18_navy-blue-lined' AND field_name = 'notes';

UPDATE item_field_sources
SET source = 'manual',
    note = 'Brand read from the woven inner waistband tape and the sewn tab, confirmed as cross|sportswear MENSWEAR on the clearer photograph of the peach twin, 2026-08-30. Size and country still not visible on this pair - left blank, not guessed.'
WHERE item_id = 'shorts_13_crosssportswear-red' AND field_name = 'notes';

UPDATE item_field_sources
SET source = 'manual',
    note = 'Brand read as cross|sportswear MENSWEAR and size as W34 from the second waistband photograph Max supplied on 2026-08-30. Supersedes the first reading, which was partly under a thumb and wrongly taken as a W38-40 range. Country still not legible.'
WHERE item_id = 'shorts_19_crosssportswear-peach' AND field_name = 'notes';

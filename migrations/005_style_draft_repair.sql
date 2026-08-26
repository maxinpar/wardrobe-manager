-- 005_style_draft_repair.sql
--
-- The first fits import (before data/style-drafts.md existed) marked `style`
-- as 'manual' on the eleven work-outfits fits, because at that point style was
-- classified as a field only Max writes. Nothing ever wrote a value: it was
-- 'manual' and NULL, which blocked the drafts from ever being offered.
--
-- That flag was set by the importer, not by Max, so clearing it destroys
-- nothing. The guard is deliberate: only rows where style IS NULL are touched.
-- A style he has actually typed keeps its 'manual' flag and its value.

DELETE FROM fit_field_sources fs
 USING fits f
 WHERE fs.fit_id = f.id
   AND fs.field_name = 'style'
   AND fs.source = 'manual'
   AND f.style IS NULL;

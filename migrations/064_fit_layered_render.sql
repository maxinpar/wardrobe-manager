-- 064_fit_layered_render.sql — the second render, for fits with an optional layer.
--
-- The golf fits of batch 1 are designed around a quarter-zip, long-sleeve or
-- vest that comes off at the range, so each was rendered twice: once without the
-- layer, once with it. Until now only one render could be held per fit, and the
-- second file sat in the photo store attached to nothing — import_photos.py
-- reported all twelve as "Not filed".
--
-- Two nullable columns, not a render_variants table. There are exactly two looks
-- per fit and no plan for a third; a table would buy generality nothing asks for
-- and cost a join on every screen that draws a fit.
--
-- hero_image_path stays the WITHOUT-layer render for these fits, deliberately:
-- the rule for the batch is that the fit has to stand up without the layer, so
-- the base image is the canonical one. The layered render is the variant.
--
-- Nullable because most fits have no layered variant and never will — a fit with
-- one image is the normal case, not a gap to be filled.

ALTER TABLE fits ADD COLUMN layered_image_path text;
ALTER TABLE fits ADD COLUMN layered_thumb_path text;

COMMENT ON COLUMN fits.layered_image_path IS
  'The generated render WITH the fit''s optional layer, filed by import_photos.py '
  'from <fit_id>_layered_render.<ext>. NULL for a fit with no optional layer. '
  'Never the hero: hero_image_path is the without-layer render, because the fit '
  'must stand up without it. Generated, so it carries the same never-worn label.';

COMMENT ON COLUMN fits.layered_thumb_path IS
  'Thumbnail of layered_image_path. The fits grid does not use it — the grid '
  'shows the base thumbnail only and marks the fit "2 looks" — but the detail '
  'pane does, so the second pane is not a full-size fetch.';

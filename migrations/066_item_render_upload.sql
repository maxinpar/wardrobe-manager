-- 066_item_render_upload.sql — a render Max uploads for one garment.
--
-- 61 garments in the catalogue have no render at all and fall back to a colour
-- swatch, which means the closet tile, the fit's piece strip, Today's pieces and
-- the builder all draw a rectangle of #A88BB5 where a shirt should be. 13 of
-- them are in the twelve authored golf fits. The renders exist — they are
-- generated one at a time and filed into Drive by hand, and the only way in was
-- to run scripts/import_photos.py against a folder Max cannot reach from his
-- phone.
--
-- This is the same shape as fits.render_upload_path (migration 016) and for the
-- same reason. Two columns on items rather than a row in photos, deliberately:
--
--   * `photos` is a record of what is ON DISK in the Drive folder, written by
--     the importer and re-written on every run. A row the importer did not put
--     there would be a row it does not know how to keep, and the next import
--     would either orphan it or delete it.
--   * There is exactly one upload per garment. The upload REPLACES the
--     catalogue render everywhere the garment is drawn rather than joining a
--     gallery, so it is a property of the item, not another photo of it.
--
-- Nothing here deletes or supersedes the retail render underneath: removing the
-- upload reverts to it, which is what makes trying one safe.

ALTER TABLE items ADD COLUMN render_upload_path text;
ALTER TABLE items ADD COLUMN render_uploaded_at timestamptz;

COMMENT ON COLUMN items.render_upload_path IS
  'A render Max uploaded in the app, store-relative (items/uploads/<id>.jpg). '
  'Outranks the retail render and every photo for this garment on every screen '
  'that draws it. NULL is the normal case. Downscaled to 700px on the long edge '
  'when written — a garment is drawn no larger than a closet tile.';

COMMENT ON COLUMN items.render_uploaded_at IS
  'When the upload was made. Nothing reads it yet; it is here so a store that '
  'has drifted from the database can be reconciled by date rather than by guess.';

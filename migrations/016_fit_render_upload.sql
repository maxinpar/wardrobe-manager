-- 016_fit_render_upload.sql — a render you can upload from inside the app.
--
-- Until now a fit's picture could only arrive as a file: drop it in the photo
-- store under a name the convention recognises. A fit built in the app can
-- never satisfy that, so it could never have a picture.
--
-- The upload is kept in its OWN column rather than overwriting hero_image_path,
-- which is what makes "Remove" cheap and lossless: clear this column and the
-- file-based render underneath is still there, unharmed. Resolution order is
-- upload first, then the file-based hero, then the piece-strip fallback.

ALTER TABLE fits ADD COLUMN render_upload_path text;
ALTER TABLE fits ADD COLUMN render_uploaded_at timestamptz;

COMMENT ON COLUMN fits.render_upload_path IS
  'A render uploaded through the app. Wins over hero_image_path. Deliberately '
  'separate from it so removing the upload reverts to the file-based render '
  'rather than destroying it.';

COMMENT ON COLUMN fits.hero_is_generated IS
  'Whether the FILE-BASED hero is a generated illustration. It says nothing '
  'about an upload: an upload is never labelled generated, because whether it '
  'is a photograph or an AI render is not something the app may assume. If that '
  'distinction ever matters, ask for it at upload time and add a column.';

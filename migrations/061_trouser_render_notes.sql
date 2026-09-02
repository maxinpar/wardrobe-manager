-- 061_trouser_render_notes.sql
-- 2026-09-01. Provenance for the six golf trouser renders, filed the same day.
--
-- All six passed the colour gate and all six are unmistakably the right garment. The gate is the
-- one settled in the outerwear batch: compare against THIS garment's measured blue-minus-red, not
-- a generic band, and pass any neutral within +/-12 automatically.
--
--   trousers_18  +21 garment / +12 render      trousers_21  -175 / -158
--   trousers_19  +5  / +1  (neutral)           trousers_22  +74  / +80
--   trousers_20  +19 / +14                     trousers_23  +23  / +16
--
-- ONE TO WATCH, recorded so the catalogue does not drift back. The trousers_23 render reads
-- distinctly GREYER than its two siblings, and greyer than the garment. It passes the gate and it
-- is the right trouser, so it is filed - but this is the exact item that migration 059 had to
-- correct after the first flat-lay made it look blue-grey. The garment is the same navy as
-- trousers_18 and trousers_20, measured within four points on every channel. If a future session
-- reads colour off this render rather than off the photographs, it will reintroduce the error.

INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT id, 'retail_prefix', 'derived',
       'Retail render filed 2026-09-01 after a colour check against the garment''s own measured blue-minus-red and a side-by-side eyeball. All six trouser renders passed both.'
FROM items WHERE id BETWEEN 'trousers_18' AND 'trousers_23_zzz'
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('trousers_23_footjoy-navy-pique','retail_prefix','manual','The render for this item reads greyer than the garment and greyer than its two siblings (blue-minus-red +16 against the garment''s +23). It passed the gate and shows the right trouser, so it was filed. DO NOT re-read this item''s colour off the render: the garment is the same navy as trousers_18 and trousers_20, within four points on every channel, and migration 059 already had to undo a blue-grey misreading of exactly this item. The hex stands as measured from the photographs.'),
('trousers_19_inesis-grey','retail_prefix','manual','Small grey smudge artefact in the white background beside the right hip. Background only, nothing on the garment - not treated as a defect and not worth a rerun.')
ON CONFLICT DO NOTHING;

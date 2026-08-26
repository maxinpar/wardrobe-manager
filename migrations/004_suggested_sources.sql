-- 004_suggested_sources.sql
--
-- `style` is seeded from data/style-drafts.md, which is explicit that those
-- values are drafts written for Max to accept, edit or bin — not values he
-- authored. 'suggested' is that fourth provenance: weaker than 'manual', and
-- distinguishable in the UI, so a hand-edit is visibly authoritative.

ALTER TABLE fit_field_sources DROP CONSTRAINT fit_field_sources_source_check;

ALTER TABLE fit_field_sources ADD CONSTRAINT fit_field_sources_source_check
  CHECK (source IN ('imported', 'derived', 'suggested', 'manual'));

-- Worn photos of a fit belong to the wear event, never to the fit: one fit worn
-- three times has three sets. The angle is inferred from the filename, exactly
-- as for garment photos.
ALTER TABLE wear_event_photos ADD COLUMN source_filename text;
ALTER TABLE wear_event_photos ADD COLUMN angle_code text REFERENCES photo_angles(code);

CREATE UNIQUE INDEX wear_event_photos_source_idx
  ON wear_event_photos (wear_event_id, source_filename);

-- Worn photos are filed as fit_<slug>_NN_<angle>.jpg. The slug names the fit
-- that was worn, which is not always one of the seeded fits — both wear events
-- so far were ad-hoc combinations — so this is a plain label, not a foreign key.
ALTER TABLE wear_events ADD COLUMN fit_photo_slug text;

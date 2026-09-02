-- 052_belts_12_white_golf.sql
-- 2026-08-31. The white golf belt. Max: "I play 99% of my rounds with a white belt."
-- It was never catalogued, so every golf fit built before today put the wrong belt on him -
-- belts_08 (Cuater grey braided) was the only belt tagged 'golf'. This is the real default.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, neck_raw, cut, material,
                   weight_code, formality_raw, formality_rank, formality_note, fit, condition,
                   verdict_code, verdict_note, scope_code, works_alone, pairs, layer, avoid,
                   notes, no_photo, photo_prefix, retail_prefix, warmth, rain_unsafe, pattern,
                   unconfirmed) VALUES
('belts_12_white-ratchet-golf','white-ratchet-golf','Belts',
 'White ratchet golf belt','White','#F0EFED','Pale neutral','-',
 'Ratchet / automatic buckle - no holes, toothed track on the underside of the strap',
 'White pebbled leather with a smooth white edge and tonal stitching','Light','Casual',3,
 'No club crest. Max''s default golf belt - worn for roughly 99% of his rounds',
 'Ratchet, cuts to length - fits a range',
 'Good, with honest wear: light scuffing and a few small marks on the buckle plate and a mark or two on the strap. It is a used belt and looks it.',
 'Keep','The default. Any golf fit should assume this belt unless there is a reason not to - on navy, charcoal or red bottoms belts_08 (grey braided) is the safer line.',
 'core',true,'White, cream, pale grey, pale blue, pale yellow, peach and salmon shorts above all; works with every white and cream polo','-',
 'Nothing significant - but on dark bottoms it draws a hard bright line, so consider belts_08 instead',
 'Rectangular polished plaque buckle, white enamel face with a steel-grey top edge and a steel keeper. Black toothed ratchet track visible through a slot on the underside. No brand mark anywhere on the strap or buckle in either photograph - NOT GUESSED.',
 false,'belts_12_white-ratchet-golf','belts_12_white-ratchet-golf_retail',1,false,'Plain',false);

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('belts_12_white-ratchet-golf','golf'),
('belts_12_white-ratchet-golf','casual')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('belts_12_white-ratchet-golf','formality_note','manual','Max stated 2026-08-31 that he plays 99% of his rounds in a white belt. This is his default golf belt, not belts_08.'),
('belts_12_white-ratchet-golf','hex','derived','White item - the measurement method reads shadow rather than colour on white, so the hex is set near-white by judgement, as on the white polos.'),
('belts_12_white-ratchet-golf','notes','manual','No brand mark visible on strap or buckle in either photograph. Left unbranded on purpose - do not guess.'),
('belts_12_white-ratchet-golf','condition','manual','Wear called from the two flat desk photographs: scuffing and small marks on the buckle plate, a mark or two on the strap.')
ON CONFLICT (item_id, field_name) DO UPDATE SET source = EXCLUDED.source, note = EXCLUDED.note;

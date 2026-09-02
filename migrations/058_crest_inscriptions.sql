-- 058_crest_inscriptions.sql
-- 2026-09-01. Records the crest inscriptions on two golf knits, read at full resolution.
--
-- Both were read to CHECK the final two renders, which arrived carrying embroidered text. After
-- the Peter Millar vest came back with an invented GLENMUIR neck label, any text a render asserts
-- gets verified against the original frame before the render is filed. Both were verbatim
-- correct, which is worth recording as much as the inscriptions themselves: the generator
-- reproduces embroidery it can see in the reference and invents only what it cannot.
--
-- These are commemorative team pieces, not plain club stock. That matters for the crossover call
-- already recorded against them - dated team text is the clearest golf-only signal in the
-- wardrobe, per golf-crossover.md on tops_53. Neither garment's occasion tags change; both are
-- already golf-only.

UPDATE items SET
  notes = notes || ' CHEST CREST reads, verbatim: RSGC crowned monogram over "Major Pennant Winners / 1912, 1930, 1934, 1938, 2021". A commemorative pennant-winners sweater, not plain club stock.',
  formality_note = 'RSGC crowned crest over "Major Pennant Winners 1912, 1930, 1934, 1938, 2021" - a dated commemorative piece, and unambiguously golf-only because of it'
WHERE id = 'glenmuir-navy-merino-vneck';

UPDATE items SET
  notes = notes || ' CHEST CREST reads, verbatim: RSGC crowned monogram over "2017 / INTERCLUB TEAM".',
  formality_note = 'RSGC crowned crest over "2017 INTERCLUB TEAM" - a dated team top, which is exactly what Max values it for'
WHERE id = 'footjoy-navy-red-quarterzip';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('glenmuir-navy-merino-vneck','notes','manual','Crest inscription read at full resolution from PXL_20260831_071707004 on 2026-09-01, after the retail render asserted it. Render text matched the garment verbatim.'),
('footjoy-navy-red-quarterzip','notes','manual','Crest inscription read at full resolution from PXL_20260831_071855198 on 2026-09-01, after the retail render asserted it. Render text matched the garment verbatim. This is the top Max named as his favourite in the batch and the best the club has produced - see migration 053.')
ON CONFLICT DO NOTHING;

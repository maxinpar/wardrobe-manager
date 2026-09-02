-- 049_golf_shoes_in_scope.sql
-- 2026-08-31. "This is a golf outfit builder too now" - Max.
--
-- PART 1 - bring the golf shoes into scope.
-- shoes_10 .. shoes_20 were catalogued 2026-08-30 with scope_code = 'out', which excludes an
-- item from outfit building entirely. That was the right default for a category nobody was
-- building fits from; it is wrong now. It is the same shape of problem as the golf tags on the
-- shorts (fixed in 044): the garments were in the catalogue but invisible to the picker, so a
-- golf fit could reach a hat, a shirt and a pair of shorts and then have nothing to stand in.
--
-- shoes_19 was ALSO missing its golf occasion tag - the only one of the eleven without it.
-- Fixed below.
--
-- NOT changed: shoes_06 (Zegna black monk) and shoes_09a (Nike Air Max running) stay 'out'.
-- Neither is golf and neither was in the eleven.
-- ALSO NOT changed: the shorts. Checked before writing this - all 17 golf shorts are already
-- scope 'core'. Only the shoes were out.

UPDATE items SET scope_code = 'core'
WHERE cat_code = 'Shoes'
  AND id IN ('shoes_10_inesis-red-worn','shoes_11_inesis-red-new','shoes_12_inesis-teal-jf100',
             'shoes_13_inesis-cream-blue','shoes_14_kalenji-olive','shoes_15_inesis-cream-yellow-jf190',
             'shoes_16_navy-lime-spiked','shoes_17_skechers-grey-spikeless','shoes_18_grey-orange-spiked',
             'shoes_19_inesis-jf100-1-grey','shoes_20_nike-yellow-trail');

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('shoes_19_inesis-jf100-1-grey','golf')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT id, 'scope', 'manual',
       'Moved from out to core 2026-08-31 on Max''s instruction - the app is a golf outfit builder now, so golf shoes must be available to the picker.'
FROM items WHERE cat_code='Shoes' AND id BETWEEN 'shoes_10' AND 'shoes_20_zzz'
ON CONFLICT DO NOTHING;

-- PART 2 - correct tops_57. MY ERROR, not the render's.
-- I described the Peter Millar periwinkle as having a "vertical cream and tan stripe down the
-- placket band". The photograph shows a HORIZONTAL cream-and-tan band running right across the
-- chest. I only caught it by putting the render beside the source photograph to QC it - and the
-- render was right. Same lesson as the hats: when a render disagrees with my description,
-- suspect the description.

UPDATE items SET
  cut = 'Short-sleeve polo, two-button placket, self collar, horizontal cream-and-tan chest band, side vents',
  notes = 'PETER MILLAR CROWN CRAFTED, size S, made in Vietnam. Horizontal cream, tan and pale-orange band running across the full width of the chest; tonal RSGC crest on the left chest. CORRECTION 2026-08-31: migration 048 recorded this as a vertical stripe down the placket. Wrong - it is a horizontal chest band. Caught while QC-ing the render against the source photograph; the render was right and my description was not.',
  verdict_note = 'Crown Crafted is Peter Millar''s tour line - the best-made polo in the batch. The horizontal chest band is the detail that lifts it.'
WHERE id = 'tops_57_peter-millar-periwinkle-rsgc-polo';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('tops_57_peter-millar-periwinkle-rsgc-polo','cut','manual','Corrected 2026-08-31: horizontal chest band, not a vertical placket stripe. Original description was wrong.')
ON CONFLICT DO NOTHING;

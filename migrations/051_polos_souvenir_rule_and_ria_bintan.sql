-- 051_polos_souvenir_rule_and_ria_bintan.sql
-- 2026-08-31. Two corrections to migration 050, both from Max.
--
-- 1. THE SOUVENIR-CREST RULE WAS WRONG, AND IT WAS MY INFERENCE, NOT HIS.
--
-- Migration 050 wrote "a visitor souvenir, not a home club" onto ten polos and, on some rows,
-- steered them away from club play. Max: "these 'souvenir' polos... I still wear them at golf at
-- my own club. we are allowed to you know."
--
-- Where the error came from is worth recording, because it is a repeat of a pattern this project
-- already has a name for. `handoff-polos-batch-2.md` says of CAPS: "Bonville and New South Wales
-- Golf Club caps are visitor souvenirs: fine socially, wrong worn as a guest at those clubs."
-- I generalised that from caps to polos, and from "wrong at THAT club" to "not really club wear",
-- and then wrote the generalisation into ten rows as though it were his rule. It was not. It is
-- the same failure as the phantom drawcords on the shorts: an inference written into the data in
-- the same voice as a thing actually observed.
--
-- The correct rule: another club's crest is FINE at Royal Sydney and Woollahra. The only caution
-- that survives is Max's original one, and only in its original narrow form - wearing a club's own
-- crest as a guest AT that club. These rows say so and say which part is his.
--
-- 2. tops_98 IS RIA BINTAN GOLF CLUB, and the render found it before I did.
--
-- Migration 050 recorded tops_98's chest as "BCLN shield" and named no club. The Gemini render
-- came back with RIA BINTAN GOLF CLUB and a leaping deer. Rather than take the render's word, I
-- went back to the source photograph and zoomed the left chest: the deer and the words RIA BINTAN
-- GOLF CLUB are plainly there. BCLN is the maker, printed inside the orange collar stand; Ria
-- Bintan is the club, embroidered on the chest. I had conflated the two.
--
-- That is the fourth time "when a render disagrees with the description, suspect the description"
-- has paid in this project, and the first time the render has read a garment better than I did.

UPDATE items SET formality_note =
  'RIA BINTAN GOLF CLUB - another club''s crest, and no restriction: Max wears these at Royal Sydney and Woollahra.'
WHERE id = 'tops_98_bcln-white-orange-polo';

UPDATE items SET notes =
  'BCLN GOLF is the MAKER, printed inside the orange collar stand with a striped shield. The CLUB is RIA BINTAN GOLF CLUB - a leaping deer above the club name, embroidered on the left chest, confirmed at full resolution on the source photograph after the render surfaced it. Orange facings and an orange-outlined chest pocket. Size unread.'
WHERE id = 'tops_98_bcln-white-orange-polo';

UPDATE items SET colour = 'White with orange trim', name = 'BCLN Ria Bintan white polo'
WHERE id = 'tops_98_bcln-white-orange-polo';

-- The other nine crests, restated. Same facts, without the invented restriction.
UPDATE items SET formality_note = 'BARNBOUGLE LOST FARM - another club''s crest, and no restriction: Max wears these at Royal Sydney and Woollahra.' WHERE id = 'tops_72_barnbougle-lost-farm-charcoal-polo';
UPDATE items SET formality_note = 'ROYAL MELBOURNE - another club''s crest, and no restriction: Max wears these at Royal Sydney and Woollahra.' WHERE id = 'tops_73_royal-melbourne-navy-argyle-polo';
UPDATE items SET formality_note = 'AUGUSTA NATIONAL / THE MASTERS - another club''s crest, and no restriction: Max wears these at Royal Sydney and Woollahra. The most recognisable badge in the wardrobe.' WHERE id = 'tops_85_masters-dark-green-polo';
UPDATE items SET formality_note = 'GOLF CLUB BARBAROUX - another club''s crest, and no restriction: Max wears these at Royal Sydney and Woollahra.' WHERE id = 'tops_92_barbaroux-grey-polo';
UPDATE items SET formality_note = 'CAMIRAL - another club''s crest, and no restriction: Max wears these at Royal Sydney and Woollahra.' WHERE id = 'tops_94_gfore-camiral-camo-polo';
UPDATE items SET formality_note = 'BONVILLE - another club''s crest, and no restriction: Max wears these at Royal Sydney and Woollahra.' WHERE id = 'tops_95_abacus-bonville-white-polo';
UPDATE items SET formality_note = 'OCEAN DUNES, KING ISLAND - another club''s crest, and no restriction: Max wears these at Royal Sydney and Woollahra.' WHERE id = 'tops_96_adidas-ocean-dunes-white-polo';
UPDATE items SET formality_note = 'BARNBOUGLE DUNES - another club''s crest, and no restriction: Max wears these at Royal Sydney and Woollahra. The pair to tops_72, which is Lost Farm.' WHERE id = 'tops_97_calvin-klein-barnbougle-dunes-polo';
UPDATE items SET formality_note = 'LINKS HOPE ISLAND - another club''s crest, and no restriction: Max wears these at Royal Sydney and Woollahra.' WHERE id = 'tops_99_bermuda-sands-hope-island-polo';

-- tops_96 was also rank 2 partly because I read the badge as a constraint. It is a loud shirt on
-- its own merits - a wide orange chest band - so the rank stands, but the reason is the stripe.
UPDATE items SET verdict_note = 'The boldest block of colour in the batch. King Island is a good story and the crest is no obstacle anywhere; the orange band is simply a lot of shirt.'
WHERE id = 'tops_96_adidas-ocean-dunes-white-polo';

UPDATE items SET verdict_note = 'A course shirt from Tasmania, and wearable anywhere including his own club. Quiet enough that the crest is the only thing anyone notices.'
WHERE id = 'tops_72_barnbougle-lost-farm-charcoal-polo';

UPDATE items SET verdict_note = 'The one argyle in the wardrobe. Loud pattern, but the Royal Melbourne crest is no obstacle - wear it where the pattern suits.',
                 avoid = 'Navy bottoms, and anything else patterned'
WHERE id = 'tops_73_royal-melbourne-navy-argyle-polo';

-- Provenance. These are Max's own words about his own clubs, so they are manual and must not be
-- re-derived by a later pass.
INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT id, 'formality_note', 'manual',
       'Corrected 2026-08-31 on Max''s instruction: another club''s crest carries NO restriction at Royal Sydney or Woollahra - he wears these polos at his own club. Migration 050''s "visitor souvenir, not a home club" framing was my generalisation of his caps rule, not his rule, and is withdrawn. Do not reinstate it.'
FROM items WHERE id IN ('tops_72_barnbougle-lost-farm-charcoal-polo','tops_73_royal-melbourne-navy-argyle-polo',
                        'tops_85_masters-dark-green-polo','tops_92_barbaroux-grey-polo',
                        'tops_94_gfore-camiral-camo-polo','tops_95_abacus-bonville-white-polo',
                        'tops_96_adidas-ocean-dunes-white-polo','tops_97_calvin-klein-barnbougle-dunes-polo',
                        'tops_98_bcln-white-orange-polo','tops_99_bermuda-sands-hope-island-polo')
ON CONFLICT (item_id, field_name) DO UPDATE SET source = EXCLUDED.source, note = EXCLUDED.note;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('tops_98_bcln-white-orange-polo','notes','manual','Club identified as RIA BINTAN GOLF CLUB on 2026-08-31, read at full resolution off the source photograph after the Gemini render surfaced it. Migration 050 had recorded only "BCLN shield" and named no club - BCLN is the maker, Ria Bintan is the club.')
ON CONFLICT (item_id, field_name) DO UPDATE SET source = EXCLUDED.source, note = EXCLUDED.note;

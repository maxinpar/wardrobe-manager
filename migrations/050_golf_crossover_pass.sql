-- 050_golf_crossover_pass.sql
-- 2026-08-31. Which golf garments actually work off the course.
--
-- THE PROBLEM, AND IT WAS MINE. Migrations 044, 046 and 048 applied occasion tags in bulk -
-- blanket SELECTs and CROSS JOINs - so every golf item ended up carrying casual + golf + weekend
-- with no judgement per garment. A database that says everything crosses over tells the picker
-- exactly as much as one that says nothing does. Max asked which golf pieces are useful outside
-- golf; the honest answer was that the data could not say, because I had never actually decided.
-- This migration decides, item by item.
--
-- THE RULE. Three visible things disqualify a golf garment off the course:
--   1. A club crest. Not because anyone decodes it - because it makes the garment a uniform.
--   2. Technical fabric. Polyester, polyamide, "sensorcool". At 48, in Sydney, performance
--      fabric off the course reads as exactly the golf-dad signal the whole project exists to
--      avoid.
--   3. Sport styling - colourblock, contrast shoulder yokes, logo monogram prints, spikes.
-- Anything carrying one of those keeps `golf` and loses `casual` and `weekend`.
--
-- SCOPE. This migration ONLY removes casual/weekend rows from item_occasions. It bins nothing,
-- changes no scope, no verdict, no colour, no formality. Fully reversible - occasion tags are
-- just rows, so a later migration can put any of them back if a call turns out to be wrong.
--
-- TWO THINGS I SAID I WOULD DO AND DID NOT, because checking showed they were already right:
--   - The golf SHOES never had casual or weekend at all (they were scope 'out' until 049), so
--     there is nothing to strip. Left alone.
--   - shoes_14 Kalenji and shoes_20 Nike trail already carry `gym`. No change needed.
--   - belts_08 (Cuater grey braided) keeps `casual`: grey woven webbing is not a golf signal.
--   - trousers_17 Inesis navy is untouched. It is the model case for crossover - a golf-brand
--     garment with no golf signals - and already carries work + casual + weekend + golf.

-- ============================================================================
-- KEEP casual/weekend on these, and only these. Everything else golf-tagged loses them.
--
--   Shorts, the four COTTON pairs:
--     shorts_04 Tony Moro pink        97% cotton
--     shorts_08 Decathlon cream twill cotton twill
--     shorts_10 Decathlon pale blue   cotton
--     shorts_16 yellow tartan-trim    cotton twill with stretch
--   The other thirteen are polyester or polyamide and belong on the course.
--
--   Polos:
--     tops_06  Vuori grey-green       athleisure by design, already only casual+golf
--     tops_51  Tikeden toucan         technical, but a print polo reads holiday, not sport
--     tops_55  Cross taupe            tonal, neutral, no crest
--     tops_56  Puma lime stripe       cotton-feel jersey, no crest - the one that is just a polo
--   Removed from the six crested polos plus tops_59 (colourblock). Note tops_53 in particular:
--   "INTERCLUB TEAM 2021" across the chest is a dated team shirt and is golf-only, full stop.
--
--   Hats:
--     hats_25 Fighting For Par        slogan trucker, no club
--     hats_26 Good Good pale blue     brand cap that reads streetwear
--     hats_27 Good Good white "GOOD"  same
--   Removed from the fourteen club caps and visors (RSGC, Bonville, NSWGC, Woollahra) and the
--   eight Titleist/FootJoy pieces. hats_35-40 are not golf-tagged and are untouched.
-- ============================================================================

DELETE FROM item_occasions
WHERE occasion_code IN ('casual','weekend')
  AND item_id IN (
    SELECT i.id FROM items i
    JOIN item_occasions g ON g.item_id = i.id AND g.occasion_code = 'golf'
    WHERE i.gone_at IS NULL
      AND i.cat_code IN ('Shorts','Tops','Hats')
      AND i.id NOT IN (
        'shorts_04_tony-moro-pink',
        'shorts_08_decathlon-cream-twill',
        'shorts_10_decathlon-pale-blue',
        'shorts_16_yellow-tartan-trim',
        'tops_06_vuori-grey-green-polo',
        'tops_51_tikeden-navy-toucan-polo',
        'tops_55_cross-taupe-diamond-polo',
        'tops_56_puma-lime-stripe-polo',
        'hats_25_fighting-for-par-trucker',
        'hats_26_good-good-cap-pale-blue',
        'hats_27_good-good-cap-white'
      )
  );

-- Record the reasoning on every row touched, including that the original tags were mine.
INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT i.id, 'occasions', 'manual',
       'Golf-only as of 2026-08-31. Carries a club crest, technical fabric or sport styling, so it does not cross over off the course. The casual/weekend tags it previously held were applied in bulk by migration 044/046/048 without per-item judgement, not decided.'
FROM items i
JOIN item_occasions g ON g.item_id = i.id AND g.occasion_code = 'golf'
WHERE i.gone_at IS NULL
  AND i.cat_code IN ('Shorts','Tops','Hats')
  AND NOT EXISTS (SELECT 1 FROM item_occasions o WHERE o.item_id = i.id AND o.occasion_code = 'casual')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT i.id, 'occasions', 'manual',
       'Crosses over off the course, confirmed 2026-08-31: no club crest, no technical sheen, no sport styling. Keeps casual and weekend alongside golf.'
FROM items i
WHERE i.id IN ('shorts_04_tony-moro-pink','shorts_08_decathlon-cream-twill',
               'shorts_10_decathlon-pale-blue','shorts_16_yellow-tartan-trim',
               'tops_06_vuori-grey-green-polo','tops_51_tikeden-navy-toucan-polo',
               'tops_55_cross-taupe-diamond-polo','tops_56_puma-lime-stripe-polo',
               'hats_25_fighting-for-par-trucker','hats_26_good-good-cap-pale-blue',
               'hats_27_good-good-cap-white')
ON CONFLICT DO NOTHING;

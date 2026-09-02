-- 054_nike_wind_jacket_not_vest.sql
-- 2026-09-01. outerwear_18 is a JACKET WITH SLEEVES, not a vest. Corrected by Max.
--
-- WHAT HAPPENED. The garment was catalogued in migration 053 as a sleeveless wind vest. Its only
-- flat-lay (PXL_20260831_072339626) is motion-blurred: the garment is laid open with the sleeves
-- folded back under the body, and it was read as sleeveless from that. When the retail render came
-- back showing sleeves, the render was held back as wrong. It was not - the render was right and
-- the catalogue row was wrong. Max settled it: "18 has sleeves."
--
-- This is the second garment in this batch whose FUNCTION was assumed from a flat-lay silhouette
-- rather than asked - outerwear_16 was the first, catalogued as a windshirt when it is a
-- short-sleeve rain jacket. CLAUDE.md already says to confirm actual usage before assigning a
-- verdict. The rule needs widening: confirm the GARMENT, not just its verdict. A blurred or folded
-- flat-lay is not evidence of a sleeve count.
--
-- THE ID CHANGES, because photo_prefix drives file matching and the files have been renamed on
-- Drive from ..._wind-vest_* to ..._wind-jacket_*. There is no ON UPDATE CASCADE on items.id, so
-- the row is deleted and re-inserted rather than updated in place. Safe here: this item was
-- created today and its only children are photos, occasions and field sources. It appears in no
-- fit, no wear event and no week plan - checked before writing this.
--
-- photos rows cascade on the delete and are re-created by the next import_photos --commit run
-- against the renamed files.

-- Guard: refuse to run if the item has picked up a dependency since this was written.
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM fit_items WHERE item_id = 'outerwear_18_nike-golf-black-wind-vest')
  OR EXISTS (SELECT 1 FROM wear_event_items WHERE item_id = 'outerwear_18_nike-golf-black-wind-vest')
  OR EXISTS (SELECT 1 FROM week_days WHERE top_item_id = 'outerwear_18_nike-golf-black-wind-vest')
  OR EXISTS (SELECT 1 FROM gap_replaces WHERE item_id = 'outerwear_18_nike-golf-black-wind-vest')
  OR EXISTS (SELECT 1 FROM fit_preconditions WHERE item_id = 'outerwear_18_nike-golf-black-wind-vest')
  THEN
    RAISE EXCEPTION 'outerwear_18 now has a fit/wear/week/gap dependency - do not delete-and-reinsert, repoint instead';
  END IF;
END $$;

DELETE FROM items WHERE id = 'outerwear_18_nike-golf-black-wind-vest';

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, neck_raw, cut, material,
                   weight_code, formality_raw, formality_rank, formality_note, fit, condition,
                   verdict_code, verdict_note, scope_code, works_alone, pairs, layer, avoid,
                   notes, no_photo, photo_prefix, retail_prefix, warmth, rain_unsafe, pattern,
                   unconfirmed) VALUES
('outerwear_18_nike-golf-black-wind-jacket','nike-golf-black-wind-jacket','Outerwear',
 'Nike Golf charcoal wind jacket','Very dark charcoal','#3C3F45','Anchor dark',NULL,
 'Full-zip wind jacket WITH LONG SLEEVES, stand collar, mesh-lined body, reflective piping down the front panels, zipped hand pockets',
 'Lightweight woven wind shell, mesh lined','Light','Casual',2,
 'No club crest. Nike swoosh only','Size S - correct for a US golf brand',
 'Good from the flat-lay and the render','Keep',
 'Plain, light and sleeved - a windproof layer for a cold or breezy round rather than a vest. No crest, which is unusual in this batch.',
 'core',true,'Navy, stone, charcoal, black','Outer layer, over a polo or a knit','Black bottoms',
 'NIKE GOLF, size S, made in Vietnam. Mesh lining, reflective piping. LONG SLEEVES - catalogued in migration 053 as a sleeveless vest from a motion-blurred flat-lay with the sleeves folded under the body; corrected by Max 2026-09-01. Colour MEASURED as very dark charcoal #3C3F45, not true black.',
 false,'outerwear_18_nike-golf-black-wind-jacket','outerwear_18_nike-golf-black-wind-jacket_retail',
 2,false,'Plain',false);

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('outerwear_18_nike-golf-black-wind-jacket','golf')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('outerwear_18_nike-golf-black-wind-jacket','hex','derived','MEASURED against the white table in the same frame, 2026-09-01, migration 050 method.'),
('outerwear_18_nike-golf-black-wind-jacket','cut','manual','SLEEVE COUNT CORRECTED 2026-09-01. Catalogued as a sleeveless vest in migration 053, read from a motion-blurred flat-lay in which the sleeves are folded back under the body. The retail render showed sleeves and was wrongly held back as a bad render; Max confirmed the garment has sleeves. Lesson: a blurred or folded flat-lay is not evidence of a sleeve count - ask.'),
('outerwear_18_nike-golf-black-wind-jacket','id','manual','Renamed from outerwear_18_nike-golf-black-wind-vest. Photo and retail prefixes renamed to match on Drive. The old id was live for roughly one hour on 2026-09-01 and appears in no fit, wear event or week plan.')
ON CONFLICT DO NOTHING;

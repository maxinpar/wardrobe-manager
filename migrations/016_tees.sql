-- 016_tees.sql
-- The 15 tees, sport shirts and the singlet photographed 2026-08-30.
-- Ids start at tees_06: tees_01..tees_05 are the placeholder plain-crew entries that 13
-- fit base-layer rows point at, and describe the Uniqlo order, not these garments.
-- Usage stated by Max before assessment: sentimental / gym / pyjamas.
-- Scope: core only for the three that survive as daywear; everything else scope 'out'
-- so it stays catalogued and searchable but never reaches the picker.
-- Safe to re-run: ON CONFLICT DO NOTHING.

INSERT INTO items (id, slug, cat_code, name, colour, material, neck_raw, neck_code, cut,
                   formality_raw, formality_rank, fit, condition, verdict_code, verdict_note,
                   scope_code, works_alone, pairs, layer, avoid, notes, no_photo,
                   photo_prefix, retail_prefix, pattern, unconfirmed) VALUES

('tees_06_sand-anchor-print','sand-anchor-print-tee','Tops','Sand anchor-print tee',
 'Sand / pale stone','Cotton','crew','crew','Regular','Casual',2,'True to size M','Good',
 'Keep','The best of the tee folder and the only one that needs no qualification. Pale neutral, small tonal print, correct size.',
 'core',true,'Indigo or black jeans; sits in the same family as the stone chinos. Under the brown leather bomber or the waxed biker.',
 'Base layer under a V-neck - the print sits low enough to be hidden. Also works alone.',
 'Nothing significant.','Small dark anchor-and-figure print at centre chest, tonal rather than high contrast. Woven tab at the hem.',
 false,'tees_06_sand-anchor-print','tees_06_sand-anchor-print','Print',true),

('tees_07_preserve-jar-graphic','preserve-jar-graphic-tee','Tops','Preserve-jar graphic tee',
 'Near-black','Cotton','crew','crew','Regular','Casual',1,'Unknown','Good',
 'Keep','Sentimental. Mid-size colour graphic across the chest - not daywear at 48.','out',
 true,'-','-','Daywear.','Neck label washed illegible. Orange and cream jar illustration at centre chest.',
 false,'tees_07_preserve-jar-graphic','tees_07_preserve-jar-graphic','Print',true),

('tees_08_ramo-black-biz','ramo-black-biz-tee','Tops','Biz Invoice promo tee, black',
 'Black','Cotton (promo blank)','crew','crew','Regular','Casual',1,'Size L - loose on a M frame','Good',
 'Keep','Corporate promotional merch with a company name across the chest. There is no register where that reads as a choice. Gym.',
 'out',true,'-','-','Anywhere outside the gym.','RAMO promotional blank, size L. White text print across the chest.',
 false,'tees_08_ramo-black-biz','tees_08_ramo-black-biz','Print',true),

('tees_09_ramo-red-biz','ramo-red-biz-tee','Tops','Biz Invoice promo tee, red',
 'Red','Cotton (promo blank)','crew','crew','Regular','Casual',1,'True to size M','Good',
 'Keep','Same as its black twin - corporate merch. Gym.','out',
 true,'-','-','Anywhere outside the gym.','RAMO "Be your own brand" label, size M. White text print across the chest.',
 false,'tees_09_ramo-red-biz','tees_09_ramo-red-biz','Print',true),

('tees_10_coolgolf-red-badge','coolgolf-red-badge-tee','Tops','Cool Golf badge tee, red',
 'Red','50% cotton 45% polyester performance knit','crew','crew','Regular','Casual',1,'True to size M','Good',
 'Keep','A golf performance tee doing exactly the job it was made for. Not daywear - the poly content is the same fault that binned tops_38.',
 'out',true,'Golf.','-','Daywear, and any warm day off the course - poly does not breathe.',
 'COOL GOLF / OZ COOL DRY label, size M. Circular black badge print at centre chest.',
 false,'tees_10_coolgolf-red-badge','tees_10_coolgolf-red-badge','Print',true),

('tees_11_bretagne-black','bretagne-black-tee','Tops','Bretagne tee',
 'Black, washed','Cotton','crew','crew','Regular','Casual',2,'True to size M','Good - honest wash fade',
 'Keep','Sentimental and wearable, which is rare on this list. One modest circular print on a washed black ground.',
 'core',true,'Black coated jeans, indigo jeans, stone chino. Under the waxed biker or the leather bomber.',
 'Works alone. Fine under an open jacket.','Nothing else patterned in the same outfit.',
 '"Quality Cotton" woven label, size M. White circular Bretagne print at centre chest.',
 false,'tees_11_bretagne-black','tees_11_bretagne-black','Print',true),

('tees_12_fruit-band-tee','fruit-band-tee','Tops','Band tee, black',
 'Black, washed','Cotton','crew','crew','Regular','Casual',1,'Size L - hangs on a M frame','Fair - washed soft',
 'Keep','Sentimental. Size L when everything else is M, so it hangs, and "too big" is the exact fault that binned three shirts on 28 Aug. Pyjamas.',
 'out',true,'-','-','Daywear.','Fruit of the Loom blank, size L. Large tour-style graphic.',
 false,'tees_12_fruit-band-tee','tees_12_fruit-band-tee','Print',true),

('tees_13_adidas-sport-jersey','adidas-sport-jersey','Tops','adidas sport jersey',
 'White with blue and red trim','Polyester piqué','collar','collar','Regular','Casual',1,'Unknown','Good',
 'Keep','Not a tee at all - a sports jersey with a crest. Sportswear, and it looks it.','out',
 true,'Sport.','-','Daywear.','adidas label. Piqué polo body, contrast blue and red sleeve trim, embroidered crest.',
 false,'tees_13_adidas-sport-jersey','tees_13_adidas-sport-jersey','Plain',true),

('tees_14_american-apparel-la-fraise','american-apparel-la-fraise-tee','Tops','La Fraise tee, red',
 'Red','Cotton','crew','crew','Slim','Casual',2,'True to size','Good',
 'Keep','Small centre-chest print on a decent American Apparel body, so it is not a bad shirt. But a red tee is loud at this age and tees_11 does the same job quietly.',
 'out',true,'Indigo or black jeans if it is ever worn out.','-','Anything else patterned.',
 'American Apparel body with a "la Fraise" print. Small centre-chest graphic.',
 false,'tees_14_american-apparel-la-fraise','tees_14_american-apparel-la-fraise','Print',true),

('tees_15_adidas-grey-henley','adidas-grey-henley','Tops','Grey henley, long sleeve',
 'Mid grey','Cotton blend jersey','henley','crew','Regular','Casual',2,'Unknown','Good',
 'Keep','Not a tee - a long-sleeve button henley, and the only non-printed thing in the folder. A henley is a legitimately useful layer, but this one is performance grey and reads as loungewear in the photo. Verdict deliberately left at out until Max says how the cloth feels in hand: soft and drapey means pyjamas, firmer means a weekend slot.',
 'out',true,'Indigo or black jeans, stone chino.','Alone, or under a jacket.','Anything smart.',
 'adidas label. Button placket at the neck, long sleeve.',
 false,'tees_15_adidas-grey-henley','tees_15_adidas-grey-henley','Plain',true),

('tees_16_standard-american-olive','standard-american-olive-tee','Tops','Faded text tee, olive',
 'Olive green','Cotton','crew','crew','Regular','Casual',2,'True to size','Good - print faded with age, honestly',
 'Keep','Muted, low contrast, and olive is already in the wardrobe through the Air Max 1. A faded tonal print reads as texture at conversational distance.',
 'core',true,'Indigo jeans, black coated jeans, stone chino. The olive Air Max picks it up.',
 'Works alone. Fine as a base layer under a dark V-neck.','Anything else patterned.',
 '"Standard American" label. Faded tonal text print at centre chest.',
 false,'tees_16_standard-american-olive','tees_16_standard-american-olive','Print',true),

('tees_17_broome-singlet','broome-singlet','Tops','Broome singlet',
 'Blue-grey','Cotton','sleeveless','crew','Regular','Casual',1,'Size S - small','Fair - washed thin',
 'Keep','Not a tee - a souvenir tank, and size S. Sentimental and gym.','out',
 true,'Gym.','-','Daywear.','"Exclusively Australian" label, size S. Broome / Western Australia souvenir print.',
 false,'tees_17_broome-singlet','tees_17_broome-singlet','Print',true),

('tees_18_black-small-graphic','black-small-graphic-tee','Tops','Small-graphic tee, black',
 'Black','Cotton','crew','crew','Regular','Casual',1,'Unknown','Good',
 'Keep','No label photographed. Small chest graphic on black - closer to wearable than most here, but tees_11 already covers black-tee-with-a-small-print and covers it better.',
 'out',true,'-','-','Daywear while tees_11 exists.','No neck label frame in the shoot. Small graphic at centre chest.',
 false,'tees_18_black-small-graphic','tees_18_black-small-graphic','Print',true),

('tees_19_four-panel-photo','four-panel-photo-tee','Tops','Four-panel photo tee',
 'Charcoal / black','Cotton','crew','crew','Regular','Casual',1,'Unknown','Fair',
 'Keep','The most dated thing in the folder. A four-panel photo print is a specific mid-2000s object and no styling rescues it.',
 'out',true,'-','-','Daywear.','Label faded past reading. Four-panel photographic print across the chest.',
 false,'tees_19_four-panel-photo','tees_19_four-panel-photo','Print',true),

('tees_20_kickasss-lobster','kickasss-lobster-tee','Tops','KICKASSS lobster tee',
 'Dark charcoal','Cotton','crew','crew','Regular','Casual',2,'Unknown','Good',
 'Keep','The best label in the folder - KICKASSS Biarritz, Limited Edition Series, a real French surf brand. Kept on merit. But the lobster graphic is large, which makes it a weekend and holiday tee rather than a fit component.',
 'out',true,'Black or indigo jeans on a weekend.','Alone.','Any fit that is trying to be quiet.',
 'KICKASSS Biarritz, "Limited Edition Series". Large lobster graphic across the chest.',
 false,'tees_20_kickasss-lobster','tees_20_kickasss-lobster','Print',true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, 'casual' FROM items WHERE id LIKE 'tees_1%' OR id LIKE 'tees_2%' OR id = 'tees_06_sand-anchor-print'
ON CONFLICT DO NOTHING;

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('tees_08_ramo-black-biz','gym'),('tees_09_ramo-red-biz','gym'),
('tees_10_coolgolf-red-badge','golf'),('tees_13_adidas-sport-jersey','gym'),
('tees_17_broome-singlet','gym'),('tees_12_fruit-band-tee','gym')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT id, 'verdict_code', 'manual',
       'Catalogued 2026-08-30 from Max''s worn photos. Usage stated by him first: sentimental / gym / pyjamas. Scope, not verdict, is what keeps these out of the picker - nothing here is Bin.'
FROM items WHERE id >= 'tees_06' AND id < 'tees_21'
ON CONFLICT DO NOTHING;

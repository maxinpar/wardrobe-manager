-- 053_golf_outerwear_knits_zips.sql
-- 2026-09-01. Golf outerwear, vests, quarter-zips and knits. 20 garments, 21 rows, 53 photographs.
--
-- COUNT, done before a row was written. 41 frames in Downloads\Golf-Other, shot 2026-08-31
-- 07:16-07:25, in garment+label pairs. 20 distinct garments, confirmed on a labelled contact
-- sheet. The Peter Millar vest is REVERSIBLE and is entered TWICE at Max's instruction, as two
-- independent rows with no link between them (outerwear_19 pink, outerwear_20 blue). Its shared
-- label frame is filed under both prefixes. 11 further frames arrived 2026-09-01 (detail shots of
-- the unbranded charcoal full-zip and the FootJoy grey/orange) and are filed to those two items.
--
-- CATEGORY SPLIT. Knits and quarter-zips go to Knitwear, following anko-black-quarterzip-fleece.
-- Vests, the softshell and the rain jacket go to Outerwear, continuing outerwear_15 - _20.
-- Knitwear ids stay slug-only, which is that category's existing convention.
--
-- SIZING. The handoff rule holds: US golf brands fit Max at S, generic and Asian-sized at M.
-- Applying it, the five S garments here (Turtleson, FootJoy purple stripe, Calvin Klein, Nike
-- knit, Nike vest) are CORRECTLY sized, and the three L garments are the outliers - two sizes up.
-- An earlier draft of the catalogue had this backwards. Label sizes are recorded as read; where
-- the rule predicts a mismatch the row is flagged unconfirmed rather than judged from a photo.
--
-- CRESTS ARE NOT A DEFECT. The first pass of this batch applied the migration 050 crossover test
-- (crest / technical fabric / sport styling) as a keep-or-bin test. It is not one - it decides
-- only whether a garment leaves the course. Max corrected this. Crests are recorded in notes and
-- drive occasion tags, nothing else. See claude/golf-crossover.md, which now says so.
--
-- CONDITION. No damage is asserted anywhere in this batch. An earlier draft called the unbranded
-- charcoal full-zip a condition bin for a "cracked and flaked logo": that was the printed care
-- label INSIDE the back neck, read from a close-up without establishing where on the garment it
-- sat. The garment is unbranded and sound. The square on the FootJoy grey/orange chest, also
-- queried, is a bonded pocket. Both were re-shot on 2026-09-01 and both are clean.
--
-- TWO ITEMS MAX HAS RULED ON DIRECTLY, not to be re-litigated:
--   footjoy-navy-red-quarterzip - his favourite garment here, the best team top RSGC has made.
--   outerwear_16 - a SHORT-SLEEVE RAIN JACKET, not a windshirt. It was catalogued as a windshirt
--   duplicating the Peter Millar softshell and binned on that basis. Function assumed from a
--   flat-lay instead of asked. Nothing else in the wardrobe is a summer waterproof.
--
-- COLOUR. Measured against the white table in frame, migration 050 method. Three results differ
-- from what the eye called: the Turtleson reads dead neutral (#D1D1CF, saturation 1%) and is
-- named stone, not sage; the Good Good is a jade green, not kelly; the Nike vest is very dark
-- charcoal, not black. Nothing near-white in this batch, so no judgement-set hexes.
--
-- VERDICTS. Provisional by design. Per CLAUDE.md, verdicts are confirmed against actual usage
-- before they are trusted. Everything is Keep; the eight rows whose fit or use is still open
-- carry unconfirmed = true.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, neck_raw, cut, material,
                   weight_code, formality_raw, formality_rank, formality_note, fit, condition,
                   verdict_code, verdict_note, scope_code, works_alone, pairs, layer, avoid,
                   notes, no_photo, photo_prefix, retail_prefix, warmth, rain_unsafe, pattern,
                   unconfirmed) VALUES

('glenmuir-navy-merino-vneck','glenmuir-navy-merino-vneck','Knitwear','Glenmuir navy merino V-neck','Navy','#464A56','Anchor dark','v-neck','Long-sleeve V-neck golf sweater, ribbed hem and cuffs','Italian merino wool','Fine','Smart-casual',4,'White RSGC crest on the left chest - home club, no restriction','Size M','Good from the flat-lay','Keep','Best fabric in this batch. Real merino, properly finished, and the one of the three navy knits worth keeping if only one survives.','core',true,'Stone, white, navy or charcoal bottoms','Over a golf polo, or over a shirt collar','The other two navy knits - they do the same job','GLENMUIR 1891, ITALIAN MERINO, size M. White RSGC crown crest, left chest.',false,'glenmuir-navy-merino-vneck','glenmuir-navy-merino-vneck_retail',3,false,'Plain',false),

('glenmuir-navy-zipneck','glenmuir-navy-zipneck','Knitwear','Glenmuir navy zip-neck','Navy','#434C64','Anchor dark','quarter-zip','Long-sleeve zip-neck sweater, lined placket, ribbed hem and cuffs','Wool knit, Bionic Finish treated','Fine','Smart-casual',4,'RSGC crest, left chest - home club','Size M','Good from the flat-lay','Keep','Near-duplicate of the merino V-neck in use. One of three navy knits; keep whichever Max actually reaches for.','core',true,'Stone, white, navy or charcoal bottoms','Over a golf polo','The other two navy knits','GLENMUIR 1891, BIONIC FINISH, size M. Zip-neck with a woven navy placket lining.',false,'glenmuir-navy-zipneck','glenmuir-navy-zipneck_retail',3,false,'Plain',true),

('glenmuir-red-merino-quarterzip','glenmuir-red-merino-quarterzip','Knitwear','Glenmuir red merino quarter-zip','Crimson red','#CF0E3D','Statement','quarter-zip','Long-sleeve quarter-zip sweater, ribbed collar, branded zip pull','Italian merino wool','Fine','Smart-casual',4,'White RSGC crown crest, left chest - home club','Size M','Good from the flat-lay','Keep','The other good knit here. Loud colour, but red reads well on a course and the fabric is the same merino as the navy V-neck.','core',true,'Navy, stone, white or charcoal bottoms','Over a golf polo','Red or pink bottoms','GLENMUIR 1891, ITALIAN MERINO, size M. Glenmuir-stamped zip pull; white RSGC crown crest.',false,'glenmuir-red-merino-quarterzip','glenmuir-red-merino-quarterzip_retail',3,false,'Plain',false),

('footjoy-navy-knit-halfzip','footjoy-navy-knit-halfzip','Knitwear','FootJoy navy knit half-zip','Navy','#383E49','Anchor dark','quarter-zip','Long-sleeve half-zip, knit-look face, ribbed hem and cuffs','Technical knit jersey','Light-Mid','Casual',3,'RSGC crest, left chest - home club','Size M. FootJoy is a US golf brand and fits Max at S, so this runs a size large','Good from the flat-lay','Keep','Third of the three navy knits and the least good fabric of them. First to go if the pile is cut.','core',true,'Stone, navy, white, charcoal','Over a golf polo','The Glenmuir navies','FOOTJOY, size M, read off the neck patch. Knit-look technical face rather than a true wool knit.',false,'footjoy-navy-knit-halfzip','footjoy-navy-knit-halfzip_retail',3,false,'Plain',true),

('nike-golf-grey-knit-halfzip','nike-golf-grey-knit-halfzip','Knitwear','Nike Golf grey knit half-zip','Light grey','#BFBCBB','Mid neutral','quarter-zip','Long-sleeve half-zip, ribbed stand collar, woven placket lining','Technical knit, Tour Performance','Light-Mid','Casual',3,'NO CREST - one of the few here without one','Size S. Nike Golf is a US golf brand, so S is the correct size','Good from the flat-lay','Keep','Plain grey, no crest, no colourblock. With the Calvin Klein, the least golf-looking mid-layer in the batch.','core',true,'Navy, stone, white, charcoal','Over a golf polo or a plain tee','Grey bottoms','NIKE GOLF TOUR PERFORMANCE, size S, made in China. Ribbed collar over a grey woven placket lining. No club mark anywhere.',false,'nike-golf-grey-knit-halfzip','nike-golf-grey-knit-halfzip_retail',3,false,'Plain',false),

('turtleson-stone-quarterzip','turtleson-stone-quarterzip','Knitwear','Turtleson stone quarter-zip','Pale stone','#D1D1CF','Pale neutral','quarter-zip','Long-sleeve quarter-zip, contrast blue collar stand and inner placket','Technical jersey','Light','Casual',3,'Small tonal crest on the left chest','Size S. Turtleson is a US golf brand, so S is the correct size','Good from the flat-lay','Keep','Palest thing in the batch. The blue collar is the only colour on it and keeps it from looking like a gym top.','core',true,'Navy, stone, charcoal','Over a golf polo','Stone or beige bottoms - too close to the top','TURTLESON, size S. MEASURED DEAD NEUTRAL: #D1D1CF, saturation 1 percent. It reads sage to the eye in room light and was first catalogued as sage; the table says otherwise, so it is named stone.',false,'turtleson-stone-quarterzip','turtleson-stone-quarterzip_retail',2,false,'Plain',false),

('unbranded-charcoal-fullzip','unbranded-charcoal-fullzip','Knitwear','Charcoal full-zip (unbranded)','Slate charcoal','#5C5E69','Anchor dark','quarter-zip','Long-sleeve full-zip, stand collar, raglan sleeves, ribbed hem and cuffs','Heathered technical knit','Light-Mid','Casual',3,'NO CREST, NO LOGO ANYWHERE - the plainest garment in the batch','Size NOT READ - no size tag appears in any of the seven frames. Measure the chest flat if it matters','Good. Seven frames including four close-ups shot 2026-09-01: clean knit face, no pilling, sound zip and ribbing','Keep','Max is not attached to it, but it is the only thing here with no branding at all and the closest garment he already owns to the plain mid-layer named as the one worth buying. Worth a second look before it goes.','core',true,'Navy, stone, black, charcoal','Over a polo or a plain tee. Works off the course, which almost nothing else here does','Charcoal bottoms','BRAND UNKNOWN and deliberately blank. No maker mark on the outside of the garment; the only print is the care and size label inside the back neck, which has worn away. CONDITION CLAIM RETRACTED: an earlier draft called that worn interior label a cracked exterior chest logo and binned the garment for it.',false,'unbranded-charcoal-fullzip','unbranded-charcoal-fullzip_retail',3,false,'Plain',true),

('footjoy-grey-orange-quarterzip','footjoy-grey-orange-quarterzip','Knitwear','FootJoy grey and orange quarter-zip','Mid grey with orange side and sleeve panels','#9998A0','Mid neutral','quarter-zip','Long-sleeve quarter-zip, orange side panels and underarm gussets, contrast overlocked seams, bonded chest pocket','Technical jersey','Light','Casual',2,'No club crest. Orange colourblock','Size L. FootJoy fits Max at S, so this is two sizes up','Good. Re-shot 2026-09-01 at the cuff, seams, zip and body - clean throughout','Keep','The one real bin candidate in the batch, and it is a size question rather than a condition one: two sizes up, and the panelled colourblock is the most dated cut here. If it fits and he likes it, it stays.','core',true,'Navy, stone, charcoal','Over a golf polo','Orange or red bottoms','FOOTJOY, size L, read off the neck patch. The square on the left chest is a BONDED CHEST POCKET, not a mark - checked in the 2026-09-01 close-ups after it was queried.',false,'footjoy-grey-orange-quarterzip','footjoy-grey-orange-quarterzip_retail',2,false,'Colourblock',true),

('footjoy-charcoal-purple-stripe-quarterzip','footjoy-charcoal-purple-stripe-quarterzip','Knitwear','FootJoy charcoal purple-stripe quarter-zip','Charcoal with a fine purple stripe','#3B3E50','Anchor dark','quarter-zip','Long-sleeve quarter-zip, self collar, fine allover stripe','Technical jersey','Light','Casual',3,'No club crest','Size S - correct for FootJoy','Good from the flat-lay','Keep','Dark and quiet. The purple only shows up close, which is what makes it wearable.','core',true,'Navy, stone, charcoal, white','Over a golf polo','Purple or charcoal bottoms','FOOTJOY, size S. Fine purple stripe on a charcoal ground.',false,'footjoy-charcoal-purple-stripe-quarterzip','footjoy-charcoal-purple-stripe-quarterzip_retail',2,false,'Fine stripe',false),

('footjoy-navy-red-quarterzip','footjoy-navy-red-quarterzip','Knitwear','FootJoy navy and red RSGC team quarter-zip','Navy with red shoulder and sleeve panels','#3C3D4B','Anchor dark','quarter-zip','Long-sleeve quarter-zip, red contrast shoulders and sleeves, white piping, stand collar','Technical jersey, Athletic Fit','Light','Casual',3,'RSGC team top - home club, no restriction','Size L, Athletic Fit. FootJoy fits Max at S, so it runs large - and he wears it anyway','Good from the flat-lay','Keep','MAX''S FAVOURITE GARMENT IN THIS BATCH and, in his words, the best team top the club has produced. Not a candidate for any future cull. An earlier draft binned it on cut; that call was wrong and withdrawn.','core',true,'Navy, stone, white, charcoal','Over a golf polo','Red bottoms','FOOTJOY ATHLETIC FIT, size L. Red shoulder and sleeve panels with white piping; RSGC crest on the left chest.',false,'footjoy-navy-red-quarterzip','footjoy-navy-red-quarterzip_retail',2,false,'Colourblock',false),

('goodgood-green-stripe-quarterzip','goodgood-green-stripe-quarterzip','Knitwear','Good Good jade stripe quarter-zip','Jade green with a fine yellow stripe','#138D75','Statement','quarter-zip','Long-sleeve quarter-zip, self collar, fine horizontal stripe','92 percent polyester technical jersey','Light','Casual',2,'Good Good is a young golf-media brand, no club crest','Size MEDIUM - correct, Good Good is Korean-made and sizes generously','Good from the flat-lay','Keep','The most current-looking piece in the batch by a distance. Matches hats_25, _26 and _27, which are the only golf hats that cross over.','core',true,'Navy, stone, white, charcoal','Over a golf polo','Green bottoms, and anything else striped','GOOD GOOD - FIGHTING FOR PAR, size MEDIUM. MEASURED as jade green, #138D75; it reads kelly green to the eye and was first catalogued that way.',false,'goodgood-green-stripe-quarterzip','goodgood-green-stripe-quarterzip_retail',2,false,'Fine stripe',false),

('calvin-klein-navy-quarterzip','calvin-klein-navy-quarterzip','Knitwear','Calvin Klein Golf navy quarter-zip','Navy','#434B62','Anchor dark','quarter-zip','Long-sleeve quarter-zip, plain body, self collar','Technical jersey with a brushed back','Light-Mid','Casual',3,'NO CREST, no colourblock, no visible logo','Size S/P - correct for a US golf brand','Good from the flat-lay','Keep','One of only two things in this batch that work off the course. Plain navy with nothing on it.','core',true,'Stone, white, charcoal, black','Over a plain tee or a polo. Fine with black coated jeans off the course','Navy bottoms','CALVIN KLEIN GOLF, size S/P, made in Vietnam. Grey brushed interior. Nothing on the outside of the garment at all.',false,'calvin-klein-navy-quarterzip','calvin-klein-navy-quarterzip_retail',3,false,'Plain',false),

('adidas-teal-quarterzip','adidas-teal-quarterzip','Knitwear','adidas teal quarter-zip','Teal turquoise','#2DB5B4','Statement','quarter-zip','Long-sleeve quarter-zip, self collar, fleece-backed body','Fleece-backed technical jersey','Mid','Casual',2,'adidas performance mark only, no club crest','Size M. adidas golf ran S in the polo batch, so this may be roomy','Good from the flat-lay','Keep','Plain, warm, no crest. The strongest colour here after the red, but a solid block of it reads better than a panel of it.','core',true,'Navy, stone, white, charcoal','Over a golf polo','Teal, green or blue bottoms','adidas, size M, made in China. Fleece-backed inside; the only warm-backed quarter-zip in the batch.',false,'adidas-teal-quarterzip','adidas-teal-quarterzip_retail',4,false,'Plain',true),

('abacus-blue-grey-quarterzip','abacus-blue-grey-quarterzip','Knitwear','Abacus blue-grey quarter-zip','Blue-grey with a black shoulder yoke','#868FAB','Mid tone','quarter-zip','Long-sleeve quarter-zip, black contrast shoulder yoke, white side panels, stand collar','Technical jersey','Light','Casual',2,'RSGC crest, left chest - home club','EUR 50 / US M / UK 40 - correct size','Good from the flat-lay','Keep','Right size, but the black shoulder yoke is the same dated cut as the FootJoy grey/orange. Goes if the pile needs cutting further.','core',true,'Navy, stone, charcoal','Over a golf polo','Blue or grey bottoms','abacus COUNT ON IT, EUR 50 / US M / UK 40, made in China. Black yoke across the shoulders with white panels down the sides.',false,'abacus-blue-grey-quarterzip','abacus-blue-grey-quarterzip_retail',2,false,'Colourblock',false),

('footjoy-pale-blue-quarterzip','footjoy-pale-blue-quarterzip','Knitwear','FootJoy pale blue quarter-zip','Pale blue','#C0D6F1','Pale blue','quarter-zip','Long-sleeve quarter-zip, self collar, plain body','Technical jersey','Light','Casual',3,'Small dark RSGC crest, left chest - home club','Size M. FootJoy fits Max at S, so this runs a size large','Good from the flat-lay','Keep','Plain and pale, and the only light blue mid-layer he owns. The crest is small and dark enough not to shout.','core',true,'Navy, stone, charcoal, white','Over a golf polo','Pale blue bottoms','FOOTJOY, size M. Plain pale blue body with a small dark crest on the left chest.',false,'footjoy-pale-blue-quarterzip','footjoy-pale-blue-quarterzip_retail',2,false,'Plain',true),

('outerwear_15_peter-millar-grey-softshell','peter-millar-grey-softshell','Outerwear','Peter Millar grey softshell jacket','Mid grey, two-tone panels','#8A8A91','Mid neutral',NULL,'Full-zip softshell jacket, fleece-backed, two-tone grey panels, zipped hand pockets','Bonded softshell with a brushed fleece back','Mid','Casual',3,'No club crest. Reads as an ordinary softshell','Size L. Peter Millar fits Max at S, so this is two sizes up - the open question on this row','Good from the flat-lay','Keep','The best-made outer layer in the batch and the most expensive-feeling. Everything depends on whether the L is wearable or swimming on him.','core',true,'Navy, stone, charcoal, black','Outer layer over a knit or a polo','Grey bottoms','PETER MILLAR, size L, made in China. Cream fleece backing, two-tone grey shell.',false,'outerwear_15_peter-millar-grey-softshell','outerwear_15_peter-millar-grey-softshell_retail',3,false,'Plain',true),

('outerwear_16_footjoy-short-sleeve-rain-jacket','footjoy-short-sleeve-rain-jacket','Outerwear','FootJoy short-sleeve rain jacket','Grey with white and orange panels','#6F6F73','Mid neutral',NULL,'SHORT-SLEEVE waterproof pullover, quarter-zip, white and orange contrast panels, drawcord hem','Lightweight waterproof shell','Light','Casual',2,'RSGC branded. Sports jacket, on-course wear','Size M','Good from the flat-lay','Keep','A SUMMER WATERPROOF, and nothing else in the wardrobe does that job. Catalogued on 2026-09-01 as a windshirt duplicating outerwear_15 and binned for redundancy; Max corrected it. Function was assumed from a flat-lay instead of asked.','core',true,'Navy, stone, charcoal','Outer layer, over a polo, in summer rain','Nothing significant - it goes on when it rains','FOOTJOY, size M. RSGC branded. Short sleeves, which is the whole point of it and what the first pass missed.',false,'outerwear_16_footjoy-short-sleeve-rain-jacket','outerwear_16_footjoy-short-sleeve-rain-jacket_retail',1,false,'Colourblock',false),

('outerwear_17_abacus-navy-softshell-vest','abacus-navy-softshell-vest','Outerwear','Abacus navy softshell vest','Navy','#414855','Anchor dark',NULL,'Full-zip sleeveless softshell vest, stand collar, zipped hand pockets, honeycomb-textured lining','Bonded softshell','Mid','Casual',3,'RSGC crest, left chest - home club','EUR 50 / US M / UK 40 - correct size','Good from the flat-lay','Keep','The workhorse vest for a cold round. Duplicates the Nike vest and, off the course, the Anko gilet he already wears daily - but on the course it is the warmer and better-made of the two.','core',true,'Navy, stone, charcoal','Over a knit or a polo. Outer layer','Navy bottoms','abacus COUNT ON IT, EUR 50 / US M / UK 40. Honeycomb-textured navy lining; RSGC crest on the left chest.',false,'outerwear_17_abacus-navy-softshell-vest','outerwear_17_abacus-navy-softshell-vest_retail',3,false,'Plain',false),

('outerwear_18_nike-golf-black-wind-vest','nike-golf-black-wind-vest','Outerwear','Nike Golf charcoal wind vest','Very dark charcoal','#3C3F45','Anchor dark',NULL,'Full-zip sleeveless wind vest, mesh-lined, reflective piping down the front panels','Lightweight woven wind shell, mesh lined','Light','Casual',2,'NO CREST. Nike swoosh only','Size S - correct for a US golf brand','Good from the flat-lay','Keep','Plain and light, the summer counterpart to the Abacus vest. No crest, which is unusual here.','core',true,'Navy, stone, charcoal, black','Over a polo. Outer layer','Black bottoms','NIKE GOLF, size S, made in Vietnam. Mesh lining, reflective piping. MEASURED as very dark charcoal #3C3F45, not true black - it was first catalogued as black.',false,'outerwear_18_nike-golf-black-wind-vest','outerwear_18_nike-golf-black-wind-vest_retail',2,false,'Plain',false),

('outerwear_19_peter-millar-reversible-vest-pink','peter-millar-reversible-vest-pink','Outerwear','Peter Millar reversible quilted vest - pink side','Rose pink','#E77387','Statement',NULL,'Full-zip sleeveless quilted vest, matte shell, contrast blue binding at the collar and armholes','Quilted synthetic-fill, matte shell','Mid','Casual',3,'NO CREST, NO LOGO. Reads as a town gilet, not golf kit','Size M. Peter Millar fits Max at S, so it runs a size large','Good from the flat-lay','Keep','THE BEST PIECE IN THE BATCH. Reversible: this row is the pink side, outerwear_20 is the blue. Entered as two independent rows at Max''s instruction, deliberately not linked.','core',true,'White or navy tee, beige or stone bottoms','Over a tee or a polo. Outer layer','Red, coral or pink bottoms - the vest is the colour','PETER MILLAR, size M. REVERSIBLE - pink one way, pale blue the other, with the opposite colour showing as binding. Quilted, matte, and completely unbranded on the outside.',false,'outerwear_19_peter-millar-reversible-vest-pink','outerwear_19_peter-millar-reversible-vest-pink_retail',3,false,'Quilted',false),

('outerwear_20_peter-millar-reversible-vest-blue','peter-millar-reversible-vest-blue','Outerwear','Peter Millar reversible quilted vest - blue side','Pale blue','#B8D9FD','Pale blue',NULL,'Full-zip sleeveless quilted vest, matte shell, contrast pink binding at the collar and armholes','Quilted synthetic-fill, matte shell','Mid','Smart-casual',3,'NO CREST, NO LOGO. The one garment here that passes at the office','Size M. Peter Millar fits Max at S, so it runs a size large','Good from the flat-lay','Keep','The blue side of the reversible vest, and the single most useful thing in this batch. Over a plain polo with the Inesis navy trousers it reads as a normal relaxed Friday rather than golf kit.','core',true,'Navy, stone, white, charcoal','Over a polo or a knit. Outer layer','Pale blue bottoms','PETER MILLAR, size M. Same garment as outerwear_19 worn the other way out. Entered separately at Max''s instruction; the two rows are not linked.',false,'outerwear_20_peter-millar-reversible-vest-blue','outerwear_20_peter-millar-reversible-vest-blue_retail',3,false,'Quilted',false)

ON CONFLICT (id) DO NOTHING;

-- Occasions. Every row is golf. Crossover is decided per garment by the migration 050 test, which
-- is a crossover test and nothing more - it does not touch verdicts. Ids are listed explicitly
-- because this batch spans two categories and two id conventions, so BETWEEN is not safe here.
INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, 'golf' FROM items WHERE id IN (
 'glenmuir-navy-merino-vneck','glenmuir-navy-zipneck','glenmuir-red-merino-quarterzip',
 'footjoy-navy-knit-halfzip','nike-golf-grey-knit-halfzip','turtleson-stone-quarterzip',
 'unbranded-charcoal-fullzip','footjoy-grey-orange-quarterzip',
 'footjoy-charcoal-purple-stripe-quarterzip','footjoy-navy-red-quarterzip',
 'goodgood-green-stripe-quarterzip','calvin-klein-navy-quarterzip','adidas-teal-quarterzip',
 'abacus-blue-grey-quarterzip','footjoy-pale-blue-quarterzip',
 'outerwear_15_peter-millar-grey-softshell','outerwear_16_footjoy-short-sleeve-rain-jacket',
 'outerwear_17_abacus-navy-softshell-vest','outerwear_18_nike-golf-black-wind-vest',
 'outerwear_19_peter-millar-reversible-vest-pink','outerwear_20_peter-millar-reversible-vest-blue')
ON CONFLICT DO NOTHING;

-- Four of twenty-one cross over. Three are unarguable: no crest, no logo, no colourblock. The
-- fourth, the unbranded charcoal full-zip, is a judgement call - it is technical fabric, which the
-- rule normally disqualifies, but it carries no mark of any kind and reads as a plain grey zip-up.
-- Reversible in one migration if it proves wrong worn.
INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, o FROM items CROSS JOIN (VALUES ('casual'),('weekend')) v(o)
WHERE id IN ('calvin-klein-navy-quarterzip','unbranded-charcoal-fullzip',
             'outerwear_19_peter-millar-reversible-vest-pink',
             'outerwear_20_peter-millar-reversible-vest-blue')
ON CONFLICT DO NOTHING;

-- One row earns work. The office is genuinely relaxed - polos, sneakers, puffer vests - so a
-- matte quilted gilet with no branding over a plain polo is unremarkable there.
INSERT INTO item_occasions (item_id, occasion_code) VALUES
('outerwear_20_peter-millar-reversible-vest-blue','work')
ON CONFLICT DO NOTHING;

-- Colour provenance. Migration 050 method: white point from the low-saturation pixels of the
-- white table in frame with the garment box excluded; garment = median of the garment box with
-- the darkest quartile and brightest decile discarded. No near-whites in this batch, so no hex
-- was set by judgement. Every white point measured COOL (blue minus red +12 to +27), so the
-- correction pushes results warm - the two greens measuring jade and turquoise is conservative,
-- not an artefact.
INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT id, 'hex', 'derived',
       'MEASURED against the white table in the same frame, 2026-09-01, migration 050 method.'
FROM items WHERE id IN (
 'glenmuir-navy-merino-vneck','glenmuir-navy-zipneck','glenmuir-red-merino-quarterzip',
 'footjoy-navy-knit-halfzip','nike-golf-grey-knit-halfzip','turtleson-stone-quarterzip',
 'unbranded-charcoal-fullzip','footjoy-grey-orange-quarterzip',
 'footjoy-charcoal-purple-stripe-quarterzip','footjoy-navy-red-quarterzip',
 'goodgood-green-stripe-quarterzip','calvin-klein-navy-quarterzip','adidas-teal-quarterzip',
 'abacus-blue-grey-quarterzip','footjoy-pale-blue-quarterzip',
 'outerwear_15_peter-millar-grey-softshell','outerwear_16_footjoy-short-sleeve-rain-jacket',
 'outerwear_17_abacus-navy-softshell-vest','outerwear_18_nike-golf-black-wind-vest',
 'outerwear_19_peter-millar-reversible-vest-pink','outerwear_20_peter-millar-reversible-vest-blue')
ON CONFLICT DO NOTHING;

-- Deliberate non-identifications, corrections and rulings. Marked manual so a re-import cannot
-- quietly overwrite them.
INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('turtleson-stone-quarterzip','hex','manual','MEASURED DEAD NEUTRAL - #D1D1CF, saturation 1 percent, hue meaningless at that saturation. The garment reads pale sage to the eye and was first catalogued as sage. The white point in its own frame measured cool, so the correction pushed the result warm if anything; the neutral result is not an artefact of the method. Named stone.'),
('unbranded-charcoal-fullzip','notes','manual','BRAND UNKNOWN and deliberately blank. No maker mark anywhere on the outside of the garment across seven frames; the only print is the interior back-neck care and size label, which has worn away. Do not guess a brand into this row.'),
('unbranded-charcoal-fullzip','fit','manual','SIZE NOT READ. No size tag appears in any of the seven frames, and the interior neck print is illegible. Not inferred from the sizing rule - the brand is unknown, so the rule cannot apply. Measure the chest flat if it matters.'),
('unbranded-charcoal-fullzip','condition','manual','CONDITION CLAIM RETRACTED 2026-09-01. An earlier draft recorded a cracked and flaked exterior logo and binned the garment on it. The flaking is the printed care label INSIDE the back neck - normal wear, invisible worn. Read from a close-up without establishing where on the garment the detail sat. Re-shot by Max at the cuff, shoulder seam, collar and full body: clean knit face, no pilling, sound zip and ribbing. Lesson: do not call condition from a detail shot until you know where it sits on the garment.'),
('footjoy-grey-orange-quarterzip','condition','manual','The square on the left chest is a BONDED CHEST POCKET, confirmed in the 2026-09-01 close-ups. It was queried as a possible mark or a removed transfer; it is neither. No damage anywhere on this garment.'),
('footjoy-navy-red-quarterzip','verdict_code','manual','KEEP, ruled by Max directly on 2026-09-01: his favourite garment in this batch and the best team top Royal Sydney has produced. An earlier draft binned it for a dated colourblock cut and for being two sizes up. Both observations are true and neither matters. Do not re-raise this item in a future cull.'),
('outerwear_16_footjoy-short-sleeve-rain-jacket','notes','manual','IDENTIFIED WRONGLY ON THE FIRST PASS. Catalogued as a long-sleeve windshirt duplicating outerwear_15 and binned for redundancy. It is a SHORT-SLEEVE RAIN JACKET - a summer waterproof with no substitute in the wardrobe. Corrected by Max 2026-09-01. Function was assumed from a flat-lay silhouette instead of asked, against the CLAUDE.md rule to confirm actual usage before assigning a verdict.'),
('outerwear_19_peter-millar-reversible-vest-pink','notes','manual','ONE PHYSICAL GARMENT, TWO ROWS. This vest is reversible. Max asked for it to be counted as two separate garments with no link between the rows, so outerwear_19 and outerwear_20 are independent and each carries its own hex, occasions and photographs. The shared label frame is filed under both prefixes. If a future reconciliation counts garments rather than rows, this pair is the one discrepancy.'),
('outerwear_20_peter-millar-reversible-vest-blue','notes','manual','The blue face of the reversible vest catalogued as outerwear_19. See that row for the counting note.'),
('glenmuir-navy-zipneck','verdict_code','manual','Provisional. One of three navy knits doing the same job - this, glenmuir-navy-merino-vneck and footjoy-navy-knit-halfzip. Max to say which he actually reaches for; the other two go. The merino V-neck is the best fabric of the three.'),
('footjoy-navy-knit-halfzip','verdict_code','manual','Provisional. See glenmuir-navy-zipneck. Least good fabric of the three navy knits.'),
('outerwear_15_peter-millar-grey-softshell','fit','manual','Size L on a Peter Millar, which fits Max at S. Two sizes up. Whether it is wearable or oversized is the open question on this row and decides its verdict.'),
('footjoy-grey-orange-quarterzip','verdict_code','manual','Provisional, and the only bin candidate left in the batch after Max''s corrections. Size L on a FootJoy is two sizes up, and the panelled colourblock is the most dated cut here. Condition is good. If it fits and he likes it, it stays.')
ON CONFLICT DO NOTHING;

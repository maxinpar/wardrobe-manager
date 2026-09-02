-- 026_shorts_batch_1.sql
-- 2026-08-30: the main shorts intake. Eighteen garments photographed in one session
-- (C:\Users\maxim\Downloads\Raw shorts, 41 files), clustered by shoot order and colour and
-- confirmed on a labelled contact sheet - not by assuming a shot count. Continues from
-- shorts_01 / shorts_02 in migration 025.
--
-- PROVENANCE: brand is recorded only where a sewn label, a woven waistband tape or a printed
-- gripper actually says so. Where the source is not a conventional brand label the notes say
-- which it was. Nothing is inferred from filenames, silhouette or renders. Every "not visible"
-- means the photograph does not show it, not that the garment lacks it.
--
-- USAGE: nothing about how often these are worn, what for, or how Max feels about them has
-- been established. All eighteen rows are unconfirmed = true, verdict_note says so, and
-- pairs / avoid are left as "To confirm.". Occasions are the same weekend + casual placeholder
-- used in 025; golf is deliberately NOT tagged even on the FootJoy and Callaway pieces,
-- because the brand is evidence about the garment, not about what Max does with it.
--
-- hex values are the median of the garment centre measured off the laid-flat photo in warm
-- indoor light, uncorrected. Good enough to seed a render prompt, not colour-managed.

INSERT INTO items (id, slug, cat_code, name, colour, hex, material, cut, formality_raw,
                   formality_rank, fit, condition, verdict_code, verdict_note, scope_code,
                   works_alone, pairs, layer, avoid, notes, no_photo, photo_prefix,
                   retail_prefix, rain_unsafe, pattern, unconfirmed) VALUES

('shorts_03_footjoy-pale-blue','footjoy-pale-blue','Shorts','FootJoy pale blue short',
 'Pale sky blue','#A2D5F8','85% polyester / 15% spandex','Flat front','Casual',2,'W34',
 'Used - yellowish staining across the front left thigh and hip, several spots',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only. The staining is an observation from photo 2, not a verdict - decide with Max whether it washes out, gets worn anyway, or bins it.',
 'core',true,'To confirm.','-','To confirm.',
 'Sewn label: FootJoy, Acushnet Company CA22544, 85% polyester / 15% spandex, made in China, size tab W34. Flat front, belt loops, zip fly, slash side pockets, plain hem. Size matches his usual W33-34.',
 false,'shorts_03_footjoy-pale-blue','shorts_03_footjoy-pale-blue',false,'Plain',true),

('shorts_04_tony-moro-pink','tony-moro-pink','Shorts','Tony Moro pink short',
 'Salmon pink','#F7B5B2','97% cotton / 3% elastane','Flat front','Casual',2,'Not visible',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only; verdict pending.',
 'core',true,'To confirm.','-','To confirm.',
 'Brand label reads TONY MORO / CLASSIC FASHION WEAR / BEST ORIGINAL. Care label: 97% cotton / 3% elastane, multilingual. No size and no country of origin visible in either photograph - both left blank rather than guessed. Flat front, belt loops, zip fly, contrast pale pink pocketing.',
 false,'shorts_04_tony-moro-pink','shorts_04_tony-moro-pink',false,'Plain',true),

('shorts_05_stone-poly-webbing','stone-poly-webbing','Shorts','Stone technical short',
 'Stone / warm off-white','#E7DFD7','100% polyester','Flat front','Casual',2,'36',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Reads as a sport or golf short from the construction - technical polyester, striped elastic inner waistband, orange piping - but that is inference from build, not from Max. Verdict pending, and see the size flag.',
 'core',true,'To confirm.','-','To confirm.',
 'NO BRAND FOUND. Neither photograph shows a brand label or mark; brand deliberately left blank. Care label: 100% polyester, size 36, country partly legible only. Green / navy / red striped elastic inner waistband with orange piping down the fly facing, zip fly, belt loops. SIZE FLAG: 36 is above his usual W33-34.',
 false,'shorts_05_stone-poly-webbing','shorts_05_stone-poly-webbing',false,'Plain',true),

('shorts_06_footjoy-navy','footjoy-navy','Shorts','FootJoy navy short',
 'Navy slate','#43464F','85% polyester / 15% spandex','Flat front','Casual',2,'W32',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only; verdict pending. See the size flag.',
 'core',true,'To confirm.','-','To confirm.',
 'Sewn label: FootJoy, Acushnet Company CA22544, 85% polyester / 15% spandex, made in Vietnam, size tab W32. Flat front, belt loops, zip fly with a metal slider, slash side pockets. SIZE FLAG: W32 is below his usual W33-34.',
 false,'shorts_06_footjoy-navy','shorts_06_footjoy-navy',false,'Plain',true),

('shorts_07_footjoy-grey-monogram','footjoy-grey-monogram','Shorts','FootJoy grey monogram short',
 'Pale grey','#E7E7E2','88% polyester / 12% spandex','Flat front','Casual',2,'W36',
 'Used - two small dark specks on the leg, otherwise clean',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only; verdict pending. See the size flag.',
 'core',true,'To confirm.','-','To confirm.',
 'Sewn label: FootJoy, Acushnet Company CA22544, 88% polyester / 12% spandex, made in China, size tab W36. The pale grey ground carries an all-over print of small white FJ monograms, regularly spaced - it reads as a dot pattern at arm length. Flat front, belt loops, zip fly. SIZE FLAG: W36 is above his usual W33-34.',
 false,'shorts_07_footjoy-grey-monogram','shorts_07_footjoy-grey-monogram',false,'All-over small FJ monogram print',true),

('shorts_08_decathlon-cream-twill','decathlon-cream-twill','Shorts','Decathlon cream twill short',
 'Cream / off-white','#F4F0E6','Cotton twill','Flat front','Casual',2,'EU 42 / US S-M',
 'Used - faint discolouration and a thin dark line on the front',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only. The marks are an observation from photo 16, not a verdict. See the size flag.',
 'core',true,'To confirm.','-','To confirm.',
 'Decathlon size label: ref 75228, CC 305517, Cm 96-99, CN 175/84A, EU 42, US S/M, BR 42, RU 48, MX 9, IR 42, ID M-L, made in Bangladesh. Fibre content is not on the panel photographed. Navy-and-white striped cotton facing inside the waistband, horn-look button, zip fly. SIZE FLAG: EU 42 is a size below his usual EUR44 and the US mark is S/M.',
 false,'shorts_08_decathlon-cream-twill','shorts_08_decathlon-cream-twill',false,'Plain',true),

('shorts_09_white-sport-unbranded','white-sport-unbranded','Shorts','White sport short',
 'White','#EFEBE7','90% polyester / 10% elastane','Elasticated waist with drawcord','Casual',2,'L',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Reads as a sport short from the build - stretch polyester, drawcord, grey inner tape - but that is inference, not something Max has said. Verdict pending.',
 'core',true,'To confirm.','-','To confirm.',
 'NO BRAND FOUND. The only label is a size tab printed with the S / M / L / XL run and L marked, plus BODY: 90% Polyester 10% Elastane, exclusive of trim, made in China. Brand deliberately left blank. Dark grey flat drawcord, grey elastic inner waistband tape. SIZE FLAG: a letter size, not comparable to W33-34.',
 false,'shorts_09_white-sport-unbranded','shorts_09_white-sport-unbranded',false,'Plain',true),

('shorts_10_decathlon-pale-blue','decathlon-pale-blue','Shorts','Decathlon pale blue short',
 'Pale blue','#E0EEF0','Cotton','Flat front','Casual',2,'EU L',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only; verdict pending.',
 'core',true,'To confirm.','-','To confirm.',
 'Decathlon size label: ref 75228, CC 125539, Cm 98-104, CN 180/88A, EU L, BR G, RU 48-50, MX G, made in Bangladesh, Maplaris SAS. Fibre content is not on the panel photographed. Navy-and-white striped cotton facing inside the waistband, tortoiseshell button, zip fly. Same Decathlon size-label family as shorts_08.',
 false,'shorts_10_decathlon-pale-blue','shorts_10_decathlon-pale-blue',false,'Plain',true),

('shorts_11_decathlon-slate-tech','decathlon-slate-tech','Shorts','Decathlon slate technical short',
 'Slate grey','#828285','89% polyamide / 11% elastane','Flat front, lined','Casual',2,'EU L / FR 44',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only; verdict pending.',
 'core',true,'To confirm.','-','To confirm.',
 'Decathlon label: ref 71332, CC 313059, Cm 99.5-103, CN 180/88A, EU L, FR 44, US L, BR 44, RU 50, MX 11, CA L/G, made in China. Main fabric 89% polyamide / 11% elastane, lining 100% polyester. SAME MODEL as shorts_15 in navy - identical style reference.',
 false,'shorts_11_decathlon-slate-tech','shorts_11_decathlon-slate-tech',false,'Plain',true),

('shorts_12_decathlon-orange-tech','decathlon-orange-tech','Shorts','Decathlon orange technical short',
 'Red-orange','#F64927','Technical woven - fibre not on the panel photographed','Flat front, lined','Casual',2,'EU 44 / US M',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only; verdict pending. See the size flag.',
 'core',true,'To confirm.','-','To confirm.',
 'Decathlon size label: ref 62495, CC 125541, Cm 100-104, CN 180/88A, EU 44, US M, plus the usual BR / RU / MX / IR run. Fibre content and country are not on the panel photographed. Grey side panel with a white vertical stripe, orange body. SIZE FLAG: EU 44 matches his usual EUR44 but the US mark is M.',
 false,'shorts_12_decathlon-orange-tech','shorts_12_decathlon-orange-tech',false,'Colour-blocked side panel',true),

('shorts_13_crosssportswear-red','crosssportswear-red','Shorts','Crosssportswear red short',
 'Red','#F0373C','100% polyester shell, 100% polyester lining','Elasticated waist with drawcord, fully lined','Casual',2,'Not visible',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. The build - light polyester shell, full lining, drawcord waist - reads as a swim or beach short rather than a tailored short, but that is inference from construction. Ask Max what it actually is before writing a verdict.',
 'core',true,'To confirm.','-','To confirm.',
 'BRAND SOURCE: no conventional sewn brand label. The name crosssportswear is woven repeatedly into the black elastic inner waistband tape and appears again on a small grey tab. Care label is the multilingual fibre panel only: shell 100% polyester, lining 100% polyester. No size and no country visible in either of the three photographs. Tan lining, red topstitching. SAME MODEL as shorts_19 in peach.',
 false,'shorts_13_crosssportswear-red','shorts_13_crosssportswear-red',false,'Plain',true),

('shorts_14_footjoy-charcoal','footjoy-charcoal','Shorts','FootJoy charcoal short',
 'Charcoal','#52545A','85% polyester / 15% spandex','Flat front','Casual',2,'W34',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only; verdict pending.',
 'core',true,'To confirm.','-','To confirm.',
 'Sewn label: FootJoy, Acushnet Company CA22544, 85% polyester / 15% spandex, made in China, size tab W34. Flat front, belt loops, zip fly, slash side pockets. Size matches his usual W33-34. Darker than shorts_06 and a separate garment - both fronts photographed.',
 false,'shorts_14_footjoy-charcoal','shorts_14_footjoy-charcoal',false,'Plain',true),

('shorts_15_decathlon-navy-tech','decathlon-navy-tech','Shorts','Decathlon navy technical short',
 'Navy','#494C5D','89% polyamide / 11% elastane','Flat front, lined','Casual',2,'EU L / FR 44',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only; verdict pending.',
 'core',true,'To confirm.','-','To confirm.',
 'Decathlon label: ref 71332, CC 313059, Cm 99.5-103, CN 180/88A, EU L, FR 44, US L, BR 44, RU 50, MX 11, CA L/G, made in China. Main fabric 89% polyamide / 11% elastane, lining 100% polyester. SAME MODEL as shorts_11 in slate grey - identical style reference.',
 false,'shorts_15_decathlon-navy-tech','shorts_15_decathlon-navy-tech',false,'Plain',true),

('shorts_16_yellow-tartan-trim','yellow-tartan-trim','Shorts','Yellow tartan-trim short',
 'Pale yellow','#F3E593','Cotton twill with stretch','Flat front','Casual',2,'34',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only; verdict pending.',
 'core',true,'To confirm.','-','To confirm.',
 'NO BRAND NAME LEGIBLE. The woven tape inside the waistband reads only COTTON TWILL WITH STRETCH. A navy tab carries the size 34 in gold plus three lines of small print that could not be resolved even at full zoom - brand deliberately left blank rather than guessed from them. Royal Stewart tartan trim bound along the inside of the waistband, cream twill pocketing and fly facing. SIZE FLAG: 34 sits at the top of his usual W33-34.',
 false,'shorts_16_yellow-tartan-trim','shorts_16_yellow-tartan-trim',false,'Plain, tartan trim inside the waistband',true),

('shorts_17_chambray-linen-look','chambray-linen-look','Shorts','Chambray linen-look short',
 'Chambray blue','#8394AE','Not stated on the label - a slubby linen-look woven','Flat front with elasticated back','Casual',2,'L',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Catalogued from photographs and the sewn labels only; verdict pending.',
 'core',true,'To confirm.','-','To confirm.',
 'NO BRAND FOUND. The only label is a small black tab printed MADE IN CHINA with the size L; brand deliberately left blank. Fibre content is not stated anywhere in the photographs. Elasticated gathered back waistband, ecru cotton pocketing and waistband facing, slubby chambray-blue cloth with a linen look.',
 false,'shorts_17_chambray-linen-look','shorts_17_chambray-linen-look',false,'Plain',true),

('shorts_18_navy-blue-lined','navy-blue-lined','Shorts','Navy short, blue lining',
 'Navy','#434551','Unknown - label illegible','Flat front, lined','Casual',2,'Not legible',
 'Used - clean, no damage seen; the sewn label itself is worn illegible',
 'Keep','USAGE NOT YET CONFIRMED. Nothing is known about this one beyond the photographs - the label has washed out. Verdict pending, and brand / size / fibre stay unknown unless Max recognises it.',
 'core',true,'To confirm.','-','To confirm.',
 'LABEL ILLEGIBLE. The sewn tape inside the waistband has washed to the point where only the care symbols survive - no brand, no size, no fibre, no country could be read even at full zoom. All four fields deliberately left unknown rather than guessed. Royal-blue lining and blue inner facing against a navy shell, zip fly, belt loops.',
 false,'shorts_18_navy-blue-lined','shorts_18_navy-blue-lined',false,'Plain',true),

('shorts_19_crosssportswear-peach','crosssportswear-peach','Shorts','Crosssportswear peach short',
 'Peach / light orange','#F4AA6E','100% polyester shell, 100% polyester lining','Elasticated waist with drawcord, fully lined','Casual',2,'Not legible',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. Same inference as shorts_13 - the build reads as a swim or beach short - but that is from construction, not from Max. Verdict pending.',
 'core',true,'To confirm.','-','To confirm.',
 'BRAND SOURCE: no conventional sewn brand label. crosssportswear is woven repeatedly into the black elastic inner waistband tape and printed on a small grey tab. Care label: shell 100% polyester, lining 100% polyester, multilingual; no country visible. SIZE NOT RECORDED: the grey tab carries a waist RANGE whose first line reads as W38-40, but the second line is under a thumb in the photograph and the whole tab is not confidently legible - left blank pending a second look at the garment. Tan lining, orange topstitching. SAME MODEL as shorts_13 in red.',
 false,'shorts_19_crosssportswear-peach','shorts_19_crosssportswear-peach',false,'Plain',true),

('shorts_20_callaway-stone','callaway-stone','Shorts','Callaway stone short',
 'Stone / warm light grey','#C9C6C1','Not visible on the label photographed','Flat front','Casual',2,'Not visible',
 'Used - clean, no damage seen',
 'Keep','USAGE NOT YET CONFIRMED. A Callaway short is golf equipment by brand, but whether Max plays in these is his to say, not the label. Verdict pending and golf deliberately not tagged.',
 'core',true,'To confirm.','-','To confirm.',
 'BRAND SOURCE: no sewn brand label in either photograph. Callaway is printed repeatedly along the black silicone shirt-gripper tape inside the waistband, between grey elastic bands - recorded on that basis and on no other. No size, no fibre and no country visible; all three left blank rather than guessed. Flat front, belt loops, zip fly, ecru pocketing.',
 false,'shorts_20_callaway-stone','shorts_20_callaway-stone',false,'Plain',true);

-- Placeholder occasions only, matching the pattern set in 025. weekend + casual is the
-- neutral default for a short; work, golf and gym are all left off until Max says otherwise.
INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, o.code
FROM items,
     (VALUES ('weekend'), ('casual')) AS o(code)
WHERE id IN ('shorts_03_footjoy-pale-blue','shorts_04_tony-moro-pink','shorts_05_stone-poly-webbing',
             'shorts_06_footjoy-navy','shorts_07_footjoy-grey-monogram','shorts_08_decathlon-cream-twill',
             'shorts_09_white-sport-unbranded','shorts_10_decathlon-pale-blue','shorts_11_decathlon-slate-tech',
             'shorts_12_decathlon-orange-tech','shorts_13_crosssportswear-red','shorts_14_footjoy-charcoal',
             'shorts_15_decathlon-navy-tech','shorts_16_yellow-tartan-trim','shorts_17_chambray-linen-look',
             'shorts_18_navy-blue-lined','shorts_19_crosssportswear-peach','shorts_20_callaway-stone')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shorts_03_footjoy-pale-blue','notes','manual','Brand, fibre, country and size read off the sewn FootJoy labels, 2026-08-30.'),
('shorts_03_footjoy-pale-blue','condition','manual','Staining observed on the close photograph of the front left thigh, not reported by Max.'),
('shorts_04_tony-moro-pink','notes','manual','Brand and fibre off the sewn labels. Size and country not visible in either photograph - left blank, not guessed.'),
('shorts_05_stone-poly-webbing','notes','manual','Size and fibre off the care label. No brand mark anywhere in the photographs - brand left blank, not guessed.'),
('shorts_06_footjoy-navy','notes','manual','Brand, fibre, country and size read off the sewn FootJoy labels, 2026-08-30.'),
('shorts_07_footjoy-grey-monogram','notes','manual','Brand, fibre, country and size read off the sewn FootJoy labels. The all-over print was identified as FJ monograms by zooming the fabric, not assumed.'),
('shorts_08_decathlon-cream-twill','notes','manual','Brand and sizing off the Decathlon size label. Fibre content is not on the panel photographed - left blank.'),
('shorts_09_white-sport-unbranded','notes','manual','Size and fibre off the printed size tab. No brand anywhere in the photographs - left blank, not guessed.'),
('shorts_10_decathlon-pale-blue','notes','manual','Brand and sizing off the Decathlon size label. Fibre content is not on the panel photographed - left blank.'),
('shorts_11_decathlon-slate-tech','notes','manual','Brand, sizing, fibre and country off the Decathlon label. Style reference 71332 / CC 313059 matches shorts_15.'),
('shorts_12_decathlon-orange-tech','notes','manual','Brand and sizing off the Decathlon size label. Fibre and country are not on the panel photographed - left blank.'),
('shorts_13_crosssportswear-red','notes','manual','Brand taken from the woven inner waistband tape and a small sewn tab, NOT from a conventional brand label. Size and country not visible - left blank.'),
('shorts_14_footjoy-charcoal','notes','manual','Brand, fibre, country and size read off the sewn FootJoy labels, 2026-08-30.'),
('shorts_15_decathlon-navy-tech','notes','manual','Brand, sizing, fibre and country off the Decathlon label. Style reference 71332 / CC 313059 matches shorts_11.'),
('shorts_16_yellow-tartan-trim','notes','manual','Size off the navy tab. No brand name legible anywhere - the tab print could not be resolved at full zoom, so brand is left blank rather than inferred.'),
('shorts_17_chambray-linen-look','notes','manual','Size and country off the black tab. No brand and no fibre content anywhere in the photographs - left blank.'),
('shorts_18_navy-blue-lined','notes','manual','Sewn label washed illegible. Brand, size, fibre and country all deliberately recorded as unknown - nothing was guessed from the garment.'),
('shorts_19_crosssportswear-peach','notes','manual','Brand taken from the woven inner waistband tape and a small sewn tab, NOT from a conventional brand label. The grey size tab is a waist range, partly obscured by a thumb and not confidently legible - size left blank pending a second look.'),
('shorts_20_callaway-stone','notes','manual','Brand taken from the Callaway print on the silicone gripper tape inside the waistband, NOT from a sewn brand label. Size, fibre and country not visible - left blank.'),
('shorts_03_footjoy-pale-blue','occasions','manual','Golf NOT tagged despite the brand: usage is Max to confirm, not the label. weekend + casual are placeholders.'),
('shorts_06_footjoy-navy','occasions','manual','Golf NOT tagged despite the brand: usage is Max to confirm. weekend + casual are placeholders.'),
('shorts_07_footjoy-grey-monogram','occasions','manual','Golf NOT tagged despite the brand: usage is Max to confirm. weekend + casual are placeholders.'),
('shorts_14_footjoy-charcoal','occasions','manual','Golf NOT tagged despite the brand: usage is Max to confirm. weekend + casual are placeholders.'),
('shorts_20_callaway-stone','occasions','manual','Golf NOT tagged despite the brand: usage is Max to confirm. weekend + casual are placeholders.')
ON CONFLICT DO NOTHING;

-- 046_hats_keepers.sql
-- 2026-08-31. The rest of the hats: 30 rows, taking the category to 40.
--
-- RECONCILIATION. 045 deliberately stopped at ten because the keepers were shot as worn
-- selfies across four batches with duplicates between them. That reconciliation is now done,
-- by building labelled contact sheets of all four batches and then comparing the ambiguous
-- groups side by side at size. Three groups needed it and all three resolved:
--   red RSGC caps      - THREE, not one: gold crest; white crest (new, Pukka SPF50 tag,
--                        photographed three times); and a soft unstructured red with a white
--                        crest.
--   coral/pink visors  - TWO, not three: a pink one with a white crest, and a coral one with a
--                        navy crest photographed twice.
--   cream RSGC caps    - THREE: cream/navy, cream/green (twice), and a white/navy that is new
--                        and still carries a 35South Platinum brim sticker.
-- 40 total against roughly 35 estimated from the photographs; the extra come from those groups.
-- Max had already binned about ten more before any photograph was taken - unrecorded.
--
-- CORRECTION TO 045: hats_07_rsgc-visor-memorabilia_02_worn-front-b.jpg was NOT the memorabilia
-- visor. It is the new white RSGC cap - a cap, not a visor. Caught while reconciling. The file
-- has been renamed on Drive to hats_16_rsgc-cap-white-navy_01_worn-front.jpg and the bad photo
-- row is deleted below. hats_07 keeps its one correct frame.
--
-- CLUB RULE (044, confirmed by Max): member at BOTH RSGC and Woollahra, so those two carry no
-- restriction. Bonville and New South Wales Golf Club are visitor souvenirs - fine socially,
-- wrong worn as a guest at those clubs. That is recorded in formality_note on the rows it
-- applies to.
--
-- PROVENANCE: every hex here is DERIVED from a worn photograph in mixed indoor light and is
-- flagged as such. After getting two condition calls wrong off exactly these photographs, the
-- condition field on every row below says what the photograph supports and no more. Nothing
-- here is a bin call; the culling is finished.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, cut, material,
                   formality_raw, formality_rank, formality_note, condition, verdict_code,
                   verdict_note, scope_code, pairs, notes, no_photo, photo_prefix,
                   retail_prefix, warmth, rain_unsafe, pattern, unconfirmed) VALUES

('hats_11_rsgc-cap-red-gold','rsgc-cap-red-gold','Hats','RSGC cap - red/gold',
 'Red with gold crest','#C8302C','Statement','Unstructured cap, curved brim','Technical knit',
 'Casual',2,'Royal Sydney - home club, no restriction','Good from the photograph; red slightly duller than hats_12',
 'Keep','Duplicate of hats_12 in a different crest colour. Keep one; this is the older.','core',
 'Coral, pink, white, navy, stone','Royal Sydney Golf Club, gold/yellow crown-and-monogram.',
 false,'hats_11_rsgc-cap-red-gold','hats_11_rsgc-cap-red-gold_retail',2,false,'Plain',false),

('hats_12_rsgc-cap-red-white','rsgc-cap-red-white','Hats','RSGC cap - red/white',
 'Red with white crest','#D62828','Statement','Structured six-panel cap, curved brim','Technical knit',
 'Casual',2,'Royal Sydney - home club, no restriction','As new. Still carries its Pukka SPF50 brim sticker and hang tag.',
 'Keep','The newest red. TAKE THE STICKER AND TAG OFF before wearing.','core',
 'Coral, pink, white, navy, stone','Royal Sydney Golf Club, white crown-and-monogram. Pukka, SPF50.',
 false,'hats_12_rsgc-cap-red-white','hats_12_rsgc-cap-red-white_retail',2,false,'Plain',false),

('hats_13_rsgc-cap-red-soft','rsgc-cap-red-soft','Hats','RSGC cap - red, soft crown',
 'Red with white crest','#DD4433','Statement','Unstructured cap, soft crown, curved brim','Cotton twill',
 'Casual',2,'Royal Sydney - home club, no restriction','Only photographed out of focus. Condition not assessed.',
 'Keep','Silhouette is clearly distinct from hats_11 and hats_12 - softer, floppier crown.','core',
 'Coral, pink, white, navy, stone','Royal Sydney Golf Club. The one blurred frame in the set; reshoot.',
 false,'hats_13_rsgc-cap-red-soft','hats_13_rsgc-cap-red-soft_retail',2,false,'Plain',true),

('hats_14_rsgc-cap-cream-navy','rsgc-cap-cream-navy','Hats','RSGC cap - cream/navy',
 'Cream with navy crest','#EFE9DC','Pale neutral','Unstructured cap, curved brim','Cotton twill',
 'Casual',2,'Royal Sydney - home club, no restriction','Good from the photograph.',
 'Keep','Pale cap - a dirty pale cap is worse than none, so watch the crown and sweatband.','core',
 'Navy, red, coral, stone, mid blue','Royal Sydney Golf Club, navy crown-and-monogram.',
 false,'hats_14_rsgc-cap-cream-navy','hats_14_rsgc-cap-cream-navy_retail',2,false,'Plain',false),

('hats_15_rsgc-cap-cream-green','rsgc-cap-cream-green','Hats','RSGC cap - cream/green',
 'Cream with green crest','#F0EBDE','Pale neutral','Unstructured cap, curved brim','Cotton twill',
 'Casual',2,'Royal Sydney - home club, no restriction','Good from the photograph.',
 'Keep','Same as hats_14 in a different crest colour.','core',
 'Navy, stone, sage, white','Royal Sydney Golf Club, green crown-and-monogram.',
 false,'hats_15_rsgc-cap-cream-green','hats_15_rsgc-cap-cream-green_retail',2,false,'Plain',false),

('hats_16_rsgc-cap-white-navy','rsgc-cap-white-navy','Hats','RSGC cap - white/navy',
 'White with navy crest','#F6F4F0','Pale neutral','Structured six-panel cap, curved brim','Technical knit',
 'Casual',2,'Royal Sydney - home club, no restriction','As new. Still carries its 35South Platinum brim sticker.',
 'Keep','TAKE THE STICKER OFF. Leaving it on is a tour-copy affectation.','core',
 'Navy, red, coral, stone, mid blue',
 'Royal Sydney Golf Club. 35South Platinum range. This is the cap I mis-filed against hats_07 on 2026-08-31 - see the note at the top of this migration.',
 false,'hats_16_rsgc-cap-white-navy','hats_16_rsgc-cap-white-navy_retail',2,false,'Plain',false),

('hats_17_rsgc-visor-pink','rsgc-visor-pink','Hats','RSGC visor - pink',
 'Rose pink with white crest','#E8798C','Statement','Visor, adjustable rear strap, marker clip','Technical knit',
 'Casual',2,'Royal Sydney - home club, no restriction','Good from the photograph.',
 'Keep','Sound.','core','Coral, white, navy','Royal Sydney Golf Club. Magnetic ball-marker clip on the brim.',
 false,'hats_17_rsgc-visor-pink','hats_17_rsgc-visor-pink_retail',1,false,'Plain',false),

('hats_18_rsgc-visor-coral','rsgc-visor-coral','Hats','RSGC visor - coral',
 'Coral with navy crest','#E1553F','Statement','Visor, adjustable rear strap','Technical knit',
 'Casual',2,'Royal Sydney - home club, no restriction','Good from the photograph.',
 'Keep','Sound.','core','Navy, white, stone','Royal Sydney Golf Club, navy crown-and-monogram.',
 false,'hats_18_rsgc-visor-coral','hats_18_rsgc-visor-coral_retail',1,false,'Plain',false),

('hats_19_rsgc-visor-lime','rsgc-visor-lime','Hats','RSGC visor - lime',
 'Lime green with white crest','#C6D62E','Statement','Visor, adjustable rear strap','Technical knit',
 'Casual',2,'Royal Sydney - home club, no restriction','As new. Still carries its 35South Platinum brim sticker.',
 'Keep','TAKE THE STICKER OFF.','core','White, navy, stone','Royal Sydney Golf Club. 35South Platinum range.',
 false,'hats_19_rsgc-visor-lime','hats_19_rsgc-visor-lime_retail',1,false,'Plain',false),

('hats_20_bonville-cap-tan-rope','bonville-cap-tan-rope','Hats','Bonville cap - tan rope',
 'Tan/mustard with navy underbrim','#C79445','Mid tone','Rope-front trucker, flat-ish brim, patch badge','Cotton twill',
 'Casual',2,'Bonville - visitor souvenir. Fine socially; not as a guest at Bonville','Good from the photograph.',
 'Keep','The best-looking cap in the set; rope front reads current rather than corporate.','core',
 'Navy, cream, olive, white','BGR Bonville Golf woven patch, navy underbrim, rope across the front.',
 false,'hats_20_bonville-cap-tan-rope','hats_20_bonville-cap-tan-rope_retail',2,false,'Plain',false),

('hats_21_bonville-cap-grey-soft','bonville-cap-grey-soft','Hats','Bonville cap - grey soft crown',
 'Grey-taupe with cream rope','#8E8A82','Mid tone','Unstructured soft crown, cream rope, curved brim','Technical, slight sheen',
 'Casual',2,'Bonville - visitor souvenir. Fine socially; not as a guest at Bonville','Good from the photograph. Crown is soft by design, not collapsed.',
 'Keep','Sound.','core','Navy, white, stone, coral','BGR Bonville Golf, white embroidery, cream rope trim.',
 false,'hats_21_bonville-cap-grey-soft','hats_21_bonville-cap-grey-soft_retail',2,false,'Plain',false),

('hats_22_nswgc-cap-stone','nswgc-cap-stone','Hats','NSW Golf Club cap - stone',
 'Stone/sand, tonal badge','#CFC5AC','Pale neutral','Structured cap, curved brim, moulded badge','Cotton twill',
 'Casual',2,'New South Wales Golf Club - visitor souvenir. Not as a guest there','Good from the photograph.',
 'Keep','Tonal badge is the discreet one of the two NSWGC caps.','core',
 'Navy, brown, olive, white','New South Wales Golf Club, tonal moulded badge.',
 false,'hats_22_nswgc-cap-stone','hats_22_nswgc-cap-stone_retail',2,false,'Plain',false),

('hats_23_nswgc-cap-white','nswgc-cap-white','Hats','NSW Golf Club cap - white',
 'White with full-colour crest and black rope','#F4F2ED','Pale neutral','Rope-front cap, curved brim','Cotton twill',
 'Casual',2,'New South Wales Golf Club - visitor souvenir. Not as a guest there','Good from the photograph.',
 'Keep','Full-colour crest is the loudest badge in the set.','core',
 'Navy, black, stone','New South Wales Golf Club, full-colour crest, black rope trim.',
 false,'hats_23_nswgc-cap-white','hats_23_nswgc-cap-white_retail',2,false,'Plain',false),

('hats_24_woollahra-cap-white','woollahra-cap-white','Hats','Woollahra cap - white',
 'White with blue crest','#F5F3EF','Pale neutral','Structured cap, curved brim','Cotton twill',
 'Casual',2,'Woollahra - home club, no restriction','Good from the photograph.',
 'Keep','The only Woollahra hat. Pairs with the Woollahra polos.','core',
 'Coral, pink, navy, stone','Woollahra Golf Club, blue crest.',
 false,'hats_24_woollahra-cap-white','hats_24_woollahra-cap-white_retail',2,false,'Plain',false),

('hats_25_fighting-for-par-trucker','fighting-for-par-trucker','Hats','Fighting For Par trucker',
 'Cream with olive-khaki patch','#E8E1D2','Pale neutral','Trucker, mesh side and rear panels, flat brim, patch badge','Cotton front, mesh back',
 'Casual',2,'Slogan cap, no club. Fine anywhere casual','Good from the photograph.',
 'Keep','One of the three non-club caps doing any work against the dad-cap risk.','core',
 'Olive, navy, stone, white','"FIGHTING FOR PAR" woven patch. Mesh back - the coolest cap here in Sydney heat.',
 false,'hats_25_fighting-for-par-trucker','hats_25_fighting-for-par-trucker_retail',1,false,'Plain',false),

('hats_26_good-good-cap-pale-blue','good-good-cap-pale-blue','Hats','Good Good cap - pale blue',
 'Pale sky blue with white script','#A9C8DE','Pale neutral','Rope-front cap, curved brim','Cotton twill',
 'Casual',2,'Brand cap, no club. Fine anywhere casual','Good from the photograph.',
 'Keep','Reads current rather than corporate-golf.','core',
 'Navy, white, stone, coral','Good Good Golf, script logo, rope front.',
 false,'hats_26_good-good-cap-pale-blue','hats_26_good-good-cap-pale-blue_retail',2,false,'Plain',false),

('hats_27_good-good-cap-white','good-good-cap-white','Hats','Good Good cap - white "GOOD"',
 'White with black block lettering','#F4F3F0','Pale neutral','Structured cap, flat-ish brim','Cotton twill',
 'Casual',2,'Brand cap, no club. Fine anywhere casual','Good from the photograph.',
 'Keep','Block lettering is the boldest thing in the drawer; wear it casually, not at a club.','core',
 'Black, navy, stone','Good Good Golf, "GOOD" in black block letters.',
 false,'hats_27_good-good-cap-white','hats_27_good-good-cap-white_retail',2,false,'Plain',false),

('hats_28_titleist-cap-cream-peach','titleist-cap-cream-peach','Hats','Titleist cap - cream/peach',
 'Cream with peach script','#EDE6D6','Pale neutral','Structured cap, curved brim','Cotton twill',
 'Casual',2,'Brand cap, no club','Good from the photograph - crown reads clean white where lit.',
 'Keep','Measured against the binned cream/orange VISOR and this cap is clean. Different item.','core',
 'Coral, pink, navy, stone','Titleist Pro V1 promotional cap.',
 false,'hats_28_titleist-cap-cream-peach','hats_28_titleist-cap-cream-peach_retail',2,false,'Plain',false),

('hats_29_titleist-cap-navy','titleist-cap-navy','Hats','Titleist cap - navy',
 'Navy with white script','#2A3550','Anchor dark','Structured cap, curved brim, marker clip','Technical knit',
 'Casual',2,'Brand cap, no club','Good from the photograph.',
 'Keep','The dark cap of the set - the one that works with everything.','core',
 'Anything - navy is neutral against every polo owned','Titleist Pro V1. Ball-marker clip on the brim.',
 false,'hats_29_titleist-cap-navy','hats_29_titleist-cap-navy_retail',2,false,'Plain',false),

('hats_30_titleist-cap-orange','titleist-cap-orange','Hats','Titleist cap - orange',
 'Bright orange with white script','#E8722A','Statement','Structured cap, curved brim, marker clip','Technical knit',
 'Casual',2,'Brand cap, no club','Good from the photograph.',
 'Keep','Loud. Fine for a social round.','core','Navy, white, stone','Titleist. Ball-marker clip on the brim.',
 false,'hats_30_titleist-cap-orange','hats_30_titleist-cap-orange_retail',2,false,'Plain',false),

('hats_31_titleist-visor-red','titleist-visor-red','Hats','Titleist visor - red',
 'Red with cream script and cream trim','#C9302B','Statement','Visor, adjustable rear strap','Cotton twill',
 'Casual',2,'Brand visor, no club','Good. Cleanest of the Titleist visors; trim intact.',
 'Keep','THE visor to keep if the pile is ever cut to one. Works with the coral and pink polos.','core',
 'Coral, pink, white, navy','Titleist Pro V1.',
 false,'hats_31_titleist-visor-red','hats_31_titleist-visor-red_retail',1,false,'Plain',false),

('hats_32_titleist-visor-light-blue','titleist-visor-light-blue','Hats','Titleist visor - light blue',
 'Mid-light blue with red and cream script','#3E8FC4','Mid tone','Visor, adjustable rear strap, marker clip','Cotton twill',
 'Casual',2,'Brand visor, no club','Good. Colour even, script crisp.',
 'Keep','SURPLUS - sound, but one of five visors kept for an activity Max rarely does now.','core',
 'White, navy, stone','Titleist Pro V1.',
 false,'hats_32_titleist-visor-light-blue','hats_32_titleist-visor-light-blue_retail',1,false,'Plain',false),

('hats_33_titleist-visor-coral','titleist-visor-coral','Hats','Titleist visor - coral',
 'Coral with grey-cream script and tan trim','#E08272','Statement','Visor, adjustable rear strap','Cotton twill',
 'Casual',2,'Brand visor, no club','Good from the photograph.',
 'Keep','SURPLUS - see hats_32.','core','Navy, white, stone','Titleist Pro V1.',
 false,'hats_33_titleist-visor-coral','hats_33_titleist-visor-coral_retail',1,false,'Plain',false),

('hats_34_titleist-visor-cream-navy','titleist-visor-cream-navy','Hats','Titleist visor - cream/navy',
 'Cream/stone with navy script','#DCD2B8','Pale neutral','Visor, adjustable rear strap, marker clip','Cotton twill',
 'Casual',2,'Brand visor, no club','Good from the photograph.',
 'Keep','SURPLUS - see hats_32. Distinct from the binned cream/ORANGE visor.','core',
 'Navy, coral, stone','Titleist Pro V1.',
 false,'hats_34_titleist-visor-cream-navy','hats_34_titleist-visor-cream-navy_retail',1,false,'Plain',false),

('hats_35_babolat-visor-navy','babolat-visor-navy','Hats','Babolat visor - navy',
 'Navy','#3A4A63','Anchor dark','Visor, adjustable rear strap','Technical polyester',
 'Casual',2,'TENNIS brand. Not for a golf course','Good from the photograph.',
 'Keep','The only piece here from another sport. Fine for tennis or the range, wrong for a round.','core',
 'Anything casual','Babolat - a tennis brand.',
 false,'hats_35_babolat-visor-navy','hats_35_babolat-visor-navy_retail',1,false,'Plain',false),

('hats_36_visor-blue-space-dye','visor-blue-space-dye','Hats','Visor - blue space-dye',
 'Heather blue, space-dyed','#7FA8C6','Mid tone','Visor, adjustable rear strap','Technical knit',
 'Casual',2,'Unbranded','Good from the photograph.',
 'Keep','Unbranded, no logo at all - the most anonymous thing in the drawer.','core',
 'White, navy, stone','Space-dyed knit; no visible branding.',
 false,'hats_36_visor-blue-space-dye','hats_36_visor-blue-space-dye_retail',1,false,'Space-dye',false),

('hats_37_visor-pink-plain','visor-pink-plain','Hats','Visor - pink, plain',
 'Bright pink','#E2547F','Statement','Visor, adjustable rear strap','Technical knit',
 'Casual',2,'Unbranded','Good from the photograph.',
 'Keep','No branding of any kind.','core','White, navy, stone','No visible branding.',
 false,'hats_37_visor-pink-plain','hats_37_visor-pink-plain_retail',1,false,'Plain',false),

('hats_38_cap-navy-plain','cap-navy-plain','Hats','Cap - navy, plain',
 'Navy with a small blue tab','#41527A','Anchor dark','Unstructured cap, curved brim','Technical, light',
 'Casual',2,'Small unidentified tab logo','Good from the photograph.',
 'Keep','Brand not identified - a small tab logo on the front, too small to read at this distance.','core',
 'Anything - navy is neutral','Brand unread. Confirm from the label if it matters.',
 false,'hats_38_cap-navy-plain','hats_38_cap-navy-plain_retail',2,false,'Plain',true),

('hats_39_tour-de-france-cap','tour-de-france-cap','Hats','Tour de France cap',
 'Black with white and yellow logo','#26262A','Anchor dark','Structured cap, curved brim','Cotton twill',
 'Casual',2,'Cycling, not golf. Casual wear only','Heavily linted. A lint roller fixes it - not damage.',
 'Keep','Not golf. Kept as casual wear.','core','Anything casual','Tour de France official cap.',
 false,'hats_39_tour-de-france-cap','hats_39_tour-de-france-cap_retail',2,false,'Plain',false),

('hats_40_bucket-hat-yellow','bucket-hat-yellow','Hats','Bucket hat - yellow',
 'Bright yellow','#E8DC2E','Statement','Bucket hat, full brim','Cotton twill',
 'Casual',2,'Unbranded','Only photographed out of focus. Condition not assessed.',
 'Keep','The only full-brim hat owned, so the only one that covers ears and neck. Worth remembering in February.','core',
 'White, navy, stone','No visible branding. Reshoot - the one frame is blurred.',
 false,'hats_40_bucket-hat-yellow','hats_40_bucket-hat-yellow_retail',2,false,'Plain',true);

-- Occasions. Golf for everything club- or golf-branded; the tennis visor, the Tour de France
-- cap and the bucket hat are not golf.
INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, 'golf' FROM items WHERE cat_code='Hats'
  AND id BETWEEN 'hats_11' AND 'hats_34_zzz'
  AND id NOT IN ('hats_35_babolat-visor-navy','hats_39_tour-de-france-cap','hats_40_bucket-hat-yellow')
ON CONFLICT DO NOTHING;

INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, 'casual' FROM items WHERE cat_code='Hats' AND id > 'hats_10_zzz'
ON CONFLICT DO NOTHING;

INSERT INTO item_occasions (item_id, occasion_code)
SELECT id, 'weekend' FROM items WHERE cat_code='Hats' AND id > 'hats_10_zzz'
ON CONFLICT DO NOTHING;

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('hats_35_babolat-visor-navy','gym'),
('hats_40_bucket-hat-yellow','gym')
ON CONFLICT DO NOTHING;

-- Every colour on these rows came off a worn selfie in mixed indoor light.
INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT id, 'hex', 'derived',
       'Estimated from a worn photograph in mixed indoor light, 2026-08-31. Not measured against a neutral. Reshoot on a plain surface in even light to confirm.'
FROM items WHERE cat_code='Hats' AND id > 'hats_10_zzz'
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('hats_13_rsgc-cap-red-soft','condition','manual','Only frame is out of focus; condition deliberately not asserted.'),
('hats_40_bucket-hat-yellow','condition','manual','Only frame is out of focus; condition deliberately not asserted.'),
('hats_38_cap-navy-plain','notes','manual','Brand tab too small to read in the available photograph; left unidentified rather than guessed.')
ON CONFLICT DO NOTHING;

-- CORRECTION: drop the photo row for the frame mis-filed against hats_07 in 045. The file has
-- been renamed on Drive to hats_16_rsgc-cap-white-navy_01_worn-front.jpg and will re-import
-- against the correct item.
DELETE FROM photos
WHERE item_id = 'hats_07_rsgc-visor-memorabilia'
  AND source_filename = 'hats_07_rsgc-visor-memorabilia_02_worn-front-b.jpg';

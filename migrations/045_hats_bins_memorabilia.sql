-- 045_hats_bins_memorabilia.sql
-- 2026-08-31. First rows in the Hats category (created in 044).
--
-- SCOPE OF THIS MIGRATION: only the ten hats whose identity and disposition are settled.
-- Six binned, two memorabilia, two rescued from my own bad call. The remaining ~20 keepers
-- are NOT here: they were photographed as worn selfies, several appear in more than one
-- batch, and I cannot deduplicate them reliably enough to insert twenty rows without
-- risking a double-count. That reconciliation gets its own migration, per the discipline
-- in count-reconciliation-and-provenance.md.
--
-- CLUB RULE, confirmed by Max 2026-08-31: he is a member at BOTH Royal Sydney Golf Club
-- (RSGC) and Woollahra Golf Club. So RSGC and Woollahra headwear carries no restriction
-- anywhere. Bonville and New South Wales Golf Club caps are visitor souvenirs: fine
-- socially, wrong worn as a guest at those clubs. That rule belongs on the individual
-- rows when the keepers are catalogued.
--
-- gone_at is used as 009 defines it - the garment is physically gone - alongside the Bin
-- verdict, which is only the opinion that it should go. Both are set here because both
-- are true: Max binned these on 2026-08-31.

INSERT INTO items (id, slug, cat_code, name, colour, hex, role_code, cut, material,
                   formality_raw, formality_rank, condition, verdict_code, verdict_note,
                   scope_code, pairs, notes, no_photo, photo_prefix, retail_prefix,
                   warmth, rain_unsafe, pattern, unconfirmed, gone_at) VALUES

('hats_01_titleist-visor-cream-orange','titleist-visor-cream-orange','Hats',
 'Titleist visor - cream/orange','Cream with orange script','#E4DCC4','Pale neutral',
 'Visor, adjustable rear strap','Cotton twill','Casual',2,
 'Yellowed through the band and brim; a ball marker had been clipped on long enough to mark it',
 'Bin','Discolouration is set in, not washable.','out','-',
 'Binned 2026-08-31. Titleist Pro V1 promotional visor.',
 false,'hats_01_titleist-visor-cream-orange','hats_01_titleist-visor-cream-orange_retail',
 1,false,'Plain',false,now()),

('hats_02_titleist-visor-peach-blue','titleist-visor-peach-blue','Hats',
 'Titleist visor - peach/blue','Peach/apricot with blue script','#E8B487','Statement',
 'Visor, adjustable rear strap','Cotton twill','Casual',2,
 'Bleached unevenly from the top of the band down to the brim edge',
 'Bin','Sun damage, uneven and permanent.','out','-',
 'Binned 2026-08-31.',
 false,'hats_02_titleist-visor-peach-blue','hats_02_titleist-visor-peach-blue_retail',
 1,false,'Plain',false,now()),

('hats_03_titleist-visor-slate-red','titleist-visor-slate-red','Hats',
 'Titleist visor - slate/red','Slate blue-grey with red script','#7C7F8C','Mid tone',
 'Visor, adjustable rear strap','Cotton twill','Casual',2,
 'Set-in staining across the band; band edge abraded',
 'Bin','Staining plus edge wear.','out','-',
 'Binned 2026-08-31.',
 false,'hats_03_titleist-visor-slate-red','hats_03_titleist-visor-slate-red_retail',
 1,false,'Plain',false,now()),

('hats_04_titleist-visor-lavender','titleist-visor-lavender','Hats',
 'Titleist visor - lavender','Lavender with orange script','#A99BC0','Mid tone',
 'Visor, adjustable rear strap','Cotton twill','Casual',2,
 'Blotched across both band and brim',
 'Bin','Blotching is set in.','out','-',
 'Binned 2026-08-31.',
 false,'hats_04_titleist-visor-lavender','hats_04_titleist-visor-lavender_retail',
 1,false,'Plain',false,now()),

('hats_05_trophy-cap-faded-navy','trophy-cap-faded-navy','Hats',
 'Trophy cap - faded navy','Navy faded to grey-purple','#6B6377','Mid tone',
 'Unstructured six-panel cap, curved brim','Cotton twill','Casual',2,
 'Sun-cooked from navy to purple, unevenly across the crown; surface fuzzed',
 'Bin','Colour gone, nap raised.','out','-',
 'Binned 2026-08-31. Silver trophy embroidery; event not identified.',
 false,'hats_05_trophy-cap-faded-navy','hats_05_trophy-cap-faded-navy_retail',
 2,false,'Plain',false,now()),

('hats_06_rsgc-cap-faded-blue','rsgc-cap-faded-blue','Hats',
 'RSGC cap - faded blue','Blue faded to pale lavender-grey','#9E97AE','Pale neutral',
 'Unstructured six-panel cap, curved brim','Cotton twill','Casual',2,
 'Heavily sun-faded across the crown; undervisor gone dingy',
 'Bin','Faded past use.','out','-',
 'Royal Sydney Golf Club. Binned by Max 2026-08-30, the first hat call of this pass.',
 false,'hats_06_rsgc-cap-faded-blue','hats_06_rsgc-cap-faded-blue_retail',
 2,false,'Plain',false,now()),

-- MEMORABILIA. Kept, catalogued, never offered for a round: scope 'out' is exactly this
-- case - the item stays in the catalogue but is excluded from outfit building. Condition
-- here is documentation, not a verdict, so neither carries a Bin verdict.

('hats_07_rsgc-visor-memorabilia','rsgc-visor-memorabilia','Hats',
 'RSGC visor - memorabilia','Slate navy with red crest','#646C75','Anchor dark',
 'Visor, adjustable rear strap','Cotton twill','Casual',2,
 'Abraded patch on the right of the band, staining across it. Not a factor - this one is not worn.',
 'Keep','MEMORABILIA. Kept regardless of condition, on Max''s instruction 2026-08-31.',
 'out','-',
 'Royal Sydney Golf Club. Max: "memorabilia. It stays. Even if not won." Body colour measured #646C75 white-balanced, crest measured #E36E73 - Max described it as navy with a blue crest, so either the description or the identification is off by one visor; confirm which physical visor this row is before filing photos against it.',
 false,'hats_07_rsgc-visor-memorabilia','hats_07_rsgc-visor-memorabilia_retail',
 1,false,'Plain',true,null),

('hats_08_masters-cap-navy','masters-cap-navy','Hats',
 'Masters cap - navy','Navy','#2F3644','Anchor dark',
 'Unstructured six-panel cap, curved brim','Cotton twill','Casual',2,
 'Faded and linted, crown softened. Documentation only - not worn for rounds.',
 'Keep','MEMORABILIA. Augusta National. Kept for what it is, not for wear.',
 'out','-',
 'Masters logo embroidered on the crown. A lint roller would tidy it if it is ever worn.',
 false,'hats_08_masters-cap-navy','hats_08_masters-cap-navy_retail',
 2,false,'Plain',false,null),

-- RESCUED. Both were in my bin grid on 2026-08-31 and both calls were wrong. Max
-- photographed them on the desk in even light and the damage I described was not there.
-- See the note on each row - the reasons differ and both are worth keeping on record.

('hats_09_new-balance-visor-neon','new-balance-visor-neon','Hats',
 'New Balance visor - neon','Neon yellow-green','#D6E83A','Statement',
 'Visor, adjustable rear strap, mesh sweatband','Technical polyester','Casual',2,
 'Good. Band print intact, brim clean, mesh sweatband sound.',
 'Keep','Running visor, not golf. Occasions set accordingly.','core','-',
 'New Balance. NOT a golf visor - branded running headwear, which is where the neon comes from. CORRECTION 2026-08-31: I put this in the bin grid as "logo bleached illegible, band blotched". Wrong. The pale shapes across the band are the "new balance" wordmark printed repeatedly in a lighter green - a deliberate tonal print, not sun damage. I read a design detail as damage from a worn selfie in shadow.',
 false,'hats_09_new-balance-visor-neon','hats_09_new-balance-visor-neon_retail',
 1,false,'Logo print',false,null),

('hats_10_titleist-fj-visor-black','titleist-fj-visor-black','Hats',
 'Titleist/FJ visor - black','Black with white script, cream undertrim','#191919','Anchor dark',
 'Visor, adjustable rear strap','Cotton twill','Casual',2,
 'Good. Black even and deep, white embroidery crisp, cream undertrim clean.',
 'Keep','Sound. The dark visor of the pair Max keeps.','core',
 'Anything - black visor is neutral against every polo in the wardrobe',
 'Co-branded Titleist front with an FJ (FootJoy) mark on the left side. CORRECTION 2026-08-31: I put this in the bin grid as "black gone brown-grey, trim soiled". Wrong. That was warm indoor light plus forehead shadow in the worn shot; on the desk it is clean.',
 false,'hats_10_titleist-fj-visor-black','hats_10_titleist-fj-visor-black_retail',
 1,false,'Plain',false,null);

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('hats_09_new-balance-visor-neon','gym'),
('hats_09_new-balance-visor-neon','casual'),
('hats_10_titleist-fj-visor-black','golf'),
('hats_10_titleist-fj-visor-black','casual')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('hats_07_rsgc-visor-memorabilia','notes','manual','Memorabilia status stated by Max 2026-08-31. Colour values measured from photograph and disagree with his description - flagged, not resolved.'),
('hats_09_new-balance-visor-neon','condition','manual','Re-assessed 2026-08-31 from a desk photograph in even light, overturning a bin call made from a worn selfie.'),
('hats_10_titleist-fj-visor-black','condition','manual','Re-assessed 2026-08-31 from a desk photograph in even light, overturning a bin call made from a worn selfie.'),
('hats_09_new-balance-visor-neon','hex','derived','Estimated from photograph; neon greens clip badly on a phone sensor. Reshoot if the swatch looks wrong in the grid.'),
('hats_01_titleist-visor-cream-orange','hex','derived','Estimated from photograph. Item is gone, so this will never be confirmed.'),
('hats_02_titleist-visor-peach-blue','hex','derived','Estimated from photograph. Item is gone.'),
('hats_03_titleist-visor-slate-red','hex','derived','Estimated from photograph. Item is gone.'),
('hats_04_titleist-visor-lavender','hex','derived','Estimated from photograph. Item is gone.'),
('hats_05_trophy-cap-faded-navy','hex','derived','Estimated from photograph. Item is gone.'),
('hats_06_rsgc-cap-faded-blue','hex','derived','Estimated from photograph. Item is gone.')
ON CONFLICT DO NOTHING;

-- 040_fits_marina.sql
-- 2026-08-30. The two harbourside fits designed in claude/fits-marina.md.
--
-- Both hero renders exist on Drive before this runs, per the project rule that no fit enters the
-- database without one: Wardrobe Photos\Fits\fit_m1_tan-and-cornflower_render.jpg and
-- fit_m2_white-blue-and-burgundy_render.jpg. import_photos.py resolves a fit render by matching
-- the filename to a fits row, so the rows have to exist before it can index them - the render
-- itself was filed first, which is what the rule is actually protecting against.
--
-- score is left NULL on both. That column is Max's own 1-10 opinion and nothing may compute it.
--
-- QC on the renders: both 2048x2048 square, pure white background, all five garments present and
-- correct, the draped knit rendered draped rather than worn, and the lower legs connecting the
-- shorts to the shoes. Two small deviations from the real garments, recorded rather than hidden:
-- the M1 render draws the penny loafer as a driving moc, and the M2 render gives shorts_10 a
-- turn-up cuff it does not have. Neither is worth a regeneration.

INSERT INTO fits (id, name, register_code, killer, vetted, hidden_by_default, style, commentary,
                  catch, formality_rank, rain_safe, source, sort_order, hero_is_generated) VALUES
('fit_m1_tan-and-cornflower', 'Tan and cornflower', 'everyday', false, true, false,
 'Riviera casual - quiet, warm-cool, nothing trying hard',
 'Tan and cornflower is a warm-cool pair that flatters Max without either half shouting, and the navy knit on the shoulders is the anchor that stops the whole thing floating away into pastel. Brown suede against tan cotton keeps the bottom half tonal so the eye goes to the shirt. Built for a Sydney marina or a harbourside lunch: cotton and linen throughout, because technical cloth reads as golf kit the moment it leaves a course.',
 'The draped knit is a substitute. fedeli-cashmere-crew is the better choice - oatmeal cashmere over cornflower linen beats navy wool, and cashmere drapes where wool can sit stiff - but its verdict is Tailor: the cuff needs repairing and there is a mark at the neck. A shoulder drape puts the cuffs knotted in the middle of the chest, which is the worst place for a damaged cuff. Swap the Fedeli in once it is repaired.',
 3, true, 'fits-marina.md 2026-08-30', 100, true),

('fit_m2_white-blue-and-burgundy', 'White, pale blue and burgundy', 'everyday', false, true, false,
 'The louder harbourside option - colour in the draped knit, not the shirt',
 'Burgundy against pale blue and white is the one properly French combination in this wardrobe, and it puts the colour where Max actually wants it: everywhere else in his summer clothes the shorts are the neutral and the top carries the colour, and here the draped knit takes that job instead. The navy-and-white webbing belt is the only overtly nautical thing in the outfit - one such item is charm, two is costume - so nothing else references boats.',
 'shoes_08c_megis-driving-moc is currently scope = out, marked holiday only. It is the most correct shoe Max owns for this setting, so this fit is the argument for bringing it back into rotation. Without it the fallback is the brown suede loafer, which then repeats M1 exactly.',
 3, true, 'fits-marina.md 2026-08-30', 110, true);

INSERT INTO fit_items (fit_id, item_id, role, position, note) VALUES
('fit_m1_tan-and-cornflower','lyle-scott-club-navy-vneck','layer',1,'DRAPED over the shoulders, sleeves knotted at the chest - not worn. Swap for fedeli-cashmere-crew once its cuff is repaired.'),
('fit_m1_tan-and-cornflower','tops_15_florentino-blue-linen-shirt','top',2,'Untucked, collar open, sleeves rolled to just below the elbow.'),
('fit_m1_tan-and-cornflower','shorts_01_zara-tan-chino','bottom',3,'Turn-up cuff left as it is - on a tan chino short it reads considered, not dated.'),
('fit_m1_tan-and-cornflower','belts_02_tan-vera-pelle','belt',4,NULL),
('fit_m1_tan-and-cornflower','shoes_08a_suede-penny-loafer','shoe',5,'Sockless.'),

('fit_m2_white-blue-and-burgundy','polo-rl-burgundy-cashmere-crew','layer',1,'DRAPED over the shoulders, not worn. Its own note warns it is too roomy to wear over a polo - draped, that does not apply, and this is why it is on the shoulders here.'),
('fit_m2_white-blue-and-burgundy','tops_02_brioni-white-blue-collar-polo','top',2,'The pale blue contrast collar is the point - do not substitute a plain white polo.'),
('fit_m2_white-blue-and-burgundy','shorts_10_decathlon-pale-blue','bottom',3,'Swap to shorts_17_chambray-linen-look if the slubbier cloth is wanted.'),
('fit_m2_white-blue-and-burgundy','belts_07_marki-navy-white-webbing','belt',4,'The one nautical reference in the outfit. Nothing else may add another.'),
('fit_m2_white-blue-and-burgundy','shoes_08c_megis-driving-moc','shoe',5,'Sockless. Currently scope = out; see the fit catch.');

INSERT INTO fit_temp_bands (fit_id, band_code) VALUES
('fit_m1_tan-and-cornflower','warm'), ('fit_m1_tan-and-cornflower','mild'),
('fit_m2_white-blue-and-burgundy','warm'), ('fit_m2_white-blue-and-burgundy','mild');

INSERT INTO fit_seasons (fit_id, season_code) VALUES
('fit_m1_tan-and-cornflower','summer'), ('fit_m1_tan-and-cornflower','spring'),
('fit_m2_white-blue-and-burgundy','summer'), ('fit_m2_white-blue-and-burgundy','spring');

INSERT INTO fit_occasions (fit_id, occasion_code, kind) VALUES
('fit_m1_tan-and-cornflower','weekend','good'), ('fit_m1_tan-and-cornflower','casual','good'),
('fit_m1_tan-and-cornflower','golf','bad'),      ('fit_m1_tan-and-cornflower','work','bad'),
('fit_m2_white-blue-and-burgundy','weekend','good'), ('fit_m2_white-blue-and-burgundy','casual','good'),
('fit_m2_white-blue-and-burgundy','golf','bad'),     ('fit_m2_white-blue-and-burgundy','work','bad');

INSERT INTO fit_preconditions (fit_id, text, item_id) VALUES
('fit_m2_white-blue-and-burgundy','Decide whether the navy suede driving moc comes back into rotation - it is currently scope = out, marked holiday only, and it is the shoe this fit is built on.','shoes_08c_megis-driving-moc');

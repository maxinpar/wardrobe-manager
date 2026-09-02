-- 063_fits_golf_batch_1.sql
-- Golf fits, batch 1: SEEN 1-4, PRO 1-4, OLD 1-4.
-- Source: claude/fits-golf-batch-1.md (2026-09-01). Renders QC'd 2026-09-02 from the
-- "Golf Fits-2" export by contact sheet, which caught that Seen-2-polo.jpeg was the
-- WITH-layer image despite its name.
--
-- Every fit has TWO renders on Drive:
--   <fit_id>_render.jpeg          without the optional layer  <- canonical, becomes hero
--   <fit_id>_layered_render.jpeg  with the optional layer     <- not yet modelled
-- The base render is canonical because the rule for this batch is that the fit must
-- stand up without the layer. import_photos.py will report the _layered_ files as
-- unfiled until the render-variant work lands.

INSERT INTO fit_categories (code, label, sort_order) VALUES
  ('golf_seen',      'Golf — I want to be SEEN', 110),
  ('golf_pro',       'Golf — Is he a pro?',      120),
  ('golf_oldschool', 'Golf — Old school',        130),
  ('golf_modern',    'Golf — Modern',            140),
  ('golf_winter',    'Golf — Winter golf',       150),
  ('golf_club',      'Golf — Club day',          160),
  ('golf_away',      'Golf — Away day',          170),
  ('golf_19th',      'Golf — The 19th',          180),
  ('golf_wet',       'Golf — Wet & windy',       190)
ON CONFLICT (code) DO NOTHING;

INSERT INTO fits (id, name, register_code, category_code, formality_rank, style,
                  commentary, catch, source, sort_order) VALUES
('fit_g1_jade-and-strawberry', 'Jade & strawberry', 'everyday', 'golf_seen', 2,
 'Loud, complementary',
 'Jade and strawberry red sit opposite each other on the wheel, so the pairing reads as a decision rather than an accident. Cream shoe and cream-and-green cap stop it becoming a traffic light.',
 'The only SEEN fit in trousers — it doubles as the loud chilly-morning option. Not for a 30-degree day.',
 'fits-golf-batch-1.md 2026-09-01', 300),

('fit_g2_orange-and-teal', 'Orange & teal', 'everyday', 'golf_seen', 2,
 'Loud, complementary',
 'The cleanest loud pairing in the wardrobe. White polo referees it, and teal appears exactly twice — belt and shoe — bracketing the orange top and bottom.',
 'Do not add a third colour. The teal belt and teal shoe are the whole structure.',
 'fits-golf-batch-1.md 2026-09-01', 301),

('fit_g3_red-and-azure', 'Red & azure', 'everyday', 'golf_seen', 2,
 'Loud, primaries',
 'Two primaries with a hard white break at the waist. Lime is the third colour, used twice — visor and shoe flash — and nowhere else; that repetition is what keeps it deliberate.',
 'The white belt is load-bearing. Swap it for a coloured one and the red and blue start fighting.',
 'fits-golf-batch-1.md 2026-09-01', 302),

('fit_g4_coral-riot', 'Coral riot', 'everyday', 'golf_seen', 2,
 'Loud, print-led',
 'The only fit in the batch where the print does the shouting, so everything below it goes quiet and dark. The indigo-violet belt picks up the polo''s magenta collar.',
 'Vest, not a quarter-zip — a sleeve over this print buries it. Alternate belt: the purple plastic one.',
 'fits-golf-batch-1.md 2026-09-01', 303),

('fit_g5_tour-charcoal', 'Tour charcoal', 'everyday', 'golf_pro', 2,
 'Tour monochrome',
 'Dark top, white bottom, black visor, zero pattern anywhere. Nothing to look at, which is the point.',
 'Keep the shoe grey or white. A coloured shoe undoes the whole register.',
 'fits-golf-batch-1.md 2026-09-01', 310),

('fit_g6_teal-and-slate', 'Teal & slate', 'everyday', 'golf_pro', 2,
 'Tonal, muted',
 'The ELORD teal is muted enough to act as a neutral, so teal over slate is a two-step tonal move rather than a colour clash. Cream at the shoe and cap lifts it off drab.',
 'Needs the cream accents. All-grey accessories and it goes flat.',
 'fits-golf-batch-1.md 2026-09-01', 311),

('fit_g7_grey-one-navy-note', 'Grey with one navy note', 'everyday', 'golf_pro', 2,
 'Grey plus one colour',
 'The grey-plus-one-colour rule at its strictest: grey polo, grey shoe, and navy used exactly three times.',
 'Swap the navy short for a grey one and the fit dies. The navy is the only thing holding it up.',
 'fits-golf-batch-1.md 2026-09-01', 312),

('fit_g8_dusty-rose-charcoal', 'Dusty rose & charcoal', 'everyday', 'golf_pro', 2,
 'Current, muted',
 'Dusty rose over charcoal is the most current thing in the wardrobe and reads as confidence rather than as a man in a pink shirt. Rescues a polo that fits nowhere else.',
 'Charcoal below, nothing warmer. A tan or khaki short turns it sickly.',
 'fits-golf-batch-1.md 2026-09-01', 313);

INSERT INTO fits (id, name, register_code, category_code, formality_rank, style,
                  commentary, catch, source, sort_order) VALUES
('fit_g9_cream-and-tan', 'Cream & tan', 'everyday', 'golf_oldschool', 2,
 'Old school, warm neutrals',
 'All cotton, all warm neutrals, tartan hidden inside the waistband where it belongs. The rope cap is the only period detail doing any work.',
 'Wool layer only. A technical quarter-zip over mercerised cotton kills the look instantly.',
 'fits-golf-batch-1.md 2026-09-01', 320),

('fit_g10_argyle-and-stone', 'Argyle & stone', 'everyday', 'golf_oldschool', 2,
 'Old school, patterned',
 'Argyle is the one pattern allowed to be the whole idea, so nothing else patterns. Cream twill below, stone above, navy in the middle.',
 'Blocked on replacing the cream twill short — see the precondition. Wool layer only.',
 'fits-golf-batch-1.md 2026-09-01', 321),

('fit_g11_masters-green', 'Masters green', 'everyday', 'golf_oldschool', 2,
 'Old school, trad',
 'Pine green over white is about as trad as golf gets. The red merino over dark green is the one combination in the batch that looks better with the layer than without it.',
 'Wool layer only, and specifically the red merino — a navy one makes it ordinary.',
 'fits-golf-batch-1.md 2026-09-01', 322),

('fit_g12_blue-medallion', 'Blue medallion', 'everyday', 'golf_oldschool', 2,
 'Old school, preppy',
 'Pale blue over salmon pink is straight 1980s American club preppy, and the single most old-school thing this wardrobe can build. Both garments cotton.',
 'Do not add a technical anything. Wool layer or no layer.',
 'fits-golf-batch-1.md 2026-09-01', 323);

-- Slots. role: top | bottom | belt | shoe | accessory | layer | outer.
-- The layer row is the optional piece Max carries to the club and takes off at the range;
-- it is the difference between the base render and the _layered_ render.
INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note) VALUES
('fit_g1_jade-and-strawberry','tops_84_royal-sydney-jade-polo','top',1,false,NULL),
('fit_g1_jade-and-strawberry','trousers_21_inesis-strawberry','bottom',1,false,NULL),
('fit_g1_jade-and-strawberry','belts_12_white-ratchet-golf','belt',1,false,NULL),
('fit_g1_jade-and-strawberry','shoes_15_inesis-cream-yellow-jf190','shoe',1,false,NULL),
('fit_g1_jade-and-strawberry','hats_15_rsgc-cap-cream-green','accessory',1,false,NULL),
('fit_g1_jade-and-strawberry','turtleson-stone-quarterzip','layer',1,false,'optional — see the layered render'),

('fit_g2_orange-and-teal','tops_95_abacus-bonville-white-polo','top',1,false,NULL),
('fit_g2_orange-and-teal','shorts_12_decathlon-orange-tech','bottom',1,false,NULL),
('fit_g2_orange-and-teal','belts_14_puma-teal','belt',1,false,NULL),
('fit_g2_orange-and-teal','shoes_12_inesis-teal-jf100','shoe',1,false,NULL),
('fit_g2_orange-and-teal','hats_30_titleist-cap-orange','accessory',1,false,NULL),
('fit_g2_orange-and-teal','turtleson-stone-quarterzip','layer',1,false,'optional — see the layered render'),

('fit_g3_red-and-azure','tops_59_ping-blue-colourblock-polo','top',1,false,NULL),
('fit_g3_red-and-azure','shorts_13_crosssportswear-red','bottom',1,false,NULL),
('fit_g3_red-and-azure','belts_12_white-ratchet-golf','belt',1,false,NULL),
('fit_g3_red-and-azure','shoes_16_navy-lime-spiked','shoe',1,false,NULL),
('fit_g3_red-and-azure','hats_19_rsgc-visor-lime','accessory',1,false,NULL),
('fit_g3_red-and-azure','calvin-klein-navy-quarterzip','layer',1,false,'optional — see the layered render'),

('fit_g4_coral-riot','tops_66_good-good-coral-floral-polo','top',1,false,NULL),
('fit_g4_coral-riot','shorts_15_decathlon-navy-tech','bottom',1,false,NULL),
('fit_g4_coral-riot','belts_13_puma-indigo-violet','belt',1,false,NULL),
('fit_g4_coral-riot','shoes_12_inesis-teal-jf100','shoe',1,false,NULL),
('fit_g4_coral-riot','hats_33_titleist-visor-coral','accessory',1,false,NULL),
('fit_g4_coral-riot','outerwear_19_peter-millar-reversible-vest-pink','outer',1,false,'optional — see the layered render');

INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note) VALUES
('fit_g5_tour-charcoal','tops_88_nike-charcoal-plain-polo','top',1,false,NULL),
('fit_g5_tour-charcoal','shorts_20_callaway-stone','bottom',1,false,NULL),
('fit_g5_tour-charcoal','belts_12_white-ratchet-golf','belt',1,false,NULL),
('fit_g5_tour-charcoal','shoes_17_skechers-grey-spikeless','shoe',1,false,NULL),
('fit_g5_tour-charcoal','hats_10_titleist-fj-visor-black','accessory',1,false,NULL),
('fit_g5_tour-charcoal','unbranded-charcoal-fullzip','layer',1,false,'optional — see the layered render'),

('fit_g6_teal-and-slate','tops_87_elord-teal-polo','top',1,false,NULL),
('fit_g6_teal-and-slate','shorts_11_decathlon-slate-tech','bottom',1,false,NULL),
('fit_g6_teal-and-slate','belts_12_white-ratchet-golf','belt',1,false,NULL),
('fit_g6_teal-and-slate','shoes_13_inesis-cream-blue','shoe',1,false,NULL),
('fit_g6_teal-and-slate','hats_34_titleist-visor-cream-navy','accessory',1,false,NULL),
('fit_g6_teal-and-slate','glenmuir-navy-zipneck','layer',1,false,'optional — see the layered render'),

('fit_g7_grey-one-navy-note','tops_86_grey-peru-unbranded-polo','top',1,false,NULL),
('fit_g7_grey-one-navy-note','shorts_15_decathlon-navy-tech','bottom',1,false,NULL),
('fit_g7_grey-one-navy-note','belts_12_white-ratchet-golf','belt',1,false,NULL),
('fit_g7_grey-one-navy-note','shoes_19_inesis-jf100-1-grey','shoe',1,false,NULL),
('fit_g7_grey-one-navy-note','hats_29_titleist-cap-navy','accessory',1,false,NULL),
('fit_g7_grey-one-navy-note','calvin-klein-navy-quarterzip','layer',1,false,'optional — see the layered render'),

('fit_g8_dusty-rose-charcoal','tops_61_rose-unbranded-polo','top',1,false,NULL),
('fit_g8_dusty-rose-charcoal','shorts_14_footjoy-charcoal','bottom',1,false,NULL),
('fit_g8_dusty-rose-charcoal','belts_12_white-ratchet-golf','belt',1,false,NULL),
('fit_g8_dusty-rose-charcoal','shoes_17_skechers-grey-spikeless','shoe',1,false,NULL),
('fit_g8_dusty-rose-charcoal','hats_16_rsgc-cap-white-navy','accessory',1,false,NULL),
('fit_g8_dusty-rose-charcoal','nike-golf-grey-knit-halfzip','layer',1,false,'optional — see the layered render');

INSERT INTO fit_items (fit_id, item_id, role, position, is_alternate, note) VALUES
('fit_g9_cream-and-tan','tops_69_glenmuir-cream-mercerised-polo','top',1,false,NULL),
('fit_g9_cream-and-tan','shorts_16_yellow-tartan-trim','bottom',1,false,NULL),
('fit_g9_cream-and-tan','belts_12_white-ratchet-golf','belt',1,false,NULL),
('fit_g9_cream-and-tan','shoes_13_inesis-cream-blue','shoe',1,false,NULL),
('fit_g9_cream-and-tan','hats_20_bonville-cap-tan-rope','accessory',1,false,NULL),
('fit_g9_cream-and-tan','glenmuir-navy-merino-vneck','layer',1,false,'optional — wool only'),

('fit_g10_argyle-and-stone','tops_73_royal-melbourne-navy-argyle-polo','top',1,false,NULL),
('fit_g10_argyle-and-stone','shorts_08_decathlon-cream-twill','bottom',1,false,'verdict Replace — the fit will badge until this is replaced'),
('fit_g10_argyle-and-stone','belts_12_white-ratchet-golf','belt',1,false,NULL),
('fit_g10_argyle-and-stone','shoes_15_inesis-cream-yellow-jf190','shoe',1,false,NULL),
('fit_g10_argyle-and-stone','hats_22_nswgc-cap-stone','accessory',1,false,NULL),
('fit_g10_argyle-and-stone','glenmuir-navy-zipneck','layer',1,false,'optional — wool only'),

('fit_g11_masters-green','tops_85_masters-dark-green-polo','top',1,false,NULL),
('fit_g11_masters-green','shorts_20_callaway-stone','bottom',1,false,NULL),
('fit_g11_masters-green','belts_12_white-ratchet-golf','belt',1,false,NULL),
('fit_g11_masters-green','shoes_17_skechers-grey-spikeless','shoe',1,false,NULL),
('fit_g11_masters-green','hats_14_rsgc-cap-cream-navy','accessory',1,false,NULL),
('fit_g11_masters-green','glenmuir-red-merino-quarterzip','layer',1,false,'optional — better WITH the layer than without'),

('fit_g12_blue-medallion','tops_76_ralph-lauren-blue-medallion-polo','top',1,false,NULL),
('fit_g12_blue-medallion','shorts_04_tony-moro-pink','bottom',1,false,NULL),
('fit_g12_blue-medallion','belts_12_white-ratchet-golf','belt',1,false,NULL),
('fit_g12_blue-medallion','shoes_13_inesis-cream-blue','shoe',1,false,NULL),
('fit_g12_blue-medallion','hats_34_titleist-visor-cream-navy','accessory',1,false,NULL),
('fit_g12_blue-medallion','glenmuir-navy-zipneck','layer',1,false,'optional — wool only');

-- Occasions. These are golf fits; none of them is a work or formal fit.
INSERT INTO fit_occasions (fit_id, occasion_code, kind)
SELECT f.id, o.code, o.kind
FROM (VALUES
  ('fit_g1_jade-and-strawberry'),('fit_g2_orange-and-teal'),('fit_g3_red-and-azure'),
  ('fit_g4_coral-riot'),('fit_g5_tour-charcoal'),('fit_g6_teal-and-slate'),
  ('fit_g7_grey-one-navy-note'),('fit_g8_dusty-rose-charcoal'),('fit_g9_cream-and-tan'),
  ('fit_g10_argyle-and-stone'),('fit_g11_masters-green'),('fit_g12_blue-medallion')
) AS f(id)
CROSS JOIN (VALUES ('golf','good'),('work','bad'),('formal','bad')) AS o(code, kind);

-- Temperature bands drive the picker. Eleven of the twelve are shorts fits.
-- fit_g1 is the only one in trousers, so it drops the warm band and picks up cold.
INSERT INTO fit_temp_bands (fit_id, band_code)
SELECT f.id, b.code
FROM (VALUES
  ('fit_g2_orange-and-teal'),('fit_g3_red-and-azure'),('fit_g4_coral-riot'),
  ('fit_g5_tour-charcoal'),('fit_g6_teal-and-slate'),('fit_g7_grey-one-navy-note'),
  ('fit_g8_dusty-rose-charcoal'),('fit_g9_cream-and-tan'),('fit_g10_argyle-and-stone'),
  ('fit_g11_masters-green'),('fit_g12_blue-medallion')
) AS f(id)
CROSS JOIN (VALUES ('mild'),('warm')) AS b(code);

INSERT INTO fit_temp_bands (fit_id, band_code) VALUES
  ('fit_g1_jade-and-strawberry','cold'),
  ('fit_g1_jade-and-strawberry','mild');

-- Seasons are a browsing label only and must not affect the picker.
INSERT INTO fit_seasons (fit_id, season_code)
SELECT f.id, s.code
FROM (VALUES
  ('fit_g2_orange-and-teal'),('fit_g3_red-and-azure'),('fit_g4_coral-riot'),
  ('fit_g5_tour-charcoal'),('fit_g6_teal-and-slate'),('fit_g7_grey-one-navy-note'),
  ('fit_g8_dusty-rose-charcoal'),('fit_g9_cream-and-tan'),('fit_g10_argyle-and-stone'),
  ('fit_g11_masters-green'),('fit_g12_blue-medallion')
) AS f(id)
CROSS JOIN (VALUES ('spring'),('summer')) AS s(code);

INSERT INTO fit_seasons (fit_id, season_code) VALUES
  ('fit_g1_jade-and-strawberry','autumn'),
  ('fit_g1_jade-and-strawberry','winter');

-- One actionable job, seeded from the doc's flag. Not a styling warning — that is the catch.
INSERT INTO fit_preconditions (fit_id, text, item_id, done)
VALUES ('fit_g10_argyle-and-stone',
        'Replace the Decathlon cream twill short — it is the only Replace-verdict garment in this batch and it carries this fit.',
        'shorts_08_decathlon-cream-twill', false);

-- Provenance. fit_field_sources.source is constrained to
-- imported | derived | suggested | manual, so the document reference goes in the note.
INSERT INTO fit_field_sources (fit_id, field_name, source, note)
SELECT f.id, 'category_code', 'manual',
       'Category set by Max, fits-golf-batch-1.md 2026-09-01; one category per fit, style not weather.'
FROM (VALUES
  ('fit_g1_jade-and-strawberry'),('fit_g2_orange-and-teal'),('fit_g3_red-and-azure'),
  ('fit_g4_coral-riot'),('fit_g5_tour-charcoal'),('fit_g6_teal-and-slate'),
  ('fit_g7_grey-one-navy-note'),('fit_g8_dusty-rose-charcoal'),('fit_g9_cream-and-tan'),
  ('fit_g10_argyle-and-stone'),('fit_g11_masters-green'),('fit_g12_blue-medallion')
) AS f(id);

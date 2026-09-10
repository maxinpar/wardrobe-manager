-- 080_this_week.sql — the week you pick on Monday, and the names it needs.
--
-- Source: design_handoff_this_week (2026-09-09).
--
-- "This Week" lays a variant set across Mon–Fri and lets Max shuffle the days
-- and tick off what he wore. Three of the four things it needs are already in
-- the database — the sets themselves (074–079), the renders, the wear log — so
-- this migration adds only what is genuinely missing:
--
--   1. A NAME for a set. `fits.variant_set` is a key (`black_canvas`), and a
--      key is not a thing you put on a screen. The handoff's names are authored
--      prose — "Slate blue-grey gilet over black jeans" — with a shape that is
--      *nearly* derivable and not quite: beige_brown has no fixed knit or gilet
--      to name, so it is called "Beige & brown" after its brief and no rule
--      relating garments to a title would ever produce that.
--
--   2. A SHORT NAME for a garment. The base line under a set reads "the
--      aubergine shawl-collar, black jeans, black belt, ecco nubuck sneaker".
--      Those are not item names ("Ben Sherman shawl-collar", "Black coated
--      straight jeans"): they are colour plus noun, because in a sentence about
--      an outfit the brand is noise and the colour is the whole point.
--
--      wardrobe/sets.py derives exactly that — `colour` + the last word of
--      `name` — and gets fourteen of the fifteen base garments right. The
--      fifteenth is belts_04, whose colour reads "Rustic / distressed medium
--      brown", which derives to "rustic belt". So the column is the override
--      and the derivation is the fallback: a set built next month names its
--      garments sensibly without anyone touching a migration, and the one word
--      the rule cannot reach is written down rather than guessed at.
--
--   3. WHICH set is on this week, and WHICH variant is on each day. The week
--      is already a stored thing (008) for exactly the reason it is stored
--      here: Monday is a fact, Thursday is a decision, and neither survives
--      being re-derived every morning.
--
-- Worn is deliberately NOT a new column. week_days.wear_event_id already means
-- "this day happened", the wear log already records which variant, and the
-- laundry already knows what that put in the basket. A second boolean saying
-- the same thing is a second boolean to disagree with the first.

-- ------------------------------------------------------- naming the sets --

CREATE TABLE variant_sets (
  key        text PRIMARY KEY,     -- matches fits.variant_set
  name       text NOT NULL,        -- what the screen calls it
  source     text,                 -- the brief that authored it
  sort_order smallint NOT NULL DEFAULT 100,
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE variant_sets IS
  'The display name of a fit variant set. A row here is not what makes a set '
  'exist — fits.variant_set is — so a set with no row still works and falls '
  'back to its key. This table only stops the screen shouting BLACK_CANVAS.';

INSERT INTO variant_sets (key, name, source, sort_order) VALUES
  ('black_canvas', 'Slate blue-grey gilet over black jeans',
   'brief-fit-variant-sets.md', 10),
  ('the_shawl',    'Aubergine shawl-collar over black jeans',
   'brief-shawl-set-and-henley.md', 20),
  -- No fixed knit or gilet: the top itself is what changes, so there is no
  -- garment to name it after and it takes the brief's own title.
  ('beige_brown',  'Beige & brown',
   'brief-beige-brown-set.md', 30),
  ('stone_brown',  'Dark brown V-neck over light stone chino',
   'brief-w5-w3-sets.md', 40),
  ('beige_blue',   'Mid blue V-neck over sand chino',
   'brief-w5-w3-sets.md', 50);

-- ---------------------------------------------------- naming the garments --

ALTER TABLE items ADD COLUMN short_name text;

COMMENT ON COLUMN items.short_name IS
  'How this garment is named inside a sentence about an outfit — "black '
  'jeans", not "Black coated straight jeans". NULL is the normal state: '
  'wardrobe.sets.short_name() derives colour + noun, and this column is the '
  'override for the garments that rule gets wrong.';

-- The one the rule cannot reach. Everything else in the five sets derives
-- correctly and is left alone on purpose — writing them all down here would
-- mean maintaining fifteen strings to fix one.
UPDATE items SET short_name = 'brown belt'
 WHERE id = 'belts_04_distressed-brown-everyday';

-- ------------------------------------------------------------- the week --

ALTER TABLE week_plans ADD COLUMN variant_set text REFERENCES variant_sets(key);

COMMENT ON COLUMN week_plans.variant_set IS
  'The set laid across this week by the This Week picker. Distinct from '
  'base_fit_id, which is what the Today screen adopts: one names a week of '
  'five pictures, the other names one fit that holds.';

ALTER TABLE week_days ADD COLUMN set_fit_id text REFERENCES fits(id);

COMMENT ON COLUMN week_days.set_fit_id IS
  'Which variant of the week''s set is on this day. The whole fit, not its '
  'varying garment: the point of the screen is the render, and a render '
  'belongs to a fit.';

CREATE INDEX week_days_set_fit_idx ON week_days (set_fit_id);

-- 008_week_plan.sql — the week is the unit, not the day.
--
-- The model the Today screen is built on: a fit is a base plus a top. The base
-- — knit, bottom, shoe, belt — is chosen once and holds Monday to Friday; only
-- the top rotates. Adopting a fit IS setting the week's base, which is why this
-- has to be stored rather than recomputed: what you wore on Monday is a fact,
-- and Thursday's plan is a decision, and neither survives being derived fresh
-- on every request.

CREATE TABLE day_contexts (
  code       text PRIMARY KEY,          -- office | home
  label      text NOT NULL,
  commutes   boolean NOT NULL DEFAULT false,   -- a day you actually ride in
  sort_order smallint NOT NULL DEFAULT 100
);

INSERT INTO day_contexts (code, label, commutes, sort_order) VALUES
  ('office', 'Office', true,  10),
  ('home',   'Home',   false, 20);

CREATE TABLE week_plans (
  week_start  date PRIMARY KEY,         -- the Monday
  base_fit_id text REFERENCES fits(id),
  adopted_at  timestamptz,
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TRIGGER week_plans_updated_at BEFORE UPDATE ON week_plans
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- One row per weekday. `top_item_id` is the garment that rotates; everything
-- else comes from the base fit. A row with worn_event_id set is history — it
-- happened — and must never be quietly rewritten by a re-plan.
CREATE TABLE week_days (
  week_start    date NOT NULL REFERENCES week_plans(week_start) ON DELETE CASCADE,
  weekday       smallint NOT NULL CHECK (weekday BETWEEN 0 AND 4),  -- Mon..Fri
  context_code  text NOT NULL REFERENCES day_contexts(code) DEFAULT 'office',
  top_item_id   text REFERENCES items(id),
  wear_event_id bigint REFERENCES wear_events(id) ON DELETE SET NULL,
  PRIMARY KEY (week_start, weekday)
);

CREATE INDEX week_days_top_idx ON week_days (top_item_id);

-- Loafers and moccasins come off on a bike; they travel in the top-box and go
-- on at the other end. Derived from the garment's own words, correctable by
-- hand like every other derived field.
ALTER TABLE items ADD COLUMN bike_safe boolean NOT NULL DEFAULT true;

COMMENT ON COLUMN items.bike_safe IS
  'False for a shoe that cannot be ridden in — it travels in the top-box.';

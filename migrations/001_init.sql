-- 001_init.sql — the wardrobe schema.
--
-- Design notes:
--  * items.id is the natural primary key: the existing string slugs from
--    wardrobe.json. They are never renumbered — photo filenames and years of
--    Claude Project context reference them.
--  * The enum-ish fields are lookup TABLES, not Postgres enums, because adding
--    a category (tees, shirts, shorts, socks are all still unlogged) must not
--    need a migration.
--  * Every free-text field from the JSON is kept verbatim. pairs/layer/avoid/
--    notes/fit/condition/verdict_note are hand-written knowledge — the rule
--    engine lives in them.
--  * App-owned state (laundry, wear log) lives in its own tables so that
--    re-running the catalogue importer can never wipe it.

CREATE FUNCTION set_updated_at() RETURNS trigger LANGUAGE plpgsql AS $fn$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$fn$;

-- ---------------------------------------------------------------- lookups --

CREATE TABLE categories (
  code         text PRIMARY KEY,          -- matches the JSON value exactly, e.g. 'Knitwear'
  label        text NOT NULL,
  photo_folder text,                      -- Drive subfolder; 'Tops' lives in 'Shirts'
  sort_order   smallint NOT NULL DEFAULT 100
);

CREATE TABLE colour_roles (
  code       text PRIMARY KEY,            -- 'Pale neutral' … 'Statement'
  label      text NOT NULL,
  sort_order smallint NOT NULL DEFAULT 100
);

CREATE TABLE verdicts (
  code       text PRIMARY KEY,            -- Keep | Tailor | Replace | Bin
  label      text NOT NULL,
  wearable   boolean NOT NULL DEFAULT true,   -- Bin is never suggested
  sort_order smallint NOT NULL DEFAULT 100
);

CREATE TABLE scopes (
  code  text PRIMARY KEY,                 -- core | out
  label text NOT NULL
);

CREATE TABLE necks (
  code       text PRIMARY KEY,            -- crew | v-neck | roll | …
  label      text NOT NULL,
  sort_order smallint NOT NULL DEFAULT 100
);

CREATE TABLE weights (
  code        text PRIMARY KEY,           -- Fine | Light-Mid | Mid | Mid-Heavy | Chunky
  label       text NOT NULL,
  warmth_hint smallint,                   -- seeds the derived warmth 1-5
  sort_order  smallint NOT NULL DEFAULT 100
);

CREATE TABLE occasions (
  code       text PRIMARY KEY,            -- work | casual | golf | formal | gym
  label      text NOT NULL,
  sort_order smallint NOT NULL DEFAULT 100
);

CREATE TABLE registers (
  code       text PRIMARY KEY,            -- everyday | sharp
  label      text NOT NULL,
  sort_order smallint NOT NULL DEFAULT 100
);

CREATE TABLE laundry_states (
  code       text PRIMARY KEY,            -- clean | worn | in_wash | at_tailor
  label      text NOT NULL,
  available  boolean NOT NULL DEFAULT false,   -- only 'clean' is wearable today
  sort_order smallint NOT NULL DEFAULT 100
);

CREATE TABLE photo_angles (
  code       text PRIMARY KEY,            -- label | hanger | worn-front | …
  label      text NOT NULL,
  sort_order smallint NOT NULL DEFAULT 100
);

-- ------------------------------------------------------------------ items --

CREATE TABLE items (
  id            text PRIMARY KEY,
  slug          text NOT NULL,
  cat_code      text NOT NULL REFERENCES categories(code),
  name          text NOT NULL,            -- NOT unique: two "Zara Man V-neck", three "Decathlon chino"
  colour        text,
  hex           text,                     -- reliable on every item; the no-photo fallback swatch
  role_code     text REFERENCES colour_roles(code),
  neck_code     text REFERENCES necks(code),
  neck_raw      text,                     -- 'polo collar (mustard-tipped, contrast placket)'
  cut           text,
  material      text,
  weight_code   text REFERENCES weights(code),
  formality_raw text,                     -- kept verbatim: 'Casual (club crest)'
  fit           text,
  condition     text,
  verdict_code  text NOT NULL REFERENCES verdicts(code),
  verdict_note  text,
  scope_code    text NOT NULL REFERENCES scopes(code),
  works_alone   boolean,                  -- NULL = not applicable (trousers, shoes, belts)
  pairs         text,
  layer         text,
  avoid         text,
  notes         text,
  care_note     text,
  no_photo      boolean NOT NULL DEFAULT false,
  photo_ref     text,
  photo_prefix  text,
  retail_prefix text,

  -- derived on import, correctable by hand; see item_field_sources
  formality_rank    smallint CHECK (formality_rank BETWEEN 1 AND 5),
  formality_note    text,                 -- the parenthetical: why the item is capped
  warmth            smallint CHECK (warmth BETWEEN 1 AND 5),
  weatherproof_rain boolean NOT NULL DEFAULT false,
  weatherproof_wind boolean NOT NULL DEFAULT false,
  rain_unsafe       boolean NOT NULL DEFAULT false,   -- suede/nubuck stay home in the rain
  pattern           text,

  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX items_cat_idx     ON items (cat_code);
CREATE INDEX items_verdict_idx ON items (verdict_code);
CREATE INDEX items_scope_idx   ON items (scope_code);

CREATE TRIGGER items_updated_at BEFORE UPDATE ON items
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TABLE item_occasions (
  item_id       text NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  occasion_code text NOT NULL REFERENCES occasions(code),
  PRIMARY KEY (item_id, occasion_code)
);

-- Where each derived value came from. The importer refreshes rows marked
-- 'derived'; it never overwrites one marked 'manual'. A hand-correction is
-- visibly authoritative over the guess.
CREATE TABLE item_field_sources (
  item_id    text NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  field_name text NOT NULL,
  source     text NOT NULL CHECK (source IN ('imported', 'derived', 'manual')),
  note       text,
  updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (item_id, field_name)
);

-- ----------------------------------------------------------------- photos --

CREATE TABLE photos (
  id              bigserial PRIMARY KEY,
  item_id         text NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  angle_code      text REFERENCES photo_angles(code),
  sort_order      smallint NOT NULL DEFAULT 0,
  -- true = generated catalogue render, NOT a photograph of the actual garment.
  -- The app must never present one as a real photo of the item.
  is_render       boolean NOT NULL DEFAULT false,
  source_folder   text NOT NULL,
  source_filename text NOT NULL,
  stored_path     text NOT NULL,          -- relative to PHOTO_STORE
  thumb_path      text,
  width           integer,
  height          integer,
  bytes           bigint,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (item_id, source_folder, source_filename)
);

CREATE INDEX photos_item_idx ON photos (item_id, sort_order);

CREATE TRIGGER photos_updated_at BEFORE UPDATE ON photos
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ---------------------------------------------------------------- outfits --

CREATE TABLE outfits (
  id                bigserial PRIMARY KEY,
  slug              text NOT NULL UNIQUE,
  name              text NOT NULL,
  register_code     text NOT NULL REFERENCES registers(code),
  rationale         text,
  hidden_by_default boolean NOT NULL DEFAULT false,   -- the roll-neck look
  vetted            boolean NOT NULL DEFAULT true,    -- hand-reasoned vs generated
  sort_order        smallint NOT NULL DEFAULT 100,
  created_at        timestamptz NOT NULL DEFAULT now(),
  updated_at        timestamptz NOT NULL DEFAULT now()
);

CREATE TRIGGER outfits_updated_at BEFORE UPDATE ON outfits
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Ordered slots, not four fixed columns: a look can be top + mid-layer +
-- trouser + shoe + belt + outer, and sometimes two tops (cardigan over polo).
CREATE TABLE outfit_items (
  id           bigserial PRIMARY KEY,
  outfit_id    bigint NOT NULL REFERENCES outfits(id) ON DELETE CASCADE,
  item_id      text NOT NULL REFERENCES items(id),
  slot_role    text NOT NULL,             -- top | mid-layer | outer | trouser | shoe | belt
  position     smallint NOT NULL,
  is_alternate boolean NOT NULL DEFAULT false,   -- the "or the Ecco sneaker" options
  note         text,
  UNIQUE (outfit_id, item_id, slot_role)
);

CREATE INDEX outfit_items_outfit_idx ON outfit_items (outfit_id, position);

-- --------------------------------------------------------------- wear log --

CREATE TABLE wear_events (
  id         bigserial PRIMARY KEY,
  worn_on    date NOT NULL,
  outfit_id  bigint REFERENCES outfits(id),      -- NULL = an ad-hoc combination
  context    text,
  temp_c     numeric(4,1),
  rain       boolean,
  rating     smallint CHECK (rating BETWEEN 1 AND 10),
  note       text,
  tweak      text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX wear_events_worn_on_idx ON wear_events (worn_on DESC);

CREATE TRIGGER wear_events_updated_at BEFORE UPDATE ON wear_events
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- item_id is nullable on purpose: the 17 Aug entry includes a plain tee that
-- has never been catalogued. Uncatalogued garments are recorded as free text.
CREATE TABLE wear_event_items (
  id            bigserial PRIMARY KEY,
  wear_event_id bigint NOT NULL REFERENCES wear_events(id) ON DELETE CASCADE,
  item_id       text REFERENCES items(id),
  free_text     text,
  is_base_layer boolean NOT NULL DEFAULT false,
  CHECK (item_id IS NOT NULL OR free_text IS NOT NULL)
);

CREATE INDEX wear_event_items_event_idx ON wear_event_items (wear_event_id);
CREATE INDEX wear_event_items_item_idx  ON wear_event_items (item_id);

CREATE TABLE wear_event_photos (
  id            bigserial PRIMARY KEY,
  wear_event_id bigint NOT NULL REFERENCES wear_events(id) ON DELETE CASCADE,
  stored_path   text NOT NULL,
  thumb_path    text,
  sort_order    smallint NOT NULL DEFAULT 0,
  note          text
);

-- ------------------------------------------------------------- app  state --

-- Laundry / availability. App-owned: the catalogue importer never touches it.
CREATE TABLE item_laundry (
  item_id    text PRIMARY KEY REFERENCES items(id) ON DELETE CASCADE,
  state_code text NOT NULL REFERENCES laundry_states(code) DEFAULT 'clean',
  changed_at timestamptz NOT NULL DEFAULT now(),
  note       text
);

CREATE INDEX item_laundry_state_idx ON item_laundry (state_code);

-- Small key/value bag for app preferences (last weather input, etc).
CREATE TABLE app_settings (
  key        text PRIMARY KEY,
  value      text,
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TRIGGER app_settings_updated_at BEFORE UPDATE ON app_settings
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- 015_gaps.sql — the Gaps tab: what isn't in the wardrobe, and what would fix it.
--
-- Numbered 015 because 014 was used twice (014_fit_gone and 014_fits_bomber).
--
-- data/gaps.json is SEED DATA, not the store. The cards carry state the user
-- changes — status, and links pasted into the card — so the database is the
-- store and the importer refreshes only the authored fields. Same rule as fits:
-- the importer is the write path and never overwrites what Max set.
--
-- `unlocks` is authored prose and stays text. It is a claim about the closet
-- made at authoring time, deliberately NOT derived from fit_items at render
-- time — a derived version would drift and start lying.

CREATE TABLE gaps (
  id                text PRIMARY KEY,               -- 'g01'
  category          text NOT NULL,                  -- Trousers | Tops | Shoes | Belts | Knitwear
  priority          text NOT NULL,                  -- high | medium | low
  status            text NOT NULL DEFAULT 'open',   -- open | bought | not_a_gap
  status_changed_at timestamptz,
  title             text NOT NULL,
  rationale         text,
  unlocks           text,
  spec              text,
  size              text,
  budget            text,
  image_path        text,
  image_is_placeholder boolean NOT NULL DEFAULT true,
  sort_order        smallint NOT NULL DEFAULT 100,
  created_at        timestamptz NOT NULL DEFAULT now(),
  updated_at        timestamptz NOT NULL DEFAULT now(),
  CHECK (priority IN ('high', 'medium', 'low')),
  CHECK (status IN ('open', 'bought', 'not_a_gap'))
);

COMMENT ON COLUMN gaps.status IS
  'App-owned. The importer must never write this, or status_changed_at.';
COMMENT ON COLUMN gaps.unlocks IS
  'Authored prose, never computed. A claim made when the gap was written.';
COMMENT ON COLUMN gaps.image_is_placeholder IS
  'True while the image is a flat spec illustration rather than a product shot. '
  'The flag is what makes swapping in real photography a data change, not a code change.';

-- The BUY AT line: retailer names, in the order they were authored.
CREATE TABLE gap_buy_at (
  gap_id     text NOT NULL REFERENCES gaps(id) ON DELETE CASCADE,
  retailer   text NOT NULL,
  sort_order smallint NOT NULL DEFAULT 0,
  PRIMARY KEY (gap_id, retailer)
);

-- Specific products. Seeded AND user-added: a row added_by 'user' is the user's
-- and the importer never touches it.
CREATE TABLE gap_candidates (
  id         bigserial PRIMARY KEY,
  gap_id     text NOT NULL REFERENCES gaps(id) ON DELETE CASCADE,
  name       text NOT NULL,
  source     text,                              -- 'meermin.es', 'Oxford, in store'
  url        text,
  -- Text, not numeric, and usually NULL: the seed data carries no verified
  -- price and must not invent one. Render an empty price blank, never as $0.
  price      text,
  added_by   text NOT NULL DEFAULT 'import',    -- import | user
  created_at timestamptz NOT NULL DEFAULT now(),
  CHECK (added_by IN ('import', 'user'))
);

CREATE INDEX gap_candidates_gap_idx ON gap_candidates (gap_id);

-- What buying this would retire. A join table rather than the single
-- `replaces_item_id` column the handoff sketched, because the authored content
-- needs more than one: g12 replaces two knits and g13 replaces two polos.
-- A column would have silently dropped the second id in each pair.
CREATE TABLE gap_replaces (
  gap_id  text NOT NULL REFERENCES gaps(id) ON DELETE CASCADE,
  item_id text NOT NULL REFERENCES items(id),
  PRIMARY KEY (gap_id, item_id)
);

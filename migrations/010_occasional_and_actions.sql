-- 010_occasional_and_actions.sql — the 2026-08-27 export, rev 4.
--
-- Three things the catalogue grew that the schema had nowhere to put.

-- 1. A third scope. Wearable and in scope, but not part of the daily rotation:
--    the four print shirts. This is one INSERT precisely because scope was
--    built as a lookup table rather than a Postgres enum.
INSERT INTO scopes (code, label) VALUES ('occasional', 'Occasional');

-- 2. A garment can need a job doing to it. The export carries this as three
--    columns on one item; several more items need one, so it is a table.
--    Same shape as fit_preconditions, which blocks a fit rather than a garment.
CREATE TABLE item_actions (
  id         bigserial PRIMARY KEY,
  item_id    text NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  required   text NOT NULL,             -- DRY CLEAN, COLLAR TREATMENT, …
  status     text NOT NULL DEFAULT 'pending'
             CHECK (status IN ('pending', 'booked', 'done', 'dropped')),
  note       text,
  created_at timestamptz NOT NULL DEFAULT now(),
  done_at    timestamptz,
  UNIQUE (item_id, required)
);

CREATE INDEX item_actions_open_idx ON item_actions (item_id) WHERE status <> 'done';

-- 3. A fit can exist as a render whose garment list is genuinely lost. Eight of
--    them: designed and rendered on 2026-08-27, composition compacted away with
--    the session. The render is real, the item list is unknown, and a list
--    inferred from the filename would be a guess indistinguishable from a fact
--    six months from now. So: no items, and the fit says so.
ALTER TABLE fits ADD COLUMN composition_known boolean NOT NULL DEFAULT true;

COMMENT ON COLUMN fits.composition_known IS
  'False when only the render survives. The UI must say "composition to '
  'confirm" rather than showing an empty fit as though it were complete.';

-- 4. The export groups fits by a taxonomy of its own — cold / warm / casual /
--    smart — which is not the same axis as register (everyday / sharp). Both
--    are useful, so both are kept.
CREATE TABLE fit_categories (
  code       text PRIMARY KEY,
  label      text NOT NULL,
  sort_order smallint NOT NULL DEFAULT 100
);

INSERT INTO fit_categories (code, label, sort_order) VALUES
  ('cold',   'Cold',   10),
  ('warm',   'Warm',   20),
  ('casual', 'Casual', 30),
  ('smart',  'Smart',  40);

ALTER TABLE fits ADD COLUMN category_code text REFERENCES fit_categories(code);

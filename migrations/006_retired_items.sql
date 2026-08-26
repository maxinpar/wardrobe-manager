-- 006_retired_items.sql — an item can leave the catalogue without being destroyed.
--
-- rev 2 of the 2026-08-26 patch removed trousers_00_decathlon-stone: it was a
-- phantom, the same Decathlon chino logged twice. The importer must be able to
-- follow that, but deleting rows is the wrong mechanism — the item may already
-- be referenced by a fit, a wear event, or a laundry state, and a wear event is
-- a record of something that actually happened.
--
-- So an id that disappears from wardrobe.json is RETIRED, never deleted:
-- excluded from the catalogue, the picker and the export, kept on disk with the
-- date it went, and reversible by clearing one column.

ALTER TABLE items ADD COLUMN retired_at timestamptz;
ALTER TABLE items ADD COLUMN retired_note text;

CREATE INDEX items_live_idx ON items (cat_code) WHERE retired_at IS NULL;

COMMENT ON COLUMN items.retired_at IS
  'Set when the id vanishes from wardrobe.json. The row and everything '
  'referencing it stay; the item is simply no longer part of the catalogue.';

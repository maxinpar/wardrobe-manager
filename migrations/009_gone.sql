-- 009_gone.sql — binned, as in physically gone.
--
-- Distinct from the `Bin` verdict, which is an audit judgement: "this should
-- go". This is the fact that it has gone. The design is explicit that the two
-- are different concepts and that conflating them is the trap.
--
-- Also distinct from `retired_at`, which means the id left wardrobe.json — a
-- catalogue correction, not a decision about a garment.
--
-- A binned garment leaves the closet grid and stops being offered, but nothing
-- is deleted: it keeps its wear history, stays in the fits that use it (which
-- are marked as needing a substitute), and comes back by clearing one column.

ALTER TABLE items ADD COLUMN gone_at timestamptz;

CREATE INDEX items_gone_idx ON items (gone_at) WHERE gone_at IS NOT NULL;

COMMENT ON COLUMN items.gone_at IS
  'Set when the garment is physically gone. Not the Bin verdict, which is only '
  'an opinion that it should go. Reversible: clear it and the garment returns.';

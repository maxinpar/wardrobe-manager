-- 014_fit_gone.sql — binning a fit.
--
-- The same idea as items.gone_at (009), one level up. A fit is binned because
-- you don't want it any more, or because the garments it was built on have
-- gone. Either way it is a decision, not a derivation: nothing computes this
-- and no import may set it.
--
-- Distinct from `hidden_by_default`, which is a standing preference about a
-- shape you rarely reach for (the roll-neck) — that fit is still a fit, and one
-- chip brings it back. A binned fit is out.
--
-- Nothing is deleted. The composition, the render, the score and every wear
-- event stay exactly as they were, and clearing one column brings it back.

ALTER TABLE fits ADD COLUMN gone_at timestamptz;

CREATE INDEX fits_gone_idx ON fits (gone_at) WHERE gone_at IS NOT NULL;

COMMENT ON COLUMN fits.gone_at IS
  'Set when the fit is binned — no longer wanted, or built on garments that '
  'have gone. Reversible: clear it and the fit returns. Never set by an import.';

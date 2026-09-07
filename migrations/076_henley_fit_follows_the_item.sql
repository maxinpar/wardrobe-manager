-- 076_henley_fit_follows_the_item.sql — the henley fit catches up with the henley.
--
-- 075 added `work` to tees_15_adidas-grey-henley, because Max says he wears it
-- to the office. It did not update the FIT built on that garment, and a fit's
-- occasions are stored rows rather than a live read — so fit_bc_grey-henley
-- went on claiming casual-only while the garment inside it had moved on.
--
-- Nothing was broken by that: the picker scores on weather, not occasion, so
-- black_canvas already rotated five deep. What it got wrong was what it SAID —
-- the gallery's "good for" line and the occasion filter chips both read the fit,
-- so position 5 of the set was filed under casual and nowhere near work.
--
-- `derived`, not `manual`. The garment's work tag is Max's own statement and 075
-- recorded it as manual. This is the ordinary consequence of that statement,
-- recomputed with wardrobe/fit_derive.py — good_for over the fit's five garments
-- now returns ['work', 'casual'] — so it stays derived and an import may
-- recompute it freely.

INSERT INTO fit_occasions (fit_id, occasion_code, kind)
VALUES ('fit_bc_grey-henley', 'work', 'good')
ON CONFLICT DO NOTHING;

UPDATE fit_field_sources
   SET note = 'Re-derived after the henley gained a work occasion — '
              'brief-shawl-set-and-henley.md 2026-09-07'
 WHERE fit_id = 'fit_bc_grey-henley' AND field_name = 'good_for';

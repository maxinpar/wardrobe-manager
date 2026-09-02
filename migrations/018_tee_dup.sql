-- 018_tee_dup.sql
-- tees_18 was a duplicate of tees_20: "somb" and "zomb" in the source folder are the same
-- black KICKASSS Biarritz tee, shot worn-front twice and worn-side/flat/label separately.
-- Its two worn-front frames are refiled under the tees_20 prefix, so nothing is lost -
-- tees_20 previously had no front view.
-- Also: the graphic is a ZOMBIE, confirmed by Max 2026-08-30. Earlier notes calling it a
-- lobster were wrong; the render is correct.

DELETE FROM item_occasions   WHERE item_id = 'tees_18_black-small-graphic';
DELETE FROM item_field_sources WHERE item_id = 'tees_18_black-small-graphic';
DELETE FROM item_laundry     WHERE item_id = 'tees_18_black-small-graphic';
DELETE FROM photos           WHERE item_id = 'tees_18_black-small-graphic';
DELETE FROM items            WHERE id      = 'tees_18_black-small-graphic';

UPDATE items SET
  notes = 'KICKASSS Biarritz, "Limited Edition Series". Black ground. Print: a zombie figure in grey with pink accents, a golf club and flag below it, and a pink text block reading "F*CK SURF PLAY GOLF / KICK ASSS". Confirmed by Max 2026-08-30.',
  updated_at = now()
WHERE id = 'tees_20_kickasss-lobster';

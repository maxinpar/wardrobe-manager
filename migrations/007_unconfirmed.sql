-- 007_unconfirmed.sql — a garment can be catalogued without being verified.
--
-- The five crew tees added on 2026-08-26 are the first items in the catalogue
-- that exist only as a description and a generated render. Their colour was
-- measured off the render, but nobody has photographed the actual garment, so
-- fit, condition and material are still guesses.
--
-- `no_photo` alone can't carry that: a garment sharing a group shot also has
-- no photo of its own but has been seen. `unconfirmed` says the record itself
-- has not been checked against the thing.

ALTER TABLE items ADD COLUMN unconfirmed boolean NOT NULL DEFAULT false;

COMMENT ON COLUMN items.unconfirmed IS
  'The record has never been checked against the physical garment. Set on '
  'items catalogued from a description; cleared once one is photographed.';

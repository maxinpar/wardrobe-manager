-- 019_henley_core.sql
-- tees_15 promoted from 'out' to 'core' by Max, 2026-08-30, after confirming the garment in
-- hand: long sleeve, button placket, chest pocket and shoulder epaulettes. The epaulettes and
-- pocket are what settle it - they give it enough construction to read as a shirt rather than
-- as loungewear, which was the open question when it was catalogued from a photo.
-- Weekend slot. Eligible for casual fits.

UPDATE items SET
  scope_code = 'core',
  formality_rank = 2,
  verdict_note = 'Keep. The only unprinted, non-sport garment in the tee folder and the only long sleeve. Button placket, chest pocket and shoulder epaulettes give it real construction - it is a shirt-weight layer, not a lounge top. Weekend wear.',
  works_alone = true,
  pairs = 'Indigo jeans, black coated jeans, stone chino. Brown or black leather both work - grey is neutral. Under the brown leather bomber or the navy sherpa fleece.',
  layer = 'Worn alone as the top layer, or under a jacket. Not a base layer under a knit - the placket and collar fight a V-neck.',
  avoid = 'Anything smart. Grey knitwear over the top - tonal collapse.',
  updated_at = now()
WHERE id = 'tees_15_adidas-grey-henley';

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('tees_15_adidas-grey-henley','weekend'),
('tees_15_adidas-grey-henley','casual')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('tees_15_adidas-grey-henley','scope_code','manual',
 'Promoted out -> core by Max 2026-08-30 on the strength of the epaulettes and pocket, having handled the garment. The catalogue entry had deliberately left this undecided.')
ON CONFLICT DO NOTHING;

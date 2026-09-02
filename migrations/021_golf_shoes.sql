-- 021_golf_shoes.sql
-- Eleven pairs photographed 2026-08-30 and filed under shoes_10..shoes_20.
-- All are golf or sport footwear. Scope 'out' throughout: catalogued and searchable, tagged
-- golf or gym, never offered by the fit picker - the same treatment as shoes_09a, the Nike
-- running trainer.
-- Brand reads come from insole and tongue labels where legible; where a label was not
-- photographed or is unreadable the field says so rather than guessing.

INSERT INTO items (id, slug, cat_code, name, colour, material, cut, formality_raw, formality_rank,
                   fit, condition, verdict_code, verdict_note, scope_code, works_alone,
                   pairs, layer, avoid, notes, no_photo, photo_prefix, retail_prefix,
                   rain_unsafe, pattern, unconfirmed) VALUES

('shoes_10_inesis-red-worn','inesis-red-worn','Shoes','Inesis red golf shoe, worn pair',
 'Strawberry red','Mesh and synthetic upper, spiked outsole','Athletic','Sport',1,'EU44','Used - scuffed toes, marked upper, grubby white midsole. Spikes worn but present',
 'Keep','In-play pair. Worn on course 2026-08-30. One of two identical red Inesis pairs - this is the used one.',
 'out',true,'Golf.','-','Anything off the course.',
 'Decathlon Inesis. Spiked outsole with replaceable soft spikes, INESIS moulded into the arch. Second identical pair kept new - see shoes_11.',
 false,'shoes_10_inesis-red-worn','shoes_10_inesis-red-worn',false,'Plain',true),

('shoes_11_inesis-red-new','inesis-red-new','Shoes','Inesis red golf shoe, new pair',
 'Strawberry red','Mesh and synthetic upper, spiked outsole','Athletic','Sport',1,'EU44','New - price tag still attached, spikes unworn, midsole clean',
 'Keep','The spare. Identical model to shoes_10, kept new for when that pair goes.',
 'out',true,'Golf.','-','Anything off the course.',
 'Decathlon Inesis, tag still on. Same model as shoes_10.',
 false,'shoes_11_inesis-red-new','shoes_11_inesis-red-new',false,'Plain',true),

('shoes_12_inesis-teal-jf100','inesis-teal-jf100','Shoes','Inesis JF100 golf shoe, teal',
 'Teal / blue-grey with cream midsole','Mesh upper, spikeless outsole','Athletic','Sport',1,'EU44','Used - grass in the tread, midsole soiled',
 'Keep','Spikeless golf shoe, JF100 GRIP printed on the midsole.','out',
 true,'Golf.','-','Off the course.',
 'Decathlon Inesis. "JF100 GRIP" on the midsole. Spikeless lugged outsole in black and lime, marked NON MARKING.',
 false,'shoes_12_inesis-teal-jf100','shoes_12_inesis-teal-jf100',false,'Plain',true),

('shoes_13_inesis-cream-blue','inesis-cream-blue','Shoes','Inesis golf shoe, cream and blue',
 'Cream with royal blue panel','Synthetic upper, spiked outsole','Athletic','Sport',1,'EU44','Used - spikes worn, sole yellowing',
 'Keep','Spiked golf shoe. INESIS moulded into the arch of the outsole.','out',
 true,'Golf.','-','Off the course.',
 'Decathlon Inesis. Cream outsole with replaceable soft spikes and black traction pads.',
 false,'shoes_13_inesis-cream-blue','shoes_13_inesis-cream-blue',false,'Plain',true),

('shoes_14_kalenji-olive','kalenji-olive','Shoes','Kalenji running shoe, olive',
 'Olive / khaki mesh with teal outsole','Mesh upper, EVA and rubber outsole','Athletic','Sport',1,'EU44','Used',
 'Keep','NOT a golf shoe - the outsole carries the Kalenji logo, so this is a Decathlon running shoe. Catalogued with the golf batch because it was shot with them.',
 'out',true,'Running, gym.','-','Golf - no traction for a swing. And anything smart.',
 'Kalenji (Decathlon running). Teal forefoot, dark grey heel, running tread.',
 false,'shoes_14_kalenji-olive','shoes_14_kalenji-olive',false,'Plain',true),

('shoes_15_inesis-cream-yellow-jf190','inesis-cream-yellow-jf190','Shoes','Inesis JF190 golf shoe, cream and yellow',
 'Cream with yellow accents','Mesh and synthetic upper, spikeless outsole','Athletic','Sport',1,'EU44','Used',
 'Keep','Spikeless golf shoe, JF190 GRIP printed on the midsole - a step up from the JF100.','out',
 true,'Golf.','-','Off the course.',
 'Decathlon Inesis. "JF190 GRIP" on the midsole. Black and yellow-green lugged outsole, NON MARKING.',
 false,'shoes_15_inesis-cream-yellow-jf190','shoes_15_inesis-cream-yellow-jf190',false,'Plain',true),

('shoes_16_navy-lime-spiked','navy-lime-spiked','Shoes','Spiked golf shoe, navy and lime',
 'Dark navy mesh with lime green','Mesh upper, spiked outsole','Athletic','Sport',1,'EU44','Used',
 'Keep','Spiked golf shoe with a bright green outsole.','out',
 true,'Golf.','-','Off the course.',
 'Brand not established - the insole label photographed reads only a size code and MADE IN CHINA. Green outsole with replaceable soft spikes.',
 false,'shoes_16_navy-lime-spiked','shoes_16_navy-lime-spiked',false,'Plain',true),

('shoes_17_skechers-grey-spikeless','skechers-grey-spikeless','Shoes','Skechers Go Golf, grey',
 'Mid grey with white midsole','Mesh and synthetic upper, spikeless outsole','Athletic','Sport',1,'EU44','Used - good',
 'Keep','Spikeless. The insole carries the Skechers Goga Mat / air-cooled branding, so this is a Skechers Go Golf.',
 'out',true,'Golf. Of all the golf shoes this is the one closest to passing as a normal trainer.','-','Smart wear.',
 'Skechers, made in China, size 44. Black spikeless outsole.',
 false,'shoes_17_skechers-grey-spikeless','shoes_17_skechers-grey-spikeless',false,'Plain',true),

('shoes_18_grey-orange-spiked','grey-orange-spiked','Shoes','Spiked golf shoe, grey and orange',
 'Grey with orange detail','Mesh and synthetic upper, spiked outsole','Athletic','Sport',1,'EU44','Used',
 'Keep','Spiked golf shoe, white outsole with orange traction pads.','out',
 true,'Golf.','-','Off the course.',
 'Decathlon label photographed but the model line is not legible in the frame. White outsole with orange pads and replaceable soft spikes.',
 false,'shoes_18_grey-orange-spiked','shoes_18_grey-orange-spiked',false,'Plain',true),

('shoes_19_inesis-jf100-1-grey','inesis-jf100-1-grey','Shoes','Inesis JF100.1 M, grey/orange',
 'Grey and white with yellow-green outsole','Mesh upper, spikeless outsole','Athletic','Sport',1,'EU44 / UK 9.5 / US 10','Good',
 'Keep','Max''s call 2026-08-30: he will likely NOT use this for golf - the sole is thin and it behaves more like a gym shoe than a golf shoe. Kept as a gym/casual sport shoe.',
 'out',true,'Gym.','-','Golf - Max has ruled it out on the sole. And smart wear.',
 'Decathlon label: "JF100.1 M GREY ORANGE", made in Vietnam, EU44 / UK9.5 / US10, model code 8735470. Spikeless black and yellow-green outsole, NON MARKING.',
 false,'shoes_19_inesis-jf100-1-grey','shoes_19_inesis-jf100-1-grey',false,'Plain',true),

('shoes_20_nike-yellow-trail','nike-yellow-trail','Shoes','Nike trail shoe, yellow and cream',
 'Yellow and cream with black','Mesh upper, lugged rubber outsole','Athletic','Sport',1,'EUR44 / UK9 / US10','Used - grass in the tread',
 'Keep','NOT a golf shoe - a Nike trail/running shoe.','out',
 true,'Running, gym.','-','Golf. And anything smart.',
 'Nike, style code FV3929-700, EUR44. Black and yellow lugged trail outsole.',
 false,'shoes_20_nike-yellow-trail','shoes_20_nike-yellow-trail',false,'Plain',true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO item_occasions (item_id, occasion_code) VALUES
('shoes_10_inesis-red-worn','golf'),('shoes_11_inesis-red-new','golf'),
('shoes_12_inesis-teal-jf100','golf'),('shoes_13_inesis-cream-blue','golf'),
('shoes_15_inesis-cream-yellow-jf190','golf'),('shoes_16_navy-lime-spiked','golf'),
('shoes_17_skechers-grey-spikeless','golf'),('shoes_18_grey-orange-spiked','golf'),
('shoes_14_kalenji-olive','gym'),('shoes_19_inesis-jf100-1-grey','gym'),
('shoes_20_nike-yellow-trail','gym')
ON CONFLICT DO NOTHING;

INSERT INTO item_field_sources (item_id, field_name, source, note)
SELECT id, 'verdict_code', 'manual',
       'Catalogued 2026-08-30 from Max''s own photos. Scope out throughout - sport footwear, tagged golf or gym, deliberately kept out of the fit picker.'
FROM items WHERE id >= 'shoes_10' AND id < 'shoes_21'
ON CONFLICT DO NOTHING;

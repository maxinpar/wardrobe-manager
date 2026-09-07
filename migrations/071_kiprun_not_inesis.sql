-- 071_kiprun_not_inesis.sql
-- 2026-09-06. Three shoes catalogued as Inesis golf shoes are Kiprun RUNNING shoes.
--
-- Established by reading the midsoles and labels in the source frames, which had never been
-- opened. All three carry the Kiprun swoosh, a KIPRUN tongue tab and a running tread; none has
-- a golf outsole. Max plays golf in running shoes deliberately, so the occasion tags are right
-- and only the identity is wrong.
--
--   shoes_12  midsole reads JF190 GRIP  -> Kiprun JF 190 Grip, Blue          (was "Inesis JF100 teal")
--   shoes_15  midsole reads JF190 GRIP  -> Kiprun JF 190 Grip, Cotton White  (was "Inesis JF190 cream and yellow")
--   shoes_19  midsole reads JF 100.1    -> Kiprun JF 100.1, grey/orange      (was "Inesis JF100.1 M")
--
-- shoes_12 and shoes_15 ARE THE SAME MODEL in two colourways. Filed under names that hid it,
-- which on 2026-09-06 led to a shopping recommendation for the Cotton White - a shoe Max already
-- owns. That is the cost of a wrong name and the reason for this migration.
--
-- shoes_13_inesis-cream-blue IS GENUINELY INESIS and genuinely golf: INESIS on the heel and
-- tongue, and a spiked golf outsole in the underside frame. Left untouched.
--
-- IDS AND PHOTO PREFIXES ARE NOT CHANGED. They are stamped into ~18 filenames on Drive; renaming
-- them buys nothing and risks orphaning photo rows. The slugs still read "inesis" and are now
-- simply historical. Names, colours and notes carry the truth.
--
-- CURRENT AVAILABILITY, Decathlon Australia, checked 2026-09-06, all EU44:
--   Blue         ref 8913912  $62.99  OUT OF STOCK online
--   Cotton white ref 8913911  $44.99  EU46 only
--   Full black   ref 8883621  $62.99  in stock   - Max looked and rejected it, "boring"
--   Black/yellow ref 8841282  $62.99  low stock
-- Max is buying another blue pair. No other golf shoe is being bought: eleven pairs already
-- cover every colour family he wants.

UPDATE items SET
    name = 'Kiprun JF 190 Grip, blue',
    colour = 'Petrol blue and navy with a white midsole and lime forefoot',
    material = 'Engineered mesh upper, rubber lugged outsole',
    cut = 'Road and trail running shoe',
    verdict_note = 'Worn for golf by choice, not a golf shoe. Max''s favourite of the running-shoe pairs and the one he is replacing like for like.',
    notes = 'DECATHLON KIPRUN JF 190 GRIP, blue - reference 8913912, about A$62.99. "JF190 GRIP" printed on the midsole, Kiprun swoosh on the quarter, KIPRUN tab on the tongue, running tread with a lime forefoot. NOT an Inesis golf shoe: catalogued as "Inesis JF100 teal" until 2026-09-06, when the midsole was actually read. Same model as shoes_15, different colourway.',
    unconfirmed = false
WHERE id = 'shoes_12_inesis-teal-jf100';

UPDATE items SET
    name = 'Kiprun JF 190 Grip, cotton white',
    colour = 'Cotton white and sand with a lime forefoot and black outsole',
    material = 'Engineered mesh upper, rubber lugged outsole',
    cut = 'Road and trail running shoe',
    verdict_note = 'Worn for golf by choice, not a golf shoe. One of the pale pairs in the golf rotation.',
    notes = 'DECATHLON KIPRUN JF 190 GRIP, cotton white - reference 8913911. "JF190 GRIP" printed on the midsole. NOT an Inesis golf shoe, and not "cream and yellow": catalogued that way until 2026-09-06, when the midsole and upper were actually read. SAME MODEL as shoes_12 in a different colourway - the two were filed under names that made them look unrelated.',
    unconfirmed = false
WHERE id = 'shoes_15_inesis-cream-yellow-jf190';

UPDATE items SET
    name = 'Kiprun JF 100.1, grey and orange',
    colour = 'Grey and white with orange perforations and a white midsole',
    material = 'Mesh upper, rubber outsole',
    cut = 'Road running shoe',
    notes = 'DECATHLON KIPRUN JF 100.1 M, grey/orange, EU44 - read off the midsole print and the size label in the source frames. NOT an Inesis golf shoe: catalogued as "Inesis JF100.1 M" until 2026-09-06. A different, plainer model from the JF 190 Grip pairs (shoes_12 and shoes_15).',
    unconfirmed = false
WHERE id = 'shoes_19_inesis-jf100-1-grey';

INSERT INTO item_field_sources (item_id, field_name, source, note) VALUES
('shoes_12_inesis-teal-jf100','name','imported','Midsole reads JF190 GRIP; Kiprun branding on quarter and tongue. Read from source frames 2026-09-06.'),
('shoes_15_inesis-cream-yellow-jf190','name','imported','Midsole reads JF190 GRIP. Read from source frames 2026-09-06.'),
('shoes_19_inesis-jf100-1-grey','name','imported','Midsole reads JF 100.1; size label reads JF100.1 M GREY ORANGE, EU44. Read from source frames 2026-09-06.');

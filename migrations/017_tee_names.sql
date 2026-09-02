-- 017_tee_names.sql
-- The renders of 2026-08-30 made the prints legible for the first time and several
-- catalogue descriptions written from mirrored selfies were wrong. Names and notes
-- corrected here; ids and photo prefixes are deliberately left alone so the 57 filed
-- photos and the retail renders keep resolving.

UPDATE items SET name='Sailor tee, sand',
  notes='Sand ground. Print: a pipe-smoking sailor above a ship''s wheel, in a single dark tonal ink. Small red woven tab on the sleeve. Catalogued as "anchor print" from a mirrored selfie - the render shows a sailor and a wheel.',
  pattern='Print', updated_at=now() WHERE id='tees_06_sand-anchor-print';

UPDATE items SET name='Belgium beer tee',
  colour='Black',
  notes='Black ground. Print: a foaming beer stein above the word BELGIUM in orange, with a small line of text beneath. Catalogued as a "preserve jar" from a mirrored selfie - it is a beer mug.',
  pattern='Print', updated_at=now() WHERE id='tees_07_preserve-jar-graphic';

UPDATE items SET name='Biz Invoice tee, black',
  notes='RAMO promotional blank, size L. Print in white: "Biz Invoice" with the strapline "Less time on admin, more time for business".',
  updated_at=now() WHERE id='tees_08_ramo-black-biz';

UPDATE items SET name='Biz Invoice tee, red',
  notes='RAMO "Be your own brand" label, size M. Print in white: "Biz Invoice bi" with the strapline "invoicing made easy" - a different strapline from the black one.',
  updated_at=now() WHERE id='tees_09_ramo-red-biz';

UPDATE items SET name='Give Me Birdies golf tee',
  notes='COOL GOLF / OZ COOL DRY, 50% cotton 45% polyester, size M. Print: a circular badge reading "GIVE ME BIRDIES OR GIVE ME DEATH" around a solid black bird.',
  updated_at=now() WHERE id='tees_10_coolgolf-red-badge';

UPDATE items SET name='Bretagne tee',
  notes='"Quality Cotton" label, size M. Washed black. Print in white: "Bretagne" in script above a fine line drawing of a lighthouse and a boat.',
  updated_at=now() WHERE id='tees_11_bretagne-black';

UPDATE items SET name='DOOM tee',
  notes='Fruit of the Loom blank, size L. Print: the DOOM video-game logo in red and gold gothic lettering over a figure and demons. Catalogued as a band tee before the print was legible - it is the game.',
  updated_at=now() WHERE id='tees_12_fruit-band-tee';

UPDATE items SET name='France FFF jersey',
  notes='adidas. White polyester piqué football jersey, royal blue and red collar and sleeve trim, adidas logo on the left chest, embroidered FFF cockerel crest with a star above it on the right chest. France national team.',
  updated_at=now() WHERE id='tees_13_adidas-sport-jersey';

UPDATE items SET name='La Fraise graphic tee, red',
  notes='American Apparel body, red. Print: a small stacked colour illustration at centre chest in yellow, cream and dark red.',
  updated_at=now() WHERE id='tees_14_american-apparel-la-fraise';

UPDATE items SET name='Grey henley, long sleeve',
  notes='adidas. Mid heather grey. Short button placket, no collar, plus a chest pocket and shoulder epaulettes - more detail than a plain henley. Long sleeve.',
  updated_at=now() WHERE id='tees_15_adidas-grey-henley';

UPDATE items SET name='Vote For Pedro ringer tee',
  colour='Green with darker green ringer trim',
  notes='"Standard American" label. Green ringer tee - contrast darker green collar and cuff bindings. Print in red: "VOTE FOR PEDRO", three lines, centred. Napoleon Dynamite.',
  pairs='Indigo jeans, black coated jeans, stone chino. The olive Air Max picks up the green.',
  updated_at=now() WHERE id='tees_16_standard-american-olive';

UPDATE items SET name='Ninja Turtles four-panel tee',
  notes='Charcoal / washed black. Print: a four-panel grid of Teenage Mutant Ninja Turtles portraits on a distressed cream ground.',
  updated_at=now() WHERE id='tees_19_four-panel-photo';

UPDATE items SET name='KICKASSS zombie tee',
  notes='KICKASSS Biarritz, "Limited Edition Series". Black ground. Print: a tall zombie figure in grey with small red accents. Catalogued as a lobster from a dark flat-lay - the render shows a figure.',
  updated_at=now() WHERE id='tees_20_kickasss-lobster';

-- ids and photo_prefix values are intentionally not renamed: 57 filed photos and 13 retail
-- renders resolve by prefix, and a rename would orphan all of them.

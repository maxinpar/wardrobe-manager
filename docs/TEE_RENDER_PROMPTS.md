# Gemini prompts — tee retail renders

**Read this first.** Your source photos are mirror selfies, so every word and graphic on them is
**backwards**. I have un-mirrored all 40 worn/detail frames — they are in
`Wardrobe Photos\Retail\_tee-references\` prefixed `UNMIRRORED_`. **Attach those, not the originals.**
Attaching a mirrored photo will produce a render with reversed lettering.

---

## THE RULE THAT MATTERS

Gemini invents text when it cannot read text. That is the failure mode that produced a fabricated
six-language care stamp on `belts_09`. Every prompt below therefore carries this block, and it is
not optional:

```
CRITICAL — REPRODUCE THE GRAPHIC EXACTLY FROM THE ATTACHED REFERENCE.
The chest graphic must be copied from the attached photograph: same wording,
same spelling, same typeface, same layout, same colours, same size and same
position on the chest. Do not redraw it in your own style. Do not add, remove,
translate, correct, complete or re-letter any word. Do not add a brand name, a
slogan, a date, a city, or any text that is not visible in the reference. If any
part of the graphic is unclear in the reference, reproduce it as the soft,
worn, partially illegible marking that it is — do NOT invent a legible version.
```

For the five where I could read the print, the exact wording is given below as a **cross-check** —
Gemini should still copy from the image, and the wording is there so you can reject a render that
gets it wrong.

---

## THE BASE PROMPT

```
Product photography for an e-commerce catalogue. A {{GARMENT}} on a pure white
seamless background.

THE ITEM: {{ITEM BLOCK — see per-garment below}}

COMPOSITION: Invisible mannequin — a ghost-mannequin product shot. The garment
is photographed as if worn by an invisible person: filled out with a natural
three-dimensional human shape, chest and shoulders holding their form, front
view, shoulders square, sleeves hanging naturally at a slight angle from the
body. The inner back of the collar is visible through the neck opening. No
mannequin, no person, no body parts, no hanger, no stand. Centred with a
generous even margin.

CRITICAL — REPRODUCE THE GRAPHIC EXACTLY FROM THE ATTACHED REFERENCE.
The chest graphic must be copied from the attached photograph: same wording,
same spelling, same typeface, same layout, same colours, same size and same
position on the chest. Do not redraw it in your own style. Do not add, remove,
translate, correct, complete or re-letter any word. Do not add a brand name, a
slogan, a date, a city, or any text that is not visible in the reference. If any
part of the graphic is unclear in the reference, reproduce it as the soft, worn,
partially illegible marking that it is — do NOT invent a legible version.

CRITICAL — NO INVENTED TEXT ANYWHERE ELSE: no neck label wording, no care
label, no fibre content, no size, no country of origin, no hem tab lettering,
unless it is visible in the reference and described above. If unsure whether
text belongs on a surface, leave that surface blank.

LIGHTING: Soft even diffused studio light from a large overhead softbox with
white fill cards on both sides. No harsh shadows, no cast shadow on the
background, no hotspots. Background pure white #FFFFFF — not grey, not
off-white — seamless and blown fully to white at the edges.

RENDERING: Photorealistic, sharp crisp focus throughout, deep depth of field.
Jersey knit texture and the neck and hem ribbing clearly resolved. Shot as if on
a 100mm macro lens at f/11. Clean commercial catalogue look. STRICTLY SQUARE 1:1
ASPECT RATIO.

DO NOT INCLUDE: people, faces, hands, necks, mannequin heads, hangers, stands,
props, watermarks, coloured or gradient background, drop shadow, reflection.
```

**Print fidelity beats crease policy.** The house style says "no creases", but a printed tee that
has been washed for years is not crisp. For these, replace the freshly-pressed line with:
*"The garment is clean and hangs naturally. Keep the print's real age — a screen print that has
softened, cracked or faded with washing must stay that way. Do not restore, sharpen or re-print it."*

---

## PER-GARMENT BLOCKS

### tees_06 — Sand anchor-print tee ⭐ core
Attach: `UNMIRRORED_tees_06_sand-anchor-print_01_worn-front.jpg`, `_03_detail.jpg`
> Short-sleeve crew-neck cotton t-shirt in **sand / pale stone**. Ribbed crew neckline. Regular fit.
> A **small dark tonal graphic at centre chest** — reproduce it exactly from the reference. A small
> woven tab at the hem.
> **Print not fully legible in the reference — copy it as-is, invent nothing.**

### tees_07 — Orange-script graphic tee
Attach: `UNMIRRORED_tees_07_preserve-jar-graphic_01_worn-front.jpg`
> Short-sleeve crew-neck cotton t-shirt in **dark navy / near-black**. Chest graphic: **orange
> handwritten script** above a **cream and orange illustration of a filled drinking vessel**.
> ⚠️ Script wording not legible at reference resolution — **copy the letterforms exactly as they
> appear, do not resolve them into words.** If you want an accurate render, reshoot this print flat.

### tees_08 — Biz Invoice promo tee, black
Attach: `UNMIRRORED_tees_08_ramo-black-biz_01_worn-front.jpg`, `_03_detail.jpg`
> Short-sleeve crew-neck cotton t-shirt in **black**, size L so it hangs loosely. Chest print in
> **white**: large serif wording **"Biz Invoice"**, with a smaller single-line strapline beneath it.
> **Cross-check: the large words are "Biz Invoice". The strapline is only partly legible — copy it
> from the reference, do not complete it.**

### tees_09 — Biz Invoice promo tee, red
Attach: `UNMIRRORED_tees_09_ramo-red-biz_01_worn-front.jpg`
> Short-sleeve crew-neck cotton t-shirt in **strong red**. Same white chest print as tees_08.
> Copy the print from the reference.

### tees_10 — Cool Golf badge tee, red
Attach: `UNMIRRORED_tees_10_coolgolf-red-badge_01_worn-front.jpg`
> Short-sleeve crew-neck **performance** t-shirt, 50% cotton / 45% polyester, in **red**, with a
> faint sheen. Chest print: a **circular badge outlined in dark red**, the words **"GIVE ME BIRDIES"**
> arced around the upper edge, a **solid black bird silhouette** filling the lower half, and
> **"COOL GOLF"** in small letters at the bottom of the circle.
> **Cross-check wording: "GIVE ME BIRDIES" and "COOL GOLF". Nothing else.**

### tees_11 — Bretagne tee ⭐ core
Attach: `UNMIRRORED_tees_11_bretagne-black_01_worn-front.jpg`
> Short-sleeve crew-neck cotton t-shirt in **washed black**, faded honestly with age. Chest print in
> **white**: the single word **"Bretagne"** in a flowing handwritten script, above a **fine white
> line-drawing**.
> **Cross-check: the word is "Bretagne" — one word, no accent, capital B. The drawing beneath it is
> not fully legible; copy it, do not identify it.**

### tees_12 — Band tee, black
Attach: `UNMIRRORED_tees_12_fruit-band-tee_01_worn-front.jpg`, `_02_worn-front.jpg`
> Short-sleeve crew-neck cotton t-shirt in **washed black**, size L, loose. Chest print: large
> **gold and yellow gothic/blackletter lettering** with an ornamental border beneath.
> ⚠️ **The band name is partly hidden by the phone in every frame. Do not guess it.** Reproduce only
> the visible letterforms. Reshoot this one flat if you want it right.

### tees_13 — adidas sport jersey
Attach: `UNMIRRORED_tees_13_adidas-sport-jersey_01_worn-front.jpg`, `_03_detail.jpg`, `_04_detail.jpg`
> **Not a t-shirt — a short-sleeve football jersey** in **white** polyester piqué. **Royal blue and
> red striped ribbed collar and matching sleeve cuff trim.** **adidas three-stripe logo on the left
> chest.** **An embroidered crest on the right chest with a small star above it.**
> **Reproduce the crest exactly from the reference. Do not substitute a generic badge, do not
> redraw it, and do not add any club, country, sponsor or tournament name.**

### tees_14 — La Fraise tee, red
Attach: `UNMIRRORED_tees_14_american-apparel-la-fraise_01_worn-front.jpg`
> Short-sleeve crew-neck cotton t-shirt in **red**, slim American Apparel cut. **Small centre-chest
> illustration in yellow, cream and dark red.**
> ⚠️ Illustration not legible at reference resolution — copy it, invent nothing.

### tees_15 — adidas grey henley
Attach: `UNMIRRORED_tees_15_adidas-grey-henley_01_worn-front.jpg`
> **Long-sleeve henley** in **mid heather grey** cotton jersey. **Short button placket at the neck
> with three or four buttons**, no collar. Regular fit, ribbed cuffs.
> **No chest print of any kind. Leave the chest completely plain — do not add a logo, a monogram or
> any marking.** *(This is the one garment here with nothing printed on it, so it is the one most
> likely to have a logo hallucinated onto it.)*

### tees_16 — Faded text tee, olive ⭐ core
Attach: `UNMIRRORED_tees_16_standard-american-olive_01_worn-front.jpg`, `_04_detail.jpg`
> Short-sleeve crew-neck cotton t-shirt in **olive green**, with a **darker green ribbed neckline**.
> Chest print: **low-contrast lettering, heavily faded and cracked with washing**, sitting low on the
> chest.
> ⚠️ **Wording not legible. Reproduce it as faded, broken, unreadable lettering — that is what it
> actually looks like. Do not sharpen it into readable words.**

### tees_17 — Broome singlet
Attach: `UNMIRRORED_tees_17_broome-singlet_01_worn-front.jpg`
> **Sleeveless tank top / singlet**, size S, in **washed blue-grey** cotton. Chest print in white and
> dark grey: the word **"BROOME"** arced across the upper chest, above a **circular design containing
> a boab tree**.
> **Cross-check: the word is "BROOME", all capitals. Do not add "Western Australia" or any other
> line unless it is visible in the reference.**

### tees_18 — Small-graphic tee, black
Attach: `UNMIRRORED_tees_18_black-small-graphic_01_worn-front.jpg`, `_02_worn-front.jpg`
> Short-sleeve crew-neck cotton t-shirt in **black**. **Small print high on the left chest in red and
> pale grey.**
> ⚠️ Not legible. Copy it as an indistinct small chest mark. **No neck label was photographed for
> this garment, so put no wording anywhere.**

### tees_19 — Four-panel photo tee
Attach: `UNMIRRORED_tees_19_four-panel-photo_01_worn-front.jpg`, `_03_detail.jpg`
> Short-sleeve crew-neck cotton t-shirt in **charcoal / washed black**. Chest print: a **large
> four-panel grid of photographic images in greyscale**, roughly square, centred.
> ⚠️ The images are not identifiable at reference resolution. **Reproduce the four-panel grid
> layout and its tonal values; do not invent recognisable faces, people or scenes inside the panels.**

### tees_20 — KICKASSS lobster tee
Attach: `UNMIRRORED_tees_20_kickasss-lobster_02_detail.jpg`, `_01_worn-side.jpg`
> Short-sleeve crew-neck cotton t-shirt in **dark charcoal**. Chest print: a **large lobster or
> crayfish rendered in pale grey with small red-orange accents**, laid across the chest.
> Brand is **KICKASSS Biarritz** but **the brand name is on the neck label, not on the chest — do
> not print it on the front.**

---

## Filing

`Wardrobe Photos\Retail\<id>_retail.<ext>` — e.g. `tees_11_bretagne-black_retail.jpg`. Send me the
folder and I'll file and index them.

## Worth doing first

Five prints are illegible even un-mirrored: **tees_06, tees_07, tees_12, tees_14, tees_16**, plus the
faces inside tees_19. For those, the render can only ever be a guess dressed up as a photo. **Two
minutes each with the shirt laid flat and the print filling the frame** would fix all of them, and
it is the difference between a catalogue image and a fabrication. Your call whether they are worth
it — four of the five are `out` scope anyway, but **tees_06 and tees_16 are two of your three
wearable ones**.

"""The two wardrobes: everyday and golf.

Max owns two wardrobes that barely overlap — an everyday/work one and 107
garments of golf kit. Before this the app could only see the everyday one: the
golf garments were in the database and no screen could reach them.

Membership is DERIVED from the occasion tags an item already carries. It is
never stored as a second flag, because a second flag is a thing that can
disagree with the first one:

    golf      the item carries the `golf` occasion
    everyday  the item carries any occasion that is NOT `golf`

**The two sets deliberately overlap.** A polo tagged ["casual", "golf"] is in
both, and that is Max's own rule: golf kit without a crest or a logo can go to
work or casual. Only a garment tagged `golf` and nothing else is golf-exclusive.
An item carrying no tags at all is in neither, which is a real answer — it means
nobody has said where it belongs.

This is a wardrobe, not a filter and not a tab. Flipping it changes which
garments the closet lists, which fits exist, what Today picks from, and the
anatomy of the fit builder itself.
"""

from __future__ import annotations

MODES = ("everyday", "golf")
LABELS = {"everyday": "Everyday", "golf": "Golf"}
DEFAULT = "everyday"

# Both clauses assume the items table is aliased `i`.
GOLF_CLAUSE = (
    "EXISTS (SELECT 1 FROM item_occasions io "
    "WHERE io.item_id = i.id AND io.occasion_code = 'golf')"
)
EVERYDAY_CLAUSE = (
    "EXISTS (SELECT 1 FROM item_occasions io "
    "WHERE io.item_id = i.id AND io.occasion_code <> 'golf')"
)


def normalise(mode: str | None) -> str:
    return mode if mode in MODES else DEFAULT


def clause(mode: str) -> str:
    """The SQL predicate for membership of one wardrobe."""
    return GOLF_CLAUSE if normalise(mode) == "golf" else EVERYDAY_CLAUSE


# --------------------------------------------------------------- crests --

# What makes a garment golf-exclusive in spirit is a club crest: not because
# anyone decodes it, but because it makes the garment a uniform.
#
# There is no `crested` column. The fact is already recorded, per garment and
# from the photographs, in `formality_note` — migrations 044-051 wrote it in a
# regular vocabulary, and this reads that vocabulary rather than guessing from
# the garment's name. A name-based regex was the design prototype's stopgap and
# it misfires on the next club shirt; a note that says "Brand polo, no club"
# says so in words.
#
# A column is still the right end state — see docs/HANDOFF-GOLF-WARDROBE.md.

_CRESTED_MARKERS = (
    "home club",              # Royal Sydney, Woollahra — his own clubs
    "another club's crest",   # the visitor souvenirs, per migration 051
    "visitor souvenir",       # the older wording, on the caps
    "representative",         # WOOLLAHRA GOLF CLUB - REPRESENTATIVE
)

# A mark that was photographed but never read is NOT a crest and NOT a
# not-crest. Three polos are in this state and the notes say so outright;
# asserting either way would invent a fact the catalogue refuses to state.
_UNREAD_MARKERS = (
    "could not be read",
    "not legible",
    "not read at full resolution",
    "no club asserted",
)


def crest_state(formality_note: str | None) -> str:
    """`crested` · `plain` · `unread` · `unknown`, from the note alone.

    `unknown` means nothing has been said — every short, shoe and belt, where
    a crest was never in question.
    """
    if not formality_note:
        return "unknown"
    note = formality_note.lower()
    if any(marker in note for marker in _UNREAD_MARKERS):
        return "unread"
    if any(marker in note for marker in _CRESTED_MARKERS):
        return "crested"
    return "plain"


def is_crested(formality_note: str | None) -> bool:
    """True only where a club crest is actually asserted. `unread` is not."""
    return crest_state(formality_note) == "crested"


# --------------------------------------------------------- builder slots --

# (slot, label, optional, eligible categories)
#
# The slot names are the fit roles, so slot_roles() keeps working unchanged:
# `knit` and `top` together still mean the knit is worn over and the lighter
# garment becomes the `base` underneath.
EVERYDAY_ROLES = [
    ("outer", "Outer", True, ("Outerwear",)),
    ("layer", "Layer", True, ("Knitwear",)),
    ("top", "Top", False, ("Tops",)),
    ("knit", "Knit", True, ("Knitwear",)),
    ("bottom", "Bottom", False, ("Trousers", "Shorts")),
    ("shoe", "Shoe", False, ("Shoes",)),
    ("belt", "Belt", False, ("Belts",)),
]

# Golf order follows how Max actually gets dressed, in his words: shoes, shorts
# or pants, polo, hat, optionally a knit or golf outerwear. Laid out top-down,
# that is hat first and shoes last.
GOLF_ROLES = [
    ("hat", "Hat", False, ("Hats",)),
    ("top", "Polo", False, ("Tops",)),
    ("knit", "Knit or outerwear", True, ("Knitwear", "Outerwear")),
    ("belt", "Belt", True, ("Belts",)),
    ("bottom", "Shorts or trousers", False, ("Shorts", "Trousers")),
    ("shoe", "Shoes", False, ("Shoes",)),
]

# Slots whose label is already plural or a compound, and must not have an "s"
# stuck on the end of it in the builder's count note.
NEVER_PLURALISED = {"Shorts or trousers", "Knit or outerwear", "Shoes"}

# Nothing in Knitwear or Outerwear carries a golf tag — Max has never said which
# of his knits he plays in. Rather than show an empty slot, the golf builder
# borrows light casual layers and says out loud that it is doing so. Tag the
# real golf knits and this fallback stops firing on its own.
BORROWED_SLOT = "knit"
BORROWED_MAX_WARMTH = 3


def roles(mode: str) -> list[tuple[str, str, bool, tuple[str, ...]]]:
    return GOLF_ROLES if normalise(mode) == "golf" else EVERYDAY_ROLES


# Every slot name either anatomy uses. Reading a submitted form against this
# rather than against one mode's list means a form posted from the golf builder
# still parses if the wardrobe was switched in another tab: what the form
# carries is what Max actually picked, whatever the setting says now.
ALL_SLOTS = tuple(
    dict.fromkeys(slot for group in (EVERYDAY_ROLES, GOLF_ROLES) for slot, *_ in group)
)

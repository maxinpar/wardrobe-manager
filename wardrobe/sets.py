"""A variant set as the This Week screen needs it: a base, and five pictures.

The screen shows a set as one sentence and five renders — "the aubergine
shawl-collar, black jeans, black belt, ecco nubuck sneaker · 5 days covered" —
so this module turns a group of fits into that sentence and that list.

WHAT MAKES A SET, and why it is not a grouping rule. A set is authored: it is
`fits.variant_set`, written by hand in a migration against a brief. Nothing here
infers one by noticing that some fits share a trouser. The design handoff
proposed grouping by the fit-id prefix (`fit_bc_*`) instead, because that is all
data/fits.json exposes — and that rule loses one variant from every set, because
each set has one member that already existed and was retagged rather than
duplicated (fit_c6, fit_the_shawl, fit_k4, fit_w5, fit_w3). Reading the column
gives five variants for five weekdays; reading the id gives four and an empty
Friday. The column is the authored thing, so the column wins.

THE BASE is every role:item the members have in common, and the ANCHOR is the
fixed `outer` or `top` among them — the gilet or the knit that stays on all
week. beige_brown has neither, because its top is the thing that changes, and
every sentence this module writes has to survive that. Hardcoding "the knit
stays on" produces copy that contradicts one set in five.

THE VARYING GARMENT is picker.variant_item's answer, not a role. That function
already knows the two hard cases — a set that varies the tee *under* a held
knit, and a member with more than one garment unique to it — and re-deriving it
here would be re-deriving them wrong.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import db, picker

# Mon–Fri. The week has five days and a set has five positions; that is not a
# coincidence, but nothing here assumes they are equal — a set with four
# variants leaves a day open and says so.
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# The roles that can hold a set together, in the order the base line names them.
# `outer` and `top` are the two an anchor can sit in.
BASE_ORDER = ("outer", "top", "layer", "bottom", "belt", "shoe")

ANCHOR_ROLES = ("outer", "top")

# picker.weather_band's vocabulary, coldest first, so a set's bands always read
# in the same order however they were stored.
BAND_ORDER = ("cold", "mild", "warm")

# The hero tiles label a garment by what it is doing in the outfit, not by the
# schema's role name. `outer` and `top` both read as the thing over everything
# else once the varying piece has been named separately.
HERO_ROLE_LABELS = {
    "outer": "layer",
    "top": "layer",
    "layer": "layer",
    "bottom": "trouser",
    "belt": "belt",
    "shoe": "shoe",
}


def and_list(parts: list[str]) -> str:
    """"cold, mild and warm" — never "cold and mild and warm"."""
    parts = list(parts)
    if len(parts) < 2:
        return "".join(parts)
    return ", ".join(parts[:-1]) + " and " + parts[-1]


@dataclass
class Piece:
    """One garment of the fixed base, named twice: fully, and in a sentence."""

    item_id: str
    name: str
    short: str
    role: str
    # Rain's one real consequence is suede and nubuck, and the sentence has to
    # name the material. Both come off the item picker already loaded, rather
    # than off a substring search of the garment's name.
    rain_unsafe: bool = False
    material: str | None = None


@dataclass
class Variant:
    """One member of the set: a render, and the garment that makes it itself."""

    fit: picker.Fit
    position: int
    vary_name: str
    vary_id: str | None
    vary_role: str | None
    # Read here rather than off the Fit: picker.load_fits scores against the
    # temperature bands and has never needed the rank, so it does not load it.
    formality: int = 0
    bands: list[str] = field(default_factory=list)


@dataclass
class Set:
    key: str
    name: str
    source: str | None
    anchor: Piece | None
    base: list[Piece]                      # anchor, bottom, belt, shoe
    variants: list[Variant] = field(default_factory=list)

    @property
    def bottom(self) -> Piece | None:
        return next((p for p in self.base if p.role == "bottom"), None)

    # --------------------------------------------------------------- copy --
    #
    # Three sentences the screen prints, all derived. The handoff is explicit
    # that hardcoding them produced a line that contradicted beige_brown, so
    # each of these reads the set rather than assuming its shape.

    def base_line(self) -> str:
        """"the aubergine shawl-collar, black jeans, black belt, ecco nubuck sneaker"."""
        parts = []
        for piece in self.base:
            if self.anchor and piece.item_id == self.anchor.item_id:
                parts.append(f"the {piece.short}")
            elif piece.role == "shoe":
                # The only piece whose short name keeps its brand, so it is the
                # only one that needs lowering to sit inside a sentence.
                parts.append(piece.short.lower())
            else:
                parts.append(piece.short)
        return ", ".join(parts)

    def vary_line(self) -> str:
        """What changes day to day, read off the variants rather than assumed."""
        roles = {v.vary_role for v in self.variants if v.vary_role}
        under = "base" in roles and "top" not in roles
        if under and self.anchor:
            return f"Only what's under the {self.anchor.short} changes"
        if under:
            return "Only the shirt or tee underneath changes"
        if self.anchor:
            return f"The {self.anchor.short} stays on; the top under it changes"
        return "The top changes; trouser, belt and shoes stay put"

    def anchor_line(self) -> str:
        if self.anchor:
            return f"the {self.anchor.short} every day"
        return "same trouser, belt and shoes every day"

    def sub_line(self, variant: "Variant | None") -> str:
        """The line under the hero: what is on today, and what it sits on.

        "Grey crew tee under the aubergine shawl-collar · the aubergine
        shawl-collar, black jeans, black belt, ecco nubuck sneaker". With no
        anchor there is nothing to be under, so the garment stands alone.
        """
        if variant is None:
            return self.base_line()
        if self.anchor:
            lead = f"{variant.vary_name} under the {self.anchor.short}"
        else:
            lead = variant.vary_name
        return f"{lead} · {self.base_line()}"

    def empty_note(self) -> str:
        """Why a day is blank: the set is short, and that is a thing to fix."""
        return (
            f"This set has {len(self.variants)} variants and the week has "
            f"{len(WEEKDAYS)} days. Build another in the app and it lands here "
            "on the next pull."
        )


    # ------------------------------------------------------------ weather --
    #
    # Three facts and one sentence. The facts are the set's own — which
    # temperatures its fits were built for, and whether its shoe survives rain.
    # The sentence is written against a week, and is the only place the two
    # meet.

    @property
    def shoe(self) -> Piece | None:
        return next((p for p in self.base if p.role == "shoe"), None)

    def bands(self) -> list[str]:
        """The union of the variants' temperature bands, coldest first."""
        held = {band for variant in self.variants for band in variant.bands}
        return [band for band in BAND_ORDER if band in held]

    def rain_word(self) -> str | None:
        """"nubuck", when this set has a shoe that cannot be rained on.

        Only the shoe and the anchor: a shirt under a knit never meets the
        weather, and warning about it would be noise on every wet day.
        """
        for piece in (self.shoe, self.anchor):
            if piece and piece.rain_unsafe:
                return piece.material or "suede"
        return None

    def shoe_phrase(self, word: str) -> str:
        """"the Ecco nubuck sneaker" — the material said once, not twice."""
        shoe = self.shoe
        if shoe is None:
            return "shoe"
        if word and word.lower() in shoe.short.lower():
            return shoe.short
        return f"{shoe.short} ({word})"

    def weather_note(self, target: str, wet: bool, range_label: str) -> dict:
        """Whether this set suits the week, in one line and a tone.

        Rain outranks temperature, because a wet week has a consequence you can
        act on — a different shoe, or a different set — and being a degree off
        does not.
        """
        soaked = self.rain_word() if wet else None
        if soaked:
            return {
                "text": f"Wet week — the {self.shoe_phrase(soaked)} stays in.",
                "tone": "rained-out",
            }

        bands = self.bands()
        if bands and target not in bands:
            return {
                "text": f"A {'/'.join(bands)} set on a {target} day.",
                "tone": "wrong-band",
            }
        if not bands:
            # A set whose fits carry no bands makes no claim, so the screen
            # makes none on its behalf.
            return {"text": "", "tone": "right"}
        return {
            "text": f"Built for {and_list(bands)} — right for {range_label}.",
            "tone": "right",
        }

    def hero_pieces(self, variant: "Variant | None") -> list[dict]:
        """The garments of one day, varying piece first.

        The base is identical all week, so the only thing worth leading with is
        the piece that makes this day itself — labelled `top` or `under`
        depending on where it sits, which is `varyRole` read out loud.
        """
        out: list[dict] = []
        if variant and variant.vary_id:
            out.append(
                {
                    "item_id": variant.vary_id,
                    "name": variant.vary_name,
                    "role": "under" if variant.vary_role == "base" else "top",
                }
            )
        for piece in self.base:
            if variant and piece.item_id == variant.vary_id:
                continue
            out.append(
                {
                    "item_id": piece.item_id,
                    "name": piece.name,
                    "role": HERO_ROLE_LABELS.get(piece.role, piece.role),
                }
            )
        return out

    def count_note(self) -> str:
        """"4 variants built, 1 day open" — or, for a full set, "5 days covered"."""
        open_days = len(WEEKDAYS) - len(self.variants)
        if open_days <= 0:
            return f"{len(WEEKDAYS)} days covered"
        days = "day" if open_days == 1 else "days"
        return f"{len(self.variants)} variants built, {open_days} {days} open"

    def bench_note(self) -> str:
        """The footer under a set on the picker: what changes, and what's spare."""
        spare = len(self.variants) - len(WEEKDAYS)
        if spare > 0:
            variants = "variant" if spare == 1 else "variants"
            return (
                f"{self.vary_line()} — {spare} more {variants} ready to swap in "
                "mid-week."
            )
        return f"{self.vary_line()} — {self.anchor_line()}."


def short_name(item: dict) -> str:
    """How a garment is named inside a sentence about an outfit.

    "Black coated straight jeans" is what the garment IS; "black jeans" is what
    you call it when you are describing what you are wearing. The rule is colour
    plus the noun the name ends in, which is how the handoff's own base lines
    are written, and it holds for every base garment in the five sets except one
    belt whose colour field starts with the word "Rustic". That one carries an
    explicit `short_name`; see migration 080.

    A shoe keeps its full name. "black sneaker" loses the only thing worth
    saying about a shoe you own four pairs of.
    """
    if item.get("short_name"):
        return item["short_name"]

    name = (item.get("name") or "").strip()
    if item.get("role") == "shoe" or item.get("cat") == "Shoes":
        return name

    colour = (item.get("colour") or "").strip()
    # "Black (coated / waxed finish)", "Sand / warm beige" — the first clause is
    # the colour and the rest is detail that does not belong in a five-word
    # sentence about four garments.
    for separator in ("(", "/", ","):
        if separator in colour:
            colour = colour.split(separator, 1)[0]
    colour = colour.strip()
    noun = name.rsplit(" ", 1)[-1] if name else ""
    if not colour or not noun:
        return name
    if noun.lower() in colour.lower():
        # "Black belt" with colour "Black": the rule would say "black black".
        return name.lower()
    return f"{colour.lower()} {noun}"


def _piece(item: dict) -> Piece:
    return Piece(
        item_id=item["item_id"],
        name=item["name"],
        short=short_name(item),
        role=item["role"],
        rain_unsafe=bool(item.get("rain_unsafe")),
        material=item.get("material_hint"),
    )


def load(conn, fits: list[picker.Fit] | None = None) -> list[Set]:
    """Every authored set, in the order the picker lists them.

    `fits` is the caller's already-loaded fits where it has them — the week
    screen loads them once for the whole request rather than twice.
    """
    if fits is None:
        fits = picker.load_fits(conn)

    names = {
        row["key"]: row
        for row in db.fetch_all(
            conn, "SELECT key, name, source, sort_order FROM variant_sets"
        )
    }
    shorts = {
        row["id"]: row["short_name"]
        for row in db.fetch_all(
            conn, "SELECT id, short_name FROM items WHERE short_name IS NOT NULL"
        )
    }
    colours = {
        row["id"]: row["colour"]
        for row in db.fetch_all(conn, "SELECT id, colour FROM items")
    }
    formality = {
        row["id"]: row["formality_rank"] or 0
        for row in db.fetch_all(
            conn, "SELECT id, formality_rank FROM fits WHERE variant_set IS NOT NULL"
        )
    }

    grouped: dict[str, list[picker.Fit]] = {}
    for fit in fits:
        if fit.variant_set and fit.variant_position is not None and not fit.gone:
            grouped.setdefault(fit.variant_set, []).append(fit)

    out: list[Set] = []
    for key, members in grouped.items():
        members.sort(key=lambda f: f.variant_position or 0)
        if len(members) < 2:
            # One fit is not a set. It behaves as an ordinary fit everywhere
            # else in the app and it does the same here.
            continue

        # Common base: the role:item pairs every member carries. Role is part of
        # the identity on purpose — the same tee worn as `base` in one member
        # and `top` in another is not a fixed piece of the base, it is the
        # thing that varies.
        shared: set[tuple[str, str]] | None = None
        catalogue: dict[str, dict] = {}
        for member in members:
            present = set()
            for item in member.primary():
                present.add((item["role"], item["item_id"]))
                catalogue[item["item_id"]] = dict(
                    item,
                    colour=colours.get(item["item_id"]),
                    short_name=shorts.get(item["item_id"]),
                )
            shared = present if shared is None else shared & present

        base = [
            _piece(dict(catalogue[item_id], role=role))
            for role, item_id in sorted(
                shared or set(),
                key=lambda pair: (
                    BASE_ORDER.index(pair[0]) if pair[0] in BASE_ORDER else 99,
                    pair[1],
                ),
            )
        ]
        anchor = next((p for p in base if p.role in ANCHOR_ROLES), None)

        variants = []
        for member in members:
            item = picker.variant_item(member, members)
            variants.append(
                Variant(
                    fit=member,
                    position=member.variant_position or 0,
                    vary_name=item["name"] if item else member.name,
                    vary_id=item["item_id"] if item else None,
                    vary_role=item["role"] if item else None,
                    formality=formality.get(member.id, 0),
                    bands=list(member.temp_bands),
                )
            )

        row = names.get(key, {})
        out.append(
            Set(
                key=key,
                # A set with no row in variant_sets still works; it is just
                # called after its key rather than after itself.
                name=row.get("name") or key.replace("_", " "),
                source=row.get("source") or members[0].source,
                anchor=anchor,
                base=base,
                variants=variants,
            )
        )

    out.sort(key=lambda s: (names.get(s.key, {}).get("sort_order", 100), s.name))
    return out


def wash_line(week_set: Set, worn: list[Variant]) -> str:
    """Friday's basket: the trouser, the anchor, and what was actually worn.

    Belt and shoes stay out — they are not washed weekly and listing them would
    make the line something to skim rather than read.
    """
    parts = []
    bottom = week_set.bottom
    if bottom:
        parts.append(bottom.short)
    if week_set.anchor:
        parts.append(f"the {week_set.anchor.short}")

    varied: list[str] = []
    for variant in worn:
        if variant.vary_name and variant.vary_name not in varied:
            varied.append(variant.vary_name)

    line = ", ".join(parts) if parts else "the base"
    if varied:
        return f"{line}, plus {', '.join(varied)}"
    return f"{line}, plus whatever you wear under it"

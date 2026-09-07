"""AI build-a-fit: three fits for one day, from Max's own closet.

Ported from the design prototype (`design_handoff_ai_fit_and_mobile`), with the
call moved server-side. In the prototype it ran in the browser through the
Design Component's own helper; here it runs in Flask, because the API key must
never reach a page. That is the only structural change to the feature — the
brief, the validation and the copy contract are the handover's.

TWO THINGS THE PORT CHANGED ON PURPOSE

1. The prompt is inverted. The prototype put the brief first and the 161-garment
   closet last. Prompt caching is a prefix match, so written that way every ask
   pays full price for the closet — the bulk of the tokens and the one part that
   does not change between asks. Here the closet is the tail of the SYSTEM
   prompt behind a cache breakpoint, and the brief is the whole user message.
   Same information, and the second ask of a session costs a tenth as much for
   its input.

2. The `submit_fits` tool is gone. It existed because free-form JSON came back
   half-formed ("position 2056"), and a tool's input_schema was the only way to
   constrain the shape. The API now constrains the response itself with
   `output_config.format`, so there is no tool, no `run` handler, and no
   fence-stripping fallback parser to keep alive.

WHAT THE SCHEMA STILL CANNOT DO is the reason `_validate` survives intact: a
schema guarantees the JSON is well-formed, not that the garment ids exist, that
a locked seed is still in the fit, or that two pieces are not fighting over the
same role. Those are semantic and they are checked below, exactly as the
prototype checked them.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field

import anthropic

from . import db, forecast, wardrobes

# Opus 5 for the styling judgement. This is a subjective task — proportion,
# colour, register, and a paragraph explaining why — which is where the
# difference between model tiers actually shows. Overridable without a code
# change, because the honest way to find out whether Sonnet is good enough here
# is to run both against real briefs.
MODEL = os.environ.get("AI_FITS_MODEL", "claude-opus-5")

# Effort governs how hard Claude thinks, and thinking tokens are most of what an
# ask costs. Measured on this closet, one real brief each:
#
#   high    103s   5,686 output tokens   ~$0.15
#   medium   30s   2,053 output tokens   ~$0.05
#   low      26s   1,764 output tokens   ~$0.04
#
# `medium` ships as the default: three and a half times faster and three times
# cheaper than `high`, still three usable fits, and 100 seconds is not a wait
# anyone will sit through to be told what to wear. `high` is a one-line change
# if the answers ever feel thin.
EFFORT = os.environ.get("AI_FITS_EFFORT", "medium")

# Three fits with a paragraph each is ~1,200 tokens of answer. The rest is
# headroom for thinking — hitting the cap truncates mid-fit and wastes the call.
MAX_TOKENS = 8000

# (code, label, what it means — the meaning goes in the prompt, because "Work"
# alone tells Claude nothing about an office where developers wear t-shirts.)
OCCASIONS = [
    ("work", "Work", "in the office — relaxed bank, nobody wears a suit"),
    ("wfh", "WFH", "working from home, maybe a walk or a coffee out"),
    ("other", "Other", "not work — errands, lunch, seeing people"),
]

# The 5-point sharpness dial. Labels are what Claude is told; the number is not.
SHARPNESS = [
    (1, "as relaxed as it gets"),
    (2, "relaxed"),
    (3, "as it comes"),
    (4, "a bit sharp"),
    (5, "sharp"),
]

DEFAULT_SHARPNESS = 3

# Physically somewhere else, so Max cannot put it on this morning however much
# it suits the day. `worn` is deliberately NOT here — see pool().
AWAY_STATES = ("in_wash", "at_tailor")


@dataclass
class Brief:
    """Everything Max chose, and everything that changes the answer."""

    mode: str
    day_key: str
    occasion: str = "work"
    sharpness: int = DEFAULT_SHARPNESS
    note: str = ""
    seeds: list[str] = field(default_factory=list)

    def key(self) -> str:
        """The cache key. Sorted seeds — order of clicking is not a difference."""
        raw = json.dumps(
            {
                "mode": self.mode,
                "day": self.day_key,
                "occasion": self.occasion,
                "sharpness": self.sharpness,
                "note": self.note.strip().lower(),
                "seeds": sorted(self.seeds),
                "model": MODEL,
            },
            sort_keys=True,
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def occasion_row(self) -> tuple[str, str, str]:
        for row in OCCASIONS:
            if row[0] == self.occasion:
                return row
        return OCCASIONS[0]

    def sharpness_label(self) -> str:
        for level, label in SHARPNESS:
            if level == self.sharpness:
                return label
        return SHARPNESS[DEFAULT_SHARPNESS - 1][1]


# ------------------------------------------------------- the garment pool --


def pool(conn, mode: str) -> tuple[list[dict], int]:
    """Every garment Max could physically put on, and how many he could not.

    The filter is the handover's, expressed in this database's vocabulary:
    in the wardrobe, in a category the builder has a slot for, not binned, not
    gone, not retired, and not away.

    AWAY IS NOT `laundry_states.available`, which was the first thing tried here
    and was wrong. That flag is false for `worn` as well as for `in_wash` and
    `at_tailor`, and `worn` is not a garment Max cannot reach — it is a garment
    he wore recently. Nothing resets it: on the live database ten garments have
    sat in `worn` since 28-30 August, long since washed and back on the shelf.
    Reading the flag literally would have quietly hidden ten wearable garments
    from the stylist forever. Away means physically elsewhere, and that is the
    two states named below.

    Verdicts match builder_pool(): Keep and Tailor. Not because Tailor is ideal
    but because the manual builder offers those garments, and the two builders
    must offer the same closet — otherwise "Tweak it by hand" opens on a fit
    containing a garment the manual builder will not show.
    """
    cats = sorted({cat for _, _, _, group in wardrobes.roles(mode) for cat in group})
    sql = """
        SELECT i.id, i.name, i.cat_code, i.colour, i.material, i.weight_code,
               i.formality_raw, i.formality_rank, i.warmth, i.avoid, i.layer,
               i.notes, i.hex, i.cut, i.neck_code, i.rain_unsafe,
               (il.state_code = ANY(%s)) AS away
        FROM items i
        LEFT JOIN item_laundry il ON il.item_id = i.id
        WHERE i.retired_at IS NULL AND i.gone_at IS NULL AND i.scope_code = 'core'
          AND i.verdict_code IN ('Keep', 'Tailor')
          AND i.cat_code = ANY(%s) AND
    """
    rows = db.fetch_all(
        conn,
        sql + wardrobes.clause(mode) + " ORDER BY i.cat_code, i.name",
        (list(AWAY_STATES), cats),
    )
    available = [row for row in rows if not row["away"]]
    return available, len(rows) - len(available)


# The closet files 84 everyday garments under `Tops` and has no Shirts category,
# so the Must-wear tabs derive one. This is the handover's heuristic, ported
# verbatim and no more trusted here than it was there: it reads a name, and a
# name is not a field.
#
# REPLACE THIS with a real subtype the moment `items` grows one. It is listed as
# open work in the handover for the same reason — the next linen overshirt Max
# buys with an unusual name lands in the wrong tab and nothing will say so.
_POLO = re.compile(r"polo", re.I)
_SHIRT = re.compile(r"shirt|oxford|linen button|overshirt", re.I)
_NOT_SHIRT = re.compile(r"t-?shirt|tee shirt", re.I)


def top_kind(row: dict) -> str:
    """`Polo` · `Shirt` · `Tee` for a Tops garment; its category otherwise."""
    if row.get("cat_code") != "Tops":
        return row.get("cat_code") or ""
    haystack = " ".join(
        str(row.get(field) or "") for field in ("name", "cut", "neck_code")
    )
    if _POLO.search(haystack):
        return "Polo"
    if _SHIRT.search(haystack) and not _NOT_SHIRT.search(haystack):
        return "Shirt"
    return "Tee"


# Tab order, as specified. `Everything` is always shown; the rest hide at zero.
TAB_ORDER = (
    "Everything", "Polos", "Shirts", "Tees", "Knitwear", "Outerwear",
    "Trousers", "Shorts", "Shoes", "Belts", "Hats",
)
_TAB_FOR_KIND = {"Polo": "Polos", "Shirt": "Shirts", "Tee": "Tees"}


def tab_for(row: dict) -> str:
    """Which Must-wear tab a garment sits under."""
    kind = top_kind(row)
    return _TAB_FOR_KIND.get(kind, row.get("cat_code") or "")


def tabs(garments: list[dict]) -> list[tuple[str, int]]:
    """(label, count) in the fixed order, dropping the empty ones."""
    counts: dict[str, int] = {}
    for row in garments:
        counts[tab_for(row)] = counts.get(tab_for(row), 0) + 1
    out = [("Everything", len(garments))]
    out += [(tab, counts[tab]) for tab in TAB_ORDER[1:] if counts.get(tab)]
    return out


def role_for(cat: str, mode: str) -> str | None:
    """The slot a category belongs in — the fallback for an invented role."""
    for slot, _, _, cats in wardrobes.roles(mode):
        if cat in cats:
            return slot
    return None


# ------------------------------------------------------------ the prompt --


def _trim(value, limit: int) -> str:
    return " ".join(str(value or "").split())[:limit]


def _garment_line(row: dict) -> str:
    """One terse line per garment. Every field earns its tokens or is dropped."""
    parts = [
        row["id"],
        row["name"],
        row["cat_code"],
        row.get("colour") or "",
        row.get("material") or "",
        f"{row['weight_code']} weight" if row.get("weight_code") else "",
        row.get("formality_raw") or "",
        f"warmth {row['warmth']}" if row.get("warmth") is not None else "",
        "rain-unsafe" if row.get("rain_unsafe") else "",
    ]
    line = " | ".join(part for part in parts if part)
    avoid = _trim(row.get("avoid"), 110)
    if avoid and avoid != "-":
        line += " | AVOID: " + avoid
    return line


def _seed_line(row: dict) -> str:
    """A locked garment gets its pairing notes too — that is why it is locked."""
    line = _garment_line(row)
    layer = _trim(row.get("layer"), 110)
    notes = _trim(row.get("notes"), 160)
    if layer and layer != "-":
        line += " | LAYERS WITH: " + layer
    if notes:
        line += " | NOTE: " + notes
    return line


def _profile(conn) -> dict:
    row = db.fetch_one(
        conn, "SELECT value FROM app_settings WHERE key = 'catalogue.profile'"
    )
    if not row:
        return {}
    try:
        return json.loads(row["value"])
    except (ValueError, TypeError):
        return {}


def system_blocks(conn, mode: str, garments: list[dict], styling_rules: list[str]) -> list[dict]:
    """The system prompt, split so the closet sits behind a cache breakpoint.

    Two blocks, and the order is the whole point: everything stable, then the
    closet, then a breakpoint. The brief goes in the user message and is not
    cached, because it changes on every ask by definition.
    """
    profile = _profile(conn)
    roles = wardrobes.roles(mode)
    role_text = ", ".join(
        f"{slot} ({label})" + (" — optional" if optional else "")
        for slot, label, optional, _ in roles
    )

    rules = [
        "You are Max's wardrobe stylist. You know his closet garment by garment "
        "and you dress him for one specific day.",
        f"Max is {profile.get('age', 48)}, French, and works in a bank in Sydney. "
        + _trim(profile.get("context"), 400),
        "His goal: " + _trim(profile.get("goal"), 300),
        "The shape of his work uniform: " + _trim(profile.get("workUniform"), 300),
        "",
        "HARD RULES",
        "- The MUST WEAR garments are fixed. Build around them. Never drop one, "
        "never swap it for something similar.",
        "- Use only garment ids from the CLOSET list. Never invent an id, a brand "
        "or a garment.",
        f"- Roles to fill: {role_text}.",
        "- One garment per role. Leave an optional role out rather than forcing a "
        "piece into it.",
        "- Obey each garment's AVOID note. It is a real constraint, not a preference.",
        "- Dress for the forecast, the occasion and the sharpness dial you are given.",
    ]
    if styling_rules:
        rules.append("")
        rules.append("MAX'S STYLING RULES")
        rules.extend(f"{n}. {rule}" for n, rule in enumerate(styling_rules, start=1))
    rules += [
        "",
        "OUTPUT",
        "Exactly 3 fits. The first is your best call. The other two are genuine "
        "alternatives — a different silhouette or register, not a near-copy with "
        "the belt changed.",
        "name: 2-5 plain words, no puns, no colons.",
        "note: ONE paragraph, 2-4 sentences, second person, why THIS works for "
        "THIS day — concrete about colour, weight and proportion. No bullets, no "
        "headings, and do not restate the weather numbers back to him.",
    ]

    closet = f"CLOSET ({len(garments)} available garments):\n" + "\n".join(
        _garment_line(row) for row in garments
    )

    return [
        {"type": "text", "text": "\n".join(rules)},
        # The breakpoint. Everything above and including the closet is reused on
        # the next ask; verify with usage.cache_read_input_tokens, which is
        # written to ai_fit_answers.cached_tokens on every call.
        {"type": "text", "text": closet, "cache_control": {"type": "ephemeral"}},
    ]


def user_message(brief: Brief, day: forecast.Day, garments: list[dict]) -> str:
    """The brief. Small, volatile, and deliberately after the cache breakpoint."""
    by_id = {row["id"]: row for row in garments}
    seeds = [by_id[item_id] for item_id in brief.seeds if item_id in by_id]
    _, occ_label, occ_meaning = brief.occasion_row()

    lines = [
        "DAY: " + day.prompt_line(),
        "PLACE: " + forecast.PLACE,
        f"OCCASION: {occ_label} — {occ_meaning}",
        "SHARPNESS: " + brief.sharpness_label(),
    ]
    if brief.note.strip():
        lines.append("MAX SAYS: " + _trim(brief.note, 400))
    lines.append("")
    if seeds:
        lines.append(f"MUST WEAR ({len(seeds)}) — these are locked in:")
        lines.extend(_seed_line(row) for row in seeds)
    else:
        lines.append("MUST WEAR: nothing locked in — the whole fit is your call.")
    return "\n".join(lines)


def _schema(mode: str) -> dict:
    slots = [slot for slot, *_ in wardrobes.roles(mode)]
    return {
        "type": "object",
        "properties": {
            # No minItems/maxItems: structured outputs rejects any value other
            # than 0 or 1 ("For 'array' type, 'minItems' values other than 0 or
            # 1 are not supported"). "Exactly 3" is asked for in the system
            # prompt and enforced in _validate, which had to hold that line
            # anyway — a schema can count fits but cannot tell a real
            # alternative from the same fit with a different belt.
            "fits": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "2-5 plain words, no puns, no colons",
                        },
                        "note": {
                            "type": "string",
                            "description": "One paragraph, 2-4 sentences, second person",
                        },
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "type": "string",
                                        "description": "a garment id from the CLOSET list",
                                    },
                                    "role": {"type": "string", "enum": slots},
                                },
                                "required": ["id", "role"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["name", "note", "items"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["fits"],
        "additionalProperties": False,
    }


# ---------------------------------------------------------- the call --


class AiError(RuntimeError):
    """A failure Max should read, not a stack trace."""


def ask(conn, brief: Brief, styling_rules: list[str], use_cache: bool = True) -> dict:
    """Three fits for the brief. Cached answers cost nothing and return instantly."""
    key = brief.key()
    if use_cache:
        row = db.fetch_one(
            conn, "SELECT payload FROM ai_fit_answers WHERE brief_key = %s", (key,)
        )
        if row:
            answer = row["payload"]
            answer["cached"] = True
            return answer

    garments, skipped = pool(conn, brief.mode)
    if not garments:
        raise AiError("Nothing in this wardrobe is available to build with.")

    days = forecast.week(conn)
    day = forecast.find(days, brief.day_key)

    try:
        client = anthropic.Anthropic()
    except Exception as exc:  # no key configured is the realistic case
        raise AiError(
            "The AI builder is not configured — no Anthropic API key. "
            "Add ANTHROPIC_API_KEY to .env."
        ) from exc

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_blocks(conn, brief.mode, garments, styling_rules),
            messages=[{"role": "user", "content": user_message(brief, day, garments)}],
            output_config={
                "effort": EFFORT,
                "format": {"type": "json_schema", "schema": _schema(brief.mode)},
            },
        )
    except anthropic.AuthenticationError as exc:
        raise AiError("The Anthropic API key was rejected. Check ANTHROPIC_API_KEY.") from exc
    except anthropic.RateLimitError as exc:
        raise AiError("Too many asks too quickly. Give it a minute and try again.") from exc
    except anthropic.APIStatusError as exc:
        detail = "the service is having trouble" if exc.status_code >= 500 else exc.message
        raise AiError(f"The stylist could not be reached — {detail}.") from exc
    except anthropic.APIConnectionError as exc:
        raise AiError("Could not reach the stylist — no network.") from exc

    # A refusal is a 200 with no usable content, so it is checked before the
    # content is read rather than after it fails to parse.
    if response.stop_reason == "refusal":
        raise AiError("That request was declined. Try rewording the note.")

    text = next((block.text for block in response.content if block.type == "text"), "")
    if not text.strip():
        raise AiError("That came back empty. Try again.")
    try:
        raw = json.loads(text)
    except ValueError as exc:
        raise AiError("That didn't come back cleanly — the answer wasn't readable.") from exc

    fits = _validate(raw, brief, garments)
    if not fits:
        raise AiError("That didn't come back cleanly — no usable fit in the answer.")

    answer = {
        "fits": fits,
        "skipped": skipped,
        "available": len(garments),
        "day": day.key,
        "cached": False,
    }
    _remember(conn, key, brief, answer, response)
    return answer


def _remember(conn, key: str, brief: Brief, answer: dict, response) -> None:
    """File the answer and what it cost. Never fails the request."""
    usage = getattr(response, "usage", None)
    try:
        conn.execute(
            """
            INSERT INTO ai_fit_answers
                (brief_key, wardrobe_mode, payload, model,
                 input_tokens, output_tokens, cached_tokens)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (brief_key) DO NOTHING
            """,
            (
                key,
                brief.mode,
                json.dumps(answer),
                MODEL,
                getattr(usage, "input_tokens", None),
                getattr(usage, "output_tokens", None),
                getattr(usage, "cache_read_input_tokens", None),
            ),
        )
    except Exception:
        # An answer Max can see beats a tidy cache. If this row is lost the only
        # cost is asking again.
        pass


# ------------------------------------------------------------ validation --


def _validate(raw: dict, brief: Brief, garments: list[dict]) -> list[dict]:
    """Turn what came back into fits this app can actually save.

    The schema guarantees shape. This guarantees meaning, and every rule here
    is one the prototype learned the hard way:
      * an id that is not in the closet is dropped, not looked up
      * a role that is not a slot is re-derived from the garment's category
      * two garments claiming one role — the second loses
      * a locked seed the model quietly dropped is put back, evicting whatever
        took its role; the alternative is throwing away an otherwise good fit
      * pieces come out in slot order, not the order the model listed them
      * a fit of one piece is not a fit
    """
    by_id = {row["id"]: row for row in garments}
    slots = [slot for slot, *_ in wardrobes.roles(brief.mode)]
    seeds = [item_id for item_id in brief.seeds if item_id in by_id]

    fits = []
    for entry in raw.get("fits") or []:
        seen: dict[str, bool] = {}
        picks: list[dict] = []
        for pair in entry.get("items") or []:
            item_id = (pair or {}).get("id")
            role = (pair or {}).get("role")
            garment = by_id.get(item_id)
            if not garment:
                continue
            if role not in slots:
                role = role_for(garment["cat_code"], brief.mode)
            if not role or seen.get(role):
                continue
            seen[role] = True
            picks.append({"id": item_id, "role": role})

        for item_id in seeds:
            if any(pick["id"] == item_id for pick in picks):
                continue
            role = role_for(by_id[item_id]["cat_code"], brief.mode)
            if not role:
                continue
            picks = [pick for pick in picks if pick["role"] != role]
            picks.append({"id": item_id, "role": role})

        picks.sort(key=lambda pick: slots.index(pick["role"]))
        if len(picks) < 2:
            continue

        fits.append(
            {
                "name": _trim(entry.get("name"), 80) or "Untitled fit",
                "note": _trim(entry.get("note"), 900),
                "items": picks,
                "seeds": [pick["id"] for pick in picks if pick["id"] in seeds],
            }
        )
    # Three is the contract the results view is laid out for. A fourth is
    # dropped rather than shown; a short answer is shown rather than refused,
    # because two good fits beat an error message.
    return fits[:3]

"""Regenerate fits.json from the database.

    python scripts/export_fits.py                     # writes export/fits.json
    python scripts/export_fits.py --out data/fits.json
    python scripts/export_fits.py --compare data/fits.json

The sibling of export_wardrobe.py, and it exists for the same reason: the
garments were exported and the outfits were not, so a Claude session reading
this repository saw 297 items and the 35 fits of 2026-08-27 — a third of what
the database holds, none of them golf, and none carrying a render it could
point at.

Same conventions as the items export: the hand-maintained file's key names and
shape are preserved so wardrobe/fits_json.py can still read the output, 1-space
indent, non-ASCII kept as-is, `generated` bumped to today.

APP-OWNED KEYS
--------------
Everything the app has learnt since the hand file was written is added rather
than substituted, and listed in APP_OWNED_KEYS so --compare does not report the
design working as a difference. The important one is `images`: the hand file
had a single `render` filename, and a fit now has up to four pictures. It is
one object rather than four loose keys so that no reader has to work out the
precedence for itself — `images.display` is the answer, resolved here exactly
as picker.Fit.render resolves it.

`render` itself is kept, unchanged and bare (no directory), because
fits_json.fit_id() derives a fit's id from that filename. `id` is now written
out too, and the loader prefers it: ten fits built in the app have an uploaded
photo and no render at all, and had no id an importer could infer.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import config, db  # noqa: E402
from wardrobe.app import golf_fit_ids  # noqa: E402

# The hand file's key order, from the fits carrying every field, then the
# app-owned keys. Absent keys are omitted rather than written null, except
# where the hand file itself wrote null (`render`).
KEY_ORDER = [
    "code", "id", "name", "source", "category", "temp", "rainSafe",
    "formalityRank", "goodFor", "badFor", "items", "compositionKnown",
    "render", "commentary", "catch", "importNote", "vetted",
    # --- app-owned from here ---
    "wardrobe", "register", "style", "score", "killer", "hiddenByDefault",
    "sortOrder", "images", "preconditions", "gone",
]

# Keys that exist in the export and have never existed in data/fits.json.
# --compare skips them: reporting them would be reporting the design working.
APP_OWNED_KEYS = (
    "id", "wardrobe", "register", "style", "score", "killer", "hiddenByDefault",
    "sortOrder", "images", "preconditions", "gone",
)

# fits_json.REGISTER_BY_CATEGORY, inverted: the hand file's `category` is a
# different axis from `register` and only `smart` implies the sharp one. The
# golf categories were added by the app and have no counterpart in that file.
CATEGORY_FOR_REGISTER = {"sharp": "smart"}


def _rows_by_fit(conn, sql: str, key: str) -> dict[str, list]:
    out: dict[str, list] = {}
    for row in db.fetch_all(conn, sql):
        out.setdefault(row["fit_id"], []).append(row[key])
    return out


def images(row: dict) -> dict:
    """Every picture of one fit, and which one a screen should draw.

    The precedence is picker.Fit.render's, stated once here so the export and
    the app cannot disagree: an upload outranks the generated hero, and the
    layered render is a variant of the hero rather than a rival to it.

    `looks` is 2 only when the pair is real — a fit with an upload has one look
    however many renders were generated for it, because the upload replaced the
    hero and pairing it with a layered render would caption a picture we did
    not make "without the layer".
    """
    upload = row["render_upload_path"]
    hero = row["hero_image_path"]
    layered = row["layered_image_path"]
    two_looks = bool(layered) and not upload

    out = {
        "display": upload or hero,
        "hero": hero,
        "heroThumb": row["hero_thumb_path"],
        # An upload is never called generated: whether it is a photograph or an
        # AI render is not ours to assume, and the app says so on the caption.
        "heroIsGenerated": bool(hero) and row["hero_is_generated"] and not upload,
        "layered": layered,
        "layeredThumb": row["layered_thumb_path"],
        "upload": upload,
        "looks": 2 if two_looks else 1,
    }
    return {k: v for k, v in out.items() if v is not None}


def build_payload(conn, generated: str) -> dict:
    golf = golf_fit_ids(conn)

    temps = _rows_by_fit(
        conn,
        "SELECT fit_id, band_code FROM fit_temp_bands ORDER BY fit_id, band_code",
        "band_code",
    )
    good = _rows_by_fit(
        conn,
        "SELECT fit_id, occasion_code FROM fit_occasions WHERE kind = 'good' "
        "ORDER BY fit_id, occasion_code",
        "occasion_code",
    )
    bad = _rows_by_fit(
        conn,
        "SELECT fit_id, occasion_code FROM fit_occasions WHERE kind = 'bad' "
        "ORDER BY fit_id, occasion_code",
        "occasion_code",
    )

    pieces: dict[str, list[dict]] = {}
    for row in db.fetch_all(
        conn,
        "SELECT fit_id, item_id, role, position, is_alternate, note FROM fit_items "
        "ORDER BY fit_id, is_alternate, position, id",
    ):
        slot = {"role": row["role"], "position": row["position"], "itemId": row["item_id"]}
        # Written only when true or present: the hand file's slots are three
        # keys and most of these still are.
        if row["is_alternate"]:
            slot["isAlternate"] = True
        if row["note"]:
            slot["note"] = row["note"]
        pieces.setdefault(row["fit_id"], []).append(slot)

    jobs: dict[str, list[dict]] = {}
    for row in db.fetch_all(
        conn,
        "SELECT fit_id, text, done FROM fit_preconditions ORDER BY fit_id, id",
    ):
        jobs.setdefault(row["fit_id"], []).append(
            {"text": row["text"], "done": row["done"]}
        )

    fits = []
    for row in db.fetch_all(conn, "SELECT * FROM fits ORDER BY sort_order, id"):
        fit: dict = {}
        composition_known = row["composition_known"]

        for key in KEY_ORDER:
            if key == "code":
                # The hand file keyed fits by code and the database does not
                # store one; it survives only where the id carries it. Absent
                # for every fit built since, which is why `id` is written.
                code = fit_code(row["id"])
                if code:
                    fit[key] = code
            elif key == "id":
                fit[key] = row["id"]
            elif key == "name":
                fit[key] = row["name"]
            elif key == "source":
                fit[key] = row["source"]
            elif key == "category":
                fit[key] = row["category_code"] or CATEGORY_FOR_REGISTER.get(
                    row["register_code"]
                )
            elif key == "temp":
                fit[key] = temps.get(row["id"], [])
            elif key == "rainSafe":
                fit[key] = row["rain_safe"]
            elif key == "formalityRank":
                fit[key] = row["formality_rank"]
            elif key == "goodFor":
                fit[key] = good.get(row["id"], [])
            elif key == "badFor":
                fit[key] = bad.get(row["id"], [])
            elif key == "items":
                # null, not [], for the eight fits whose garment lists were
                # lost: an empty list would read as "wears nothing", and
                # fits_json.py refuses to guess a composition for exactly this
                # reason. The flag below says which case this is.
                fit[key] = pieces.get(row["id"], []) if composition_known else None
            elif key == "compositionKnown":
                if not composition_known:
                    fit[key] = False
            elif key == "render":
                # Bare filename, as the hand file wrote it: fits_json.fit_id()
                # reads this. null for a fit with no generated hero.
                hero = row["hero_image_path"]
                fit[key] = hero.rsplit("/", 1)[-1] if hero else None
            elif key in ("commentary", "catch", "style"):
                if row[key] is not None:
                    fit[key] = row[key]
            elif key == "importNote":
                pass  # a note about the 2026-08-27 import; nothing writes it now
            elif key == "vetted":
                fit[key] = row["vetted"]
            elif key == "wardrobe":
                # Derived, never stored — the same call the /fits screen makes,
                # so the export cannot claim a fit the app would not show.
                fit[key] = "golf" if row["id"] in golf else "everyday"
            elif key == "register":
                fit[key] = row["register_code"]
            elif key == "score":
                if row["score"] is not None:
                    fit[key] = row["score"]
            elif key == "killer":
                if row["killer"]:
                    fit[key] = True
            elif key == "hiddenByDefault":
                if row["hidden_by_default"]:
                    fit[key] = True
            elif key == "sortOrder":
                fit[key] = row["sort_order"]
            elif key == "images":
                fit[key] = images(row)
            elif key == "preconditions":
                if row["id"] in jobs:
                    fit[key] = jobs[row["id"]]
            elif key == "gone":
                # Binned in the app. Exported so a session reading this file
                # does not recommend an outfit Max has thrown out.
                if row["gone_at"]:
                    fit[key] = True

        fits.append(fit)

    live = [f for f in fits if not f.get("gone")]
    return {
        "generated": generated,
        "owner": "Max",
        "schemaNote": (
            "Fits are ordered slots. Roles: outer, layer, top, base, bottom, shoe, "
            "belt, accessory. 'position' is the layering/display order. itemId "
            "references wardrobe.json items[].id. 'id' is the database key and the "
            "only reliable one — 'code' survives only on the fits that were "
            "imported from the 2026-08-27 markdown."
        ),
        "renderNote": (
            "'images' carries every picture of a fit and 'images.display' is the "
            "one a screen should draw. A hero or layered render is a GENERATED "
            "IMAGE, never a photograph of Max wearing the clothes, and "
            "images.heroIsGenerated says so. 'images.upload' is a picture Max "
            "uploaded in the app: it outranks the hero and is deliberately NOT "
            "labelled — whether it is a photograph or a render of his own is not "
            "recorded. images.looks is 2 only when a base/layered pair should be "
            "shown as a pair."
        ),
        "wardrobeNote": (
            "'wardrobe' is derived from the occasion tags of a fit and its "
            "garments, exactly as the /fits screen derives it — it is not a "
            "stored flag. A fit is golf when it carries the golf occasion, or is "
            "built on a crested club garment."
        ),
        "counts": {
            "total": len(fits),
            "live": len(live),
            "golf": sum(1 for f in live if f["wardrobe"] == "golf"),
            "withComposition": sum(1 for f in live if f.get("items")),
            "twoLooks": sum(1 for f in live if f["images"].get("looks") == 2),
            "uploaded": sum(1 for f in live if f["images"].get("upload")),
            "noImage": sum(1 for f in live if not f["images"].get("display")),
        },
        "fits": fits,
    }


def fit_code(fit_id: str) -> str | None:
    """The 2026-08-27 file's short code, where the id still carries one.

    `fit_c1_slate-and-biker` -> `c1`. The killer-looks fits (`fit_the_shawl`)
    had their codes mapped by hand in fits_json.KILLER_LOOK_IDS and that map is
    read back rather than reversed by rule. Everything else has no code, which
    is not a gap: `id` is the key now.
    """
    from wardrobe.fits_json import KILLER_LOOK_IDS

    for code, mapped in KILLER_LOOK_IDS.items():
        if mapped == fit_id:
            return code
    parts = fit_id.split("_")
    if len(parts) >= 3 and parts[0] == "fit":
        head = parts[1]
        if head[:1].isalpha() and head[1:].isdigit():
            # Upper case, as the file wrote them: C1, K7, S4. The killer-look
            # codes above are the exception and are returned as mapped.
            return head.upper()
    return None


# JSON key -> the field_name fit_field_sources records a provenance under.
SOURCE_FIELD_FOR = {
    "temp": "temp_bands",
    "rainSafe": "rain_safe",
    "formalityRank": "formality_rank",
    "goodFor": "good_for",
    "badFor": "bad_for",
    "items": "composition",
    "commentary": "commentary",
    "category": "category_code",
    "style": "style",
}

# Sets in the database, lists in the JSON. fit_occasions and fit_temp_bands
# have no ordering column, so the export sorts them and a different order in
# the hand file is a difference in nothing.
UNORDERED = ("temp", "goodFor", "badFor")


def field_sources(conn) -> dict[str, dict[str, str]]:
    """Where each fit's field came from: imported, derived, manual, suggested."""
    out: dict[str, dict[str, str]] = {}
    for row in db.fetch_all(
        conn, "SELECT fit_id, field_name, source FROM fit_field_sources"
    ):
        out.setdefault(row["fit_id"], {})[row["field_name"]] = row["source"]
    return out


def compare(
    exported: dict, original_path: Path, sources: dict[str, dict[str, str]] | None = None
) -> tuple[list[str], list[str]]:
    """Value-by-value against the file this supersedes, keyed by fit id.

    Returns (problems, drift). The two are different things and collapsing them
    would make this check useless within a day:

      * A field the database still records as `imported` came from that file and
        nothing has touched it since. If it disagrees, something corrupted it.
      * A field recorded as `derived`, `manual` or `suggested` is *meant* to
        disagree — the app worked it out, or Max set it. So is a value the file
        left null and the database has since filled in: eight fits lost their
        garment lists in a compaction and Max has been filling them back in from
        the pictures, and that progress is not a fault to report.

    App-owned keys are skipped entirely, and so is every fit the original never
    had. The question this answers is "is anything the 2026-08-27 file said
    still true", not "does the database contain only what it contained then".
    """
    sources = sources or {}
    original = json.loads(original_path.read_text(encoding="utf-8"))
    problems: list[str] = []
    drift: list[str] = []

    from wardrobe.fits_json import KILLER_LOOK_IDS

    by_id = {}
    for entry in original["fits"]:
        render = entry.get("render")
        if render:
            by_id[render.rsplit("_render.", 1)[0]] = entry
        else:
            by_id[KILLER_LOOK_IDS.get(entry["code"], entry["code"])] = entry

    exported_by_id = {f["id"]: f for f in exported["fits"]}

    missing = set(by_id) - set(exported_by_id)
    if missing:
        problems.append(f"missing from export: {sorted(missing)}")

    for fit_id in sorted(set(by_id) & set(exported_by_id)):
        a = by_id[fit_id]
        b = {k: v for k, v in exported_by_id[fit_id].items() if k not in APP_OWNED_KEYS}
        for key in sorted(set(a) & set(b)):
            before, after = a[key], b[key]
            if key in UNORDERED and before is not None and after is not None:
                if sorted(before) == sorted(after):
                    continue
            if key == "items" and after:
                # The hand file kept a fit's optional piece in a separate
                # `alternate` prose line; fits_json._alternates() read the item
                # id out of that line and made it a slot. Comparing the slots
                # against the file's `items` therefore has to leave the
                # alternates out, or the importer's own work reads as a
                # difference. Two fits are affected, both from killer-looks.md.
                after = [slot for slot in after if not slot.get("isAlternate")]
            if before == after:
                continue
            line = f"{fit_id}.{key}: {before!r} -> {after!r}"
            provenance = sources.get(fit_id, {}).get(SOURCE_FIELD_FOR.get(key, key))
            if before is None or (provenance and provenance != "imported"):
                drift.append(line)
            else:
                problems.append(line)
    return problems, drift


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=None, help="output path")
    parser.add_argument("--compare", default=None, help="verify against this JSON file")
    parser.add_argument("--database-url", default=None)
    parser.add_argument("--generated", default=None, help="override the generated date")
    args = parser.parse_args()

    generated = args.generated or datetime.now(ZoneInfo(config.TIMEZONE)).date().isoformat()
    out = Path(args.out) if args.out else config.REPO_ROOT / "export" / "fits.json"

    with db.connect(args.database_url) as conn:
        payload = build_payload(conn, generated)
        sources = field_sources(conn) if args.compare else {}

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    counts = payload["counts"]
    print(
        f"Wrote {out}  ({counts['total']} fits, {counts['live']} live, "
        f"{counts['golf']} golf, {counts['twoLooks']} with two looks, "
        f"generated {generated})"
    )

    if args.compare:
        problems, drift = compare(payload, Path(args.compare), sources)
        if drift:
            print(
                f"\n{len(drift)} field(s) the file is behind on — derived, "
                "hand-set, or filled in since:"
            )
            for d in drift[:20]:
                print("  ·", d[:160])
            if len(drift) > 20:
                print(f"  … and {len(drift) - 20} more")
        if problems:
            print(f"\nRound-trip FAILED against {args.compare}:")
            for p in problems[:60]:
                print("  *", p)
            if len(problems) > 60:
                print(f"  … and {len(problems) - 60} more")
            return 2
        tail = " apart from the drift above" if drift else ""
        print(
            f"\nRound-trip clean: every imported field {args.compare} states "
            f"still matches{tail}."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

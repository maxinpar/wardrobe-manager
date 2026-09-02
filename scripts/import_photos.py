"""Copy photos out of Google Drive into the app's own store and index them.

    python scripts/import_photos.py             # dry run
    python scripts/import_photos.py --commit    # copy files and write rows

The Drive folder is treated as strictly read-only: files are COPIED, never
moved, and nothing is ever written back. The script snapshots the source folder
(name, size, mtime) before and after and reports any difference, so "nothing in
Drive was modified" is verified rather than assumed.

Matching rule (unchanged from the old build_app.py): a file belongs to an item
when its filename starts with that item's photoPrefix. Generated catalogue
renders live in Retail/ as <retailPrefix>_retail.<ext> and are flagged
is_render — the app must never present one as a photo of the actual garment.

A fit carries up to two renders. <fit_id>_render is the canonical one; a fit
built around an optional layer also has <fit_id>_layered_render, the same fit
with the layer on. Both are generated, and both are labelled as such.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageOps  # noqa: E402

from wardrobe import config, db  # noqa: E402

def is_stale(target: Path, source: Path) -> bool:
    """True when `target` is missing, a different size, or older than `source`.

    Existence alone is not enough: a regenerated render keeps its filename, so
    an exists-only check leaves the old picture in the store and the app goes on
    showing it. Thumbnails had the same fault and it was worse, because list
    views are all thumbnails.
    """
    if not target.exists():
        return True
    t, s = target.stat(), source.stat()
    return t.st_size != s.st_size or t.st_mtime < s.st_mtime - 1


THUMB_BOX = (500, 500)
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".gif"}

# Filename suffix -> photo_angles.code. Checked longest-first.
ANGLE_HINTS = [
    ("worn-closed", "worn-closed"),
    ("worn-front", "worn-front"),
    ("worn-side", "worn-side"),
    ("worn-back", "worn-back"),
    ("underside", "underside"),
    ("hanger", "hanger"),
    ("buckle", "buckle"),
    ("damage", "damage"),
    ("detail", "detail"),
    ("label", "label"),
    ("retail", "render"),
    ("full", "full"),
]

ANGLE_ORDER = {
    "label": 10,
    "hanger": 20,
    "worn-front": 30,
    "worn-side": 40,
    "worn-back": 50,
    "worn-closed": 60,
    "buckle": 70,
    "full": 80,
    "underside": 90,
    "detail": 100,
    "damage": 110,
    "render": 200,  # renders sort last: they are illustrations, not photos
}


def snapshot(root: Path) -> dict[str, tuple[int, int]]:
    """(size, mtime) for every file under root — used to prove we didn't write."""
    out = {}
    for path in root.rglob("*"):
        if path.is_file():
            stat = path.stat()
            out[str(path.relative_to(root))] = (stat.st_size, int(stat.st_mtime))
    return out


def guess_angle(filename: str, prefix: str) -> str | None:
    tail = filename[len(prefix):].lower() if filename.startswith(prefix) else filename.lower()
    for hint, code in ANGLE_HINTS:
        if hint in tail:
            return code
    return None


def make_thumb(source: Path, target: Path) -> tuple[int, int] | None:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(source) as img:
            img = ImageOps.exif_transpose(img)
            img = img.convert("RGB")
            img.thumbnail(THUMB_BOX)
            img.save(target, "JPEG", quality=82, optimize=True)
            return img.size
    except Exception as exc:  # a corrupt or unreadable frame must not stop the run
        print(f"    ! could not thumbnail {source.name}: {exc}")
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true", help="copy files and write rows")
    parser.add_argument("--database-url", default=None)
    args = parser.parse_args()

    source_root = config.photo_source_root()
    if not source_root.exists():
        raise SystemExit(f"Photo source {source_root} is not reachable.")

    store = config.photo_store()
    print(f"Source: {source_root}  (read-only)")
    print(f"Store:  {store}")
    print(f"Mode:   {'COMMIT' if args.commit else 'DRY RUN — nothing copied or written'}\n")

    before = snapshot(source_root)

    copied = 0
    indexed = 0
    skipped_existing = 0
    items_with_photos = 0

    with db.connect(args.database_url) as conn:
        folders = {
            r["code"]: r["photo_folder"]
            for r in db.fetch_all(conn, "SELECT code, photo_folder FROM categories")
        }
        listings = {}
        for cat, folder in folders.items():
            path = source_root / folder
            listings[cat] = sorted(
                p for p in path.iterdir()
                if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
            ) if path.exists() else []

        retail_dir = source_root / "Retail"
        retail_files = sorted(
            p for p in retail_dir.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
        ) if retail_dir.exists() else []

        items = db.fetch_all(
            conn,
            "SELECT id, cat_code, photo_prefix, retail_prefix, no_photo FROM items ORDER BY id",
        )

        # A render stands for one specific garment, so it must never attach to
        # more than one. Five items (three loafers, two Nikes) share a group
        # retail prefix; for those, only <item_id>_retail is accepted.
        prefix_owners: dict[str, int] = {}
        for item in items:
            if item["retail_prefix"]:
                prefix_owners[item["retail_prefix"]] = (
                    prefix_owners.get(item["retail_prefix"], 0) + 1
                )
        shared_prefixes = {p for p, n in prefix_owners.items() if n > 1}
        if shared_prefixes:
            print(
                f"Ignoring {len(shared_prefixes)} retail prefix(es) shared by several "
                f"items; those items match <id>_retail only:"
            )
            for p in sorted(shared_prefixes):
                print("   ", p)
            print()

        for item in items:
            matches = []
            prefix = item["photo_prefix"]
            if prefix:
                for path in listings.get(item["cat_code"], []):
                    if path.name.startswith(prefix):
                        matches.append((path, folders[item["cat_code"]], False))

            accepted = [f"{item['id']}_retail"]
            if item["retail_prefix"] and item["retail_prefix"] not in shared_prefixes:
                accepted.append(item["retail_prefix"])
            for path in retail_files:
                if any(path.name.startswith(a) for a in accepted):
                    matches.append((path, "Retail", True))

            if not matches:
                continue
            items_with_photos += 1

            ordered = []
            for path, folder, is_render in matches:
                angle = "render" if is_render else guess_angle(path.name, prefix or "")
                ordered.append((ANGLE_ORDER.get(angle, 150), path.name, path, folder, angle, is_render))
            ordered.sort()

            for sort_index, (_, _, path, folder, angle, is_render) in enumerate(ordered):
                existing = db.fetch_one(
                    conn,
                    "SELECT id, stored_path FROM photos "
                    "WHERE item_id = %s AND source_folder = %s AND source_filename = %s",
                    (item["id"], folder, path.name),
                )

                rel_original = Path("originals") / item["id"] / path.name
                rel_thumb = (Path("thumbs") / item["id"] / path.name).with_suffix(".jpg")
                target = store / rel_original
                thumb_target = store / rel_thumb

                if args.commit:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if is_stale(target, path):
                        shutil.copy2(path, target)  # copy, never move
                        copied += 1
                    if is_stale(thumb_target, target):
                        make_thumb(target, thumb_target)

                size = None
                if args.commit and target.exists():
                    try:
                        with Image.open(target) as img:
                            size = img.size
                    except Exception:
                        size = None

                params = (
                    angle,
                    sort_index,
                    is_render,
                    str(rel_original).replace("\\", "/"),
                    str(rel_thumb).replace("\\", "/"),
                    size[0] if size else None,
                    size[1] if size else None,
                    path.stat().st_size,
                )

                if existing:
                    conn.execute(
                        "UPDATE photos SET angle_code = %s, sort_order = %s, is_render = %s, "
                        "stored_path = %s, thumb_path = %s, width = %s, height = %s, bytes = %s "
                        "WHERE id = %s",
                        params + (existing["id"],),
                    )
                    skipped_existing += 1
                else:
                    conn.execute(
                        "INSERT INTO photos (item_id, source_folder, source_filename, "
                        "angle_code, sort_order, is_render, stored_path, thumb_path, "
                        "width, height, bytes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (item["id"], folder, path.name) + params,
                    )
                    indexed += 1

        # ---- fits: hero renders, layered renders and worn photos --------
        # fit_<slug>_render.<ext>         generated render — NOT evidence it was worn
        # fit_<slug>_layered_render.<ext> the same fit WITH its optional layer
        # fit_<slug>_NN_<angle>.jpg       real worn photo, belongs to the wear event
        fits_dir = source_root / "Fits"
        fit_files = (
            sorted(
                p for p in fits_dir.iterdir()
                if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
            )
            if fits_dir.exists()
            else []
        )
        unfiled = []
        heroes = 0
        layered_renders = 0
        worn_photos = 0

        for path in fit_files:
            if not path.name.startswith("fit_"):
                # Gemini names every export identically. An unnamed file cannot
                # be attributed to a fit, and guessing is how photos get lost.
                unfiled.append(path.name)
                continue

            # _layered_render is tested FIRST because it also ends with
            # "_render": the other order strips only the shorter suffix and
            # leaves a slug ending in "_layered", which matches no fit. That is
            # what made all twelve layered files report as unfiled.
            stem = path.stem
            is_layered = stem.endswith("_layered_render")
            is_render = is_layered or stem.endswith("_render")
            if is_layered:
                slug = stem[: -len("_layered_render")]
            elif is_render:
                slug = stem[: -len("_render")]
            else:
                slug = stem.rsplit("_", 2)[0]

            rel = Path("fits") / path.name
            rel_thumb = (Path("fits") / "thumbs" / path.name).with_suffix(".jpg")
            if args.commit:
                (store / rel).parent.mkdir(parents=True, exist_ok=True)
                if is_stale(store / rel, path):
                    shutil.copy2(path, store / rel)  # copy, never move
                    copied += 1
                if is_stale(store / rel_thumb, store / rel):
                    make_thumb(store / rel, store / rel_thumb)

            stored = str(rel).replace("\\", "/")
            thumb = str(rel_thumb).replace("\\", "/")

            if is_render:
                fit = db.fetch_one(conn, "SELECT id FROM fits WHERE id = %s", (slug,))
                if fit is None:
                    unfiled.append(f"{path.name} (no fit {slug!r})")
                    continue
                if is_layered:
                    # The variant, never the hero: the base render stays
                    # canonical because the fit has to stand up without
                    # the layer.
                    conn.execute(
                        "UPDATE fits SET layered_image_path = %s, "
                        "layered_thumb_path = %s WHERE id = %s",
                        (stored, thumb, slug),
                    )
                    layered_renders += 1
                else:
                    conn.execute(
                        "UPDATE fits SET hero_image_path = %s, hero_thumb_path = %s, "
                        "hero_is_generated = true WHERE id = %s",
                        (stored, thumb, slug),
                    )
                    heroes += 1
            else:
                # A worn photo belongs to the wear event, never to the fit.
                event = db.fetch_one(
                    conn,
                    "SELECT id FROM wear_events WHERE fit_photo_slug = %s "
                    "ORDER BY worn_on DESC LIMIT 1",
                    (slug,),
                )
                if event is None:
                    unfiled.append(f"{path.name} (no wear event for {slug!r})")
                    continue
                angle = guess_angle(path.name, slug)
                conn.execute(
                    "INSERT INTO wear_event_photos (wear_event_id, stored_path, "
                    "thumb_path, source_filename, angle_code, sort_order) "
                    "VALUES (%s, %s, %s, %s, %s, 0) "
                    "ON CONFLICT (wear_event_id, source_filename) DO UPDATE SET "
                    "stored_path = EXCLUDED.stored_path, thumb_path = EXCLUDED.thumb_path",
                    (event["id"], stored, thumb, path.name, angle),
                )
                worn_photos += 1

        print(
            f"\nFits folder: {heroes} hero render(s), "
            f"{layered_renders} layered render(s), {worn_photos} worn photo(s)"
        )
        if unfiled:
            print("  Not filed — a fit photo must be named for its fit:")
            for name in unfiled:
                print("   ", name)
            print(
                "    fit_<slug>_render.<ext>          generated render\n"
                "    fit_<slug>_layered_render.<ext>  the same fit, layer on\n"
                "    fit_<slug>_NN_<angle>.jpg        real worn photo"
            )

        # ---- prune rows whose file no longer belongs to the item ---------
        # The five group-shot shoes were given individual prefixes on
        # 2026-08-26, which orphans their rows against the old group stems.
        # Photo rows are derived from disk, so dropping a stale one destroys
        # nothing: the file itself is untouched, in Drive and in the store.
        stale = db.fetch_all(
            conn,
            """
            SELECT p.id, p.item_id, p.source_filename, i.photo_prefix, i.retail_prefix
            FROM photos p JOIN items i ON i.id = p.item_id
            """,
        )
        pruned = []
        for row in stale:
            prefixes = [
                row["photo_prefix"],
                row["retail_prefix"],
                f"{row['item_id']}_retail",
                row["item_id"],
            ]
            if not any(
                p and row["source_filename"].startswith(p) for p in prefixes
            ):
                pruned.append(f"{row['item_id']}  {row['source_filename']}")
                if args.commit:
                    conn.execute("DELETE FROM photos WHERE id = %s", (row["id"],))

        if pruned:
            print(f"\nPhoto rows no longer matching their item ({len(pruned)}):")
            for line in pruned:
                print("   ", line)
            print("    The files are untouched — only the index rows go.")

        no_photo_rows = db.fetch_all(
            conn,
            "SELECT i.id FROM items i LEFT JOIN photos p ON p.item_id = i.id "
            "WHERE p.id IS NULL ORDER BY i.id",
        )

        print(f"Items with at least one matched file: {items_with_photos}")
        print(f"New photo rows:      {indexed}")
        print(f"Refreshed rows:      {skipped_existing}")
        print(f"Files copied:        {copied}")
        print(f"\nItems with no photo at all: {len(no_photo_rows)}")
        for row in no_photo_rows:
            print("   ", row["id"])

        if args.commit:
            conn.commit()
            print("\nCommitted.")
        else:
            conn.rollback()
            print("\nDry run — rolled back. Re-run with --commit to copy and index.")

    after = snapshot(source_root)
    if before == after:
        print(f"\nSource folder verified unchanged: {len(before)} files, same size and mtime.")
    else:
        changed = {k for k in before.keys() | after.keys() if before.get(k) != after.get(k)}
        print("\n!! SOURCE FOLDER CHANGED — this should never happen:")
        for name in sorted(changed):
            print("   ", name)
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

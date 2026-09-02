"""The fits round-trip check, which has to tell three kinds of difference apart.

A field the database still records as `imported` came from data/fits.json and
nothing has touched it since: if it disagrees, something corrupted it. A field
the app derived or Max set by hand is *meant* to disagree. And a slot the
importer created by reading an item id out of a free-text `alternate` line is
the importer working, not a difference at all.

Runs offline — no database needed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import export_fits  # noqa: E402


def source_file(tmp_path: Path, *fits) -> Path:
    path = tmp_path / "fits.json"
    path.write_text(
        json.dumps({"generated": "2026-08-27", "owner": "Max", "fits": list(fits)}),
        encoding="utf-8",
    )
    return path


def original(**overrides) -> dict:
    entry = {
        "code": "C1",
        "name": "Slate and biker",
        "render": "fit_c1_slate-and-biker_render.png",
        "goodFor": ["casual", "weekend"],
    }
    entry.update(overrides)
    return entry


def exported(**overrides) -> dict:
    entry = {
        "code": "C1",
        "id": "fit_c1_slate-and-biker",
        "name": "Slate and biker",
        "render": "fit_c1_slate-and-biker_render.png",
        "goodFor": ["casual", "weekend"],
        "wardrobe": "everyday",
        "images": {"display": "fits/fit_c1_slate-and-biker_render.png", "looks": 1},
    }
    entry.update(overrides)
    return entry


def payload(*fits) -> dict:
    return {"generated": "2026-09-02", "fits": list(fits)}


def test_identical_files_have_nothing_to_report(tmp_path):
    problems, drift = export_fits.compare(
        payload(exported()), source_file(tmp_path, original())
    )
    assert problems == []
    assert drift == []


def test_app_owned_keys_are_never_a_difference(tmp_path):
    """id, wardrobe and images have never been in the hand file."""
    problems, drift = export_fits.compare(
        payload(exported(wardrobe="golf", images={"looks": 2})),
        source_file(tmp_path, original()),
    )
    assert problems == []
    assert drift == []


def test_a_changed_imported_field_is_a_problem(tmp_path):
    problems, _ = export_fits.compare(
        payload(exported(name="Something else")),
        source_file(tmp_path, original()),
        {"fit_c1_slate-and-biker": {"name": "imported"}},
    )
    assert problems == ["fit_c1_slate-and-biker.name: 'Slate and biker' -> 'Something else'"]


def test_a_derived_field_is_drift_not_a_problem(tmp_path):
    problems, drift = export_fits.compare(
        payload(exported(goodFor=["casual", "dinner"])),
        source_file(tmp_path, original()),
        {"fit_c1_slate-and-biker": {"good_for": "derived"}},
    )
    assert problems == []
    assert len(drift) == 1


def test_a_field_the_file_left_null_is_drift(tmp_path):
    """The eight fits whose garment lists were lost are being filled back in."""
    problems, drift = export_fits.compare(
        payload(exported(items=[{"role": "top", "position": 1, "itemId": "x"}])),
        source_file(tmp_path, original(items=None)),
    )
    assert problems == []
    assert len(drift) == 1


def test_occasion_order_is_not_a_difference(tmp_path):
    """fit_occasions has no ordering column; the export sorts."""
    problems, drift = export_fits.compare(
        payload(exported(goodFor=["casual", "weekend"])),
        source_file(tmp_path, original(goodFor=["weekend", "casual"])),
    )
    assert problems == []
    assert drift == []


def test_an_importer_made_alternate_slot_is_not_a_difference(tmp_path):
    """The hand file kept the optional piece in a prose `alternate` line."""
    slots = [
        {"role": "top", "position": 1, "itemId": "tissaia-blue-vneck"},
        {"role": "outer", "position": 1, "itemId": "outerwear_02", "isAlternate": True},
    ]
    problems, drift = export_fits.compare(
        payload(exported(items=slots)),
        source_file(
            tmp_path,
            original(items=[{"role": "top", "position": 1, "itemId": "tissaia-blue-vneck"}]),
        ),
    )
    assert problems == []
    assert drift == []


def test_a_fit_the_file_had_and_the_export_lost_is_a_problem(tmp_path):
    problems, _ = export_fits.compare(payload(), source_file(tmp_path, original()))
    assert problems == ["missing from export: ['fit_c1_slate-and-biker']"]


def test_code_is_read_back_from_the_id(tmp_path):
    assert export_fits.fit_code("fit_c1_slate-and-biker") == "C1"
    assert export_fits.fit_code("fit_the_shawl") == "kl1"
    assert export_fits.fit_code("fit_augusta") is None

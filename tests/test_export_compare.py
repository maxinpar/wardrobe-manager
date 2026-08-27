"""The round-trip comparison, which has to tell two kinds of difference apart.

A field Max has set by hand is *meant* to disagree with data/wardrobe.json —
that is what setting it by hand means. A field that disagrees for no recorded
reason is the corruption the check exists to catch. Collapsing the two would
make the check fail forever after his first correction, and a check that always
fails is a check nobody reads.

Runs offline — no database needed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import export_wardrobe  # noqa: E402


def payload(*items) -> dict:
    return {"generated": "2026-08-27", "owner": "Max", "profile": {}, "items": list(items)}


def source_file(tmp_path: Path, *items) -> Path:
    path = tmp_path / "wardrobe.json"
    path.write_text(json.dumps(payload(*items)), encoding="utf-8")
    return path


def trouser(**overrides) -> dict:
    row = {"id": "trousers_04_oxford-stone", "name": "Oxford chino", "verdict": "Tailor"}
    row.update(overrides)
    return row


def test_identical_files_have_nothing_to_report(tmp_path):
    original = source_file(tmp_path, trouser())
    problems, deliberate = export_wardrobe.compare(payload(trouser()), original)
    assert problems == []
    assert deliberate == []


def test_a_hand_set_field_is_a_divergence_not_a_failure(tmp_path):
    original = source_file(tmp_path, trouser())
    problems, deliberate = export_wardrobe.compare(
        payload(trouser(verdict="Keep")),
        original,
        {"trousers_04_oxford-stone": {"verdict"}},
    )
    assert problems == []
    assert deliberate == ["trousers_04_oxford-stone.verdict: 'Tailor' -> 'Keep'"]


def test_the_same_difference_without_a_hand_set_record_is_a_failure(tmp_path):
    """No provenance row means nobody decided this. That is the thing to catch."""
    original = source_file(tmp_path, trouser())
    problems, deliberate = export_wardrobe.compare(payload(trouser(verdict="Keep")), original)
    assert deliberate == []
    assert problems == ["trousers_04_oxford-stone.verdict: 'Tailor' -> 'Keep'"]


def test_an_override_on_one_field_does_not_excuse_another(tmp_path):
    original = source_file(tmp_path, trouser())
    problems, _ = export_wardrobe.compare(
        payload(trouser(verdict="Keep", name="Something else")),
        original,
        {"trousers_04_oxford-stone": {"verdict"}},
    )
    assert problems == ["trousers_04_oxford-stone.name: 'Oxford chino' -> 'Something else'"]


def test_the_bin_flag_is_not_reported_as_a_difference(tmp_path):
    """`gone` is set in the app, so the source file has never heard of it."""
    original = source_file(tmp_path, trouser())
    problems, deliberate = export_wardrobe.compare(payload(trouser(gone=True)), original)
    assert problems == []
    assert deliberate == []


def test_a_missing_item_is_still_a_failure(tmp_path):
    original = source_file(tmp_path, trouser(), {"id": "belts_01", "name": "A belt"})
    problems, _ = export_wardrobe.compare(payload(trouser()), original)
    assert problems == ["missing from export: ['belts_01']"]

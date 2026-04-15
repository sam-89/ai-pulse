"""Unit tests for scripts/validate_registry.py."""

import json
import sys
import tempfile
from pathlib import Path

# Ensure scripts/ is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_registry import validate_entry, validate_file  # noqa: E402


def _valid_entry(**overrides) -> dict:
    """Return a fully valid registry entry, optionally overriding fields."""
    entry = {
        "id": "test-tool",
        "name": "Test Tool",
        "category": "tool",
        "description": "A valid test tool description that is long enough.",
        "url": "https://example.com",
        "tags": ["ai", "testing"],
        "added_date": "2024-01-15",
        "stars_approx": 100,
        "pricing": "free",
        "maturity": "stable",
    }
    entry.update(overrides)
    return entry


def _write_json(data: list[dict]) -> Path:
    """Write data to a temp file and return its Path. Caller owns cleanup."""
    tf = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, tf)
    tf.flush()
    tf.close()
    return Path(tf.name)


# ---------------------------------------------------------------------------
# validate_entry tests
# ---------------------------------------------------------------------------

def test_valid_entry():
    errors, warnings = validate_entry(_valid_entry(), "test.json", 0)
    assert errors == [], f"Unexpected errors: {errors}"
    assert warnings == [], f"Unexpected warnings: {warnings}"


def test_missing_required_fields():
    required = ["id", "name", "category", "description", "url", "tags", "added_date", "stars_approx"]
    for field in required:
        entry = _valid_entry()
        del entry[field]
        errors, _ = validate_entry(entry, "test.json", 0)
        assert any(field in e for e in errors), f"Expected error for missing '{field}', got: {errors}"


def test_invalid_category():
    errors, _ = validate_entry(_valid_entry(category="not-a-category"), "test.json", 0)
    assert any("category" in e.lower() or "not-a-category" in e for e in errors)


def test_invalid_pricing():
    errors, _ = validate_entry(_valid_entry(pricing="unknown"), "test.json", 0)
    assert any("pricing" in e.lower() or "unknown" in e for e in errors)


def test_invalid_maturity():
    errors, _ = validate_entry(_valid_entry(maturity="legacy"), "test.json", 0)
    assert any("maturity" in e.lower() or "legacy" in e for e in errors)


def test_url_must_be_https():
    errors, _ = validate_entry(_valid_entry(url="ftp://example.com"), "test.json", 0)
    assert any("http" in e.lower() or "url" in e.lower() for e in errors)


def test_description_too_long():
    long_desc = "x" * 281
    _, warnings = validate_entry(_valid_entry(description=long_desc), "test.json", 0)
    assert any("description" in w.lower() for w in warnings)


def test_description_too_short():
    _, warnings = validate_entry(_valid_entry(description="Too short"), "test.json", 0)
    assert any("description" in w.lower() for w in warnings)


def test_curator_note_too_long():
    long_note = "a" * 141
    _, warnings = validate_entry(_valid_entry(curator_note=long_note), "test.json", 0)
    assert any("curator_note" in w for w in warnings)


def test_tags_not_a_list():
    errors, _ = validate_entry(_valid_entry(tags="ai,testing"), "test.json", 0)
    assert any("tags" in e.lower() for e in errors)


def test_empty_tags():
    errors, _ = validate_entry(_valid_entry(tags=[]), "test.json", 0)
    assert any("tags" in e.lower() for e in errors)


def test_stars_negative():
    errors, _ = validate_entry(_valid_entry(stars_approx=-1), "test.json", 0)
    assert any("stars_approx" in e for e in errors)


def test_invalid_date_format():
    errors, _ = validate_entry(_valid_entry(added_date="15-01-2024"), "test.json", 0)
    assert any("added_date" in e or "date" in e.lower() for e in errors)


def test_placeholder_curator_note():
    _, warnings = validate_entry(_valid_entry(curator_note="⚠️ needs review"), "test.json", 0)
    assert any("placeholder" in w.lower() or "curator" in w.lower() for w in warnings)


def test_tag_not_lowercase():
    errors, _ = validate_entry(_valid_entry(tags=["AI", "testing"]), "test.json", 0)
    assert any("AI" in e or "lowercase" in e.lower() for e in errors)


def test_deprecated_entry_warns():
    _, warnings = validate_entry(_valid_entry(deprecated=True), "test.json", 0)
    assert any("deprecated" in w.lower() for w in warnings)


# ---------------------------------------------------------------------------
# validate_file tests
# ---------------------------------------------------------------------------

def test_duplicate_ids_in_file():
    entry1 = _valid_entry(id="dup-id")
    entry2 = _valid_entry(id="dup-id", name="Another Tool")
    path = _write_json([entry1, entry2])
    try:
        errors, _ = validate_file(path)
        assert any("dup-id" in e and "Duplicate" in e for e in errors), (
            f"Expected duplicate ID error, got: {errors}"
        )
    finally:
        path.unlink()

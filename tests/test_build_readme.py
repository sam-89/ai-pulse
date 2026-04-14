"""Unit tests for scripts/build_readme.py."""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from build_readme import (  # noqa: E402
    render_entry,
    render_category_section,
    render_recently_added,
    load_registry,
)


def _minimal_entry(**overrides) -> dict:
    entry = {
        "id": "my-tool",
        "name": "My Tool",
        "category": "tool",
        "description": "Does something useful.",
        "url": "https://example.com/tool",
        "tags": ["ai"],
        "added_date": "2024-03-01",
        "stars_approx": 0,
        "pricing": "free",
        "maturity": "stable",
    }
    entry.update(overrides)
    return entry


def _write_registry(registry_dir: Path, filename: str, data: list[dict]) -> Path:
    path = registry_dir / filename
    path.write_text(json.dumps(data))
    return path


# ---------------------------------------------------------------------------
# render_entry tests
# ---------------------------------------------------------------------------

def test_render_entry_basic():
    result = render_entry(_minimal_entry())
    assert "My Tool" in result
    assert "https://example.com/tool" in result
    assert "Does something useful." in result


def test_render_entry_with_all_fields():
    entry = _minimal_entry(
        github_url="https://github.com/org/my-tool",
        curator_note="This is a great tool for testing purposes in AI.",
        stars_approx=1500,
    )
    result = render_entry(entry)
    assert "GitHub" in result
    assert "1,500" in result
    assert "💡" in result
    assert "This is a great tool" in result


def test_render_entry_no_github_url():
    result = render_entry(_minimal_entry())
    assert "GitHub" not in result


def test_render_entry_no_curator_note():
    result = render_entry(_minimal_entry())
    assert "💡" not in result


def test_render_entry_placeholder_note_skipped():
    result = render_entry(_minimal_entry(curator_note="⚠️ needs human review"))
    assert "💡" not in result
    assert "⚠️" not in result


# ---------------------------------------------------------------------------
# render_category_section tests
# ---------------------------------------------------------------------------

def test_render_category_section():
    entries = [
        _minimal_entry(name="Low Stars", stars_approx=10),
        _minimal_entry(id="high-stars", name="High Stars", stars_approx=9000),
    ]
    result = render_category_section("tool", entries)
    assert "🛠️ Tools & Utilities" in result
    assert "2 entries" in result
    # High stars should appear before low stars
    assert result.index("High Stars") < result.index("Low Stars")


# ---------------------------------------------------------------------------
# load_registry tests
# ---------------------------------------------------------------------------

def test_load_registry_excludes_schema():
    with tempfile.TemporaryDirectory() as tmpdir:
        reg_dir = Path(tmpdir)
        _write_registry(reg_dir, "schema.json", [_minimal_entry(id="schema-entry")])
        _write_registry(reg_dir, "tools.json", [_minimal_entry()])
        result = load_registry(reg_dir)
        ids = [e["id"] for entries in result.values() for e in entries]
        assert "schema-entry" not in ids
        assert "my-tool" in ids


def test_load_registry_excludes_audit():
    with tempfile.TemporaryDirectory() as tmpdir:
        reg_dir = Path(tmpdir)
        _write_registry(reg_dir, "audit.json", [_minimal_entry(id="audit-entry")])
        _write_registry(reg_dir, "tools.json", [_minimal_entry()])
        result = load_registry(reg_dir)
        ids = [e["id"] for entries in result.values() for e in entries]
        assert "audit-entry" not in ids


def test_load_registry_excludes_trending():
    with tempfile.TemporaryDirectory() as tmpdir:
        reg_dir = Path(tmpdir)
        _write_registry(reg_dir, "trending.json", [_minimal_entry(id="trending-entry")])
        _write_registry(reg_dir, "tools.json", [_minimal_entry()])
        result = load_registry(reg_dir)
        ids = [e["id"] for entries in result.values() for e in entries]
        assert "trending-entry" not in ids


# ---------------------------------------------------------------------------
# render_recently_added tests
# ---------------------------------------------------------------------------

def test_recently_added_top_5():
    entries_by_cat: dict[str, list[dict]] = {"tool": []}
    for i in range(8):
        entries_by_cat["tool"].append(
            _minimal_entry(
                id=f"tool-{i}",
                name=f"Tool {i}",
                added_date=f"2024-0{(i % 9) + 1}-01",
            )
        )

    result = render_recently_added(entries_by_cat, n=5)
    # Count bullet lines
    bullet_lines = [line for line in result.splitlines() if line.startswith("- ")]
    assert len(bullet_lines) == 5, f"Expected 5 recent entries, got {len(bullet_lines)}"

#!/usr/bin/env python3
"""
AI-Pulse: build_readme.py
--------------------------
Reads all JSON files in /registry/ and compiles them into the main README.md.
Run this after approving new entries.

Usage:
    python scripts/build_readme.py
    python scripts/build_readme.py --output README.md
"""

import json
import datetime
import argparse
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CATEGORY_ORDER = [
    "llm",
    "agent-framework",
    "vector-db",
    "mcp-server",
    "tool",
    "dataset",
    "paper",
    "course",
    "project",
]

CATEGORY_LABELS = {
    "llm": "🧠 Large Language Models",
    "agent-framework": "🤖 Agent Frameworks & Orchestration",
    "vector-db": "🔍 Vector Databases & Embedding Stores",
    "mcp-server": "🔌 MCP Servers",
    "tool": "🛠️ Tools & Utilities",
    "dataset": "📊 Datasets & Benchmarks",
    "paper": "📄 Must-Read Papers",
    "course": "🎓 Courses & Learning Resources",
    "project": "🚀 Example Projects",
}

PRICING_ICONS = {
    "free": "🆓",
    "open-source": "🟢",
    "freemium": "🟡",
    "paid": "💰",
    "enterprise": "🏢",
}

MATURITY_ICONS = {
    "experimental": "🧪",
    "beta": "🔶",
    "stable": "✅",
    "production": "🚀",
}

# ---------------------------------------------------------------------------
# README Template Parts
# ---------------------------------------------------------------------------

HEADER = """\
<div align="center">

# ⚡ AI-Pulse

### The structured, high-density AI resource repository for 2026

[![GitHub Stars](https://img.shields.io/github/stars/sam-89/ai-pulse?style=flat-square&color=gold)](https://github.com/sam-89/ai-pulse/stargazers)
[![Last Updated](https://img.shields.io/badge/updated-{today}-blue?style=flat-square)](https://github.com/sam-89/ai-pulse/commits/main)
[![Entries](https://img.shields.io/badge/entries-{total_entries}-green?style=flat-square)](https://github.com/sam-89/ai-pulse/tree/main/registry)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

*Not just a list — a living, structured database of the AI ecosystem.*
*Updated weekly. Every entry is curated, not scraped.*

[🗺️ Learning Paths](#learning-paths) · [🧠 LLMs](#llms) · [🤖 Agent Frameworks](#agent-frameworks) · [🔌 MCP Servers](#mcp-servers) · [📄 Papers](#papers) · [🤝 Contribute](CONTRIBUTING.md)

🧠 LLMs: `{llm_count}` · 🤖 Frameworks: `{framework_count}` · 🔌 MCP: `{mcp_count}` · 🛠️ Tools: `{tool_count}`

</div>

---

## What makes this different?

Most "Awesome AI" lists are link dumps. AI-Pulse is a **structured registry**:

- 📋 **JSON schema** — every entry has consistent fields (pricing, maturity, curator note)
- 🤖 **Weekly auto-updates** — GitHub Actions + AI scraper finds new tools every Monday
- 🗺️ **Role-based learning paths** — not just links, but curated journeys
- 💬 **Curator notes** — a human insight on *why* each entry matters
- ✅ **Human reviewed** — all entries pass a quality gate before merging

---

## Learning Paths

| Path | Target Role | Duration |
|------|------------|----------|
| [Zero to AI Agent Engineer](learning-paths/zero-to-agent-engineer.md) | AI/Agentic Platform Engineer | 12–16 weeks |
| [LLM Researcher Track](learning-paths/llm-researcher.md) *(coming soon)* | ML Researcher | 20–24 weeks |
| [AI Product Manager Track](learning-paths/ai-pm.md) *(coming soon)* | AI Product Manager | 6–8 weeks |

---
"""

FOOTER = """
---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add entries, suggest learning paths, or improve the automation scripts.

**Quick add:** Copy `registry/schema.json`, fill in your entry, and open a PR targeting `registry/candidates/`.

---

## Stats

| Category | Entries |
|----------|---------|
{stats_rows}

*Last compiled: {today} by build_readme.py*

---

<div align="center">
Made with ❤️ by the AI-Pulse community · <a href="https://github.com/sam-89/ai-pulse">Star us on GitHub</a>
</div>
"""

# ---------------------------------------------------------------------------
# Registry Loading
# ---------------------------------------------------------------------------

def load_registry(registry_dir: Path) -> dict[str, list[dict]]:
    """Load all registry JSON files and return entries grouped by category."""
    all_entries = defaultdict(list)

    for json_file in sorted(registry_dir.glob("*.json")):
        if json_file.name in ("schema.json", "audit.json", "trending.json") or json_file.parent.name == "candidates":
            continue
        try:
            with open(json_file) as f:
                data = json.load(f)
                if isinstance(data, list):
                    for entry in data:
                        cat = entry.get("category", "tool")
                        all_entries[cat].append(entry)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Error loading {json_file}: {e}")

    return all_entries


# ---------------------------------------------------------------------------
# Markdown Generators
# ---------------------------------------------------------------------------

def render_entry(entry: dict) -> str:
    """Render a single registry entry as a markdown block."""
    name = entry.get("name", "Unknown")
    url = entry.get("url", "")
    github_url = entry.get("github_url", "")
    desc = entry.get("description", "")
    tags = entry.get("tags", [])
    stars = entry.get("stars_approx", 0)
    curator_note = entry.get("curator_note", "")
    pricing = entry.get("pricing", "")
    maturity = entry.get("maturity", "")

    pricing_icon = PRICING_ICONS.get(pricing, "")
    maturity_icon = MATURITY_ICONS.get(maturity, "")

    name_part = f"[{name}]({url})" if url else name
    github_part = f" · [GitHub]({github_url})" if github_url else ""
    stars_part = f" · ⭐ {stars:,}" if stars else ""
    meta_line = f"{pricing_icon} `{pricing}` · {maturity_icon} `{maturity}`{stars_part}"

    tag_badges = " ".join(f"`{t}`" for t in tags[:6])

    lines = [
        f"#### {name_part}{github_part}",
        f"",
        f"{desc}",
        f"",
        f"{meta_line}  ",
        f"{tag_badges}",
    ]

    if curator_note and not curator_note.startswith("⚠️"):
        lines.append(f"")
        lines.append(f"> 💡 {curator_note}")

    lines.append("")
    return "\n".join(lines)


RECENT_DESC_MAX_LENGTH = 100


def render_recently_added(entries_by_category: dict[str, list[dict]], n: int = 5) -> str:
    """Render the 'Recently Added' section showing the n most recent entries."""
    all_entries = [e for entries in entries_by_category.values() for e in entries]
    recent = sorted(all_entries, key=lambda e: e.get("added_date", ""), reverse=True)[:n]

    lines = ["## 🆕 Recently Added", ""]
    for entry in recent:
        name = entry.get("name", "Unknown")
        url = entry.get("url", "")
        category = entry.get("category", "")
        desc = entry.get("description", "")
        desc_short = desc[:RECENT_DESC_MAX_LENGTH] + "…" if len(desc) > RECENT_DESC_MAX_LENGTH else desc
        name_link = f"[{name}]({url})" if url else name
        lines.append(f"- **{name_link}** `{category}` — {desc_short}")

    lines.append("")
    return "\n".join(lines)


def render_category_section(category: str, entries: list[dict]) -> str:
    """Render a full category section with anchor and entries."""
    label = CATEGORY_LABELS.get(category, category.title())

    lines = [
        f"---",
        f"",
        f"## {label}",
        f"",
        f"*{len(entries)} entries*",
        f"",
    ]

    # Sort by stars descending
    sorted_entries = sorted(entries, key=lambda e: e.get("stars_approx", 0), reverse=True)

    for entry in sorted_entries:
        lines.append(render_entry(entry))

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI-Pulse README builder")
    parser.add_argument("--output", default="README.md", help="Output file path")
    parser.add_argument("--registry", default="registry", help="Registry directory")
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    registry_dir = root_dir / args.registry
    output_path = root_dir / args.output

    print("🔨 Building README from registry...")

    entries_by_category = load_registry(registry_dir)

    total_entries = sum(len(v) for v in entries_by_category.values())
    today = datetime.date.today().isoformat()

    llm_count = len(entries_by_category.get("llm", []))
    framework_count = len(entries_by_category.get("agent-framework", []))
    mcp_count = len(entries_by_category.get("mcp-server", []))
    tool_count = len(entries_by_category.get("tool", []))

    print(f"   Found {total_entries} entries across {len(entries_by_category)} categories")

    # Build header
    header = HEADER.format(
        today=today,
        total_entries=total_entries,
        llm_count=llm_count,
        framework_count=framework_count,
        mcp_count=mcp_count,
        tool_count=tool_count,
    )
    sections = [header]

    # Recently added section
    sections.append(render_recently_added(entries_by_category))

    # Build category sections in defined order
    for category in CATEGORY_ORDER:
        if category in entries_by_category:
            section = render_category_section(category, entries_by_category[category])
            sections.append(section)

    # Any categories not in the order list
    for category, entries in entries_by_category.items():
        if category not in CATEGORY_ORDER:
            section = render_category_section(category, entries)
            sections.append(section)

    # Build stats
    stats_rows = "\n".join(
        f"| {CATEGORY_LABELS.get(cat, cat)} | {len(entries)} |"
        for cat, entries in sorted(entries_by_category.items(), key=lambda x: -len(x[1]))
    )

    footer = FOOTER.format(stats_rows=stats_rows, today=today)
    sections.append(footer)

    readme_content = "\n".join(sections)

    with open(output_path, "w") as f:
        f.write(readme_content)

    print(f"✅ README written to {output_path}")
    print(f"   {total_entries} entries · {len(readme_content):,} characters")


if __name__ == "__main__":
    main()

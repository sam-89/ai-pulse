# Local Development Guide

## Prerequisites

- Python 3.12+
- Git
- An Anthropic API key (for agent scripts only)

## Setup

```bash
# Clone
git clone https://github.com/sam-89/ai-pulse.git
cd ai-pulse

# Install agent dependencies
pip install anthropic

# Set your API key (agent scripts only — core scripts need no deps)
export ANTHROPIC_API_KEY=sk-ant-...
# Add to ~/.zshrc or ~/.bashrc to persist
```

## Day-to-Day Commands

### Validate before every commit

```bash
python scripts/validate_registry.py --strict
```

### Rebuild README after changing registry files

```bash
python scripts/build_readme.py
```

### Add a new entry

```bash
# Interactive (recommended — Claude fills missing fields)
python agents/add_entry.py

# Or pre-supply category
python agents/add_entry.py --category llm

# Or paste raw JSON
python agents/add_entry.py --json '{"name": "MyTool", "url": "https://example.com"}'
```

### Search the registry

```bash
# Keyword search
python agents/search_registry.py "vector database"

# Filter by category + tag
python agents/search_registry.py --category mcp-server --tag github

# Claude-powered semantic search
python agents/search_registry.py "best open-source model for RAG" --semantic

# Browse stats and tags
python agents/search_registry.py --stats
python agents/search_registry.py --list-tags
```

### Run the full candidate pipeline (weekly cadence)

```bash
# 1. Scrape new candidates
python scripts/fetch_new.py

# 2. Generate curator notes for all placeholder entries
python agents/curator_agent.py registry/candidates/$(date +%Y-%m-%d).json

# 3. Score candidates, promote approved ones (score ≥ 7/10) to registry/
python agents/review_agent.py registry/candidates/$(date +%Y-%m-%d).json \
  --threshold 7 \
  --promote \
  --out registry/candidates/$(date +%Y-%m-%d)-reviewed.json

# 4. Manually review flagged entries in the -reviewed.json file

# 5. Validate everything
python scripts/validate_registry.py --strict

# 6. Rebuild README
python scripts/build_readme.py
```

### Validate a specific file

```bash
python scripts/validate_registry.py --file registry/llms.json
python scripts/validate_registry.py --file registry/candidates/2026-04-14.json
```

### Validate candidates directory too

```bash
python scripts/validate_registry.py --strict --candidates
```

## File Naming Conventions

| File | Convention |
|---|---|
| Registry files | `registry/<category-plural>.json` (e.g. `llms.json`, `agent-frameworks.json`) |
| Candidate files | `registry/candidates/YYYY-MM-DD.json` (date of scrape) |
| Learning paths | `learning-paths/<role-slug>.md` |

## Registry Schema Quick Reference

```json
{
  "id": "my-tool",
  "name": "My Tool",
  "category": "tool",
  "subcategory": "optional",
  "description": "One sentence, max 280 chars. Who is it for and what does it do?",
  "url": "https://example.com",
  "github_url": "https://github.com/org/repo",
  "stars_approx": 1500,
  "tags": ["tag1", "tag2"],
  "license": "MIT",
  "added_date": "2026-04-14",
  "last_updated": "2026-04-14",
  "curator_note": "One insight on WHY this matters. Max 140 chars.",
  "pricing": "open-source",
  "maturity": "stable"
}
```

Valid `category` values: `llm` · `agent-framework` · `vector-db` · `mcp-server` · `tool` · `dataset` · `paper` · `course` · `project`

Valid `pricing` values: `free` · `open-source` · `freemium` · `paid` · `enterprise`

Valid `maturity` values: `experimental` · `beta` · `stable` · `production`

## Contributing a New Registry Category

1. Add a new `registry/<category>.json` file with an initial array `[]`
2. Add the category to `VALID_CATEGORIES` in `scripts/validate_registry.py`
3. Add it to `CATEGORY_ORDER` and `CATEGORY_LABELS` in `scripts/build_readme.py`
4. Add a `CATEGORY_FILES` entry in `agents/add_entry.py` and `agents/review_agent.py`
5. Run `python scripts/validate_registry.py --strict && python scripts/build_readme.py`

## CI Behavior

| Trigger | Workflow | What it does |
|---|---|---|
| PR touching `registry/` | `validate.yml` | Runs `validate_registry.py --strict`, posts result as PR comment |
| Monday 08:00 UTC | `weekly-update.yml` | Runs scraper, opens a PR with new candidates if found |
| Push to `main` | `weekly-update.yml` (build-readme job) | Re-validates and rebuilds README |

## Troubleshooting

**`anthropic` not found**
```bash
pip install anthropic
```

**`ANTHROPIC_API_KEY` not set**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

**Validation errors on a new entry**
```bash
python scripts/validate_registry.py --file registry/llms.json
# Fix reported errors, then re-run
```

**README looks wrong after adding entries**
```bash
# README is auto-generated — don't edit it directly
python scripts/build_readme.py
```

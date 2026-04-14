# Contributing to AI-Pulse

Thanks for contributing! AI-Pulse stays useful only because of community curation. Here's how to help.

## Quick Add (90 seconds)

1. Find an entry in `registry/` that matches your tool's category (e.g. `llms.json`, `agent-frameworks.json`)
2. Add your entry following the schema below
3. Open a PR — the CI will validate it automatically

## Entry Schema

```json
{
  "id": "my-tool-name",
  "name": "My Tool Name",
  "category": "tool",
  "subcategory": "optional-finer-grouping",
  "description": "One clear sentence explaining what this does and who it's for. Max 280 chars.",
  "url": "https://example.com",
  "github_url": "https://github.com/org/repo",
  "stars_approx": 1500,
  "tags": ["tag1", "tag2", "tag3"],
  "license": "MIT",
  "added_date": "2026-04-14",
  "last_updated": "2026-04-14",
  "curator_note": "One sentence on why this matters — your human insight. Max 140 chars.",
  "pricing": "open-source",
  "maturity": "stable"
}
```

**Valid categories:** `llm` · `agent-framework` · `vector-db` · `mcp-server` · `tool` · `dataset` · `paper` · `course` · `project`

**Valid pricing:** `free` · `open-source` · `freemium` · `paid` · `enterprise`

**Valid maturity:** `experimental` · `beta` · `stable` · `production`

## Quality Bar

Before submitting, verify:

- [ ] The tool/project is actively maintained (commit in last 6 months, or stable release)
- [ ] Description explains the *use case*, not just the technology
- [ ] Curator note offers a genuine insight — not just "very useful tool"
- [ ] URL is live and correct
- [ ] No duplicates (search existing `registry/` files first)

## Suggesting a Learning Path

Open an issue with the label `learning-path` and include:
- Target role/audience
- Suggested stages (3–6 stages)
- Key resources for each stage

## Running Scripts Locally

```bash
# Validate all registry entries
python scripts/validate_registry.py

# Rebuild README from registry
python scripts/build_readme.py

# Run the weekly scraper (dry run)
python scripts/fetch_new.py --dry-run
```

## Code of Conduct

Be constructive. Disagreements about curation decisions should be backed by reasoning, not opinion alone.

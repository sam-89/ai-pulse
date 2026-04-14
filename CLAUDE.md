# AI-Pulse — Claude Code Instructions

## Project Overview

AI-Pulse is a **structured JSON registry** of AI tools, models, frameworks, papers, and learning paths. It is not a link dump — every entry is schema-validated and curated. The registry is auto-updated weekly via GitHub Actions and Claude-powered agentic scripts.

## Key Commands

```bash
# Validate all registry files (run before committing)
python scripts/validate_registry.py --strict

# Rebuild README from registry (run after adding/changing entries)
python scripts/build_readme.py

# Scrape new candidates (dry-run first)
python scripts/fetch_new.py --dry-run
python scripts/fetch_new.py

# Agentic pipeline for candidate processing
python agents/curator_agent.py registry/candidates/YYYY-MM-DD.json
python agents/review_agent.py  registry/candidates/YYYY-MM-DD.json --promote
python agents/add_entry.py                          # interactive
python agents/search_registry.py "query" --semantic # search

# Install dependencies (no package manager config yet — install directly)
pip install anthropic
```

## Project Structure

```
ai-pulse/
├── CLAUDE.md                          # ← you are here
├── README.md                          # auto-built — DO NOT edit manually
├── CONTRIBUTING.md
├── .github/
│   ├── DEVELOPMENT.md                 # local dev setup
│   ├── copilot-instructions.md        # GitHub Copilot workspace rules
│   └── workflows/
│       ├── weekly-update.yml          # Monday 08:00 UTC scraper
│       └── validate.yml               # PR validation CI
├── registry/
│   ├── schema.json                    # JSON schema (source of truth for field rules)
│   ├── llms.json                      # LLM entries
│   ├── agent-frameworks.json          # Agent framework entries
│   ├── mcp-servers.json               # MCP server entries
│   └── candidates/                    # Pending entries — never go directly to registry
├── agents/                            # Claude-powered agentic helpers
│   ├── curator_agent.py               # Writes curator notes via Claude API
│   ├── review_agent.py                # Scores/filters candidates via Claude API
│   ├── add_entry.py                   # Interactive entry adder
│   └── search_registry.py             # Keyword + semantic search
├── scripts/                           # Data pipeline
│   ├── fetch_new.py                   # Scraper (RSS + ArXiv)
│   ├── validate_registry.py           # Schema validator
│   └── build_readme.py                # README compiler
└── learning-paths/
    └── zero-to-agent-engineer.md
```

## Registry Entry Rules

Every entry in `registry/*.json` must conform to `registry/schema.json`. Key rules:

- **`id`**: kebab-case, lowercase, max 60 chars (e.g. `claude-sonnet-4`)
- **`category`**: one of `llm | agent-framework | vector-db | mcp-server | tool | dataset | paper | course | project`
- **`pricing`**: one of `free | open-source | freemium | paid | enterprise`
- **`maturity`**: one of `experimental | beta | stable | production`
- **`description`**: max 280 chars — explains *what it is and who it's for*
- **`curator_note`**: max 140 chars — explains *why it matters* (not generic praise)
- **`stars_approx`**: integer (0 for non-OSS entries)
- **`tags`**: array, 1–10 items
- **`url`** and optional **`github_url`**: must start with `https://`

**Never edit `README.md` manually.** It is compiled by `scripts/build_readme.py` from registry JSON files.

## Workflow for Adding New Entries

### Option A — Interactive (recommended)
```bash
python agents/add_entry.py
```

### Option B — Manual
1. Add your entry JSON to the correct `registry/*.json` file
2. Run `python scripts/validate_registry.py --strict`
3. Run `python scripts/build_readme.py`
4. Open a PR

### Option C — Candidate pipeline (for bulk additions)
```bash
python scripts/fetch_new.py             # generates registry/candidates/DATE.json
python agents/curator_agent.py registry/candidates/DATE.json
python agents/review_agent.py  registry/candidates/DATE.json --threshold 7 --promote
python scripts/validate_registry.py --strict
python scripts/build_readme.py
```

## Agent Scripts — Important Notes

All agents in `agents/` use the **Anthropic Python SDK** with `claude-opus-4-6`. They require:

```bash
export ANTHROPIC_API_KEY=your-key
pip install anthropic
```

- **`curator_agent.py`**: Uses streaming + prompt caching (system prompt cached across batch)
- **`review_agent.py`**: Uses adaptive thinking; produces `approve | flag | reject` per entry
- **`add_entry.py`**: Interactive — fills missing fields via Claude, then validates before saving
- **`search_registry.py`**: Local keyword search by default; `--semantic` calls Claude for ranking

## Do Not

- Edit `README.md` directly — it gets overwritten by `build_readme.py`
- Add entries directly to `registry/candidates/` — that folder is for scraper output
- Skip `validate_registry.py` before committing — CI will catch it on PRs
- Use `budget_tokens` with `claude-opus-4-6` — use `thinking: {type: "adaptive"}` instead

## Environment

- Python 3.12+
- No `requirements.txt` yet — agents need `anthropic`, scripts need no external deps
- `ANTHROPIC_API_KEY` env var required for any agent script

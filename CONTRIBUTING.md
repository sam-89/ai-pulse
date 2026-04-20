# Contributing to AI-Pulse

> **This registry is maintained by AI agents.** The [ai-pulse-agents](https://github.com/sam-89/ai-pulse-agents) pipeline automatically discovers, curates, scores, and promotes new entries every two days — without human intervention. Your contribution requests are what shapes what the agents prioritise.

---

## How This Repo Works

AI-Pulse is not a manually maintained list. It's a **living registry** powered by an autonomous agentic pipeline:

1. **Every 2 days**, agents scrape RSS feeds (DeepLearning.AI, HuggingFace, Anthropic, LangChain, Simon Willison) and ArXiv for new AI tools, models, papers, and frameworks
2. **Llama 3.3 70B** generates a 140-character practitioner-focused curator note for each candidate
3. **Llama 3.3 70B** scores each entry **0–10** on relevance, quality, and uniqueness — entries scoring ≥7 are auto-promoted into the registry
4. If the free model is unavailable, **Grok 4.1 Fast** kicks in automatically as a paid fallback — the pipeline never silently skips entries
5. Every 180 days, stale entries are re-checked: dead URLs are flagged, descriptions refreshed, maturity levels updated

The registry JSON files in this repo are the **output** of that pipeline — not a manually curated list.

---

## Contribution Is Request-Based

Because the registry is agent-maintained, **we don't accept direct PRs to registry JSON files**. Every entry needs to pass through the scoring pipeline to ensure consistent quality.

Instead, contributions happen through **GitHub Issues** — you bring the idea, the agents do the work.

---

## Ways to Contribute

### 💡 Suggest a New Entry ← most impactful

Open a [**Suggest a Registry Entry**](https://github.com/sam-89/ai-pulse/issues/new?template=suggest-entry.yml) issue.

Fill in the URL, category, and — most importantly — **why it matters**. The LLM curator uses your reasoning as additional context when generating the curator note and score.

**What gets added:**
- Tools and frameworks that solve real, specific practitioner problems
- Papers with working implementations or measurable community impact
- MCP servers, datasets, and courses with unique positioning
- Models that introduce a new capability or cost/quality tradeoff

**What doesn't get added:**
- "Yet another X" without clear differentiation
- Projects with no real users or abandoned maintenance
- Entries already in the registry (check first)

---

### 🐛 Report a Registry Error

If an entry has a dead URL, outdated description, wrong maturity rating, or a bad curator note:

- Open an issue with the label `registry-error`
- Include the entry `id` (from the JSON file) and what's wrong

The stale-entry agent runs on a schedule, but human-reported errors get fixed in the next pipeline run.

---

### 🗺️ Suggest a Learning Path

Learning paths are handcrafted, not agent-generated. If you see a role or skill track that's missing:

- Open an issue with the label `learning-path`
- Include: target role, suggested stages (3–6), ~3–5 resources per stage, and why this path is underserved

If you've already drafted the content, a **direct PR to `learning-paths/`** is welcome — this is the one exception to the no-direct-PR rule.

---

### 🏷️ Propose a New Category or Tag

The current categories (`llm`, `agent-framework`, `vector-db`, `mcp-server`, `tool`, `dataset`, `paper`, `course`, `project`) were chosen to keep the schema tight and the registry focused.

If you think a new category is warranted, open an issue explaining:
- The gap it fills
- How many existing entries would move into it
- At least 3 concrete examples of what would belong there

---

## What Makes a Strong Suggestion

The LLM scorer weights these factors — give the agent strong signal by covering them in your issue:

| Factor | What we look for |
|--------|------------------|
| **Relevance** | Directly useful for AI practitioners in 2026 |
| **Quality** | Active maintenance, real documentation, working demos |
| **Uniqueness** | Fills a gap — not a clone or marginal improvement on what's already listed |
| **Maturity** | Has real users, not just a GitHub repo with 12 stars |
| **Insight** | You can explain *why it matters* in one sentence |

---

## Entry Schema (for reference)

You don't need to write JSON to suggest an entry — but knowing the schema helps you provide the right information:

```json
{
  "id": "my-tool-name",
  "name": "My Tool Name",
  "category": "tool",
  "description": "One clear sentence explaining what this does and who it's for. Max 280 chars.",
  "url": "https://example.com",
  "github_url": "https://github.com/org/repo",
  "stars_approx": 1500,
  "tags": ["tag1", "tag2", "tag3"],
  "license": "MIT",
  "added_date": "2026-04-20",
  "last_updated": "2026-04-20",
  "curator_note": "One sentence on why this matters — practitioner insight. Max 140 chars.",
  "pricing": "open-source",
  "maturity": "stable"
}
```

**Valid categories:** `llm` · `agent-framework` · `vector-db` · `mcp-server` · `tool` · `dataset` · `paper` · `course` · `project`

**Valid pricing:** `free` · `open-source` · `freemium` · `paid` · `enterprise`

**Valid maturity:** `experimental` · `beta` · `stable` · `production`

---

## Want to Improve the Agents?

The automation pipeline lives in **[ai-pulse-agents](https://github.com/sam-89/ai-pulse-agents)**. If you want to improve the scrapers, scoring prompts, or fallback logic — that's the place. Issues and ideas are open there.

---

## Code of Conduct

Be constructive. Curation decisions should be backed by reasoning. If you think an entry's score or curator note is wrong, explain why with specifics — the agents update on the next run.

---

## Contributor Credits

Contributions to this registry are tracked and credited:

- **When you open a suggestion issue** — you appear in the issue history and are referenced in any discussion around that entry
- **When your entry is accepted** — your GitHub username is stored in the `suggested_by` field of the registry JSON entry and you're added to [CONTRIBUTORS.md](./CONTRIBUTORS.md)

The `suggested_by` field is permanent — even when the entry is later updated by agents, the original suggester is preserved.

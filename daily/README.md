# daily/

This folder contains daily AI news bundles produced by [`ai-pulse-agents`](https://github.com/sam-89/ai-pulse-agents).

- `YYYY-MM-DD.json` — permanent dated bundle (top-5 AI stories for that day)
- `latest.json` — always mirrors the most recent dated file
- `schema.json` — JSON contract; both writer and consumer validate against this

## Schema contract

See [`schema.json`](./schema.json) for the full field specification.

**Deterministic fields** (computed by Python): `rank`, `id`, `authority_score`, `virality_score`, `recency_hours`, `source`, `source_type`, `published_at`, `url`, `date`, `generated_at`, `generator_version`, `sources_polled`.

**LLM-generated fields**: `title`, `summary`, `why_it_matters`, `suggested_reel_angle`, `suggested_long_angle`, `tags`, `related_registry_entries`.

## Consumer

`pulse-broadcast` (local Mac project, not hosted) reads `daily/latest.json` via `git pull` to produce YouTube reels and long-form content.

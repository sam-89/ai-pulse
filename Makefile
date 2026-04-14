.DEFAULT_GOAL := help

# ──────────────────────────────────────────────
# Variables
# ──────────────────────────────────────────────
DATE   ?= $(shell date +%Y-%m-%d)
FILE   ?=
QUERY  ?=

# ──────────────────────────────────────────────
# Help
# ──────────────────────────────────────────────
.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

# ──────────────────────────────────────────────
# Registry
# ──────────────────────────────────────────────
.PHONY: validate
validate: ## Validate all registry JSON files (strict)
	python scripts/validate_registry.py --strict

.PHONY: validate-candidates
validate-candidates: ## Validate candidate JSON files (strict)
	python scripts/validate_registry.py --strict --candidates

.PHONY: build
build: ## Rebuild README.md from registry JSON
	python scripts/build_readme.py

.PHONY: lint-registry
lint-registry: ## Alias for validate
	python scripts/validate_registry.py --strict

# ──────────────────────────────────────────────
# Scraper
# ──────────────────────────────────────────────
.PHONY: fetch
fetch: ## Scrape new candidates into registry/candidates/
	python scripts/fetch_new.py

.PHONY: fetch-dry
fetch-dry: ## Dry-run scraper (no files written)
	python scripts/fetch_new.py --dry-run

# ──────────────────────────────────────────────
# Agents
# ──────────────────────────────────────────────
.PHONY: curate
curate: ## Write curator notes via Claude  (FILE=registry/candidates/DATE.json)
	@test -n "$(FILE)" || (echo "❌  Usage: make curate FILE=registry/candidates/YYYY-MM-DD.json" && exit 1)
	python agents/curator_agent.py $(FILE)

.PHONY: review
review: ## Score & filter candidates via Claude  (FILE=registry/candidates/DATE.json)
	@test -n "$(FILE)" || (echo "❌  Usage: make review FILE=registry/candidates/YYYY-MM-DD.json" && exit 1)
	python agents/review_agent.py $(FILE)

.PHONY: add
add: ## Interactively add a new registry entry
	python agents/add_entry.py

.PHONY: search
search: ## Search the registry  (QUERY="your query")
	@test -n "$(QUERY)" || (echo "❌  Usage: make search QUERY=\"your search query\"" && exit 1)
	python agents/search_registry.py "$(QUERY)"

# ──────────────────────────────────────────────
# Pipeline (fetch → curate → review)
# ──────────────────────────────────────────────
.PHONY: pipeline
pipeline: ## Run full pipeline for a given DATE (default: today)
	python scripts/fetch_new.py
	python agents/curator_agent.py registry/candidates/$(DATE).json
	python agents/review_agent.py  registry/candidates/$(DATE).json --promote

# ──────────────────────────────────────────────
# Dependencies
# ──────────────────────────────────────────────
.PHONY: install
install: ## Install production dependencies
	pip install -r requirements.txt

.PHONY: install-dev
install-dev: ## Install development dependencies (includes pytest, pre-commit)
	pip install -r requirements-dev.txt

# ──────────────────────────────────────────────
# Tests & checks
# ──────────────────────────────────────────────
.PHONY: test
test: ## Run test suite
	python -m pytest tests/ -v

.PHONY: check-urls
check-urls: ## Check all registry URLs for dead links
	@if [ -f scripts/check_urls.py ]; then \
		python scripts/check_urls.py; \
	else \
		echo "ℹ️  scripts/check_urls.py not yet implemented — skipping"; \
	fi

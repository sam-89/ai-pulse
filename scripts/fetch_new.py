#!/usr/bin/env python3
"""
AI-Pulse: fetch_new.py
----------------------
Weekly scraper that monitors AI news sources, extracts new tools/models,
and generates a candidate JSON file for human review.

Usage:
    python scripts/fetch_new.py
    python scripts/fetch_new.py --sources arxiv,rss --limit 20

Output:
    registry/candidates/YYYY-MM-DD.json  (ready for human review + agent curation)
"""

import json
import re
import sys
import datetime
import argparse
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RSS_FEEDS = [
    {
        "name": "The Batch (DeepLearning.AI)",
        "url": "https://www.deeplearning.ai/the-batch/feed/",
        "category": "newsletter"
    },
    {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml",
        "category": "llm"
    },
    {
        "name": "LangChain Blog",
        "url": "https://blog.langchain.dev/rss/",
        "category": "agent-framework"
    },
    {
        "name": "Anthropic News",
        "url": "https://www.anthropic.com/news.rss",
        "category": "llm"
    },
    {
        "name": "Simon Willison's Blog",
        "url": "https://simonwillison.net/atom/everything/",
        "category": "tool"
    },
    {
        "name": "Sebastian Raschka's Newsletter",
        "url": "https://magazine.sebastianraschka.com/feed",
        "category": "llm"
    },
]

ARXIV_QUERIES = [
    "large language model agents",
    "multi-agent reinforcement learning 2026",
    "model context protocol",
    "autonomous AI systems",
    "agentic AI safety",
]

GITHUB_TRENDING_TOPICS = [
    "llm",
    "agent",
    "mcp",
    "langchain",
    "autonomous-agents",
]

CANDIDATE_SCHEMA = {
    "id": "",
    "name": "",
    "category": "tool",
    "subcategory": "",
    "description": "",
    "url": "",
    "github_url": "",
    "stars_approx": 0,
    "tags": [],
    "license": "unknown",
    "added_date": str(datetime.date.today()),
    "last_updated": str(datetime.date.today()),
    "curator_note": "⚠️ NEEDS HUMAN REVIEW",
    "pricing": "free",
    "maturity": "experimental",
    "_source": "",
    "_confidence": 0.0,
    "_raw_title": "",
}

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def fetch_url(url: str, timeout: int = 10) -> str | None:
    """Fetch a URL and return the content as a string, or None on error."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "AI-Pulse-Bot/1.0 (https://github.com/sam-89/ai-pulse)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, Exception) as e:
        print(f"  ⚠️  Failed to fetch {url}: {e}", file=sys.stderr)
        return None


def slugify(text: str) -> str:
    """Convert a title to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:60].strip("-")


def guess_category(text: str) -> str:
    """Heuristically assign a category based on text content."""
    text_lower = text.lower()
    if any(k in text_lower for k in ["gpt", "llm", "language model", "claude", "gemini", "llama"]):
        return "llm"
    if any(k in text_lower for k in ["agent", "autogen", "swarm", "orchestrat"]):
        return "agent-framework"
    if any(k in text_lower for k in ["vector", "embedding", "pinecone", "weaviate", "chroma"]):
        return "vector-db"
    if any(k in text_lower for k in ["mcp", "model context protocol", "tool server"]):
        return "mcp-server"
    if any(k in text_lower for k in ["dataset", "benchmark", "eval"]):
        return "dataset"
    if any(k in text_lower for k in ["paper", "research", "arxiv"]):
        return "paper"
    if any(k in text_lower for k in ["course", "tutorial", "learn"]):
        return "course"
    return "tool"


# ---------------------------------------------------------------------------
# Scrapers
# ---------------------------------------------------------------------------

def scrape_rss_feeds(feeds: list[dict], limit_per_feed: int = 5) -> list[dict]:
    """Fetch and parse RSS feeds, returning candidate entries."""
    candidates = []
    for feed in feeds:
        print(f"  📡 Fetching RSS: {feed['name']}")
        content = fetch_url(feed["url"])
        if not content:
            continue

        try:
            root = ET.fromstring(content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            items = root.findall(".//item") or root.findall(".//atom:entry", ns)

            for i, item in enumerate(items[:limit_per_feed]):
                title_el = item.find("title") or item.find("atom:title", ns)
                link_el = item.find("link") or item.find("atom:link", ns)
                desc_el = item.find("description") or item.find("atom:summary", ns)

                title = title_el.text if title_el is not None else "Untitled"
                link = (link_el.text or link_el.get("href", "")) if link_el is not None else ""
                desc = desc_el.text if desc_el is not None else ""

                desc = re.sub(r"<[^>]+>", "", desc or "")[:280]

                candidate = CANDIDATE_SCHEMA.copy()
                candidate.update({
                    "id": slugify(title),
                    "name": title,
                    "category": guess_category(title + " " + desc),
                    "subcategory": feed.get("category", ""),
                    "description": desc.strip() or f"From {feed['name']}",
                    "url": link,
                    "tags": [slugify(feed["name"]), "rss-import"],
                    "_source": feed["name"],
                    "_confidence": 0.4,
                    "_raw_title": title,
                })
                candidates.append(candidate)

        except ET.ParseError as e:
            print(f"  ⚠️  XML parse error for {feed['name']}: {e}", file=sys.stderr)

    return candidates


def scrape_arxiv(queries: list[str], max_results: int = 5) -> list[dict]:
    """Search ArXiv for recent AI papers and return candidate entries."""
    candidates = []
    base_url = "http://export.arxiv.org/api/query"

    for query in queries:
        print(f"  📄 ArXiv query: '{query}'")
        encoded_query = urllib.parse.quote(query)
        url = f"{base_url}?search_query=all:{encoded_query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"

        content = fetch_url(url)
        if not content:
            continue

        try:
            root = ET.fromstring(content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}

            for entry in root.findall("atom:entry", ns):
                title_el = entry.find("atom:title", ns)
                summary_el = entry.find("atom:summary", ns)
                link_el = entry.find("atom:id", ns)
                authors = entry.findall("atom:author/atom:name", ns)

                title = (title_el.text or "").strip().replace("\n", " ")
                summary = (summary_el.text or "").strip().replace("\n", " ")[:280]
                link = (link_el.text or "").strip()
                author_names = [a.text for a in authors[:3]]

                candidate = CANDIDATE_SCHEMA.copy()
                candidate.update({
                    "id": slugify(title),
                    "name": title,
                    "category": "paper",
                    "subcategory": "arxiv",
                    "description": summary,
                    "url": link,
                    "tags": ["arxiv", "paper", "research"] + [slugify(a) for a in author_names],
                    "_source": f"ArXiv — {query}",
                    "_confidence": 0.7,
                    "_raw_title": title,
                })
                candidates.append(candidate)

        except ET.ParseError as e:
            print(f"  ⚠️  XML parse error for ArXiv: {e}", file=sys.stderr)

    return candidates


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def load_existing_ids(registry_dir: Path) -> set[str]:
    """Load all IDs from existing registry JSON files to avoid duplicates."""
    existing = set()
    for json_file in registry_dir.glob("*.json"):
        if json_file.name == "schema.json":
            continue
        try:
            with open(json_file) as f:
                data = json.load(f)
                if isinstance(data, list):
                    existing.update(item.get("id", "") for item in data)
        except (json.JSONDecodeError, IOError):
            pass
    return existing


def deduplicate(candidates: list[dict], existing_ids: set[str]) -> list[dict]:
    """Remove candidates that already exist in the registry."""
    seen_ids = set()
    unique = []
    for c in candidates:
        cid = c.get("id", "")
        if cid and cid not in existing_ids and cid not in seen_ids:
            seen_ids.add(cid)
            unique.append(c)
    return unique


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI-Pulse weekly resource scraper")
    parser.add_argument("--sources", default="rss,arxiv", help="Comma-separated list of sources to fetch")
    parser.add_argument("--limit", type=int, default=10, help="Max items per source")
    parser.add_argument("--dry-run", action="store_true", help="Print candidates without saving")
    args = parser.parse_args()

    sources = [s.strip() for s in args.sources.split(",")]

    print("🚀 AI-Pulse Scraper starting...")
    print(f"   Sources: {sources}")
    print(f"   Date: {datetime.date.today()}")
    print()

    root_dir = Path(__file__).parent.parent
    registry_dir = root_dir / "registry"
    candidates_dir = registry_dir / "candidates"
    candidates_dir.mkdir(exist_ok=True)

    existing_ids = load_existing_ids(registry_dir)
    print(f"📚 Loaded {len(existing_ids)} existing registry IDs")
    print()

    all_candidates = []

    if "rss" in sources:
        print("📡 Fetching RSS feeds...")
        rss_candidates = scrape_rss_feeds(RSS_FEEDS, limit_per_feed=args.limit)
        all_candidates.extend(rss_candidates)
        print(f"   → {len(rss_candidates)} items found")
        print()

    if "arxiv" in sources:
        print("📄 Querying ArXiv...")
        arxiv_candidates = scrape_arxiv(ARXIV_QUERIES, max_results=args.limit)
        all_candidates.extend(arxiv_candidates)
        print(f"   → {len(arxiv_candidates)} papers found")
        print()

    unique_candidates = deduplicate(all_candidates, existing_ids)
    print(f"✅ After dedup: {len(unique_candidates)} new candidates (from {len(all_candidates)} total)")
    print()

    if args.dry_run:
        print("🔍 Dry run — candidates:")
        for c in unique_candidates[:5]:
            print(f"  - [{c['category']}] {c['name'][:60]}")
        print("   (not saved)")
        return

    today = datetime.date.today().isoformat()
    output_path = candidates_dir / f"{today}.json"

    with open(output_path, "w") as f:
        json.dump(unique_candidates, f, indent=2, ensure_ascii=False)

    print(f"💾 Saved {len(unique_candidates)} candidates to:")
    print(f"   {output_path}")
    print()
    print("👉 Next steps:")
    print("   1. Run agents/curator_agent.py to auto-generate curator notes")
    print("   2. Run agents/review_agent.py to score and filter entries")
    print("   3. Move approved entries to registry/*.json")
    print("   4. Run: python scripts/build_readme.py")


if __name__ == "__main__":
    main()

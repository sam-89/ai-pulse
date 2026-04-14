#!/usr/bin/env python3
"""
AI-Pulse: search_registry.py
------------------------------
Search across all registry entries by keyword, tag, or category.
Supports fast local search and optional Claude-powered semantic search.

Usage:
    python agents/search_registry.py "vector database"
    python agents/search_registry.py --tag mcp --category mcp-server
    python agents/search_registry.py "best model for code generation" --semantic
    python agents/search_registry.py --list-tags
    python agents/search_registry.py --list-categories
    python agents/search_registry.py --stats

Requires (for --semantic):
    pip install anthropic
    export ANTHROPIC_API_KEY=your-key
"""

import json
import sys
import argparse
import re
from pathlib import Path
from collections import Counter

import anthropic

# ---------------------------------------------------------------------------
# Registry loading
# ---------------------------------------------------------------------------

def load_all_entries(registry_dir: Path) -> list[dict]:
    """Load all entries from all registry JSON files."""
    all_entries = []
    for json_file in sorted(registry_dir.glob("*.json")):
        if json_file.name in ("schema.json",) or json_file.parent.name == "candidates":
            continue
        try:
            with open(json_file) as f:
                data = json.load(f)
            if isinstance(data, list):
                for entry in data:
                    entry["_source_file"] = json_file.name
                all_entries.extend(data)
        except (json.JSONDecodeError, IOError):
            pass
    return all_entries


# ---------------------------------------------------------------------------
# Local search
# ---------------------------------------------------------------------------

def keyword_search(entries: list[dict], query: str) -> list[tuple[int, dict]]:
    """Search entries by keyword across name, description, tags, and curator_note."""
    query_lower = query.lower()
    query_words = re.findall(r"\w+", query_lower)

    results = []
    for entry in entries:
        score = 0
        name = entry.get("name", "").lower()
        desc = entry.get("description", "").lower()
        tags = [t.lower() for t in entry.get("tags", [])]
        note = entry.get("curator_note", "").lower()
        subcategory = entry.get("subcategory", "").lower()

        for word in query_words:
            if word in name:
                score += 10  # Strongest signal
            if word in tags:
                score += 6
            if word in desc:
                score += 4
            if word in note:
                score += 2
            if word in subcategory:
                score += 3

        if score > 0:
            results.append((score, entry))

    # Sort by score desc, then stars desc
    results.sort(key=lambda x: (x[0], x[1].get("stars_approx", 0)), reverse=True)
    return results


def filter_entries(
    entries: list[dict],
    category: str | None = None,
    tag: str | None = None,
    pricing: str | None = None,
    maturity: str | None = None,
) -> list[dict]:
    """Filter entries by exact field values."""
    result = entries
    if category:
        result = [e for e in result if e.get("category") == category]
    if tag:
        result = [e for e in result if tag.lower() in [t.lower() for t in e.get("tags", [])]]
    if pricing:
        result = [e for e in result if e.get("pricing") == pricing]
    if maturity:
        result = [e for e in result if e.get("maturity") == maturity]
    return result


# ---------------------------------------------------------------------------
# Claude-powered semantic search
# ---------------------------------------------------------------------------

SEMANTIC_SYSTEM = """\
You are a search assistant for the AI-Pulse registry. Given a user query and a list
of registry entries, return the IDs of the most relevant entries in ranked order.

Consider:
- Semantic relevance to the query (not just keyword matching)
- Use-case fit
- Maturity and quality of the entry

Return ONLY a JSON array of entry IDs in order of relevance (most relevant first).
Return max 5 entries. If nothing is relevant, return [].
Example: ["claude-sonnet-4", "langgraph", "pydantic-ai"]
"""


def semantic_search(
    client: anthropic.Anthropic,
    entries: list[dict],
    query: str,
    max_results: int = 5,
) -> list[dict]:
    """Use Claude to semantically rank entries for a query."""
    # Build a compact summary for each entry to fit in context
    summaries = []
    for e in entries:
        summaries.append({
            "id": e.get("id"),
            "name": e.get("name"),
            "category": e.get("category"),
            "description": e.get("description", "")[:150],
            "tags": e.get("tags", [])[:5],
        })

    prompt = f"""Query: "{query}"

Registry entries:
{json.dumps(summaries, indent=2)}

Return a JSON array of the most relevant entry IDs (max {max_results}), ranked by relevance.
"""

    print("  🤖 Running semantic search with Claude...")
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=200,
        system=[
            {
                "type": "text",
                "text": SEMANTIC_SYSTEM,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": prompt}],
    )

    text = next((b.text for b in response.content if b.type == "text"), "[]")
    try:
        ranked_ids = json.loads(text.strip())
    except json.JSONDecodeError:
        ranked_ids = []

    # Map IDs back to entries, preserving rank
    id_to_entry = {e.get("id"): e for e in entries}
    return [id_to_entry[eid] for eid in ranked_ids if eid in id_to_entry]


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

PRICING_ICONS = {
    "free": "🆓", "open-source": "🟢", "freemium": "🟡", "paid": "💰", "enterprise": "🏢",
}
MATURITY_ICONS = {
    "experimental": "🧪", "beta": "🔶", "stable": "✅", "production": "🚀",
}

def display_entry(entry: dict, score: int | None = None) -> None:
    name = entry.get("name", "Unknown")
    url = entry.get("url", "")
    desc = entry.get("description", "")
    tags = entry.get("tags", [])
    stars = entry.get("stars_approx", 0)
    note = entry.get("curator_note", "")
    pricing = entry.get("pricing", "")
    maturity = entry.get("maturity", "")
    category = entry.get("category", "")
    source = entry.get("_source_file", "")

    p_icon = PRICING_ICONS.get(pricing, "")
    m_icon = MATURITY_ICONS.get(maturity, "")
    stars_str = f" · ⭐ {stars:,}" if stars else ""
    score_str = f" [score: {score}]" if score is not None else ""

    print(f"\n  ── {name}{score_str}")
    print(f"     {url}")
    print(f"     {desc[:100]}{'...' if len(desc) > 100 else ''}")
    print(f"     {p_icon} {pricing} · {m_icon} {maturity} · [{category}]{stars_str}")
    tag_str = " ".join(f"`{t}`" for t in tags[:6])
    print(f"     {tag_str}")
    if note and not note.startswith("⚠️"):
        print(f"     💡 {note}")
    if source:
        print(f"     📁 {source}")


def display_results(results: list, mode: str = "search") -> None:
    if not results:
        print("\n  No results found.")
        return

    count = len(results)
    print(f"\n  Found {count} result{'s' if count != 1 else ''}:\n")

    for item in results:
        if isinstance(item, tuple):
            score, entry = item
            display_entry(entry, score=score)
        else:
            display_entry(item)

    print()


# ---------------------------------------------------------------------------
# Stats & metadata commands
# ---------------------------------------------------------------------------

def show_stats(entries: list[dict]) -> None:
    print(f"\n📊 Registry Stats")
    print(f"   Total entries: {len(entries)}")
    print()

    by_cat = Counter(e.get("category", "?") for e in entries)
    print("   By category:")
    for cat, count in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"     {cat:<20} {count}")

    by_pricing = Counter(e.get("pricing", "?") for e in entries)
    print("\n   By pricing:")
    for p, count in sorted(by_pricing.items(), key=lambda x: -x[1]):
        icon = PRICING_ICONS.get(p, "")
        print(f"     {icon} {p:<15} {count}")

    by_maturity = Counter(e.get("maturity", "?") for e in entries)
    print("\n   By maturity:")
    for m, count in sorted(by_maturity.items(), key=lambda x: -x[1]):
        icon = MATURITY_ICONS.get(m, "")
        print(f"     {icon} {m:<15} {count}")
    print()


def show_tags(entries: list[dict]) -> None:
    all_tags: list[str] = []
    for e in entries:
        all_tags.extend(e.get("tags", []))
    tag_counts = Counter(t.lower() for t in all_tags)
    print(f"\n🏷️  All Tags ({len(tag_counts)} unique):\n")
    for tag, count in tag_counts.most_common(50):
        print(f"   {tag:<25} {count}")
    print()


def show_categories(entries: list[dict]) -> None:
    by_cat = Counter(e.get("category", "?") for e in entries)
    print(f"\n📁 Categories:\n")
    for cat, count in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"   {cat:<25} {count} entries")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI-Pulse registry search")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--category", "-c", help="Filter by category")
    parser.add_argument("--tag", "-t", help="Filter by tag")
    parser.add_argument("--pricing", "-p", choices=["free","open-source","freemium","paid","enterprise"])
    parser.add_argument("--maturity", "-m", choices=["experimental","beta","stable","production"])
    parser.add_argument("--semantic", "-s", action="store_true",
                        help="Use Claude for semantic search (requires ANTHROPIC_API_KEY)")
    parser.add_argument("--limit", "-n", type=int, default=10,
                        help="Max results to show (default: 10)")
    parser.add_argument("--list-tags", action="store_true", help="List all tags")
    parser.add_argument("--list-categories", action="store_true", help="List all categories")
    parser.add_argument("--stats", action="store_true", help="Show registry stats")
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    registry_dir = root_dir / "registry"
    all_entries = load_all_entries(registry_dir)

    if not all_entries:
        print("⚠️  No registry entries found. Run scripts/build_readme.py or add entries first.")
        sys.exit(0)

    # --- Metadata commands ---
    if args.stats:
        show_stats(all_entries)
        return
    if args.list_tags:
        show_tags(all_entries)
        return
    if args.list_categories:
        show_categories(all_entries)
        return

    # --- Filter first ---
    filtered = filter_entries(
        all_entries,
        category=args.category,
        tag=args.tag,
        pricing=args.pricing,
        maturity=args.maturity,
    )

    if args.category or args.tag or args.pricing or args.maturity:
        filters = []
        if args.category:
            filters.append(f"category={args.category}")
        if args.tag:
            filters.append(f"tag={args.tag}")
        if args.pricing:
            filters.append(f"pricing={args.pricing}")
        if args.maturity:
            filters.append(f"maturity={args.maturity}")
        print(f"\n🔍 Filtering: {' + '.join(filters)}")

    if not args.query:
        # Just filter, no text search
        display_results(filtered[:args.limit])
        if len(filtered) > args.limit:
            print(f"  ... and {len(filtered) - args.limit} more (use --limit to see more)")
        return

    # --- Text/semantic search ---
    query = args.query
    print(f'\n🔍 Searching for: "{query}"')

    if args.semantic:
        try:
            client = anthropic.Anthropic()
            results = semantic_search(client, filtered, query, max_results=args.limit)
            display_results(results)
        except anthropic.AuthenticationError:
            print("⚠️  ANTHROPIC_API_KEY not set or invalid. Falling back to keyword search.")
            results = keyword_search(filtered, query)[:args.limit]
            display_results(results)
    else:
        results = keyword_search(filtered, query)[:args.limit]
        display_results(results)

    total_filtered = len(filtered)
    total_results = len(results)
    if total_filtered > total_results:
        print(f"  Searched {total_filtered} entries · showing top {total_results}")
    print(f"  Tip: Add --semantic for Claude-powered semantic search\n")


if __name__ == "__main__":
    main()

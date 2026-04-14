#!/usr/bin/env python3
"""
AI-Pulse: curator_agent.py
---------------------------
Uses Claude to auto-generate high-quality curator notes for candidate entries
that still have the placeholder "⚠️ NEEDS HUMAN REVIEW" note.

Usage:
    python agents/curator_agent.py registry/candidates/2026-04-14.json
    python agents/curator_agent.py registry/candidates/2026-04-14.json --dry-run
    python agents/curator_agent.py registry/candidates/2026-04-14.json --out approved.json

Requires:
    pip install anthropic
    export ANTHROPIC_API_KEY=your-key
"""

import json
import sys
import argparse
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# System prompt (cached — stable across all entries in a batch)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are an expert AI curator for the AI-Pulse registry — a structured, high-density
repository of AI tools, models, papers, and frameworks. Your job is to write concise,
insightful curator notes that tell practitioners *why* an entry matters, not just
what it is.

Rules for a great curator note:
- Max 140 characters
- Must offer a genuine practitioner insight (not "very useful tool")
- Focus on: unique value, key use case, surprising capability, or important tradeoff
- Write for AI engineers and researchers who are time-constrained
- Use concrete language — avoid vague adjectives like "powerful" or "amazing"
- Do NOT start with "This is" or repeat the tool name

Good examples:
  "The async event-driven architecture in 0.4 is a major leap. Best for complex multi-agent systems."
  "Unprecedented cost/performance ratio for reasoning tasks. Critical for cost-sensitive agentic pipelines."
  "Start here. The reference implementation — essential for any local agentic workflow."

Bad examples:
  "A very useful and powerful tool for AI development."
  "This framework is amazing and you should use it."
"""

CURATOR_PROMPT_TEMPLATE = """\
Write a curator note for this registry entry. Return ONLY the curator note text,
no quotes, no explanation, no JSON. Max 140 characters.

Entry:
- Name: {name}
- Category: {category}
- Description: {description}
- Tags: {tags}
- Pricing: {pricing}
- Maturity: {maturity}
- URL: {url}
"""


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def needs_curation(entry: dict) -> bool:
    """Return True if the entry needs a curator note written."""
    note = entry.get("curator_note", "")
    return not note or note.startswith("⚠️")


def curate_entry(client: anthropic.Anthropic, entry: dict) -> str:
    """Call Claude to generate a curator note for a single entry."""
    prompt = CURATOR_PROMPT_TEMPLATE.format(
        name=entry.get("name", ""),
        category=entry.get("category", ""),
        description=entry.get("description", ""),
        tags=", ".join(entry.get("tags", [])),
        pricing=entry.get("pricing", ""),
        maturity=entry.get("maturity", ""),
        url=entry.get("url", ""),
    )

    # Stream so we get responsive output even for large batches
    full_text = ""
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=200,
        thinking={"type": "adaptive"},
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},  # cache system across all entries
            }
        ],
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            full_text += text

    # Truncate to 140 chars hard limit and strip whitespace
    note = full_text.strip()
    if len(note) > 140:
        note = note[:137] + "..."
    return note


def process_candidates(
    client: anthropic.Anthropic,
    candidates: list[dict],
    dry_run: bool = False,
) -> list[dict]:
    """Process all candidates, generating curator notes where needed."""
    total = len(candidates)
    to_curate = [e for e in candidates if needs_curation(e)]
    already_done = total - len(to_curate)

    print(f"📋 {total} entries total:")
    print(f"   ✅ {already_done} already have curator notes")
    print(f"   🤖 {len(to_curate)} need AI curation")
    print()

    if not to_curate:
        print("Nothing to do.")
        return candidates

    results = list(candidates)  # copy

    for i, entry in enumerate(to_curate, 1):
        name = entry.get("name", "Unknown")
        print(f"  [{i}/{len(to_curate)}] Curating: {name[:50]}")

        if dry_run:
            print(f"    → [dry-run] Would generate curator note")
            continue

        try:
            note = curate_entry(client, entry)
            print(f"    → {note[:80]}{'...' if len(note) > 80 else ''}")
            # Update in-place in results list
            for r in results:
                if r.get("id") == entry.get("id"):
                    r["curator_note"] = note
                    break
        except anthropic.APIError as e:
            print(f"    ⚠️  API error: {e}", file=sys.stderr)
        except Exception as e:
            print(f"    ⚠️  Unexpected error: {e}", file=sys.stderr)

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI-Pulse curator agent")
    parser.add_argument("input", help="Path to candidate JSON file")
    parser.add_argument("--out", help="Output path (defaults to overwriting input)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_path) as f:
            candidates = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(candidates, list):
        print("❌ Input must be a JSON array", file=sys.stderr)
        sys.exit(1)

    print("🤖 AI-Pulse Curator Agent")
    print(f"   Input: {input_path}")
    print(f"   Model: claude-opus-4-6 (adaptive thinking + prompt caching)")
    print()

    client = anthropic.Anthropic()
    updated = process_candidates(client, candidates, dry_run=args.dry_run)

    if args.dry_run:
        print("\n[dry-run] No changes saved.")
        return

    output_path = Path(args.out) if args.out else input_path
    with open(output_path, "w") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved to: {output_path}")
    print("\n👉 Next steps:")
    print("   1. Run: python agents/review_agent.py <file>   (score & filter)")
    print("   2. Move approved entries to registry/*.json")
    print("   3. Run: python scripts/build_readme.py")


if __name__ == "__main__":
    main()

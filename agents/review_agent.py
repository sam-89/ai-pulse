#!/usr/bin/env python3
"""
AI-Pulse: review_agent.py
--------------------------
Uses Claude to score and filter candidate entries. Produces a ranked list
of entries ready for promotion to the main registry, with low-quality entries
flagged for rejection.

Usage:
    python agents/review_agent.py registry/candidates/2026-04-14.json
    python agents/review_agent.py registry/candidates/2026-04-14.json --threshold 6
    python agents/review_agent.py registry/candidates/2026-04-14.json --out approved.json
    python agents/review_agent.py registry/candidates/2026-04-14.json --promote

Requires:
    pip install anthropic
    export ANTHROPIC_API_KEY=your-key
"""

import json
import sys
import argparse
import datetime
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Category → registry filename mapping (shared by promote_entries and audit)
# ---------------------------------------------------------------------------

CATEGORY_FILES: dict[str, str] = {
    "llm": "llms.json",
    "agent-framework": "agent-frameworks.json",
    "vector-db": "vector-dbs.json",
    "mcp-server": "mcp-servers.json",
    "tool": "tools.json",
    "dataset": "datasets.json",
    "paper": "papers.json",
    "course": "courses.json",
    "project": "projects.json",
}

# ---------------------------------------------------------------------------
# System prompt (cached across all scored entries)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a quality gatekeeper for AI-Pulse — a curated, structured registry of AI
tools, models, papers, and frameworks. Your job is to score candidate entries and
decide if they meet the bar for inclusion.

Scoring criteria (each 0–2 points, max 10):
1. Relevance: Is this genuinely relevant to AI practitioners in 2026?
2. Uniqueness: Does this add something not already in common AI registries?
3. Description quality: Is the description accurate, clear, and use-case focused?
4. Production readiness: Is this actually usable (not vaporware, not abandoned)?
5. Curator note quality: Is the note insightful and specific (not generic praise)?

Output format — respond with ONLY valid JSON, no markdown, no explanation:
{
  "score": <integer 0-10>,
  "verdict": "approve" | "flag" | "reject",
  "reason": "<one sentence explaining the verdict>",
  "suggested_category": "<corrected category if wrong, else null>"
}

Verdicts:
- approve (score 7+): Ready for registry
- flag (score 4-6): Needs human review — borderline quality
- reject (score 0-3): Not suitable — too generic, off-topic, or low quality
"""

REVIEW_PROMPT_TEMPLATE = """\
Score this candidate entry for the AI-Pulse registry.

Entry:
{entry_json}

Return ONLY valid JSON with keys: score, verdict, reason, suggested_category
"""


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def score_entry(client: anthropic.Anthropic, entry: dict) -> dict:
    """Call Claude to score a single candidate entry."""
    entry_json = json.dumps(entry, indent=2, ensure_ascii=False)
    prompt = REVIEW_PROMPT_TEMPLATE.format(entry_json=entry_json)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=300,
        thinking={"type": "adaptive"},
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": prompt}],
    )

    text = next((b.text for b in response.content if b.type == "text"), "{}")

    try:
        result = json.loads(text.strip())
    except json.JSONDecodeError:
        # Fallback if Claude returns non-JSON
        result = {
            "score": 0,
            "verdict": "flag",
            "reason": "Could not parse review response — manual review needed",
            "suggested_category": None,
        }

    return result


def review_candidates(
    client: anthropic.Anthropic,
    candidates: list[dict],
    threshold: int = 7,
    dry_run: bool = False,
) -> tuple[list[dict], list[dict], list[dict]]:
    """
    Score all candidates.
    Returns (approved, flagged, rejected) lists with _review metadata added.
    """
    approved, flagged, rejected = [], [], []
    total = len(candidates)

    print(f"🔍 Reviewing {total} candidates (threshold: {threshold}/10)...")
    print()

    for i, entry in enumerate(candidates, 1):
        name = entry.get("name", "Unknown")[:45]
        print(f"  [{i}/{total}] {name}")

        if dry_run:
            review = {
                "score": 0,
                "verdict": "flag",
                "reason": "[dry-run]",
                "suggested_category": None,
            }
        else:
            try:
                review = score_entry(client, entry)
            except anthropic.APIError as e:
                print(f"    ⚠️  API error: {e}", file=sys.stderr)
                review = {
                    "score": 0,
                    "verdict": "flag",
                    "reason": f"API error during review: {e}",
                    "suggested_category": None,
                }

        score = review.get("score", 0)
        verdict = review.get("verdict", "flag")
        reason = review.get("reason", "")

        verdict_icon = {"approve": "✅", "flag": "⚠️ ", "reject": "❌"}.get(verdict, "?")
        print(f"    {verdict_icon} Score: {score}/10 — {reason[:80]}")

        annotated = {**entry, "_review": review}

        if verdict == "approve" and score >= threshold:
            approved.append(annotated)
        elif verdict == "reject" or score < 4:
            rejected.append(annotated)
        else:
            flagged.append(annotated)

    return approved, flagged, rejected


def write_audit_records(
    approved: list[dict],
    source_file: Path,
    registry_dir: Path,
) -> None:
    """Append promotion audit records to registry/audit.json."""
    audit_path = registry_dir / "audit.json"
    existing: list[dict] = []
    if audit_path.exists():
        try:
            with open(audit_path) as f:
                existing = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    root_dir = registry_dir.parent
    today = datetime.date.today().isoformat()

    for entry in approved:
        cat = entry.get("category", "tool")
        filename = CATEGORY_FILES.get(cat, f"{cat}.json")
        review = entry.get("_review", {})
        record = {
            "id": entry.get("id", ""),
            "action": "promote",
            "date": today,
            "score": review.get("score", 0),
            "reviewer": "review_agent",
            "source_file": str(source_file.relative_to(root_dir)),
            "target_file": f"registry/{filename}",
        }
        existing.append(record)

    with open(audit_path, "w") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"    📝 Wrote {len(approved)} audit record(s) to registry/audit.json")


def promote_entries(approved: list[dict], registry_dir: Path) -> None:
    """
    Promote approved entries to the correct registry/*.json files,
    stripping review metadata and candidate-only fields.
    """
    CANDIDATE_FIELDS = {"_source", "_confidence", "_raw_title", "_review"}
    by_category: dict[str, list[dict]] = {}

    for entry in approved:
        cat = entry.get("category", "tool")
        clean = {k: v for k, v in entry.items() if k not in CANDIDATE_FIELDS}
        by_category.setdefault(cat, []).append(clean)

    for cat, entries in by_category.items():
        filename = CATEGORY_FILES.get(cat, f"{cat}.json")
        target = registry_dir / filename

        existing = []
        if target.exists():
            try:
                with open(target) as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        existing_ids = {e.get("id") for e in existing}
        new_entries = [e for e in entries if e.get("id") not in existing_ids]
        skipped = len(entries) - len(new_entries)

        if skipped:
            print(f"    ⏭️  Skipped {skipped} duplicate IDs in {filename}")

        if new_entries:
            existing.extend(new_entries)
            with open(target, "w") as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)
            print(f"    ✅ Added {len(new_entries)} entries to {filename}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI-Pulse review agent")
    parser.add_argument("input", help="Path to candidate JSON file")
    parser.add_argument("--threshold", type=int, default=7,
                        help="Min score (0-10) to auto-approve (default: 7)")
    parser.add_argument("--out", help="Save reviewed candidates to this file")
    parser.add_argument("--promote", action="store_true",
                        help="Promote approved entries to registry/ files")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without calling Claude or writing files")
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

    print("🔬 AI-Pulse Review Agent")
    print(f"   Input:     {input_path}")
    print(f"   Threshold: {args.threshold}/10")
    print(f"   Model:     claude-opus-4-6 (adaptive thinking + prompt caching)")
    print()

    client = anthropic.Anthropic()
    approved, flagged, rejected = review_candidates(
        client, candidates, threshold=args.threshold, dry_run=args.dry_run
    )

    print()
    print("=" * 50)
    print(f"Results:")
    print(f"  ✅ Approved: {len(approved)}")
    print(f"  ⚠️  Flagged:  {len(flagged)}")
    print(f"  ❌ Rejected: {len(rejected)}")
    print()

    if args.promote and approved and not args.dry_run:
        print("🚀 Promoting approved entries to registry/...")
        root_dir = Path(__file__).parent.parent
        promote_entries(approved, root_dir / "registry")
        write_audit_records(approved, input_path, root_dir / "registry")
        print()

    if args.out and not args.dry_run:
        output = {
            "approved": approved,
            "flagged": flagged,
            "rejected": rejected,
        }
        with open(args.out, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"💾 Full review saved to: {args.out}")
    elif args.dry_run:
        print("[dry-run] No files written.")

    if approved and not args.promote:
        print("👉 Next steps:")
        print(f"   Re-run with --promote to add {len(approved)} approved entries to registry/")
        print("   Or review them manually in the approved list")
        print("   Then run: python scripts/build_readme.py")


if __name__ == "__main__":
    main()

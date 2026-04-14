#!/usr/bin/env python3
"""
AI-Pulse: update_entry.py
--------------------------
Re-checks existing registry entries for staleness, dead URLs, and
suggests updated descriptions or curator notes via Claude.

Usage:
    python agents/update_entry.py
    python agents/update_entry.py --file registry/llms.json
    python agents/update_entry.py --url-check
    python agents/update_entry.py --dry-run
    python agents/update_entry.py --out suggestions.json

Requires:
    pip install anthropic
    export ANTHROPIC_API_KEY=your-key
"""

import json
import sys
import argparse
import datetime
import urllib.request
import urllib.error
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

STALE_DAYS = 180
URL_TIMEOUT = 5

EXCLUDED_FILES = {"schema.json", "audit.json", "trending.json"}

# ---------------------------------------------------------------------------
# System prompt (cached across all entries in a batch)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are an expert AI curator for the AI-Pulse registry — a structured, high-density
repository of AI tools, models, papers, and frameworks. Your job is to review flagged
registry entries and suggest concise, accurate updates.

When suggesting changes:
- Descriptions: max 280 chars, accurate, use-case focused, written for AI practitioners
- Curator notes: max 140 chars, must offer genuine practitioner insight, not generic praise

Rules:
- Only suggest changes if the entry genuinely needs updating based on what you know
- If the entry looks accurate, say so — set needs_update to false
- Be specific about what changed and why
- If you cannot verify current state, note the uncertainty
- Write for AI engineers and researchers who are time-constrained

Good curator note examples:
  "The async event-driven architecture in 0.4 is a major leap. Best for complex multi-agent systems."
  "Unprecedented cost/performance ratio for reasoning tasks. Critical for cost-sensitive agentic pipelines."

Output format — respond with ONLY valid JSON, no markdown, no explanation:
{
  "needs_update": true | false,
  "suggested_description": "<updated description or null if unchanged>",
  "suggested_curator_note": "<updated note or null if unchanged>",
  "reason": "<one sentence explaining what changed or why update is needed>"
}
"""

UPDATE_PROMPT_TEMPLATE = """\
Review this registry entry that has been flagged as potentially stale.
Suggest updates if needed based on your knowledge of the current AI ecosystem.

Entry:
{entry_json}

Flags:
{flags}

Return ONLY valid JSON with keys: needs_update, suggested_description, suggested_curator_note, reason
"""


# ---------------------------------------------------------------------------
# URL checking
# ---------------------------------------------------------------------------

def check_url(url: str, timeout: int = URL_TIMEOUT) -> tuple[bool, str]:
    """Check if a URL is reachable. Returns (is_alive, status_message)."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "AI-Pulse/1.0 (registry health check)")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        # Try GET fallback for 405 (Method Not Allowed), 403, or redirects
        if e.code in (405, 403, 301, 302):
            try:
                req2 = urllib.request.Request(url)
                req2.add_header("User-Agent", "AI-Pulse/1.0 (registry health check)")
                with urllib.request.urlopen(req2, timeout=timeout) as resp:
                    return True, f"HTTP {resp.status} (GET fallback)"
            except Exception:
                pass
        if e.code >= 400:
            return False, f"HTTP {e.code}"
        return True, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, f"URL error: {e.reason}"
    except TimeoutError:
        return False, "Timeout"
    except Exception as e:
        return False, f"Error: {e}"


# ---------------------------------------------------------------------------
# Staleness detection
# ---------------------------------------------------------------------------

def get_entry_age_days(entry: dict) -> int | None:
    """Return the age in days based on last_updated or added_date, or None."""
    date_str = entry.get("last_updated", "") or entry.get("added_date", "")
    if not date_str:
        return None
    try:
        updated = datetime.date.fromisoformat(date_str)
        return (datetime.date.today() - updated).days
    except ValueError:
        return None


def get_flags(entry: dict, url_alive: bool | None) -> list[str]:
    """Return a list of flag strings describing why an entry was flagged."""
    flags = []

    age = get_entry_age_days(entry)
    if age is None:
        flags.append("no last_updated or added_date field")
    elif age > STALE_DAYS:
        date_str = entry.get("last_updated", "") or entry.get("added_date", "")
        flags.append(f"last_updated is {age} days ago (>{STALE_DAYS} day threshold, since {date_str})")

    if url_alive is False:
        flags.append(f"URL appears unreachable: {entry.get('url', '')}")

    return flags


# ---------------------------------------------------------------------------
# Claude suggestion
# ---------------------------------------------------------------------------

def suggest_update(client: anthropic.Anthropic, entry: dict, flags: list[str]) -> dict:
    """Call Claude to suggest updates for a flagged entry using streaming."""
    entry_json = json.dumps(entry, indent=2, ensure_ascii=False)
    flags_text = "\n".join(f"- {f}" for f in flags)
    prompt = UPDATE_PROMPT_TEMPLATE.format(entry_json=entry_json, flags=flags_text)

    full_text = ""
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=400,
        thinking={"type": "adaptive"},
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            full_text += text

    try:
        result = json.loads(full_text.strip())
    except json.JSONDecodeError:
        result = {
            "needs_update": False,
            "suggested_description": None,
            "suggested_curator_note": None,
            "reason": "Could not parse Claude response — manual review needed",
        }

    # Enforce length limits on suggestions
    if result.get("suggested_description") and len(result["suggested_description"]) > 280:
        result["suggested_description"] = result["suggested_description"][:277] + "..."
    if result.get("suggested_curator_note") and len(result["suggested_curator_note"]) > 140:
        result["suggested_curator_note"] = result["suggested_curator_note"][:137] + "..."

    return result


# ---------------------------------------------------------------------------
# Registry loading
# ---------------------------------------------------------------------------

def load_registry_files(
    registry_dir: Path,
    target_file: str | None = None,
) -> list[tuple[Path, list[dict]]]:
    """Load registry files. Returns list of (path, entries) tuples."""
    results = []

    if target_file:
        path = Path(target_file)
        if not path.is_absolute():
            path = registry_dir.parent / target_file
        try:
            with open(path) as f:
                data = json.load(f)
            if isinstance(data, list):
                results.append((path, data))
            else:
                print(f"❌ {path}: root element must be a JSON array", file=sys.stderr)
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Error loading {path}: {e}", file=sys.stderr)
    else:
        for json_file in sorted(registry_dir.glob("*.json")):
            if json_file.name in EXCLUDED_FILES:
                continue
            try:
                with open(json_file) as f:
                    data = json.load(f)
                if isinstance(data, list):
                    results.append((json_file, data))
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  Error loading {json_file}: {e}", file=sys.stderr)

    return results


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def process_entries(
    client: anthropic.Anthropic,
    registry_files: list[tuple[Path, list[dict]]],
    url_check: bool = False,
    dry_run: bool = False,
) -> list[dict]:
    """Process all entries, flag stale/dead ones, and gather Claude suggestions."""
    suggestions = []
    total_entries = sum(len(entries) for _, entries in registry_files)

    print(f"📋 Loaded {total_entries} entries from {len(registry_files)} file(s)")
    print()

    for file_path, entries in registry_files:
        stale_in_file = sum(1 for e in entries if (get_entry_age_days(e) or 0) > STALE_DAYS)
        print(f"📁 {file_path.name}: {len(entries)} entries, {stale_in_file} potentially stale")

        for entry in entries:
            entry_id = entry.get("id", "unknown")
            name = entry.get("name", "Unknown")
            url = entry.get("url", "")

            url_alive: bool | None = None
            if url_check and url:
                url_alive, url_status = check_url(url)
                status_icon = "🟢" if url_alive else "🔴"
                if not url_alive:
                    print(f"  {status_icon} Dead URL [{entry_id}]: {url_status}")

            flags = get_flags(entry, url_alive)
            if not flags:
                continue

            print(f"  🔍 Flagged: {name[:50]} — {flags[0][:60]}")

            if dry_run:
                suggestions.append({
                    "id": entry_id,
                    "name": name,
                    "file": str(file_path),
                    "flags": flags,
                    "suggestion": {"needs_update": None, "reason": "[dry-run]"},
                })
                continue

            try:
                suggestion = suggest_update(client, entry, flags)
                record = {
                    "id": entry_id,
                    "name": name,
                    "file": str(file_path),
                    "flags": flags,
                    "suggestion": suggestion,
                }
                suggestions.append(record)

                icon = "✏️ " if suggestion.get("needs_update") else "💤"
                reason = suggestion.get("reason", "")[:70]
                print(f"    {icon} {reason}")

            except anthropic.APIError as e:
                print(f"    ⚠️  API error for {entry_id}: {e}", file=sys.stderr)
            except Exception as e:
                print(f"    ⚠️  Unexpected error for {entry_id}: {e}", file=sys.stderr)

    return suggestions


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def render_report(suggestions: list[dict]) -> str:
    """Render a human-readable summary report of all suggestions."""
    lines = [
        "=" * 60,
        "AI-Pulse Update Agent — Suggestions Report",
        "=" * 60,
        "",
    ]

    needs_update = [s for s in suggestions if s.get("suggestion", {}).get("needs_update")]
    no_change = [s for s in suggestions if not s.get("suggestion", {}).get("needs_update")]

    lines.append(f"📊 Summary: {len(suggestions)} flagged entries analysed")
    lines.append(f"   ✏️  Needs update:    {len(needs_update)}")
    lines.append(f"   💤 No update needed: {len(no_change)}")
    lines.append("")

    if needs_update:
        lines.append("── Suggested Updates ──")
        lines.append("")
        for s in needs_update:
            lines.append(f"🔧 {s['name']} ({s['id']})")
            lines.append(f"   File:   {Path(s['file']).name}")
            lines.append(f"   Flags:  {'; '.join(s['flags'])}")
            reason = s["suggestion"].get("reason", "")
            lines.append(f"   Reason: {reason}")
            new_desc = s["suggestion"].get("suggested_description")
            if new_desc:
                preview = new_desc[:100] + ("..." if len(new_desc) > 100 else "")
                lines.append(f"   New description:   {preview}")
            new_note = s["suggestion"].get("suggested_curator_note")
            if new_note:
                lines.append(f"   New curator_note:  {new_note}")
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="AI-Pulse update agent — flags and re-curates stale registry entries"
    )
    parser.add_argument("--file", help="Target a specific registry file (e.g. registry/llms.json)")
    parser.add_argument(
        "--url-check",
        action="store_true",
        help="Enable URL liveness checking via HEAD requests (off by default to save time)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Flag stale entries without calling Claude or writing output files",
    )
    parser.add_argument("--out", help="Write JSON suggestions report to this file")
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    registry_dir = root_dir / "registry"

    print("🔄 AI-Pulse Update Agent")
    print(f"   Model:           claude-opus-4-6 (adaptive thinking + prompt caching)")
    print(f"   URL check:       {'enabled' if args.url_check else 'disabled (use --url-check to enable)'}")
    print(f"   Stale threshold: {STALE_DAYS} days")
    if args.dry_run:
        print(f"   Mode:            dry-run")
    print()

    registry_files = load_registry_files(registry_dir, args.file)
    if not registry_files:
        print("❌ No registry files found.", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic()
    suggestions = process_entries(
        client,
        registry_files,
        url_check=args.url_check,
        dry_run=args.dry_run,
    )

    print()
    print(render_report(suggestions))

    if args.out and not args.dry_run:
        out_path = Path(args.out)
        with open(out_path, "w") as f:
            json.dump(suggestions, f, indent=2, ensure_ascii=False)
        print(f"💾 Suggestions written to: {out_path}")
    elif args.dry_run:
        print("[dry-run] No files written.")
    elif not suggestions:
        print("✅ No stale entries found — registry is up to date.")


if __name__ == "__main__":
    main()

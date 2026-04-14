#!/usr/bin/env python3
"""
AI-Pulse: add_entry.py
-----------------------
Interactive CLI to add a new entry directly to a registry file.
Validates against schema rules, uses Claude to suggest missing fields,
and saves the result.

Usage:
    python agents/add_entry.py
    python agents/add_entry.py --category llm
    python agents/add_entry.py --json '{"name": "MyTool", ...}'
    python agents/add_entry.py --from-url https://github.com/org/repo

Requires:
    pip install anthropic
    export ANTHROPIC_API_KEY=your-key
"""

import json
import sys
import argparse
import datetime
import re
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_CATEGORIES = [
    "llm", "agent-framework", "vector-db", "mcp-server",
    "tool", "dataset", "paper", "course", "project",
]
VALID_PRICING = ["free", "open-source", "freemium", "paid", "enterprise"]
VALID_MATURITY = ["experimental", "beta", "stable", "production"]

CATEGORY_FILES = {
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

FILL_PROMPT = """\
You are helping add a new entry to the AI-Pulse registry.

Given the partial entry below, fill in ALL missing or empty fields.
Return ONLY valid JSON with these exact fields (no extras):
- id: kebab-case slug (max 60 chars, lowercase, alphanumeric + hyphens only)
- name: human-readable display name
- category: one of {categories}
- subcategory: optional finer grouping (string, can be empty string)
- description: one clear sentence, max 280 chars, explains what it is and who it's for
- url: primary URL (must start with https://)
- github_url: GitHub repo URL (start with https://github.com/) or empty string if none
- stars_approx: approximate GitHub stars as integer (0 if not OSS)
- tags: array of 3-8 lowercase tag strings
- license: SPDX identifier, "proprietary", or "unknown"
- added_date: today's date {today} in YYYY-MM-DD
- last_updated: same as added_date
- curator_note: one insightful sentence, max 140 chars, explains WHY it matters (not generic praise)
- pricing: one of {pricing}
- maturity: one of {maturity}

Partial entry:
{partial}

Return ONLY valid JSON. No markdown, no explanation.
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:60].strip("-")


def load_registry_file(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        with open(path) as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_registry_file(path: Path, entries: list[dict]) -> None:
    with open(path, "w") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def prompt_input(label: str, default: str = "", required: bool = False) -> str:
    suffix = f" [{default}]" if default else (" (required)" if required else " (optional)")
    while True:
        value = input(f"  {label}{suffix}: ").strip()
        if not value and default:
            return default
        if not value and required:
            print(f"  ⚠️  {label} is required.")
            continue
        return value


def prompt_choice(label: str, choices: list[str], default: str = "") -> str:
    options = " / ".join(choices)
    suffix = f" [{default}]" if default else ""
    print(f"  {label} ({options}){suffix}:")
    while True:
        value = input("  > ").strip().lower()
        if not value and default:
            return default
        if value in choices:
            return value
        print(f"  ⚠️  Must be one of: {options}")


# ---------------------------------------------------------------------------
# Claude-powered field filler
# ---------------------------------------------------------------------------

def fill_with_claude(client: anthropic.Anthropic, partial: dict) -> dict:
    """Ask Claude to complete any missing fields in the entry."""
    today = datetime.date.today().isoformat()
    prompt = FILL_PROMPT.format(
        categories=", ".join(VALID_CATEGORIES),
        pricing=", ".join(VALID_PRICING),
        maturity=", ".join(VALID_MATURITY),
        today=today,
        partial=json.dumps(partial, indent=2, ensure_ascii=False),
    )

    print("\n  🤖 Claude is filling in missing fields...")

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1000,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": prompt}],
    )

    text = next((b.text for b in response.content if b.type == "text"), "{}")

    try:
        filled = json.loads(text.strip())
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Could not parse Claude's response: {e}")
        filled = partial

    return filled


# ---------------------------------------------------------------------------
# Interactive entry builder
# ---------------------------------------------------------------------------

def build_entry_interactively(
    client: anthropic.Anthropic,
    prefill: dict | None = None,
    ai_assist: bool = True,
) -> dict:
    """Walk the user through building a registry entry interactively."""
    print("\n📝 New Registry Entry")
    print("   Leave blank to skip optional fields. Claude will fill missing required fields.\n")

    entry = prefill.copy() if prefill else {}

    # --- Core required fields ---
    if "name" not in entry:
        entry["name"] = prompt_input("Name", required=True)

    if "category" not in entry:
        entry["category"] = prompt_choice("Category", VALID_CATEGORIES, default="tool")

    if "url" not in entry:
        entry["url"] = prompt_input("URL (homepage or docs)", required=True)

    if "description" not in entry:
        entry["description"] = prompt_input("Description (one sentence, max 280 chars)")

    # --- Optional fields ---
    if "github_url" not in entry:
        entry["github_url"] = prompt_input("GitHub URL")

    if "pricing" not in entry:
        entry["pricing"] = prompt_choice("Pricing", VALID_PRICING, default="open-source")

    if "maturity" not in entry:
        entry["maturity"] = prompt_choice("Maturity", VALID_MATURITY, default="stable")

    if "tags" not in entry:
        raw_tags = prompt_input("Tags (comma-separated, 3-8)")
        entry["tags"] = [t.strip() for t in raw_tags.split(",") if t.strip()]

    # --- Let Claude fill in the rest ---
    if ai_assist:
        filled = fill_with_claude(client, entry)
        # Merge: user values take precedence over AI suggestions for fields already set
        for key, value in filled.items():
            if key not in entry or not entry[key]:
                entry[key] = value
    else:
        # Manual fallback — ensure required fields have values
        today = datetime.date.today().isoformat()
        entry.setdefault("id", slugify(entry.get("name", "entry")))
        entry.setdefault("subcategory", "")
        entry.setdefault("stars_approx", 0)
        entry.setdefault("license", "unknown")
        entry.setdefault("added_date", today)
        entry.setdefault("last_updated", today)
        entry.setdefault("curator_note", "")

    return entry


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_entry(entry: dict) -> list[str]:
    """Return list of validation errors (empty = valid)."""
    errors = []
    required = ["id", "name", "category", "description", "url", "tags", "added_date", "stars_approx"]
    for field in required:
        if field not in entry or entry[field] is None or entry[field] == "":
            errors.append(f"Missing required field: {field}")

    if entry.get("category") not in VALID_CATEGORIES:
        errors.append(f"Invalid category: {entry.get('category')}")
    if entry.get("pricing") and entry.get("pricing") not in VALID_PRICING:
        errors.append(f"Invalid pricing: {entry.get('pricing')}")
    if entry.get("maturity") and entry.get("maturity") not in VALID_MATURITY:
        errors.append(f"Invalid maturity: {entry.get('maturity')}")

    url = entry.get("url", "")
    if url and not (url.startswith("http://") or url.startswith("https://")):
        errors.append(f"URL must start with http:// or https://")

    tags = entry.get("tags", [])
    if not isinstance(tags, list) or len(tags) == 0:
        errors.append("tags must be a non-empty array")

    desc = entry.get("description", "")
    if len(desc) > 280:
        errors.append(f"description too long ({len(desc)} chars, max 280)")

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI-Pulse interactive entry adder")
    parser.add_argument("--category", choices=VALID_CATEGORIES,
                        help="Pre-select category")
    parser.add_argument("--json", dest="json_str",
                        help="Start with a partial JSON entry string")
    parser.add_argument("--no-ai", action="store_true",
                        help="Skip Claude assistance (manual mode)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview entry without saving")
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    registry_dir = root_dir / "registry"

    prefill: dict = {}
    if args.category:
        prefill["category"] = args.category
    if args.json_str:
        try:
            prefill = json.loads(args.json_str)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    print("➕ AI-Pulse Add Entry")
    print(f"   Registry: {registry_dir}")
    print(f"   AI assist: {'off' if args.no_ai else 'on (claude-opus-4-6)'}")

    client = anthropic.Anthropic() if not args.no_ai else None

    entry = build_entry_interactively(
        client=client,
        prefill=prefill,
        ai_assist=not args.no_ai,
    )

    # --- Show preview ---
    print("\n" + "=" * 50)
    print("📋 Entry Preview:")
    print(json.dumps(entry, indent=2, ensure_ascii=False))
    print("=" * 50)

    # --- Validate ---
    errors = validate_entry(entry)
    if errors:
        print("\n❌ Validation errors:")
        for e in errors:
            print(f"   • {e}")
        if not args.dry_run:
            print("\nFix these errors and re-run.")
            sys.exit(1)

    if args.dry_run:
        print("\n[dry-run] Entry not saved.")
        return

    # --- Confirm ---
    confirm = input("\nSave this entry? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    # --- Save ---
    category = entry.get("category", "tool")
    filename = CATEGORY_FILES.get(category, f"{category}.json")
    target = registry_dir / filename

    existing = load_registry_file(target)
    existing_ids = {e.get("id") for e in existing}

    if entry.get("id") in existing_ids:
        print(f"⚠️  Entry with ID '{entry['id']}' already exists in {filename}")
        overwrite = input("   Overwrite? [y/N]: ").strip().lower()
        if overwrite != "y":
            print("Aborted.")
            return
        existing = [e for e in existing if e.get("id") != entry["id"]]

    existing.append(entry)
    save_registry_file(target, existing)

    print(f"\n✅ Entry saved to {filename}")
    print(f"\n👉 Next steps:")
    print(f"   python scripts/validate_registry.py --file {target}")
    print(f"   python scripts/build_readme.py")


if __name__ == "__main__":
    main()

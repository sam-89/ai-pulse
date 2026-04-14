#!/usr/bin/env python3
"""
AI-Pulse: validate_registry.py
--------------------------------
Validates all JSON registry files against the schema rules.
Used as a pre-commit hook and in CI/CD.

Usage:
    python scripts/validate_registry.py
    python scripts/validate_registry.py --strict   # Fail on warnings too
    python scripts/validate_registry.py --file registry/llms.json
    python scripts/validate_registry.py --candidates  # Also validate candidates/
"""

import json
import sys
import argparse
import datetime
from pathlib import Path

REQUIRED_FIELDS = ["id", "name", "category", "description", "url", "tags", "added_date", "stars_approx"]

VALID_CATEGORIES = {
    "llm", "agent-framework", "vector-db", "mcp-server",
    "tool", "dataset", "paper", "course", "project"
}

VALID_PRICING = {"free", "open-source", "freemium", "paid", "enterprise"}
VALID_MATURITY = {"experimental", "beta", "stable", "production"}


def validate_entry(entry: dict, file_path: str, index: int) -> tuple[list[str], list[str]]:
    """Validate a single registry entry. Returns (errors, warnings)."""
    errors = []
    warnings = []
    loc = f"{file_path}[{index}]"

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in entry or entry[field] is None:
            errors.append(f"{loc}: Missing required field '{field}'")
        elif entry[field] == "":
            errors.append(f"{loc}: Field '{field}' must not be empty")

    # Category validation
    cat = entry.get("category", "")
    if cat and cat not in VALID_CATEGORIES:
        errors.append(f"{loc}: Invalid category '{cat}'. Must be one of: {sorted(VALID_CATEGORIES)}")

    # Pricing validation
    pricing = entry.get("pricing", "")
    if pricing and pricing not in VALID_PRICING:
        errors.append(f"{loc}: Invalid pricing '{pricing}'. Must be one of: {sorted(VALID_PRICING)}")

    # Maturity validation
    maturity = entry.get("maturity", "")
    if maturity and maturity not in VALID_MATURITY:
        errors.append(f"{loc}: Invalid maturity '{maturity}'. Must be one of: {sorted(VALID_MATURITY)}")

    # URL format check
    url = entry.get("url", "")
    if url and not (url.startswith("http://") or url.startswith("https://")):
        errors.append(f"{loc}: URL must start with http:// or https://: '{url}'")

    # GitHub URL check
    github_url = entry.get("github_url", "")
    if github_url and not github_url.startswith("https://github.com/"):
        warnings.append(f"{loc}: 'github_url' should start with https://github.com/")

    # Tags must be a list
    tags = entry.get("tags", [])
    if not isinstance(tags, list):
        errors.append(f"{loc}: 'tags' must be an array")
    elif len(tags) == 0:
        errors.append(f"{loc}: 'tags' must have at least 1 entry")
    elif len(tags) > 10:
        warnings.append(f"{loc}: 'tags' has {len(tags)} entries (recommended max 10)")

    # Description length
    desc = entry.get("description", "")
    if len(desc) > 280:
        warnings.append(f"{loc}: 'description' is {len(desc)} chars (max 280)")
    elif len(desc) < 20:
        warnings.append(f"{loc}: 'description' is very short ({len(desc)} chars)")

    # Curator note check
    curator = entry.get("curator_note", "")
    if curator and curator.startswith("⚠️"):
        warnings.append(f"{loc}: Entry still has placeholder curator_note — needs human review")
    if curator and len(curator) > 140:
        warnings.append(f"{loc}: 'curator_note' is {len(curator)} chars (max 140)")

    # Stars must be a non-negative integer
    stars = entry.get("stars_approx", 0)
    if not isinstance(stars, int) or stars < 0:
        errors.append(f"{loc}: 'stars_approx' must be a non-negative integer")

    # Date format check
    for date_field in ("added_date", "last_updated"):
        val = entry.get(date_field, "")
        if val:
            try:
                datetime.date.fromisoformat(val)
            except ValueError:
                errors.append(f"{loc}: '{date_field}' must be ISO date format YYYY-MM-DD, got '{val}'")

    return errors, warnings


def validate_file(file_path: Path) -> tuple[list[str], list[str]]:
    """Validate a registry JSON file. Returns (errors, warnings)."""
    errors = []
    warnings = []

    try:
        with open(file_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"{file_path}: Invalid JSON — {e}"], []
    except IOError as e:
        return [f"{file_path}: Cannot read file — {e}"], []

    if not isinstance(data, list):
        return [f"{file_path}: Root element must be a JSON array"], []

    ids = []
    for i, entry in enumerate(data):
        entry_errors, entry_warnings = validate_entry(entry, str(file_path), i)
        errors.extend(entry_errors)
        warnings.extend(entry_warnings)

        # Check for duplicate IDs within file
        entry_id = entry.get("id", "")
        if entry_id in ids:
            errors.append(f"{file_path}[{i}]: Duplicate ID '{entry_id}' within file")
        elif entry_id:
            ids.append(entry_id)

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="AI-Pulse registry validator")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--file", help="Validate a specific file only")
    parser.add_argument("--candidates", action="store_true", help="Also validate candidates/ directory")
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    registry_dir = root_dir / "registry"

    if args.file:
        files = [Path(args.file)]
    else:
        files = [
            f for f in registry_dir.glob("*.json")
            if f.name not in ("schema.json",)
        ]
        if args.candidates:
            candidates_dir = registry_dir / "candidates"
            if candidates_dir.exists():
                files.extend(candidates_dir.glob("*.json"))

    if not files:
        print("⚠️  No registry files found.")
        sys.exit(0)

    print(f"🔍 Validating {len(files)} registry file(s)...")
    print()

    all_errors = []
    all_warnings = []
    total_entries = 0

    for file_path in sorted(files):
        try:
            with open(file_path) as f:
                data = json.load(f)
            total_entries += len(data) if isinstance(data, list) else 0
        except Exception:
            pass

        errors, warnings = validate_file(file_path)
        rel_path = file_path.relative_to(root_dir)

        if errors or warnings:
            print(f"📁 {rel_path}")
            for e in errors:
                print(f"  ❌ {e}")
            for w in warnings:
                print(f"  ⚠️  {w}")
            print()

        all_errors.extend(errors)
        all_warnings.extend(warnings)

    print(f"{'='*50}")
    print(f"Validated {total_entries} entries across {len(files)} files")
    print(f"❌ {len(all_errors)} errors · ⚠️  {len(all_warnings)} warnings")

    if not all_errors and not all_warnings:
        print("✅ All entries valid!")

    if all_errors:
        sys.exit(1)
    if args.strict and all_warnings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

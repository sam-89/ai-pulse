#!/usr/bin/env python3
"""
AI-Pulse: check_urls.py
-----------------------
Checks all URLs in registry files for liveness.
Reports dead/unreachable URLs and optionally fails CI if too many are dead.

Usage:
    python scripts/check_urls.py
    python scripts/check_urls.py --fail-threshold 10   # fail if >10% dead
    python scripts/check_urls.py --timeout 5
    python scripts/check_urls.py --file registry/llms.json
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


SKIP_FILES = {"schema.json", "audit.json", "trending.json"}


def load_urls(registry_dir: Path, specific_file: Path | None) -> list[tuple[str, str]]:
    """Return a list of (entry_id, url) pairs from registry files."""
    pairs: list[tuple[str, str]] = []

    if specific_file:
        files = [specific_file]
    else:
        files = [
            f for f in sorted(registry_dir.glob("*.json"))
            if f.name not in SKIP_FILES
        ]

    for json_file in files:
        try:
            with open(json_file) as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Cannot load {json_file}: {e}")
            continue

        if not isinstance(data, list):
            continue

        for entry in data:
            url = entry.get("url", "")
            entry_id = entry.get("id", "?")
            if url:
                pairs.append((entry_id, url))

    return pairs


def check_url(url: str, timeout: int) -> tuple[bool, str]:
    """
    Check whether a URL is reachable.

    Returns (is_alive, status_message).
    Tries HEAD first; falls back to GET on 405 or other failures.
    """
    req_head = urllib.request.Request(url, method="HEAD")
    req_head.add_header("User-Agent", "AI-Pulse/url-checker")

    try:
        with urllib.request.urlopen(req_head, timeout=timeout) as resp:
            return True, str(resp.status)
    except urllib.error.HTTPError as e:
        if e.code == 405:
            # Server doesn't allow HEAD — retry with GET
            req_get = urllib.request.Request(url, method="GET")
            req_get.add_header("User-Agent", "AI-Pulse/url-checker")
            try:
                with urllib.request.urlopen(req_get, timeout=timeout) as resp:
                    return True, str(resp.status)
            except urllib.error.HTTPError as e2:
                return False, f"HTTP {e2.code}"
            except (urllib.error.URLError, OSError) as e2:
                return False, str(e2)
        return False, f"HTTP {e.code}"
    except (urllib.error.URLError, OSError) as e:
        return False, str(e)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI-Pulse URL liveness checker")
    parser.add_argument("--timeout", type=int, default=5, help="Request timeout in seconds (default: 5)")
    parser.add_argument(
        "--fail-threshold",
        type=float,
        default=20.0,
        dest="fail_threshold",
        help="Exit with code 1 if dead%% exceeds this value (default: 20)",
    )
    parser.add_argument("--file", help="Check a specific registry file only")
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    registry_dir = root_dir / "registry"

    specific_file = Path(args.file) if args.file else None
    pairs = load_urls(registry_dir, specific_file)

    if not pairs:
        print("⚠️  No URLs found to check.")
        sys.exit(0)

    print(f"🔗 Checking {len(pairs)} URLs (timeout={args.timeout}s)...\n")

    total = len(pairs)
    ok = 0
    dead = 0
    skipped = 0
    dead_entries: list[tuple[str, str, str]] = []

    col_id = max(len(eid) for eid, _ in pairs)
    col_url = min(max(len(url) for _, url in pairs), 60)

    for entry_id, url in pairs:
        if not url.startswith("https://"):
            skipped += 1
            status_icon = "⏭️ "
            status_msg = "skipped (non-https)"
        else:
            is_alive, status_msg = check_url(url, args.timeout)
            if is_alive:
                ok += 1
                status_icon = "✅"
            else:
                dead += 1
                status_icon = "❌"
                dead_entries.append((entry_id, url, status_msg))

        url_display = url[:col_url] + "…" if len(url) > col_url else url
        print(f"  {status_icon} {entry_id:<{col_id}}  {url_display:<{col_url}}  {status_msg}")

    checked = ok + dead
    dead_pct = (dead / checked * 100) if checked > 0 else 0.0

    print(f"\n{'='*60}")
    print(f"Total: {total}  |  ✅ OK: {ok}  |  ❌ Dead: {dead}  |  ⏭️  Skipped: {skipped}")
    if checked > 0:
        print(f"Dead rate: {dead_pct:.1f}%  (threshold: {args.fail_threshold:.0f}%)")

    if dead_entries:
        print("\n📋 Dead URLs summary:")
        for eid, url, reason in dead_entries:
            print(f"  ❌ [{eid}] {url}  — {reason}")

    if dead_pct > args.fail_threshold:
        print(f"\n💥 Dead rate {dead_pct:.1f}% exceeds threshold {args.fail_threshold:.0f}% — failing.")
        sys.exit(1)

    print("\n✅ URL check passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()

"""Resolve every relative Markdown link in the series and report the broken ones.

Examples:

    python3 scripts/verify_links.py
    python3 scripts/verify_links.py --root rag-deep-dive

Only relative links are checked. External URLs, mailto:, and bare anchors are
out of scope: this exists to catch a file that moved without its inbound links
moving with it, which is the failure a reorganisation actually causes.

A link into a submodule that has not been checked out is reported separately
rather than as a break, so a shallow clone does not produce false alarms.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]

# [text](target) with the target not starting a scheme, an anchor, or a slash.
LINK = re.compile(r"\[(?:[^\]]*)\]\(\s*(?!<)([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".history", ".ruff_cache"}
EXTERNAL = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)


def is_relative(target: str) -> bool:
    """True when the target names a path inside the working tree."""
    if not target or target.startswith("#"):
        return False
    if EXTERNAL.match(target):
        return False
    return not target.startswith("//")


def markdown_files(base: Path) -> list[Path]:
    found = []
    for path in base.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        found.append(path)
    return sorted(found)


def submodule_dirs(base: Path) -> set[Path]:
    """Directories that are submodules, checked out or not."""
    gitmodules = base / ".gitmodules"
    if not gitmodules.is_file():
        return set()
    paths = re.findall(r"^\s*path\s*=\s*(.+)$", gitmodules.read_text(), re.MULTILINE)
    return {base / p.strip() for p in paths}


def check(base: Path) -> tuple[list[str], list[str], int]:
    broken: list[str] = []
    uncheckable: list[str] = []
    total = 0

    submodules = submodule_dirs(base)
    empty = {d for d in submodules if not any(d.iterdir())} if submodules else set()

    for doc in markdown_files(base):
        text = doc.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for raw in LINK.findall(line):
                target = raw.split("#", 1)[0].strip()
                if not is_relative(target):
                    continue
                total += 1
                resolved = (doc.parent / unquote(target)).resolve()
                if resolved.exists():
                    continue
                where = f"{doc.relative_to(base)}:{lineno}"
                if any(str(resolved).startswith(str(d)) for d in empty):
                    uncheckable.append(f"  {where}\n    -> {raw} (submodule not checked out)")
                else:
                    broken.append(f"  {where}\n    -> {raw}")

    return broken, uncheckable, total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=str(ROOT),
        help="directory to check (defaults to the repository root)",
    )
    args = parser.parse_args()

    base = Path(args.root).resolve()
    if not base.is_dir():
        print(f"not a directory: {base}", file=sys.stderr)
        return 2

    broken, uncheckable, total = check(base)
    files = len(markdown_files(base))
    print(f"checked {total} relative links in {files} files")

    if uncheckable:
        print(f"\nSKIPPED ({len(uncheckable)}): submodule not checked out")
        for item in uncheckable[:10]:
            print(item)
        if len(uncheckable) > 10:
            print(f"  ... and {len(uncheckable) - 10} more")

    if broken:
        print(f"\nBROKEN ({len(broken)}):")
        for item in broken:
            print(item)
        return 1

    print("all relative links resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

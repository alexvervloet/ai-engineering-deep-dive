"""Resolve every file path a comment or doc line tells the reader to go look at.

Examples:

    python3 scripts/verify_paths.py
    python3 scripts/verify_paths.py --root rag-deep-dive

verify_links.py covers Markdown links. This covers the other half: the paths
named in prose, inside error messages, comments, docstrings, and file maps.
Those are never links, so nothing checked them, and they are read at the worst
possible moment. The series shipped `see SECRETS.md` in 129 files for months
while the file sat at `docs/SECRETS.md`, and the reader who met that message
had just failed to run something.

Only navigational mentions count: a path introduced by "see". A filename that
merely appears in a sentence is usually a description rather than an
instruction, and treating those as links produces about fifty false alarms for
every real one. "read" is deliberately not a cue, because it is also something
programs do to files that do not exist yet.

A path resolves if it exists relative to the file that names it, to the root of
the repository that contains it, or to the series root. A path that matches a
file anywhere in the same repository also passes, which is what makes file-map
blocks work: they list `providers.py` under a heading, not from the repo root.

Add `verify-paths: ignore` in a comment on the line to skip a deliberate
mention of something that is not meant to resolve.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".history", ".ruff_cache"}

# CHANGELOG and LESSONS quote paths as they were, which is the point of them.
SKIP_NAMES = {"CHANGELOG.md", "LESSONS.md"}

SCAN_SUFFIXES = {".py", ".sh", ".md", ".toml", ".txt", ".example"}

EXTENSIONS = "md|py|sh|toml|yml|yaml|json|jsonl|txt|cfg|ini|example"
PATH = rf"((?:\.{{1,2}}/)?(?:[\w.-]+/)*[\w.-]+\.(?:{EXTENSIONS}))"

# "see", optionally through an article and opening bracket, then a path.
CUE = re.compile(rf"\bsee\b[^\S\n]*(?:the[^\S\n]+)?[\[`(]*{PATH}", re.IGNORECASE)

URL = re.compile(r"https?://\S+")
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\([^)]*\)")
IGNORE = re.compile(r"verify-paths:\s*ignore")


def repositories(base: Path) -> list[Path]:
    """The series root plus every checked-out submodule under it."""
    subs = sorted(p for p in base.iterdir() if p.is_dir() and (p / ".git").exists())
    return [base, *subs]


def scannable(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.name in SKIP_NAMES:
        return False
    return path.suffix in SCAN_SUFFIXES or path.name.endswith(".example")


def file_index(repo: Path) -> set[str]:
    """Every file in a repository, as a path relative to that repository."""
    return {
        str(p.relative_to(repo))
        for p in repo.rglob("*")
        if p.is_file() and not any(part in SKIP_DIRS for part in p.parts)
    }


def check(base: Path) -> tuple[list[str], int, int]:
    repos = repositories(base)
    indexes = {repo: file_index(repo) for repo in repos}

    def owner(path: Path) -> Path:
        found = base
        for repo in repos:
            if repo != base and str(path).startswith(f"{repo}/"):
                found = repo
        return found

    broken: list[str] = []
    total = 0
    scanned = 0

    for path in sorted(base.rglob("*")):
        if not path.is_file() or not scannable(path):
            continue
        repo = owner(path)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scanned += 1

        for lineno, line in enumerate(text.splitlines(), 1):
            if IGNORE.search(line):
                continue
            # Markdown links belong to verify_links.py; strip them so a correct
            # link is not reported twice under its own link text.
            stripped = MARKDOWN_LINK.sub(" ", URL.sub(" ", line))
            for target in CUE.findall(stripped):
                total += 1
                if (path.parent / target).exists():
                    continue
                if (repo / target).exists() or (base / target).exists():
                    continue
                index = indexes[repo]
                if target in index or any(e.endswith(f"/{target}") for e in index):
                    continue
                where = f"{path.relative_to(base)}:{lineno}"
                broken.append(f"  {where}\n    -> {target}\n       {line.strip()[:100]}")

    return broken, total, scanned


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

    broken, total, scanned = check(base)
    print(f"checked {total} referenced paths in {scanned} files")

    if broken:
        print(f"\nBROKEN ({len(broken)}):")
        for item in broken:
            print(item)
        return 1

    print("every referenced path resolves")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

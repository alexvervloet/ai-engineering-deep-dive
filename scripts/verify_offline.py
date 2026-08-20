"""Validate and execute the manifest of submodule offline paths.

Examples:

    python3 scripts/verify_offline.py --validate
    python3 scripts/verify_offline.py --matrix
    python3 scripts/verify_offline.py --repo rag-deep-dive

The manifest uses argv arrays rather than shell strings. Verification removes
provider credentials from the child environment so an allegedly offline command
cannot pass merely because a developer happened to have a key loaded.
"""

from __future__ import annotations

import argparse
import configparser
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tomllib
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "offline-paths.toml"
GITMODULES = ROOT / ".gitmodules"
SECRET_NAMES = {
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GROQ_API_KEY",
    "MISTRAL_API_KEY",
    "OPENAI_API_KEY",
    "TOGETHER_API_KEY",
    "VOYAGE_API_KEY",
}


class ManifestError(ValueError):
    """The offline-path manifest is incomplete, ambiguous, or unsafe to execute."""


def _submodule_paths() -> set[str]:
    parser = configparser.ConfigParser()
    if not parser.read(GITMODULES):
        raise ManifestError(f"could not read {GITMODULES}")
    return {parser[section]["path"] for section in parser.sections()}


def _commands(entry: dict[str, Any], field: str) -> tuple[tuple[str, ...], ...]:
    raw = entry.get(field, [])
    if not isinstance(raw, list):
        raise ManifestError(f"{entry.get('path')}: {field} must be an array")
    commands: list[tuple[str, ...]] = []
    for command in raw:
        if not isinstance(command, list) or not command:
            raise ManifestError(f"{entry.get('path')}: every {field} command must be nonempty")
        if not all(isinstance(token, str) and token for token in command):
            raise ManifestError(f"{entry.get('path')}: command tokens must be strings")
        if any(token in {"..", "/"} for token in command):
            raise ManifestError(f"{entry.get('path')}: broad path token is not allowed")
        commands.append(tuple(command))
    return tuple(commands)


def load_manifest() -> tuple[dict[str, Any], ...]:
    """Load the manifest and require exact path coverage of ``.gitmodules``."""

    try:
        document = tomllib.loads(MANIFEST.read_text())
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ManifestError(f"could not parse {MANIFEST}: {error}") from error
    if document.get("version") != 1:
        raise ManifestError("offline manifest version must be 1")
    raw_entries = document.get("repositories")
    if not isinstance(raw_entries, list) or not raw_entries:
        raise ManifestError("offline manifest must contain repositories")

    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in raw_entries:
        if not isinstance(raw, dict):
            raise ManifestError("every repository entry must be a table")
        path = raw.get("path")
        runtime = raw.get("runtime")
        claim = raw.get("claim")
        if not isinstance(path, str) or not path or Path(path).is_absolute() or ".." in Path(path).parts:
            raise ManifestError(f"invalid repository path: {path!r}")
        if path in seen:
            raise ManifestError(f"duplicate repository path: {path}")
        seen.add(path)
        if runtime not in {"python", "node"}:
            raise ManifestError(f"{path}: runtime must be python or node")
        version_field = "python" if runtime == "python" else "node"
        if not isinstance(raw.get(version_field), str):
            raise ManifestError(f"{path}: {version_field} version is required")
        if not isinstance(claim, str) or len(claim) < 30:
            raise ManifestError(f"{path}: claim must state the verified boundary")
        if not _commands(raw, "commands"):
            raise ManifestError(f"{path}: at least one verification command is required")
        _commands(raw, "install")
        environment = raw.get("environment", {})
        if not isinstance(environment, dict) or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in environment.items()
        ):
            raise ManifestError(f"{path}: environment must contain string pairs")
        if SECRET_NAMES & set(environment):
            raise ManifestError(f"{path}: offline path must not declare provider credentials")
        if not (ROOT / path).is_dir():
            raise ManifestError(f"{path}: submodule directory is missing")
        entries.append(raw)

    declared = set(seen)
    submodules = _submodule_paths()
    missing = sorted(submodules - declared)
    extra = sorted(declared - submodules)
    if missing or extra:
        raise ManifestError(f"manifest/.gitmodules mismatch: missing={missing}, extra={extra}")
    return tuple(entries)


def matrix(entries: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    """Return a deterministic GitHub Actions matrix for isolated repo jobs."""

    include = []
    for entry in sorted(entries, key=lambda item: item["path"]):
        version_field = "python" if entry["runtime"] == "python" else "node"
        include.append(
            {
                "path": entry["path"],
                "runtime": entry["runtime"],
                "version": entry[version_field],
            }
        )
    return {"include": include}


def _resolved(command: tuple[str, ...]) -> tuple[str, ...]:
    if command[0] == "python":
        return (sys.executable, *command[1:])
    return command


def run_entry(entry: dict[str, Any], *, skip_install: bool) -> None:
    """Run one entry in its submodule directory with provider keys removed."""

    environment = os.environ.copy()
    for name in SECRET_NAMES:
        environment.pop(name, None)
    environment.update(entry.get("environment", {}))
    environment["DEEP_DIVES_OFFLINE_VERIFY"] = "1"

    fields = ("commands",) if skip_install else ("install", "commands")
    print(f"[{entry['path']}] {entry['claim']}", flush=True)
    for field in fields:
        for command in _commands(entry, field):
            resolved = _resolved(command)
            print("+", shlex.join(resolved), flush=True)
            subprocess.run(
                resolved,
                cwd=ROOT / entry["path"],
                env=environment,
                check=True,
            )


def main() -> int:
    """Validate, print a matrix, or execute one declared offline path."""

    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--validate", action="store_true")
    action.add_argument("--matrix", action="store_true")
    action.add_argument("--repo")
    parser.add_argument("--skip-install", action="store_true")
    args = parser.parse_args()

    try:
        entries = load_manifest()
        if args.validate:
            print(f"offline manifest covers {len(entries)} submodules")
            return 0
        if args.matrix:
            print(json.dumps(matrix(entries), separators=(",", ":")))
            return 0
        selected = [entry for entry in entries if entry["path"] == args.repo]
        if not selected:
            raise ManifestError(f"repository is not declared: {args.repo}")
        run_entry(selected[0], skip_install=args.skip_install)
        return 0
    except (ManifestError, subprocess.CalledProcessError) as error:
        print(f"offline verification failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

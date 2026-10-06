#!/usr/bin/env python3
"""Basic public-repo hygiene check for a portfolio project."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DENYLIST = ROOT / ".publish-denylist"


def _git_tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [ROOT / rel for rel in result.stdout.splitlines() if rel]


def main() -> None:
    deny_terms = [line.strip() for line in DENYLIST.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]

    for path in _git_tracked_files():
        if path.suffix.lower() in {".py", ".md", ".toml", ".json", ".yml", ".yaml", ".env", ".example"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for term in deny_terms:
                if term in text:
                    raise SystemExit(f"Found denylisted term {term!r} in {path}")

    print("Public repo check passed.")


if __name__ == "__main__":
    main()

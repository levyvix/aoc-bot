#!/usr/bin/env python3
"""Post-agent sanity check — solution exists and tests pass."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ARTIFACT_DIR = Path(".aoc")


def main() -> int:
    dry_run = os.environ.get("AOC_DRY_RUN", "").lower() in {"1", "true", "yes"}
    parts = [1] if dry_run else [1, 2]

    if not (ARTIFACT_DIR / "meta.json").exists():
        print("ERROR: agent did not run prepare — missing .aoc/meta.json", file=sys.stderr)
        return 1

    failed = False
    for part in parts:
        result = subprocess.run(
            ["uv", "run", "python", "scripts/aoc_tool.py", "test", str(part)],
            env={**os.environ, "AOC_PART": str(part)},
        )
        if result.returncode != 0:
            failed = True

    if failed:
        print("ERROR: post-agent verification failed", file=sys.stderr)
        return 1

    print("Post-agent check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

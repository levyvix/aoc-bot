#!/usr/bin/env python3
"""Re-fetch puzzle page after Part 1 submit; fail if Part 2 text is still locked."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ARTIFACT_DIR = Path(".aoc")


def main() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/prepare_day.py"],
        check=False,
    )
    if result.returncode != 0:
        sys.exit(result.returncode)

    meta = json.loads((ARTIFACT_DIR / "meta.json").read_text(encoding="utf-8"))
    if not meta.get("has_part2"):
        print(
            "ERROR: Part 2 is still locked. Part 1 must be submitted and accepted "
            "before Part 2 text appears on adventofcode.com.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("Part 2 unlocked — puzzle text available")


if __name__ == "__main__":
    main()

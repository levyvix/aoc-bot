#!/usr/bin/env python3
"""Append retry feedback to the base agent prompt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ARTIFACT_DIR = Path(".aoc")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", type=int, required=True)
    parser.add_argument("--attempt", type=int, required=True)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--feedback", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    base = args.base.read_text(encoding="utf-8")
    feedback = args.feedback.read_text(encoding="utf-8").strip()
    meta = json.loads((ARTIFACT_DIR / "meta.json").read_text(encoding="utf-8"))
    solution_dir = meta.get("solution_dir", f"solutions/{meta['year']}/{meta['day']}")

    retry = f"""
---

## Retry (attempt {args.attempt})

Your previous solution did not work. Fix files under `{solution_dir}/` and try again.

### What went wrong

{feedback}

### Instructions

1. Diagnose the bug in your implementation.
2. Update the solution file.
3. Run `AOC_PART={args.part} uv run python scripts/verify_solution.py` before finishing.
"""

    args.output.write_text(base + retry, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

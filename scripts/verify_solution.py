#!/usr/bin/env python3
"""Run the local solution against cached input (no network)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aoc_bot.solver.local import LocalSolver

ARTIFACT_DIR = Path(".aoc")


def main() -> None:
    meta = json.loads((ARTIFACT_DIR / "meta.json").read_text(encoding="utf-8"))
    day = int(meta["day"])
    puzzle_input = (ARTIFACT_DIR / "input.txt").read_text(encoding="utf-8")

    solver = LocalSolver()
    if not solver.has_solution(day):
        print(f"ERROR: no solution file for day {day}", file=sys.stderr)
        sys.exit(1)

    for part in (1, 2):
        try:
            result = solver.solve(
                day=day,
                part=part,
                puzzle_html="",
                puzzle_input=puzzle_input,
            )
            print(f"part{part}={result.answer}")
        except (NotImplementedError, AttributeError, FileNotFoundError) as exc:
            print(f"part{part}=SKIP ({exc})")


if __name__ == "__main__":
    main()

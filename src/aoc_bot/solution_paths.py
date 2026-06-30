from __future__ import annotations

from pathlib import Path

SOLUTIONS_ROOT = Path("solutions")


def solution_dir(year: int, day: int) -> Path:
    return SOLUTIONS_ROOT / str(year) / str(day)


def part_file(year: int, day: int, part: int) -> Path:
    return solution_dir(year, day) / f"part{part}.py"


def ensure_solution_dir(year: int, day: int) -> Path:
    directory = solution_dir(year, day)
    directory.mkdir(parents=True, exist_ok=True)
    return directory

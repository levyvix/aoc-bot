from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from aoc_bot.solution_paths import part_file
from aoc_bot.solver.base import SolveResult, Solver


class LocalSolver(Solver):
    """Load solutions from solutions/{year}/{day}/part{N}.py."""

    def __init__(self, solutions_dir: Path | None = None) -> None:
        self.solutions_dir = solutions_dir or Path("solutions")

    def part_path(self, year: int, day: int, part: int) -> Path:
        return self.solutions_dir / str(year) / str(day) / f"part{part}.py"

    def has_solution(self, year: int, day: int, part: int | None = None) -> bool:
        if part is not None:
            return self.part_path(year, day, part).exists()
        return self.part_path(year, day, 1).exists() or self.part_path(year, day, 2).exists()

    def solve(
        self,
        *,
        year: int,
        day: int,
        part: int,
        puzzle_html: str,
        puzzle_input: str,
    ) -> SolveResult:
        path = self.part_path(year, day, part)
        if not path.exists():
            raise FileNotFoundError(f"No solution file: {path}")

        module_name = f"aoc_{year}_day_{day}_part_{part}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load {path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        fn = None
        for name in ("solve", f"part{part}"):
            if hasattr(module, name):
                fn = getattr(module, name)
                break
        if fn is None:
            raise AttributeError(f"{path} must define solve(data: str) -> str")

        answer = fn(puzzle_input)
        return SolveResult(answer=str(answer).strip(), source="local")

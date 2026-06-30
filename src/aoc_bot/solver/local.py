from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from aoc_bot.solver.base import SolveResult, Solver


class LocalSolver(Solver):
    """Run a committed solution module from solutions/dayXX.py."""

    def __init__(self, solutions_dir: Path | None = None) -> None:
        self.solutions_dir = solutions_dir or Path("solutions")

    def _module_path(self, day: int) -> Path | None:
        for pattern in (f"day{day:02d}.py", f"day{day}.py"):
            path = self.solutions_dir / pattern
            if path.exists():
                return path
        return None

    def has_solution(self, day: int) -> bool:
        return self._module_path(day) is not None

    def solve(self, *, day: int, part: int, puzzle_html: str, puzzle_input: str) -> SolveResult:
        path = self._module_path(day)
        if path is None:
            raise FileNotFoundError(f"No local solution for day {day} in {self.solutions_dir}")

        module_name = f"aoc_day_{day}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load {path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        fn_name = f"part{part}"
        if not hasattr(module, fn_name):
            raise AttributeError(f"{path} is missing function {fn_name}(data: str) -> str")

        fn = getattr(module, fn_name)
        answer = fn(puzzle_input)
        return SolveResult(answer=str(answer).strip(), source="local")

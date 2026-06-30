from __future__ import annotations

import importlib.util
from pathlib import Path

_part1_path = Path(__file__).with_name("part1.py")
_spec = importlib.util.spec_from_file_location("aoc_2021_24_part1", _part1_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Could not load {_part1_path}")
_part1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_part1)


def solve(data: str) -> str:
    return _part1._solve_monad(data, find_max=False)

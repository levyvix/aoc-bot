from __future__ import annotations

import importlib.util
from pathlib import Path

_part1_path = Path(__file__).with_name("part1.py")
_spec = importlib.util.spec_from_file_location("aoc_2021_20_part1", _part1_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Could not load {_part1_path}")
_part1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_part1)

_parse = _part1._parse
_enhance = _part1._enhance


def solve(data: str) -> str:
    algo, grid = _parse(data)
    fill = "."
    for _ in range(50):
        grid, fill = _enhance(algo, grid, fill)
    return str(sum(row.count("#") for row in grid))

from __future__ import annotations

import importlib.util
from pathlib import Path

_part1_path = Path(__file__).with_name("part1.py")
_spec = importlib.util.spec_from_file_location("aoc_2021_19_part1", _part1_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Could not load {_part1_path}")
_part1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_part1)

_assemble = _part1._assemble
_parse = _part1._parse


def _manhattan(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def solve(data: str) -> str:
    scanners = _parse(data)
    _, scanner_positions = _assemble(scanners)
    positions = list(scanner_positions.values())
    best = 0
    for i, a in enumerate(positions):
        for b in positions[i + 1 :]:
            best = max(best, _manhattan(a, b))
    return str(best)

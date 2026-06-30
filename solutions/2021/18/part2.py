from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "day18_part1", Path(__file__).with_name("part1.py")
)
assert _spec is not None and _spec.loader is not None
_part1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_part1)


def solve(data: str) -> str:
    numbers = [ast.literal_eval(line) for line in data.strip().splitlines() if line.strip()]
    best = 0
    for i, left in enumerate(numbers):
        for j, right in enumerate(numbers):
            if i == j:
                continue
            total = _part1._add(left, right)
            best = max(best, _part1._magnitude(total))
    return str(best)

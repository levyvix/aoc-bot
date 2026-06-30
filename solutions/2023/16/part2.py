import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("part1", Path(__file__).with_name("part1.py"))
_part1 = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_part1)
energized_count = _part1.energized_count


def solve(data: str) -> str:
    grid = data.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    best = 0
    for c in range(cols):
        best = max(best, energized_count(grid, 0, c, 1))
        best = max(best, energized_count(grid, rows - 1, c, 3))
    for r in range(rows):
        best = max(best, energized_count(grid, r, 0, 0))
        best = max(best, energized_count(grid, r, cols - 1, 2))

    return str(best)

import importlib.util
from collections import deque
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "aoc_2019_19_part1",
    Path(__file__).with_name("part1.py"),
)
_part1 = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_part1)

parse_program = _part1.parse_program


class Beam:
    def __init__(self, program: list[int]) -> None:
        self.program = program
        self.cache: dict[tuple[int, int], bool] = {}

    def __call__(self, x: int, y: int) -> bool:
        key = (x, y)
        if key not in self.cache:
            self.cache[key] = _part1.in_beam(self.program, x, y)
        return self.cache[key]

    def row_bounds(self, y: int, x_start: int = 0) -> tuple[int, int]:
        x = x_start
        while not self(x, y):
            x += 1
        left = x
        while self(x, y):
            x += 1
        return left, x - 1


def find_square(program: list[int], size: int = 100) -> tuple[int, int]:
    beam = Beam(program)
    x_start = 0
    max_left: deque[int] = deque()
    min_right: deque[int] = deque()

    for y in range(size - 1, 10_000):
        left, right = beam.row_bounds(y, x_start)
        x_start = left
        max_left.append(left)
        min_right.append(right)
        if len(max_left) > size:
            max_left.popleft()
            min_right.popleft()
        if len(max_left) < size:
            continue

        top = y - size + 1
        widest_left = max(max_left)
        narrowest_right = min(min_right)
        if widest_left + size - 1 <= narrowest_right:
            return widest_left, top

    raise RuntimeError("square not found")


def solve(data: str) -> str:
    program = parse_program(data)
    x, y = find_square(program)
    return str(x * 10_000 + y)

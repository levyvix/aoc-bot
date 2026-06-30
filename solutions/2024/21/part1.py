from functools import cache

NUM_KEYS = [
    ("7", (0, 0)),
    ("8", (1, 0)),
    ("9", (2, 0)),
    ("4", (0, 1)),
    ("5", (1, 1)),
    ("6", (2, 1)),
    ("1", (0, 2)),
    ("2", (1, 2)),
    ("3", (2, 2)),
    ("0", (1, 3)),
    ("A", (2, 3)),
]
NUM_GAP = (0, 3)

DIR_KEYS = [
    ("^", (1, 0)),
    ("A", (2, 0)),
    ("<", (0, 1)),
    ("v", (1, 1)),
    (">", (2, 1)),
]
DIR_GAP = (0, 0)


def _move_sequence(a: int, b: int, positive: str, negative: str) -> str:
    ch = positive if a < b else negative
    return ch * abs(b - a)


def _pad_routes(keys: list[tuple[str, tuple[int, int]]], gap: tuple[int, int]) -> dict[tuple[str, str], tuple[str, ...]]:
    combinations: dict[tuple[str, str], list[str]] = {}
    for first, (x1, y1) in keys:
        for second, (x2, y2) in keys:
            h = _move_sequence(x1, x2, ">", "<")
            v = _move_sequence(y1, y2, "v", "^")
            if (x1, y2) != gap:
                path = v + h + "A"
                combinations.setdefault((first, second), []).append(path)
            if x1 != x2 and y1 != y2 and (x2, y1) != gap:
                path = h + v + "A"
                combinations.setdefault((first, second), []).append(path)
    return {key: tuple(value) for key, value in combinations.items()}


ROUTES: dict[tuple[str, str], tuple[str, ...]] = {}
ROUTES.update(_pad_routes(NUM_KEYS, NUM_GAP))
ROUTES.update(_pad_routes(DIR_KEYS, DIR_GAP))


@cache
def _presses(code: str, depth: int) -> int:
    if depth == 0:
        return len(code)
    total = 0
    prev = "A"
    for ch in code:
        total += min(_presses(path, depth - 1) for path in ROUTES[(prev, ch)])
        prev = ch
    return total


def _code_value(code: str) -> int:
    return int(code[:-1])


def solve(data: str) -> str:
    total = 0
    for code in data.strip().splitlines():
        total += _presses(code, 3) * _code_value(code)
    return str(total)

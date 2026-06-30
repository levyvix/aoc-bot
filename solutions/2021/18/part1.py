from __future__ import annotations

import ast
from copy import deepcopy


def _magnitude(node: int | list) -> int:
    if isinstance(node, int):
        return node
    return 3 * _magnitude(node[0]) + 2 * _magnitude(node[1])


def _add_left(node: list, value: int) -> None:
    if isinstance(node[1], int):
        node[1] += value
    else:
        _add_left(node[1], value)


def _add_right(node: list, value: int) -> None:
    if isinstance(node[0], int):
        node[0] += value
    else:
        _add_right(node[0], value)


def _explode(node: list, depth: int = 0) -> tuple[int, int, bool] | None:
    if isinstance(node[0], list):
        result = _explode(node[0], depth + 1)
        if result is not None:
            left, right, self_exploded = result
            if isinstance(node[1], int):
                node[1] += right
            else:
                _add_right(node[1], right)
            if self_exploded:
                node[0] = 0
            return left, 0, False

    if isinstance(node[1], list):
        result = _explode(node[1], depth + 1)
        if result is not None:
            left, right, self_exploded = result
            if isinstance(node[0], int):
                node[0] += left
            else:
                _add_left(node[0], left)
            if self_exploded:
                node[1] = 0
            return 0, right, False

    if depth == 4 and isinstance(node[0], int) and isinstance(node[1], int):
        return node[0], node[1], True

    return None


def _split(node: list) -> bool:
    if isinstance(node[0], int):
        if node[0] >= 10:
            node[0] = [node[0] // 2, (node[0] + 1) // 2]
            return True
    elif _split(node[0]):
        return True

    if isinstance(node[1], int):
        if node[1] >= 10:
            node[1] = [node[1] // 2, (node[1] + 1) // 2]
            return True
    elif _split(node[1]):
        return True

    return False


def _reduce(node: list) -> None:
    while True:
        if _explode(node) is not None:
            continue
        if _split(node):
            continue
        return


def _add(a: list, b: list) -> list:
    result = [deepcopy(a), deepcopy(b)]
    _reduce(result)
    return result


def solve(data: str) -> str:
    numbers = [ast.literal_eval(line) for line in data.strip().splitlines() if line.strip()]
    total = numbers[0]
    for number in numbers[1:]:
        total = _add(total, number)
    return str(_magnitude(total))

import re
import sys
from enum import Enum

sys.setrecursionlimit(500_000)


class Kind(Enum):
    SAND = 0
    MOVING = 1
    STOPPED = 2


def parse(data: str) -> tuple[list[Kind], int, int, int, int]:
    clay: list[tuple[int, int, int, int]] = []
    min_x = min_y = 10**9
    max_x = max_y = 0
    for line in data.strip().splitlines():
        if m := re.match(r"([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)", line):
            fixed_axis, fixed, _, start, end = m.groups()
            fixed = int(fixed)
            start, end = int(start), int(end)
            if fixed_axis == "x":
                clay.append((fixed, fixed, start, end))
            else:
                clay.append((start, end, fixed, fixed))
            min_x = min(min_x, start if fixed_axis == "y" else fixed)
            max_x = max(max_x, end if fixed_axis == "y" else fixed)
            min_y = min(min_y, fixed if fixed_axis == "y" else start)
            max_y = max(max_y, fixed if fixed_axis == "y" else end)

    width = max_x - min_x + 3
    top = width * min_y
    bottom = width * (max_y + 1)
    kind = [Kind.SAND] * bottom

    for x1, x2, y1, y2 in clay:
        if x1 == x2:
            for y in range(y1, y2 + 1):
                kind[width * y + x1 - min_x + 1] = Kind.STOPPED
        else:
            for x in range(x1, x2 + 1):
                kind[width * y1 + x - min_x + 1] = Kind.STOPPED

    return kind, width, top, bottom, 500 - min_x + 1


def solve(data: str) -> str:
    kind, width, top, bottom, spring = parse(data)
    moving = 0
    stopped = 0

    def flow(index: int) -> Kind:
        nonlocal moving, stopped
        if index >= bottom:
            return Kind.MOVING
        if kind[index] != Kind.SAND:
            return kind[index]
        if flow(index + width) == Kind.MOVING:
            kind[index] = Kind.MOVING
            if index >= top:
                moving += 1
            return Kind.MOVING

        left = next(i for i in range(index - 1, -1, -1) if not spread(i))
        right = next(i for i in range(index + 1, bottom) if not spread(i))

        if kind[left] == Kind.STOPPED and kind[right] == Kind.STOPPED:
            for i in range(left + 1, right):
                kind[i] = Kind.STOPPED
            stopped += right - left - 1
            return Kind.STOPPED

        flow(left)
        flow(right)
        for i in range(left + 1, right):
            kind[i] = Kind.MOVING
        if index >= top:
            moving += right - left - 1
        return Kind.MOVING

    def spread(index: int) -> bool:
        return kind[index] == Kind.SAND and (
            kind[index + width] == Kind.STOPPED
            or flow(index + width) == Kind.STOPPED
        )

    flow(spring)
    return str(moving + stopped)

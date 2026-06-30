from __future__ import annotations

import re

LIMIT = 50


def parse_line(line: str) -> tuple[bool, tuple[int, int], tuple[int, int], tuple[int, int]]:
    action = line.startswith("on")
    parts = re.findall(r"(-?\d+)\.\.(-?\d+)", line)
    return action, (int(parts[0][0]), int(parts[0][1])), (int(parts[1][0]), int(parts[1][1])), (
        int(parts[2][0]),
        int(parts[2][1]),
    )


def solve(data: str) -> str:
    cubes: set[tuple[int, int, int]] = set()

    for line in data.strip().splitlines():
        action, (x1, x2), (y1, y2), (z1, z2) = parse_line(line)
        for x in range(max(x1, -LIMIT), min(x2, LIMIT) + 1):
            for y in range(max(y1, -LIMIT), min(y2, LIMIT) + 1):
                for z in range(max(z1, -LIMIT), min(z2, LIMIT) + 1):
                    if action:
                        cubes.add((x, y, z))
                    else:
                        cubes.discard((x, y, z))

    return str(len(cubes))

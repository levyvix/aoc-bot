from __future__ import annotations

import re

Cuboid = tuple[int, int, int, int, int, int]


def parse_line(line: str) -> tuple[bool, Cuboid]:
    action = line.startswith("on")
    parts = re.findall(r"(-?\d+)\.\.(-?\d+)", line)
    return action, (
        int(parts[0][0]),
        int(parts[0][1]),
        int(parts[1][0]),
        int(parts[1][1]),
        int(parts[2][0]),
        int(parts[2][1]),
    )


def volume(c: Cuboid) -> int:
    x1, x2, y1, y2, z1, z2 = c
    return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)


def intersects(a: Cuboid, b: Cuboid) -> bool:
    ax1, ax2, ay1, ay2, az1, az2 = a
    bx1, bx2, by1, by2, bz1, bz2 = b
    return ax1 <= bx2 and bx1 <= ax2 and ay1 <= by2 and by1 <= ay2 and az1 <= bz2 and bz1 <= az2


def subtract(a: Cuboid, b: Cuboid) -> list[Cuboid]:
    if not intersects(a, b):
        return [a]

    ax1, ax2, ay1, ay2, az1, az2 = a
    bx1, bx2, by1, by2, bz1, bz2 = b
    ix1, ix2 = max(ax1, bx1), min(ax2, bx2)
    iy1, iy2 = max(ay1, by1), min(ay2, by2)
    iz1, iz2 = max(az1, bz1), min(az2, bz2)

    result: list[Cuboid] = []
    if ax1 <= bx1 - 1:
        result.append((ax1, bx1 - 1, ay1, ay2, az1, az2))
    if bx2 + 1 <= ax2:
        result.append((bx2 + 1, ax2, ay1, ay2, az1, az2))
    if ay1 <= by1 - 1:
        result.append((ix1, ix2, ay1, by1 - 1, az1, az2))
    if by2 + 1 <= ay2:
        result.append((ix1, ix2, by2 + 1, ay2, az1, az2))
    if az1 <= bz1 - 1:
        result.append((ix1, ix2, iy1, iy2, az1, bz1 - 1))
    if bz2 + 1 <= az2:
        result.append((ix1, ix2, iy1, iy2, bz2 + 1, az2))

    return [c for c in result if volume(c) > 0]


def solve(data: str) -> str:
    on_cuboids: list[Cuboid] = []

    for line in data.strip().splitlines():
        action, box = parse_line(line)
        if action:
            pieces = [box]
            for existing in on_cuboids:
                pieces = [p for piece in pieces for p in subtract(piece, existing)]
            on_cuboids.extend(pieces)
        else:
            on_cuboids = [p for existing in on_cuboids for p in subtract(existing, box)]

    return str(sum(volume(c) for c in on_cuboids))

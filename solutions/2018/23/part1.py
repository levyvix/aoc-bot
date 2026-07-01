import re


def parse(data: str) -> list[tuple[tuple[int, int, int], int]]:
    bots = []
    for line in data.strip().splitlines():
        m = re.match(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line)
        if m:
            x, y, z, r = map(int, m.groups())
            bots.append(((x, y, z), r))
    return bots


def manhattan(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def solve(data: str) -> str:
    bots = parse(data)
    strongest = max(bots, key=lambda b: b[1])
    pos, radius = strongest
    count = sum(1 for p, _ in bots if manhattan(pos, p) <= radius)
    return str(count)

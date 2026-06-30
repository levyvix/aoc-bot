from collections import defaultdict


def _parse_bricks(data: str) -> list[list[tuple[int, int, int]]]:
    bricks: list[list[tuple[int, int, int]]] = []
    for line in data.strip().splitlines():
        a, b = line.split("~")
        x1, y1, z1 = map(int, a.split(","))
        x2, y2, z2 = map(int, b.split(","))
        cubes = [
            (x, y, z)
            for x in range(min(x1, x2), max(x1, x2) + 1)
            for y in range(min(y1, y2), max(y1, y2) + 1)
            for z in range(min(z1, z2), max(z1, z2) + 1)
        ]
        bricks.append(cubes)
    return bricks


def _settle(bricks: list[list[tuple[int, int, int]]]) -> tuple[
    list[list[tuple[int, int, int]]], dict[tuple[int, int, int], int]
]:
    indexed = list(enumerate(bricks))
    indexed.sort(key=lambda item: min(c[2] for c in item[1]))

    occupied: dict[tuple[int, int, int], int] = {}
    settled: list[list[tuple[int, int, int]]] = [[] for _ in bricks]

    for brick_id, cubes in indexed:
        while True:
            min_z = min(c[2] for c in cubes)
            if min_z == 1:
                break
            if any((x, y, z - 1) in occupied for x, y, z in cubes):
                break
            cubes = [(x, y, z - 1) for x, y, z in cubes]

        settled[brick_id] = cubes
        for pos in cubes:
            occupied[pos] = brick_id

    return settled, occupied


def _support_graph(
    bricks: list[list[tuple[int, int, int]]],
    occupied: dict[tuple[int, int, int], int],
) -> tuple[dict[int, set[int]], dict[int, set[int]]]:
    supports: dict[int, set[int]] = defaultdict(set)
    supported_by: dict[int, set[int]] = defaultdict(set)

    for brick_id, cubes in enumerate(bricks):
        min_z = min(c[2] for c in cubes)
        for x, y, z in cubes:
            if z != min_z:
                continue
            below = occupied.get((x, y, z - 1))
            if below is not None and below != brick_id:
                supports[below].add(brick_id)
                supported_by[brick_id].add(below)

    return supports, supported_by


def _falling_count(
    removed: int,
    supports: dict[int, set[int]],
    supported_by: dict[int, set[int]],
    n: int,
) -> int:
    sup_count = [len(supported_by[i]) for i in range(n)]
    falling = {removed}
    queue = [removed]

    while queue:
        brick = queue.pop()
        for child in supports[brick]:
            if child in falling:
                continue
            sup_count[child] -= 1
            if sup_count[child] == 0:
                falling.add(child)
                queue.append(child)

    return len(falling) - 1


def solve(data: str) -> str:
    bricks = _parse_bricks(data)
    settled, occupied = _settle(bricks)
    supports, supported_by = _support_graph(settled, occupied)

    n = len(bricks)
    total = sum(
        _falling_count(brick_id, supports, supported_by, n) for brick_id in range(n)
    )
    return str(total)

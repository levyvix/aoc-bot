import heapq
import re


def parse(data: str) -> list[tuple[tuple[int, int, int], int]]:
    bots = []
    for line in data.strip().splitlines():
        m = re.match(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line)
        if m:
            x, y, z, r = map(int, m.groups())
            bots.append(((x, y, z), r))
    return bots


def dist_point_to_box(
    px: int, py: int, pz: int, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int
) -> int:
    d = 0
    if px < x1:
        d += x1 - px
    elif px > x2:
        d += px - x2
    if py < y1:
        d += y1 - py
    elif py > y2:
        d += py - y2
    if pz < z1:
        d += z1 - pz
    elif pz > z2:
        d += pz - z2
    return d


def dist_box_to_origin(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> int:
    cx = min(max(0, x1), x2)
    cy = min(max(0, y1), y2)
    cz = min(max(0, z1), z2)
    return abs(cx) + abs(cy) + abs(cz)


def count_reachable(
    bots: list[tuple[tuple[int, int, int], int]],
    x1: int,
    y1: int,
    z1: int,
    x2: int,
    y2: int,
    z2: int,
) -> int:
    return sum(
        1
        for (bx, by, bz), r in bots
        if dist_point_to_box(bx, by, bz, x1, y1, z1, x2, y2, z2) <= r
    )


def solve(data: str) -> str:
    bots = parse(data)
    if not bots:
        return "0"

    min_x = min(x - r for (x, y, z), r in bots)
    max_x = max(x + r for (x, y, z), r in bots)
    min_y = min(y - r for (x, y, z), r in bots)
    max_y = max(y + r for (x, y, z), r in bots)
    min_z = min(z - r for (x, y, z), r in bots)
    max_z = max(z + r for (x, y, z), r in bots)

    span = max(max_x - min_x, max_y - min_y, max_z - min_z, 1)
    size = 1
    while size < span:
        size *= 2

    cx = (min_x + max_x) // 2
    cy = (min_y + max_y) // 2
    cz = (min_z + max_z) // 2
    half = size // 2
    x1, x2 = cx - half, cx + half - 1
    y1, y2 = cy - half, cy + half - 1
    z1, z2 = cz - half, cz + half - 1

    best_count = 0
    best_dist = float("inf")

    heap: list[tuple[int, int, int, int, int, int, int, int]] = []
    upper = count_reachable(bots, x1, y1, z1, x2, y2, z2)
    dist = dist_box_to_origin(x1, y1, z1, x2, y2, z2)
    heapq.heappush(heap, (-upper, dist, x1, y1, z1, x2, y2, z2))

    while heap:
        neg_upper, dist, x1, y1, z1, x2, y2, z2 = heapq.heappop(heap)
        upper = -neg_upper
        if upper < best_count:
            continue
        if upper == best_count and dist >= best_dist:
            continue

        if x1 == x2 and y1 == y2 and z1 == z2:
            count = count_reachable(bots, x1, y1, z1, x2, y2, z2)
            if count > best_count or (count == best_count and dist < best_dist):
                best_count = count
                best_dist = dist
            continue

        mx = (x1 + x2) // 2
        my = (y1 + y2) // 2
        mz = (z1 + z2) // 2
        for sx1, sx2 in ((x1, mx), (mx + 1, x2)):
            for sy1, sy2 in ((y1, my), (my + 1, y2)):
                for sz1, sz2 in ((z1, mz), (mz + 1, z2)):
                    sub_upper = count_reachable(bots, sx1, sy1, sz1, sx2, sy2, sz2)
                    if sub_upper < best_count:
                        continue
                    sub_dist = dist_box_to_origin(sx1, sy1, sz1, sx2, sy2, sz2)
                    if sub_upper == best_count and sub_dist >= best_dist:
                        continue
                    heapq.heappush(
                        heap, (-sub_upper, sub_dist, sx1, sy1, sz1, sx2, sy2, sz2)
                    )

    return str(int(best_dist))

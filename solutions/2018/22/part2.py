import heapq

MOD = 20183
TORCH = 0
CLIMBING = 1
NEITHER = 2

ALLOWED = {
    0: {TORCH, CLIMBING},
    1: {CLIMBING, NEITHER},
    2: {TORCH, NEITHER},
}

DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))


def _parse(data: str) -> tuple[int, int, int]:
    depth = 0
    target_x = 0
    target_y = 0
    for line in data.strip().splitlines():
        line = line.strip()
        if line.startswith("depth:"):
            depth = int(line.split(":")[1].strip())
        elif line.startswith("target:"):
            coords = line.split(":")[1].strip().split(",")
            target_x = int(coords[0])
            target_y = int(coords[1])
    return depth, target_x, target_y


def solve(data: str) -> str:
    depth, target_x, target_y = _parse(data)
    erosion: dict[tuple[int, int], int] = {}

    def get_erosion(x: int, y: int) -> int:
        if x < 0 or y < 0:
            raise ValueError("solid rock")
        key = (x, y)
        if key not in erosion:
            if key == (0, 0) or key == (target_x, target_y):
                gi = 0
            elif y == 0:
                gi = x * 16807
            elif x == 0:
                gi = y * 48271
            else:
                gi = get_erosion(x - 1, y) * get_erosion(x, y - 1)
            erosion[key] = (gi + depth) % MOD
        return erosion[key]

    def region_type(x: int, y: int) -> int:
        return get_erosion(x, y) % 3

    start = (0, 0, TORCH)
    goal = (target_x, target_y, TORCH)
    dist = {start: 0}
    heap: list[tuple[int, int, int, int]] = [(0, 0, 0, TORCH)]

    while heap:
        cost, x, y, tool = heapq.heappop(heap)
        if (x, y, tool) == goal:
            return str(cost)
        if dist.get((x, y, tool), float("inf")) < cost:
            continue

        region = region_type(x, y)
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0:
                continue
            nregion = region_type(nx, ny)
            if tool not in ALLOWED[nregion]:
                continue
            nstate = (nx, ny, tool)
            ncost = cost + 1
            if ncost < dist.get(nstate, float("inf")):
                dist[nstate] = ncost
                heapq.heappush(heap, (ncost, nx, ny, tool))

        for new_tool in ALLOWED[region]:
            if new_tool == tool:
                continue
            nstate = (x, y, new_tool)
            ncost = cost + 7
            if ncost < dist.get(nstate, float("inf")):
                dist[nstate] = ncost
                heapq.heappush(heap, (ncost, x, y, new_tool))

    raise RuntimeError("no path found")

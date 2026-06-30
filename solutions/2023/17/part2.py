import heapq

DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))  # right, down, left, up
MIN_STREAK = 4
MAX_STREAK = 10


def solve(data: str) -> str:
    grid = data.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    goal = (rows - 1, cols - 1)

    dist: dict[tuple[int, int, int, int], int] = {}
    heap: list[tuple[int, int, int, int, int]] = []

    for d, (dr, dc) in enumerate(DIRS):
        nr, nc = dr, dc
        if 0 <= nr < rows and 0 <= nc < cols:
            cost = int(grid[nr][nc])
            state = (nr, nc, d, 1)
            dist[state] = cost
            heapq.heappush(heap, (cost, nr, nc, d, 1))

    while heap:
        cost, r, c, d, count = heapq.heappop(heap)
        if (r, c) == goal and count >= MIN_STREAK:
            return str(cost)
        if cost > dist.get((r, c, d, count), float("inf")):
            continue

        dr, dc = DIRS[d]

        if count < MAX_STREAK:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + int(grid[nr][nc])
                state = (nr, nc, d, count + 1)
                if new_cost < dist.get(state, float("inf")):
                    dist[state] = new_cost
                    heapq.heappush(heap, (new_cost, nr, nc, d, count + 1))

        if count >= MIN_STREAK:
            for nd in ((d - 1) % 4, (d + 1) % 4):
                ndr, ndc = DIRS[nd]
                nr, nc = r + ndr, c + ndc
                if 0 <= nr < rows and 0 <= nc < cols:
                    new_cost = cost + int(grid[nr][nc])
                    state = (nr, nc, nd, 1)
                    if new_cost < dist.get(state, float("inf")):
                        dist[state] = new_cost
                        heapq.heappush(heap, (new_cost, nr, nc, nd, 1))

    best = min(
        (
            dist[k]
            for k in dist
            if k[0] == goal[0] and k[1] == goal[1] and k[3] >= MIN_STREAK
        ),
        default=0,
    )
    return str(best)

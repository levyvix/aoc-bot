import heapq

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N, E, S, W


def solve(data: str) -> str:
    grid = [list(row) for row in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])

    start = end = None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "S":
                start = (r, c)
            elif cell == "E":
                end = (r, c)

    sr, sc = start
    start_dir = 1  # East

    dist = {(sr, sc, start_dir): 0}
    heap = [(0, sr, sc, start_dir)]

    while heap:
        cost, r, c, d = heapq.heappop(heap)
        if (r, c) == end:
            return str(cost)
        if cost > dist.get((r, c, d), float("inf")):
            continue

        for nd in ((d - 1) % 4, (d + 1) % 4):
            turn_cost = cost + 1000
            key = (r, c, nd)
            if turn_cost < dist.get(key, float("inf")):
                dist[key] = turn_cost
                heapq.heappush(heap, (turn_cost, r, c, nd))

        dr, dc = DIRS[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
            move_cost = cost + 1
            key = (nr, nc, d)
            if move_cost < dist.get(key, float("inf")):
                dist[key] = move_cost
                heapq.heappush(heap, (move_cost, nr, nc, d))

    raise RuntimeError("no path to end")

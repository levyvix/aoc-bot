import heapq

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N, E, S, W


def _dijkstra_forward(grid, start_states):
    rows, cols = len(grid), len(grid[0])
    dist = {}
    heap = []
    for cost, r, c, d in start_states:
        key = (r, c, d)
        if cost < dist.get(key, float("inf")):
            dist[key] = cost
            heapq.heappush(heap, (cost, r, c, d))

    while heap:
        cost, r, c, d = heapq.heappop(heap)
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

    return dist


def _dijkstra_backward(grid, start_states):
    rows, cols = len(grid), len(grid[0])
    dist = {}
    heap = []
    for cost, r, c, d in start_states:
        key = (r, c, d)
        if cost < dist.get(key, float("inf")):
            dist[key] = cost
            heapq.heappush(heap, (cost, r, c, d))

    while heap:
        cost, r, c, d = heapq.heappop(heap)
        if cost > dist.get((r, c, d), float("inf")):
            continue

        for nd in ((d - 1) % 4, (d + 1) % 4):
            turn_cost = cost + 1000
            key = (r, c, nd)
            if turn_cost < dist.get(key, float("inf")):
                dist[key] = turn_cost
                heapq.heappush(heap, (turn_cost, r, c, nd))

        dr, dc = DIRS[d]
        pr, pc = r - dr, c - dc
        if 0 <= pr < rows and 0 <= pc < cols and grid[pr][pc] != "#":
            move_cost = cost + 1
            key = (pr, pc, d)
            if move_cost < dist.get(key, float("inf")):
                dist[key] = move_cost
                heapq.heappush(heap, (move_cost, pr, pc, d))

    return dist


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
    er, ec = end

    dist_from = _dijkstra_forward(grid, [(0, sr, sc, 1)])
    dist_to = _dijkstra_backward(grid, [(0, er, ec, d) for d in range(4)])

    min_cost = min(dist_from[(er, ec, d)] for d in range(4))

    tiles = set()
    for (r, c, d), cost_from in dist_from.items():
        cost_to = dist_to.get((r, c, d), float("inf"))
        if cost_from + cost_to == min_cost:
            tiles.add((r, c))

        for nd in ((d - 1) % 4, (d + 1) % 4):
            cost_to = dist_to.get((r, c, nd), float("inf"))
            if cost_from + 1000 + cost_to == min_cost:
                tiles.add((r, c))

        dr, dc = DIRS[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
            cost_to = dist_to.get((nr, nc, d), float("inf"))
            if cost_from + 1 + cost_to == min_cost:
                tiles.add((r, c))
                tiles.add((nr, nc))

    return str(len(tiles))

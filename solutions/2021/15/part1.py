import heapq


def solve(data: str) -> str:
    grid = [list(map(int, line.strip())) for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])
    dist = [[float("inf")] * cols for _ in range(rows)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        cost, r, c = heapq.heappop(heap)
        if cost > dist[r][c]:
            continue
        if r == rows - 1 and c == cols - 1:
            return str(cost)
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + grid[nr][nc]
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    heapq.heappush(heap, (new_cost, nr, nc))
    return str(dist[rows - 1][cols - 1])

import heapq


def solve(data: str) -> str:
    grid = [list(map(int, line.strip())) for line in data.strip().splitlines()]
    tile_h, tile_w = len(grid), len(grid[0])
    rows, cols = tile_h * 5, tile_w * 5

    def risk(r: int, c: int) -> int:
        val = grid[r % tile_h][c % tile_w] + r // tile_h + c // tile_w
        return ((val - 1) % 9) + 1

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
                new_cost = cost + risk(nr, nc)
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    heapq.heappush(heap, (new_cost, nr, nc))
    return str(dist[rows - 1][cols - 1])

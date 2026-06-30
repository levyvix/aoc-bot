def solve(data: str) -> str:
    grid = [list(line.strip()) for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])
    heights = [[int(ch) for ch in row] for row in grid]

    def flow_to(r: int, c: int) -> tuple[int, int]:
        memo: dict[tuple[int, int], tuple[int, int]] = {}

        def sink(r: int, c: int) -> tuple[int, int]:
            if (r, c) in memo:
                return memo[(r, c)]
            h = heights[r][c]
            best = None
            best_h = h
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    nh = heights[nr][nc]
                    if nh < best_h:
                        best_h = nh
                        best = (nr, nc)
            if best is None:
                memo[(r, c)] = (r, c)
            else:
                memo[(r, c)] = sink(*best)
            return memo[(r, c)]

        return sink(r, c)

    basin_sizes: dict[tuple[int, int], int] = {}
    for r in range(rows):
        for c in range(cols):
            if heights[r][c] == 9:
                continue
            low = flow_to(r, c)
            basin_sizes[low] = basin_sizes.get(low, 0) + 1

    top_three = sorted(basin_sizes.values(), reverse=True)[:3]
    product = 1
    for size in top_three:
        product *= size
    return str(product)

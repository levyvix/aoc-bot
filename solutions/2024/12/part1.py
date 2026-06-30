def solve(data: str) -> str:
    grid = [line.rstrip("\n") for line in data.strip().split("\n")]
    rows, cols = len(grid), len(grid[0])
    visited: set[tuple[int, int]] = set()
    total = 0

    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue
            plant = grid[r][c]
            stack = [(r, c)]
            region: list[tuple[int, int]] = []
            while stack:
                cr, cc = stack.pop()
                if (cr, cc) in visited:
                    continue
                if grid[cr][cc] != plant:
                    continue
                visited.add((cr, cc))
                region.append((cr, cc))
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                        if grid[nr][nc] == plant:
                            stack.append((nr, nc))

            area = len(region)
            perimeter = 0
            for cr, cc in region:
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = cr + dr, cc + dc
                    if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != plant:
                        perimeter += 1
            total += area * perimeter

    return str(total)

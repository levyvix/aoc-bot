def count_sides(region: set[tuple[int, int]]) -> int:
    sides = 0
    for r, c in region:
        if (r - 1, c) not in region:
            if (r, c - 1) not in region or (r - 1, c - 1) in region:
                sides += 1
        if (r + 1, c) not in region:
            if (r, c - 1) not in region or (r + 1, c - 1) in region:
                sides += 1
        if (r, c - 1) not in region:
            if (r - 1, c) not in region or (r - 1, c - 1) in region:
                sides += 1
        if (r, c + 1) not in region:
            if (r - 1, c) not in region or (r - 1, c + 1) in region:
                sides += 1
    return sides


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
            sides = count_sides(set(region))
            total += area * sides

    return str(total)

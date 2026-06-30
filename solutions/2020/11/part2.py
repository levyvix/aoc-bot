def solve(data: str) -> str:
    grid = [list(line) for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def count_visible(r: int, c: int) -> int:
        count = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == "#":
                    count += 1
                    break
                if grid[nr][nc] == "L":
                    break
                nr += dr
                nc += dc
        return count

    changed = True
    while changed:
        changed = False
        new_grid = [row[:] for row in grid]
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "L" and count_visible(r, c) == 0:
                    new_grid[r][c] = "#"
                    changed = True
                elif grid[r][c] == "#" and count_visible(r, c) >= 5:
                    new_grid[r][c] = "L"
                    changed = True
        grid = new_grid

    return str(sum(row.count("#") for row in grid))

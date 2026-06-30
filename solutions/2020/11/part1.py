def solve(data: str) -> str:
    grid = [list(line) for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])

    def count_adjacent(r: int, c: int) -> int:
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "#":
                    count += 1
        return count

    changed = True
    while changed:
        changed = False
        new_grid = [row[:] for row in grid]
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "L" and count_adjacent(r, c) == 0:
                    new_grid[r][c] = "#"
                    changed = True
                elif grid[r][c] == "#" and count_adjacent(r, c) >= 4:
                    new_grid[r][c] = "L"
                    changed = True
        grid = new_grid

    return str(sum(row.count("#") for row in grid))

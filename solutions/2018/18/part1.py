def solve(data: str) -> str:
    grid = [list(line.strip()) for line in data.strip().splitlines() if line.strip()]
    rows, cols = len(grid), len(grid[0])

    def count_adj(r: int, c: int, ch: str) -> int:
        n = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == ch:
                    n += 1
        return n

    def step() -> None:
        nonlocal grid
        new = [row[:] for row in grid]
        for r in range(rows):
            for c in range(cols):
                cell = grid[r][c]
                if cell == ".":
                    if count_adj(r, c, "|") >= 3:
                        new[r][c] = "|"
                elif cell == "|":
                    if count_adj(r, c, "#") >= 3:
                        new[r][c] = "#"
                elif cell == "#":
                    if count_adj(r, c, "#") >= 1 and count_adj(r, c, "|") >= 1:
                        new[r][c] = "#"
                    else:
                        new[r][c] = "."
        grid = new

    def resource_value() -> int:
        trees = sum(row.count("|") for row in grid)
        lumber = sum(row.count("#") for row in grid)
        return trees * lumber

    for _ in range(10):
        step()

    return str(resource_value())

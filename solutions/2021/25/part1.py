def solve(data: str) -> str:
    grid = [list(row) for row in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])

    step = 0
    while True:
        step += 1
        moved = False

        moves: list[tuple[int, int, int, int]] = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == ">":
                    nc = (c + 1) % cols
                    if grid[r][nc] == ".":
                        moves.append((r, c, r, nc))
        for r, c, nr, nc in moves:
            grid[r][c] = "."
            grid[nr][nc] = ">"
            moved = True

        moves = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "v":
                    nr = (r + 1) % rows
                    if grid[nr][c] == ".":
                        moves.append((r, c, nr, c))
        for r, c, nr, nc in moves:
            grid[r][c] = "."
            grid[nr][nc] = "v"
            moved = True

        if not moved:
            return str(step)


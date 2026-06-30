def solve(data: str) -> str:
    grid = [list(line) for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])

    for c in range(cols):
        write = 0
        for r in range(rows):
            cell = grid[r][c]
            if cell == "#":
                write = r + 1
            elif cell == "O":
                grid[r][c] = "."
                grid[write][c] = "O"
                write += 1

    total = sum(rows - r for r in range(rows) for c in range(cols) if grid[r][c] == "O")
    return str(total)

def solve(data: str) -> str:
    grid = [line.strip() for line in data.strip().splitlines() if line.strip()]
    rows, cols = len(grid), len(grid[0])

    def is_mas(a: str, b: str, c: str) -> bool:
        return (a + b + c) in ("MAS", "SAM")

    count = 0
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] != "A":
                continue
            tl, tr = grid[r - 1][c - 1], grid[r - 1][c + 1]
            bl, br = grid[r + 1][c - 1], grid[r + 1][c + 1]
            if is_mas(tl, grid[r][c], br) and is_mas(tr, grid[r][c], bl):
                count += 1

    return str(count)

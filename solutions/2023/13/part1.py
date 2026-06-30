def solve(data: str) -> str:
    total = 0
    for pattern in data.strip().split("\n\n"):
        grid = [list(row) for row in pattern.splitlines()]
        h, w = len(grid), len(grid[0])

        for left in range(1, w):
            if all(
                grid[r][c] == grid[r][2 * left - 1 - c]
                for r in range(h)
                for c in range(left)
                if 2 * left - 1 - c < w
            ):
                total += left
                break
        else:
            for top in range(1, h):
                if all(
                    grid[r][c] == grid[2 * top - 1 - r][c]
                    for r in range(top)
                    for c in range(w)
                    if 2 * top - 1 - r < h
                ):
                    total += 100 * top
                    break

    return str(total)

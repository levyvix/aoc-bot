def solve(data: str) -> str:
    grid = data.strip().splitlines()
    rows = len(grid)
    cols = len(grid[0])

    galaxies = [
        (r, c)
        for r, row in enumerate(grid)
        for c, ch in enumerate(row)
        if ch == "#"
    ]

    empty_rows = {r for r in range(rows) if all(grid[r][c] != "#" for c in range(cols))}
    empty_cols = {c for c in range(cols) if all(grid[r][c] != "#" for r in range(rows))}

    def expanded(r: int, c: int) -> tuple[int, int]:
        er = r + sum(1 for row in empty_rows if row < r)
        ec = c + sum(1 for col in empty_cols if col < c)
        return er, ec

    total = 0
    for i, (r1, c1) in enumerate(galaxies):
        er1, ec1 = expanded(r1, c1)
        for r2, c2 in galaxies[i + 1 :]:
            er2, ec2 = expanded(r2, c2)
            total += abs(er1 - er2) + abs(ec1 - ec2)

    return str(total)

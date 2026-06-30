DIRS = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def solve(data: str) -> str:
    map_text, moves_text = data.strip().split("\n\n")
    grid = [list(row) for row in map_text.splitlines()]
    moves = moves_text.replace("\n", "")

    robot = next(
        (r, c)
        for r, row in enumerate(grid)
        for c, cell in enumerate(row)
        if cell == "@"
    )

    for move in moves:
        dr, dc = DIRS[move]
        r, c = robot
        nr, nc = r + dr, c + dc

        if grid[nr][nc] == "#":
            continue
        if grid[nr][nc] == ".":
            grid[r][c] = "."
            grid[nr][nc] = "@"
            robot = (nr, nc)
            continue

        br, bc = nr, nc
        while grid[br][bc] == "O":
            br, bc = br + dr, bc + dc
        if grid[br][bc] == "#":
            continue

        cr, cc = br, bc
        while (cr, cc) != (r, c):
            pr, pc = cr - dr, cc - dc
            grid[cr][cc] = grid[pr][pc]
            cr, cc = pr, pc
        grid[r][c] = "."
        grid[nr][nc] = "@"
        robot = (nr, nc)

    total = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "O":
                total += 100 * r + c

    return str(total)

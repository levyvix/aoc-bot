def solve(data: str) -> str:
    grid = [line.rstrip("\n") for line in data.splitlines() if line.strip()]
    rows, cols = len(grid), len(grid[0])

    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    guard_dir = {"^": 0, ">": 1, "v": 2, "<": 3}

    r = c = d = None
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] in guard_dir:
                r, c, d = i, j, guard_dir[grid[i][j]]
                break
        if r is not None:
            break

    visited = {(r, c)}
    while True:
        dr, dc = dirs[d]
        nr, nc = r + dr, c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            break
        if grid[nr][nc] == "#":
            d = (d + 1) % 4
        else:
            r, c = nr, nc
            visited.add((r, c))

    return str(len(visited))

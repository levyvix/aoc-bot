def solve(data: str) -> str:
    grid = [list(line.rstrip("\n")) for line in data.splitlines() if line.strip()]
    rows, cols = len(grid), len(grid[0])

    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    guard_dir = {"^": 0, ">": 1, "v": 2, "<": 3}

    start_r = start_c = start_d = None
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] in guard_dir:
                start_r, start_c, start_d = i, j, guard_dir[grid[i][j]]
                break
        if start_r is not None:
            break

    def patrol_path() -> set[tuple[int, int]]:
        r, c, d = start_r, start_c, start_d
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
        return visited

    def causes_loop(obstacle: tuple[int, int]) -> bool:
        orow, ocol = obstacle
        grid[orow][ocol] = "#"
        r, c, d = start_r, start_c, start_d
        seen: set[tuple[int, int, int]] = set()
        loop = False
        while True:
            state = (r, c, d)
            if state in seen:
                loop = True
                break
            seen.add(state)
            dr, dc = dirs[d]
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                break
            if grid[nr][nc] == "#":
                d = (d + 1) % 4
            else:
                r, c = nr, nc
        grid[orow][ocol] = "."
        return loop

    path = patrol_path()
    count = 0
    for r, c in path:
        if (r, c) == (start_r, start_c) or grid[r][c] == "#":
            continue
        if causes_loop((r, c)):
            count += 1

    return str(count)

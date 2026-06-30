from collections import deque

DIRS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}
OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}

PIPES = {
    "|": {"N", "S"},
    "-": {"E", "W"},
    "L": {"N", "E"},
    "J": {"N", "W"},
    "7": {"S", "W"},
    "F": {"S", "E"},
}


def connections(grid: list[str], r: int, c: int) -> set[str]:
    ch = grid[r][c]
    if ch == "S":
        conns: set[str] = set()
        for d, (dr, dc) in DIRS.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                if OPP[d] in connections(grid, nr, nc):
                    conns.add(d)
        return conns
    return PIPES.get(ch, set())


def pipe_char(conns: set[str]) -> str:
    for ch, dirs in PIPES.items():
        if dirs == conns:
            return ch
    raise ValueError(f"invalid pipe connections: {conns}")


def loop_tiles(grid: list[str]) -> set[tuple[int, int]]:
    start = next(
        (r, c)
        for r, row in enumerate(grid)
        for c, ch in enumerate(row)
        if ch == "S"
    )
    visited = {start}
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        for direction in connections(grid, r, c):
            dr, dc = DIRS[direction]
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return visited


def solve(data: str) -> str:
    grid = [list(row) for row in data.strip().splitlines()]
    loop = loop_tiles(["".join(row) for row in grid])

    for r, c in loop:
        if grid[r][c] == "S":
            grid[r][c] = pipe_char(connections(["".join(row) for row in grid], r, c))

    enclosed = 0
    for r, row in enumerate(grid):
        north_crossings = 0
        for c, ch in enumerate(row):
            if (r, c) in loop:
                if "N" in PIPES[ch]:
                    north_crossings += 1
                continue
            if north_crossings % 2 == 1:
                enclosed += 1

    return str(enclosed)

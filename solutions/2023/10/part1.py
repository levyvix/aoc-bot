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


def solve(data: str) -> str:
    grid = data.strip().splitlines()
    start = next(
        (r, c)
        for r, row in enumerate(grid)
        for c, ch in enumerate(row)
        if ch == "S"
    )

    dist: dict[tuple[int, int], int] = {start: 0}
    queue = deque([start])

    while queue:
        r, c = queue.popleft()
        d = dist[(r, c)]
        for direction in connections(grid, r, c):
            dr, dc = DIRS[direction]
            nr, nc = r + dr, c + dc
            if (nr, nc) not in dist:
                dist[(nr, nc)] = d + 1
                queue.append((nr, nc))

    return str(max(dist.values()))

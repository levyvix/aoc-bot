from collections import deque


def solve(data: str) -> str:
    grid = [list(line) for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])

    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)

    def bfs(src: tuple[int, int]) -> dict[tuple[int, int], int]:
        dist = {src: 0}
        q = deque([src])
        while q:
            r, c = q.popleft()
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                    if (nr, nc) not in dist:
                        dist[(nr, nc)] = dist[(r, c)] + 1
                        q.append((nr, nc))
        return dist

    dist_s = bfs(start)
    dist_e = bfs(end)
    total = dist_s[end]

    track = [
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if grid[r][c] != "#"
    ]

    count = 0
    for r1, c1 in track:
        for r2, c2 in track:
            md = abs(r1 - r2) + abs(c1 - c2)
            if md not in (1, 2):
                continue
            saved = total - dist_s[(r1, c1)] - md - dist_e[(r2, c2)]
            if saved >= 100:
                count += 1

    return str(count)

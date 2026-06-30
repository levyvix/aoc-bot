from collections import deque


def solve(data: str) -> str:
    grid = [list(line) for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])
    max_cheat = 20
    min_save = 100

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
    track = {
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if grid[r][c] != "#"
    }

    count = 0
    for r1, c1 in track:
        d1 = dist_s[(r1, c1)]
        for dr in range(-max_cheat, max_cheat + 1):
            for dc in range(-max_cheat, max_cheat + 1):
                md = abs(dr) + abs(dc)
                if md == 0 or md > max_cheat:
                    continue
                pos = (r1 + dr, c1 + dc)
                if pos not in track:
                    continue
                if dist_s[pos] - d1 - md >= min_save:
                    count += 1

    return str(count)

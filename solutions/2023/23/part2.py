NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def solve(data: str) -> str:
    grid = data.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    start = end = None
    for c in range(cols):
        if grid[0][c] == ".":
            start = (0, c)
        if grid[rows - 1][c] == ".":
            end = (rows - 1, c)

    def walkable(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < cols and grid[r][c] != "#"

    def next_positions(r: int, c: int) -> list[tuple[int, int]]:
        return [
            (r + dr, c + dc)
            for dr, dc in NEIGHBORS
            if walkable(r + dr, c + dc)
        ]

    def is_junction(pos: tuple[int, int]) -> bool:
        if pos == start or pos == end:
            return True
        return len(next_positions(*pos)) != 2

    junctions: list[tuple[int, int]] = []
    junction_index: dict[tuple[int, int], int] = {}

    for r in range(rows):
        for c in range(cols):
            if not walkable(r, c):
                continue
            pos = (r, c)
            if is_junction(pos):
                junction_index[pos] = len(junctions)
                junctions.append(pos)

    graph: dict[int, list[tuple[int, int]]] = {i: [] for i in range(len(junctions))}

    for idx, (r, c) in enumerate(junctions):
        for nr, nc in next_positions(r, c):
            steps = 1
            pr, pc = r, c
            cr, cc = nr, nc
            while not is_junction((cr, cc)):
                nxt = [p for p in next_positions(cr, cc) if p != (pr, pc)]
                if len(nxt) != 1:
                    break
                pr, pc = cr, cc
                cr, cc = nxt[0]
                steps += 1
            if is_junction((cr, cc)):
                graph[idx].append((junction_index[(cr, cc)], steps))

    best = 0
    start_idx = junction_index[start]
    end_idx = junction_index[end]

    def dfs(node: int, visited: frozenset[int], steps: int) -> None:
        nonlocal best
        if node == end_idx:
            best = max(best, steps)
            return
        for nxt, dist in graph[node]:
            if nxt not in visited:
                dfs(nxt, visited | {nxt}, steps + dist)

    dfs(start_idx, frozenset({start_idx}), 0)
    return str(best)

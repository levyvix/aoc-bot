from collections import deque


def parse(data: str) -> tuple[list[str], tuple[int, int], tuple[int, int], dict[tuple[int, int], tuple[int, int]]]:
    grid = data.splitlines()
    rows = len(grid)
    cols = max(len(row) for row in grid)

    def cell(r: int, c: int) -> str | None:
        if 0 <= r < rows and 0 <= c < len(grid[r]):
            return grid[r][c]
        return None

    def walkable_neighbors(r: int, c: int) -> list[tuple[int, int]]:
        out: list[tuple[int, int]] = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if cell(nr, nc) == ".":
                out.append((nr, nc))
        return out

    start = end = None
    portal_entrances: dict[str, list[tuple[int, int]]] = {}
    seen_labels: set[tuple[str, int, int]] = set()

    for r in range(rows):
        for c in range(cols):
            ch = cell(r, c)
            if ch is None or not ("A" <= ch <= "Z"):
                continue

            label = None
            orientation = None
            if cell(r, c + 1) and "A" <= cell(r, c + 1) <= "Z":
                label = ch + cell(r, c + 1)
                orientation = "h"
            elif cell(r + 1, c) and "A" <= cell(r + 1, c) <= "Z":
                label = ch + cell(r + 1, c)
                orientation = "v"
            else:
                continue

            key = (label, r, c)
            if key in seen_labels:
                continue
            seen_labels.add(key)

            positions = [(r, c)]
            if orientation == "h":
                positions.append((r, c + 1))
            else:
                positions.append((r + 1, c))

            entrances: set[tuple[int, int]] = set()
            for pr, pc in positions:
                for pos in walkable_neighbors(pr, pc):
                    entrances.add(pos)

            if label == "AA":
                assert len(entrances) == 1
                start = next(iter(entrances))
                continue
            if label == "ZZ":
                assert len(entrances) == 1
                end = next(iter(entrances))
                continue

            portal_entrances.setdefault(label, []).extend(sorted(entrances))

    assert start is not None and end is not None

    portal_map: dict[tuple[int, int], tuple[int, int]] = {}
    for label, entrances in portal_entrances.items():
        if len(entrances) != 2:
            raise ValueError(f"portal {label} has {len(entrances)} entrances")
        a, b = entrances
        portal_map[a] = b
        portal_map[b] = a

    return grid, start, end, portal_map


def bfs(
    grid: list[str],
    start: tuple[int, int],
    end: tuple[int, int],
    portal_map: dict[tuple[int, int], tuple[int, int]],
) -> int:
    rows = len(grid)
    queue = deque([(start, 0)])
    seen = {start}

    while queue:
        (r, c), dist = queue.popleft()
        if (r, c) == end:
            return dist

        for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if not (0 <= nr < rows and 0 <= nc < len(grid[nr])):
                continue
            if grid[nr][nc] != ".":
                continue
            if (nr, nc) in seen:
                continue
            seen.add((nr, nc))
            queue.append(((nr, nc), dist + 1))

        if (r, c) in portal_map:
            dest = portal_map[(r, c)]
            if dest not in seen:
                seen.add(dest)
                queue.append((dest, dist + 1))

    raise RuntimeError("no path found")


def solve(data: str) -> str:
    grid, start, end, portal_map = parse(data)
    return str(bfs(grid, start, end, portal_map))

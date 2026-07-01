from collections import deque


def parse(data: str) -> tuple[
    list[str],
    tuple[int, int],
    tuple[int, int],
    dict[tuple[int, int], tuple[int, int]],
    dict[tuple[int, int], str],
]:
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
    portal_label: dict[tuple[int, int], str] = {}
    for label, entrances in portal_entrances.items():
        if len(entrances) != 2:
            raise ValueError(f"portal {label} has {len(entrances)} entrances")
        a, b = entrances
        portal_map[a] = b
        portal_map[b] = a
        portal_label[a] = label
        portal_label[b] = label

    inner_void = find_inner_void(grid)
    portal_ring: dict[tuple[int, int], str] = {}
    for pos in portal_map:
        portal_ring[pos] = classify_portal_ring(pos, grid, inner_void)

    return grid, start, end, portal_map, portal_ring


def find_inner_void(grid: list[str]) -> set[tuple[int, int]]:
    rows = len(grid)
    cols = max(len(row) for row in grid)
    center = (rows // 2, cols // 2)
    seed = None
    for radius in range(max(rows, cols)):
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                r, c = center[0] + dr, center[1] + dc
                if 0 <= r < rows and 0 <= c < len(grid[r]) and grid[r][c] == " ":
                    seed = (r, c)
                    break
            if seed:
                break
        if seed:
            break
    if seed is None:
        raise ValueError("inner void not found")

    void: set[tuple[int, int]] = set()
    queue = deque([seed])
    while queue:
        r, c = queue.popleft()
        if (r, c) in void:
            continue
        if not (0 <= r < rows and 0 <= c < len(grid[r])):
            continue
        if grid[r][c] != " ":
            continue
        void.add((r, c))
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            queue.append((r + dr, c + dc))
    return void


def label_touches_void(r: int, c: int, grid: list[str], void: set[tuple[int, int]]) -> bool:
    rows = len(grid)
    if (r, c) in void:
        return True
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if (nr, nc) in void:
            return True
    return False


def classify_portal_ring(
    entrance: tuple[int, int],
    grid: list[str],
    void: set[tuple[int, int]],
) -> str:
    rows = len(grid)
    r, c = entrance
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if not (0 <= nr < rows and 0 <= nc < len(grid[nr])):
            continue
        ch = grid[nr][nc]
        if "A" <= ch <= "Z":
            if label_touches_void(nr, nc, grid, void):
                return "inner"
    return "outer"


def bfs_recursive(
    grid: list[str],
    start: tuple[int, int],
    end: tuple[int, int],
    portal_map: dict[tuple[int, int], tuple[int, int]],
    portal_ring: dict[tuple[int, int], str],
) -> int:
    rows = len(grid)
    queue = deque([(start, 0, 0)])
    seen = {(start, 0)}

    while queue:
        (r, c), dist, level = queue.popleft()
        if (r, c) == end and level == 0:
            return dist

        for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if not (0 <= nr < rows and 0 <= nc < len(grid[nr])):
                continue
            if grid[nr][nc] != ".":
                continue
            state = ((nr, nc), level)
            if state in seen:
                continue
            seen.add(state)
            queue.append(((nr, nc), dist + 1, level))

        if (r, c) not in portal_map:
            continue

        dest = portal_map[(r, c)]
        ring = portal_ring[(r, c)]
        if ring == "inner":
            new_level = level + 1
        else:
            if level == 0:
                continue
            new_level = level - 1

        state = (dest, new_level)
        if state in seen:
            continue
        seen.add(state)
        queue.append((dest, dist + 1, new_level))

    raise RuntimeError("no path found")


def solve(data: str) -> str:
    grid, start, end, portal_map, portal_ring = parse(data)
    return str(bfs_recursive(grid, start, end, portal_map, portal_ring))

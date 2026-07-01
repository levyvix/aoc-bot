def neighbors(level: int, r: int, c: int) -> list[tuple[int, int, int]]:
    if (r, c) == (2, 2):
        return []

    nbrs: list[tuple[int, int, int]] = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr <= 4 and 0 <= nc <= 4:
            nbrs.append((level, nr, nc))

    if r == 0:
        nbrs.append((level - 1, 1, 2))
    if r == 4:
        nbrs.append((level - 1, 3, 2))
    if c == 0:
        nbrs.append((level - 1, 2, 1))
    if c == 4:
        nbrs.append((level - 1, 2, 3))

    if (r, c) == (1, 2):
        for col in range(5):
            nbrs.append((level + 1, 0, col))
    elif (r, c) == (3, 2):
        for col in range(5):
            nbrs.append((level + 1, 4, col))
    elif (r, c) == (2, 1):
        for row in range(5):
            nbrs.append((level + 1, row, 0))
    elif (r, c) == (2, 3):
        for row in range(5):
            nbrs.append((level + 1, row, 4))

    return nbrs


def parse_initial(data: str) -> set[tuple[int, int, int]]:
    bugs: set[tuple[int, int, int]] = set()
    for r, line in enumerate(data.strip().splitlines()):
        for c, cell in enumerate(line.strip()):
            if cell == "#":
                bugs.add((0, r, c))
    return bugs


def step(bugs: set[tuple[int, int, int]]) -> set[tuple[int, int, int]]:
    candidates: set[tuple[int, int, int]] = set(bugs)
    for level, r, c in bugs:
        for nbr in neighbors(level, r, c):
            candidates.add(nbr)

    next_bugs: set[tuple[int, int, int]] = set()
    for level, r, c in candidates:
        if (r, c) == (2, 2):
            continue
        count = sum(1 for nbr in neighbors(level, r, c) if nbr in bugs)
        if (level, r, c) in bugs:
            if count == 1:
                next_bugs.add((level, r, c))
        elif count in (1, 2):
            next_bugs.add((level, r, c))
    return next_bugs


def solve(data: str) -> str:
    bugs = parse_initial(data)
    for _ in range(200):
        bugs = step(bugs)
    return str(len(bugs))

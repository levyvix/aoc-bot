DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))  # right, down, left, up

MIRROR_SLASH = (3, 2, 1, 0)  # /
MIRROR_BACKSLASH = (1, 0, 3, 2)  # \


def energized_count(grid: list[str], start_r: int, start_c: int, start_d: int) -> int:
    rows, cols = len(grid), len(grid[0])
    energized: set[tuple[int, int]] = set()
    visited: set[tuple[int, int, int]] = set()
    stack = [(start_r, start_c, start_d)]

    while stack:
        r, c, d = stack.pop()
        if (r, c, d) in visited:
            continue
        if not (0 <= r < rows and 0 <= c < cols):
            continue
        visited.add((r, c, d))
        energized.add((r, c))

        tile = grid[r][c]
        if tile == ".":
            next_dirs = (d,)
        elif tile == "/":
            next_dirs = (MIRROR_SLASH[d],)
        elif tile == "\\":
            next_dirs = (MIRROR_BACKSLASH[d],)
        elif tile == "-":
            next_dirs = (d,) if d in (0, 2) else (2, 0)
        elif tile == "|":
            next_dirs = (d,) if d in (1, 3) else (3, 1)
        else:
            next_dirs = (d,)

        for nd in next_dirs:
            dr, dc = DIRS[nd]
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                stack.append((nr, nc, nd))

    return len(energized)


def solve(data: str) -> str:
    grid = data.strip().splitlines()
    return str(energized_count(grid, 0, 0, 0))

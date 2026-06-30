DIRS = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def expand_map(map_text: str) -> list[list[str]]:
    grid = []
    for row in map_text.splitlines():
        line = []
        for cell in row:
            if cell == "#":
                line.extend("##")
            elif cell == "O":
                line.extend("[]")
            elif cell == ".":
                line.extend("..")
            elif cell == "@":
                line.extend("@.")
            else:
                line.append(cell)
        grid.append(line)
    return grid


def boxes_to_push(
    grid: list[list[str]], row: int, col: int, dr: int, dc: int, seen: frozenset[tuple[int, int]]
) -> frozenset[tuple[int, int]] | None:
    cell = grid[row][col]
    if cell == "#":
        return None
    if cell == ".":
        return seen
    left = (row, col) if cell == "[" else (row, col - 1)
    if left in seen:
        return seen
    seen = seen | {left}
    br, bc = left
    next_left = boxes_to_push(grid, br + dr, bc, dr, dc, seen)
    if next_left is None:
        return None
    return boxes_to_push(grid, br + dr, bc + 1, dr, dc, next_left)


def try_move(grid: list[list[str]], robot: tuple[int, int], dr: int, dc: int) -> tuple[int, int] | None:
    r, c = robot
    boxes = boxes_to_push(grid, r + dr, c + dc, dr, dc, frozenset())
    if boxes is None:
        return None

    if dr < 0:
        order = sorted(boxes, key=lambda p: p[0])
    elif dr > 0:
        order = sorted(boxes, key=lambda p: p[0], reverse=True)
    elif dc < 0:
        order = sorted(boxes, key=lambda p: p[1])
    else:
        order = sorted(boxes, key=lambda p: p[1], reverse=True)

    for br, bc in order:
        grid[br][bc] = "."
        grid[br][bc + 1] = "."
        grid[br + dr][bc] = "["
        grid[br + dr][bc + 1] = "]"

    grid[r][c] = "."
    grid[r + dr][c + dc] = "@"
    return (r + dr, c + dc)


def solve(data: str) -> str:
    map_text, moves_text = data.strip().split("\n\n")
    grid = expand_map(map_text)
    moves = moves_text.replace("\n", "")

    robot = next(
        (r, c)
        for r, row in enumerate(grid)
        for c, cell in enumerate(row)
        if cell == "@"
    )

    for move in moves:
        dr, dc = DIRS[move]
        new_robot = try_move(grid, robot, dr, dc)
        if new_robot is not None:
            robot = new_robot

    total = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "[":
                total += 100 * r + c

    return str(total)

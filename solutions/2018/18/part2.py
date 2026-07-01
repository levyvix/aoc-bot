def solve(data: str) -> str:
    grid = [list(line.strip()) for line in data.strip().splitlines() if line.strip()]
    rows, cols = len(grid), len(grid[0])
    target = 1_000_000_000

    def grid_key() -> tuple[str, ...]:
        return tuple("".join(row) for row in grid)

    def count_adj(r: int, c: int, ch: str) -> int:
        n = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == ch:
                    n += 1
        return n

    def step() -> None:
        nonlocal grid
        new = [row[:] for row in grid]
        for r in range(rows):
            for c in range(cols):
                cell = grid[r][c]
                if cell == ".":
                    if count_adj(r, c, "|") >= 3:
                        new[r][c] = "|"
                elif cell == "|":
                    if count_adj(r, c, "#") >= 3:
                        new[r][c] = "#"
                elif cell == "#":
                    if count_adj(r, c, "#") >= 1 and count_adj(r, c, "|") >= 1:
                        new[r][c] = "#"
                    else:
                        new[r][c] = "."
        grid = new

    def resource_value() -> int:
        trees = sum(row.count("|") for row in grid)
        lumber = sum(row.count("#") for row in grid)
        return trees * lumber

    seen: dict[tuple[str, ...], int] = {}
    values: list[int] = []
    minute = 0

    while minute < target:
        step()
        minute += 1
        values.append(resource_value())
        key = grid_key()
        if key in seen:
            first = seen[key]
            cycle_len = minute - first
            idx = first - 1 + (target - first) % cycle_len
            return str(values[idx])
        seen[key] = minute

    return str(values[target - 1])

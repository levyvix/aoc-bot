def solve(data: str) -> str:
    grid = [list(line) for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])
    target_cycles = 1_000_000_000

    def tilt_north() -> None:
        for c in range(cols):
            write = 0
            for r in range(rows):
                cell = grid[r][c]
                if cell == "#":
                    write = r + 1
                elif cell == "O":
                    grid[r][c] = "."
                    grid[write][c] = "O"
                    write += 1

    def tilt_south() -> None:
        for c in range(cols):
            write = rows - 1
            for r in range(rows - 1, -1, -1):
                cell = grid[r][c]
                if cell == "#":
                    write = r - 1
                elif cell == "O":
                    grid[r][c] = "."
                    grid[write][c] = "O"
                    write -= 1

    def tilt_west() -> None:
        for r in range(rows):
            write = 0
            for c in range(cols):
                cell = grid[r][c]
                if cell == "#":
                    write = c + 1
                elif cell == "O":
                    grid[r][c] = "."
                    grid[r][write] = "O"
                    write += 1

    def tilt_east() -> None:
        for r in range(rows):
            write = cols - 1
            for c in range(cols - 1, -1, -1):
                cell = grid[r][c]
                if cell == "#":
                    write = c - 1
                elif cell == "O":
                    grid[r][c] = "."
                    grid[r][write] = "O"
                    write -= 1

    def spin_cycle() -> None:
        tilt_north()
        tilt_west()
        tilt_south()
        tilt_east()

    def load() -> int:
        return sum(
            rows - r
            for r in range(rows)
            for c in range(cols)
            if grid[r][c] == "O"
        )

    def grid_key() -> tuple[str, ...]:
        return tuple("".join(row) for row in grid)

    seen: dict[tuple[str, ...], int] = {}
    loads: dict[int, int] = {}

    for n in range(1, target_cycles + 1):
        spin_cycle()
        key = grid_key()
        current_load = load()

        if key in seen:
            first = seen[key]
            period = n - first
            rem = (target_cycles - first) % period
            cycle = target_cycles if rem == 0 else first + rem
            return str(loads[cycle])

        seen[key] = n
        loads[n] = current_load

    return str(loads[target_cycles])

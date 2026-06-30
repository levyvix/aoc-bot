def solve(data: str) -> str:
    grid = [[int(c) for c in line.strip()] for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])
    total_flashes = 0

    for _ in range(100):
        for r in range(rows):
            for c in range(cols):
                grid[r][c] += 1

        flashed: set[tuple[int, int]] = set()
        while True:
            new_flashes = [
                (r, c)
                for r in range(rows)
                for c in range(cols)
                if grid[r][c] > 9 and (r, c) not in flashed
            ]
            if not new_flashes:
                break
            for r, c in new_flashes:
                flashed.add((r, c))
                total_flashes += 1
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            grid[nr][nc] += 1

        for r, c in flashed:
            grid[r][c] = 0

    return str(total_flashes)

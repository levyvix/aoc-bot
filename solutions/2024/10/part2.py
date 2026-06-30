def solve(data: str) -> str:
    grid = [line.strip() for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    cache: dict[tuple[int, int, int], int] = {}

    def count_trails(r: int, c: int, h: int) -> int:
        key = (r, c, h)
        if key in cache:
            return cache[key]
        if h == 9:
            result = 1
        else:
            nh = h + 1
            result = 0
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and int(grid[nr][nc]) == nh:
                    result += count_trails(nr, nc, nh)
        cache[key] = result
        return result

    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "0":
                total += count_trails(r, c, 0)

    return str(total)

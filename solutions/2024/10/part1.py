def solve(data: str) -> str:
    grid = [line.strip() for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    cache: dict[tuple[int, int, int], frozenset[tuple[int, int]]] = {}

    def reachable_nines(r: int, c: int, h: int) -> frozenset[tuple[int, int]]:
        key = (r, c, h)
        if key in cache:
            return cache[key]
        if h == 9:
            result = frozenset({(r, c)})
        else:
            nh = h + 1
            reachable: set[tuple[int, int]] = set()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and int(grid[nr][nc]) == nh:
                    reachable |= reachable_nines(nr, nc, nh)
            result = frozenset(reachable)
        cache[key] = result
        return result

    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "0":
                total += len(reachable_nines(r, c, 0))

    return str(total)

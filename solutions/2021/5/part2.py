def solve(data: str) -> str:
    counts: dict[tuple[int, int], int] = {}

    for line in data.strip().splitlines():
        a, b = line.split(" -> ")
        x1, y1 = map(int, a.split(","))
        x2, y2 = map(int, b.split(","))

        dx = (x2 > x1) - (x2 < x1)
        dy = (y2 > y1) - (y2 < y1)
        steps = max(abs(x2 - x1), abs(y2 - y1))

        x, y = x1, y1
        for _ in range(steps + 1):
            counts[(x, y)] = counts.get((x, y), 0) + 1
            x += dx
            y += dy

    return str(sum(1 for c in counts.values() if c >= 2))

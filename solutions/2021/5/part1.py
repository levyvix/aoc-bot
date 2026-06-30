def solve(data: str) -> str:
    counts: dict[tuple[int, int], int] = {}

    for line in data.strip().splitlines():
        a, b = line.split(" -> ")
        x1, y1 = map(int, a.split(","))
        x2, y2 = map(int, b.split(","))

        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                key = (x1, y)
                counts[key] = counts.get(key, 0) + 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                key = (x, y1)
                counts[key] = counts.get(key, 0) + 1

    return str(sum(1 for c in counts.values() if c >= 2))

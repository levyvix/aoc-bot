def solve(data: str) -> str:
    grid = [line.rstrip("\n") for line in data.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])

    by_freq: dict[str, list[tuple[int, int]]] = {}
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch != ".":
                by_freq.setdefault(ch, []).append((r, c))

    antinodes: set[tuple[int, int]] = set()
    for positions in by_freq.values():
        for i, (r1, c1) in enumerate(positions):
            for r2, c2 in positions[i + 1 :]:
                for ar, ac in ((2 * r2 - r1, 2 * c2 - c1), (2 * r1 - r2, 2 * c1 - c2)):
                    if 0 <= ar < rows and 0 <= ac < cols:
                        antinodes.add((ar, ac))

    return str(len(antinodes))

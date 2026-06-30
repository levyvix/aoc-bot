from math import gcd


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
                dr, dc = r2 - r1, c2 - c1
                g = gcd(dr, dc)
                sr, sc = dr // g, dc // g

                r, c = r1, c1
                while 0 <= r < rows and 0 <= c < cols:
                    antinodes.add((r, c))
                    r += sr
                    c += sc
                r, c = r1 - sr, c1 - sc
                while 0 <= r < rows and 0 <= c < cols:
                    antinodes.add((r, c))
                    r -= sr
                    c -= sc

    return str(len(antinodes))

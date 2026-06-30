from collections import deque


def shortest_path(size: int, corrupted: set[tuple[int, int]], start: tuple[int, int], end: tuple[int, int]) -> int:
    if start in corrupted or end in corrupted:
        raise RuntimeError("no path to end")

    queue = deque([(start, 0)])
    seen = {start}

    while queue:
        (x, y), steps = queue.popleft()
        if (x, y) == end:
            return steps
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx <= size and 0 <= ny <= size:
                pos = (nx, ny)
                if pos not in corrupted and pos not in seen:
                    seen.add(pos)
                    queue.append((pos, steps + 1))

    raise RuntimeError("no path to end")


def solve(data: str) -> str:
    positions = [
        tuple(map(int, line.split(",")))
        for line in data.strip().splitlines()
        if line.strip()
    ]
    size = 70
    corrupted = set(positions[:1024])
    return str(shortest_path(size, corrupted, (0, 0), (size, size)))

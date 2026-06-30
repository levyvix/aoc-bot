from collections import deque


def has_path(size: int, corrupted: set[tuple[int, int]], start: tuple[int, int], end: tuple[int, int]) -> bool:
    if start in corrupted or end in corrupted:
        return False

    queue = deque([start])
    seen = {start}

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            return True
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx <= size and 0 <= ny <= size:
                pos = (nx, ny)
                if pos not in corrupted and pos not in seen:
                    seen.add(pos)
                    queue.append(pos)

    return False


def solve(data: str) -> str:
    positions = [
        tuple(map(int, line.split(",")))
        for line in data.strip().splitlines()
        if line.strip()
    ]
    size = 70
    start = (0, 0)
    end = (size, size)
    corrupted: set[tuple[int, int]] = set()

    for x, y in positions:
        corrupted.add((x, y))
        if not has_path(size, corrupted, start, end):
            return f"{x},{y}"

    raise RuntimeError("path never blocked")

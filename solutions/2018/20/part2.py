from collections import deque


def solve(data: str) -> str:
    regex = data.strip()
    x = y = 0
    stack: list[tuple[int, int]] = []
    doors: set[tuple[tuple[int, int], tuple[int, int]]] = set()

    for c in regex[1:-1]:
        if c in "NSEW":
            px, py = x, y
            if c == "N":
                y += 1
            elif c == "S":
                y -= 1
            elif c == "E":
                x += 1
            else:
                x -= 1
            edge = (px, py), (x, y)
            doors.add(tuple(sorted(edge)))
        elif c == "(":
            stack.append((x, y))
        elif c == "|":
            x, y = stack[-1]
        elif c == ")":
            x, y = stack.pop()

    dist = {(0, 0): 0}
    queue = deque([(0, 0)])
    while queue:
        cx, cy = queue.popleft()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = cx + dx, cy + dy
            edge = tuple(sorted(((cx, cy), (nx, ny))))
            if edge in doors and (nx, ny) not in dist:
                dist[(nx, ny)] = dist[(cx, cy)] + 1
                queue.append((nx, ny))

    threshold = 1000
    count = sum(1 for d in dist.values() if d >= threshold)
    return str(count)

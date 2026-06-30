import re


def solve(data: str) -> str:
    width, height = 101, 103

    robots = []
    for line in data.strip().splitlines():
        px, py, vx, vy = map(int, re.findall(r"-?\d+", line))
        robots.append((px, py, vx, vy))

    best_t = 0
    best_var = float("inf")
    for t in range(width * height):
        xs = []
        ys = []
        for px, py, vx, vy in robots:
            xs.append((px + vx * t) % width)
            ys.append((py + vy * t) % height)
        mx = sum(xs) / len(xs)
        my = sum(ys) / len(ys)
        var = sum((x - mx) ** 2 for x in xs) + sum((y - my) ** 2 for y in ys)
        if var < best_var:
            best_var = var
            best_t = t

    return str(best_t)

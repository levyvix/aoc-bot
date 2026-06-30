import re


def solve(data: str) -> str:
    width, height = 101, 103
    mid_x, mid_y = width // 2, height // 2
    seconds = 100

    q1 = q2 = q3 = q4 = 0
    for line in data.strip().splitlines():
        px, py, vx, vy = map(int, re.findall(r"-?\d+", line))
        x = (px + vx * seconds) % width
        y = (py + vy * seconds) % height
        if x == mid_x or y == mid_y:
            continue
        if x < mid_x and y < mid_y:
            q1 += 1
        elif x > mid_x and y < mid_y:
            q2 += 1
        elif x < mid_x and y > mid_y:
            q3 += 1
        else:
            q4 += 1

    return str(q1 * q2 * q3 * q4)

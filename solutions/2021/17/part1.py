import re


def _parse(data: str) -> tuple[int, int, int, int]:
    m = re.search(r"x=(\d+)\.\.(\d+), y=(-?\d+)\.\.(-?\d+)", data.strip())
    return tuple(map(int, m.groups()))  # type: ignore[return-value]


def _hits_target(
    vx: int, vy: int, x_min: int, x_max: int, y_min: int, y_max: int
) -> tuple[bool, int]:
    x, y = 0, 0
    max_y = 0
    while True:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True, max_y

        if x > x_max and vx >= 0:
            return False, max_y
        if y < y_min and vy < 0:
            return False, max_y

        x += vx
        y += vy
        max_y = max(max_y, y)

        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True, max_y

        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1

        if x > x_max + 500 or y < y_min - 500:
            break

    return False, max_y


def solve(data: str) -> str:
    x_min, x_max, y_min, y_max = _parse(data)
    best = 0
    for vy in range(y_min, -y_min + 1):
        for vx in range(1, x_max + 2):
            hit, peak = _hits_target(vx, vy, x_min, x_max, y_min, y_max)
            if hit:
                best = max(best, peak)
    return str(best)

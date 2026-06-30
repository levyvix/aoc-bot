import re


def _parse(data: str) -> tuple[int, int, int, int]:
    m = re.search(r"x=(\d+)\.\.(\d+), y=(-?\d+)\.\.(-?\d+)", data.strip())
    return tuple(map(int, m.groups()))  # type: ignore[return-value]


def _hits_target(
    vx: int, vy: int, x_min: int, x_max: int, y_min: int, y_max: int
) -> bool:
    x, y = 0, 0
    while True:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True

        if x > x_max and vx >= 0:
            return False
        if y < y_min and vy < 0:
            return False

        x += vx
        y += vy

        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True

        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1

        if x > x_max + 500 or y < y_min - 500:
            break

    return False


def solve(data: str) -> str:
    x_min, x_max, y_min, y_max = _parse(data)
    count = 0
    for vy in range(y_min, -y_min + 1):
        for vx in range(1, x_max + 2):
            if _hits_target(vx, vy, x_min, x_max, y_min, y_max):
                count += 1
    return str(count)

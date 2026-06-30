from fractions import Fraction


def parse_hailstones(data: str) -> list[tuple[int, int, int, int]]:
    stones = []
    for line in data.strip().splitlines():
        pos, vel = line.split("@")
        px, py, _pz = map(int, pos.split(","))
        vx, vy, _vz = map(int, vel.split(","))
        stones.append((px, py, vx, vy))
    return stones


def paths_intersect_in_area(
    a: tuple[int, int, int, int],
    b: tuple[int, int, int, int],
    lo: int,
    hi: int,
) -> bool:
    px_a, py_a, vx_a, vy_a = a
    px_b, py_b, vx_b, vy_b = b

    det = vx_b * vy_a - vx_a * vy_b
    if det == 0:
        return False

    t_num = vy_b * (px_a - px_b) + vx_b * (py_b - py_a)
    s_num = vx_a * (py_b - py_a) - vy_a * (px_b - px_a)

    if det > 0:
        if t_num < 0 or s_num < 0:
            return False
    else:
        if t_num > 0 or s_num > 0:
            return False

    t = Fraction(t_num, det)
    x = px_a + vx_a * t
    y = py_a + vy_a * t

    return lo <= x <= hi and lo <= y <= hi


def solve(data: str) -> str:
    lo = 200_000_000_000_000
    hi = 400_000_000_000_000
    stones = parse_hailstones(data)
    count = 0
    for i in range(len(stones)):
        for j in range(i + 1, len(stones)):
            if paths_intersect_in_area(stones[i], stones[j], lo, hi):
                count += 1
    return str(count)

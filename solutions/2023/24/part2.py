from fractions import Fraction


def parse_hailstones(data: str) -> list[tuple[int, ...]]:
    stones = []
    for line in data.strip().splitlines():
        pos, vel = line.split("@")
        px, py, pz = map(int, pos.split(","))
        vx, vy, vz = map(int, vel.split(","))
        stones.append((px, py, pz, vx, vy, vz))
    return stones


def pair_equations(
    a: tuple[int, ...], b: tuple[int, ...]
) -> list[tuple[list[int], int]]:
    px_i, py_i, pz_i, vx_i, vy_i, vz_i = a
    px_j, py_j, pz_j, vx_j, vy_j, vz_j = b
    c_i_xy = px_i * vy_i - py_i * vx_i
    c_j_xy = px_j * vy_j - py_j * vx_j
    c_i_xz = px_i * vz_i - pz_i * vx_i
    c_j_xz = px_j * vz_j - pz_j * vx_j
    c_i_yz = py_i * vz_i - pz_i * vy_i
    c_j_yz = py_j * vz_j - pz_j * vy_j

    return [
        (
            [vy_i - vy_j, vx_j - vx_i, 0, py_j - py_i, px_i - px_j, 0],
            c_i_xy - c_j_xy,
        ),
        (
            [vz_i - vz_j, 0, vx_j - vx_i, pz_j - pz_i, 0, px_i - px_j],
            c_i_xz - c_j_xz,
        ),
        (
            [0, vz_i - vz_j, vy_j - vy_i, 0, pz_j - pz_i, py_i - py_j],
            c_i_yz - c_j_yz,
        ),
    ]


def solve_linear(
    equations: list[tuple[list[int], int]],
) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]:
    # variables: px, py, pz, vx, vy, vz
    rows: list[list[Fraction]] = []
    for coeffs, rhs in equations:
        rows.append([Fraction(c) for c in coeffs] + [Fraction(rhs)])

    width = 7
    height = len(rows)
    col = 0
    for row in range(height):
        while col < 6:
            pivot = None
            for r in range(row, height):
                if rows[r][col] != 0:
                    pivot = r
                    break
            if pivot is None:
                col += 1
                continue
            rows[row], rows[pivot] = rows[pivot], rows[row]
            pivot_val = rows[row][col]
            rows[row] = [v / pivot_val for v in rows[row]]
            for r in range(height):
                if r != row and rows[r][col] != 0:
                    factor = rows[r][col]
                    rows[r] = [rows[r][c] - factor * rows[row][c] for c in range(width)]
            col += 1
            break

    solution = [Fraction(0)] * 6
    for r in range(height):
        lead = next((c for c in range(6) if rows[r][c] != 0), None)
        if lead is not None:
            solution[lead] = rows[r][6]
    return tuple(solution)  # type: ignore[return-value]


def collides(
    rock: tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction],
    stone: tuple[int, ...],
) -> bool:
    px, py, pz, vx, vy, vz = rock
    px_i, py_i, pz_i, vx_i, vy_i, vz_i = stone
    times: list[Fraction] = []
    if vx != vx_i:
        times.append((px_i - px) / (vx - vx_i))
    if vy != vy_i:
        times.append((py_i - py) / (vy - vy_i))
    if vz != vz_i:
        times.append((pz_i - pz) / (vz - vz_i))
    if not times:
        return px == px_i and py == py_i and pz == pz_i
    t0 = times[0]
    if t0 < 0:
        return False
    for t in times[1:]:
        if t != t0:
            return False
    t = t0
    return (
        px + vx * t == px_i + vx_i * t
        and py + vy * t == py_i + vy_i * t
        and pz + vz * t == pz_i + vz_i * t
    )


def solve(data: str) -> str:
    stones = parse_hailstones(data)
    equations: list[tuple[list[int], int]] = []
    for i in range(len(stones)):
        for j in range(i + 1, len(stones)):
            equations.extend(pair_equations(stones[i], stones[j]))
            if len(equations) >= 6:
                break
        if len(equations) >= 6:
            break

    rock = solve_linear(equations[:6])

    for stone in stones:
        if not collides(rock, stone):
            raise ValueError("solution does not collide with all hailstones")

    px, py, pz, *_ = rock
    if any(v.denominator != 1 for v in (px, py, pz)):
        raise ValueError("non-integer rock position")
    return str(int(px) + int(py) + int(pz))

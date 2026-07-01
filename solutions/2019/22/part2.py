def modinv(a: int, n: int) -> int:
    t, new_t = 0, 1
    r, new_r = n, a % n
    while new_r:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r
    if r != 1:
        raise ValueError("not invertible")
    return t % n


def apply_op(a: int, b: int, line: str, n: int) -> tuple[int, int]:
    if line == "deal into new stack":
        a_op, b_op = -1, n - 1
    elif line.startswith("cut"):
        x = int(line.split()[-1])
        a_op, b_op = 1, (-x) % n
    elif line.startswith("deal with increment"):
        inc = int(line.split()[-1])
        a_op, b_op = inc, 0
    else:
        raise ValueError(f"unknown instruction: {line}")
    return (a_op * a) % n, (a_op * b + b_op) % n


def pow_affine(a: int, b: int, k: int, n: int) -> tuple[int, int]:
    ra, rb = 1, 0
    ca, cb = a, b
    while k:
        if k & 1:
            ra, rb = (ca * ra) % n, (ca * rb + cb) % n
        ca, cb = (ca * ca) % n, (ca * cb + cb) % n
        k >>= 1
    return ra, rb


def solve(data: str) -> str:
    n = 119315717514047
    repeats = 101741582076661
    target_pos = 2020

    a, b = 1, 0
    for line in data.strip().splitlines():
        a, b = apply_op(a, b, line.strip(), n)

    a, b = pow_affine(a, b, repeats, n)
    card = (modinv(a, n) * (target_pos - b)) % n
    return str(card)

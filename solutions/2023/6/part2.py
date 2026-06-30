import math


def count_ways(time: int, record: int) -> int:
    disc = time * time - 4 * record
    if disc <= 0:
        return 0
    s = math.isqrt(disc)
    lo = (time - s) // 2
    if lo * (time - lo) <= record:
        lo += 1
    hi = (time + s) // 2
    if hi * (time - hi) <= record:
        hi -= 1
    if lo > hi:
        return 0
    return hi - lo + 1


def solve(data: str) -> str:
    lines = data.strip().splitlines()
    time = int("".join(lines[0].split(":")[1].split()))
    record = int("".join(lines[1].split(":")[1].split()))
    return str(count_ways(time, record))

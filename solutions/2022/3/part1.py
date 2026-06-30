def priority(c: str) -> int:
    if c.islower():
        return ord(c) - ord("a") + 1
    return ord(c) - ord("A") + 27


def solve(data: str) -> str:
    total = 0
    for line in data.strip().splitlines():
        if not line:
            continue
        n = len(line)
        half = n // 2
        left, right = set(line[:half]), set(line[half:])
        common = left & right
        total += priority(next(iter(common)))
    return str(total)

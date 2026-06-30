def priority(c: str) -> int:
    if c.islower():
        return ord(c) - ord("a") + 1
    return ord(c) - ord("A") + 27


def solve(data: str) -> str:
    lines = [line for line in data.strip().splitlines() if line]
    total = 0
    for i in range(0, len(lines), 3):
        group = lines[i : i + 3]
        common = set(group[0]) & set(group[1]) & set(group[2])
        total += priority(next(iter(common)))
    return str(total)

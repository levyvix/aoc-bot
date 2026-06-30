def solve(data: str) -> str:
    total = 0
    for line in data.splitlines():
        if not line.strip():
            continue
        _, rest = line.split(":", 1)
        winning, have = rest.split("|")
        winning_nums = set(winning.split())
        matches = sum(1 for n in have.split() if n in winning_nums)
        if matches:
            total += 1 << (matches - 1)
    return str(total)

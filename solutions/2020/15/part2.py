def solve(data: str) -> str:
    starting = list(map(int, data.strip().split(",")))

    last_seen: dict[int, int] = {}
    for turn, num in enumerate(starting[:-1], start=1):
        last_seen[num] = turn

    last = starting[-1]

    for turn in range(len(starting) + 1, 30_000_001):
        prev = last
        if prev in last_seen:
            last = (turn - 1) - last_seen[prev]
        else:
            last = 0
        last_seen[prev] = turn - 1

    return str(last)

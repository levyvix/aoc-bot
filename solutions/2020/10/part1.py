def solve(data: str) -> str:
    adapters = sorted(int(line) for line in data.strip().splitlines())
    chain = [0] + adapters + [adapters[-1] + 3]

    ones = threes = 0
    for a, b in zip(chain, chain[1:]):
        diff = b - a
        if diff == 1:
            ones += 1
        elif diff == 3:
            threes += 1

    return str(ones * threes)

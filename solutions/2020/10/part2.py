def solve(data: str) -> str:
    adapters = sorted(int(line) for line in data.strip().splitlines())
    target = adapters[-1] + 3
    positions = [0] + adapters + [target]

    ways = {0: 1}
    for pos in positions[1:]:
        ways[pos] = sum(ways.get(pos - d, 0) for d in (1, 2, 3))

    return str(ways[target])

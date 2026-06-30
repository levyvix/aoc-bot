def count_ways(design: str, patterns: list[str]) -> int:
    n = len(design)
    ways = [0] * (n + 1)
    ways[0] = 1
    for i in range(1, n + 1):
        for pattern in patterns:
            plen = len(pattern)
            if i >= plen and design[i - plen : i] == pattern:
                ways[i] += ways[i - plen]
    return ways[n]


def solve(data: str) -> str:
    blocks = data.strip().split("\n\n")
    patterns = [p.strip() for p in blocks[0].split(", ")]
    designs = blocks[1].splitlines()

    total = sum(count_ways(design, patterns) for design in designs)
    return str(total)

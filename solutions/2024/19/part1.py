def can_make(design: str, patterns: list[str]) -> bool:
    n = len(design)
    reachable = [False] * (n + 1)
    reachable[0] = True
    for i in range(1, n + 1):
        for pattern in patterns:
            plen = len(pattern)
            if i >= plen and reachable[i - plen] and design[i - plen : i] == pattern:
                reachable[i] = True
                break
    return reachable[n]


def solve(data: str) -> str:
    blocks = data.strip().split("\n\n")
    patterns = [p.strip() for p in blocks[0].split(", ")]
    designs = blocks[1].splitlines()

    count = sum(1 for design in designs if can_make(design, patterns))
    return str(count)

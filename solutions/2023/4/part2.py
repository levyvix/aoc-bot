def solve(data: str) -> str:
    lines = [line for line in data.splitlines() if line.strip()]
    matches = []
    for line in lines:
        _, rest = line.split(":", 1)
        winning, have = rest.split("|")
        winning_nums = set(winning.split())
        matches.append(sum(1 for n in have.split() if n in winning_nums))

    counts = [1] * len(matches)
    for i, m in enumerate(matches):
        for j in range(1, m + 1):
            if i + j < len(counts):
                counts[i + j] += counts[i]

    return str(sum(counts))

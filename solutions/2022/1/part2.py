def solve(data: str) -> str:
    totals: list[int] = []
    current = 0
    for line in data.splitlines():
        if not line.strip():
            totals.append(current)
            current = 0
        else:
            current += int(line)
    totals.append(current)
    top_three = sorted(totals, reverse=True)[:3]
    return str(sum(top_three))

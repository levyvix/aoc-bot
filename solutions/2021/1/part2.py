def solve(data: str) -> str:
    depths = [int(line) for line in data.strip().splitlines() if line.strip()]
    count = sum(1 for i in range(len(depths) - 3) if depths[i + 3] > depths[i])
    return str(count)

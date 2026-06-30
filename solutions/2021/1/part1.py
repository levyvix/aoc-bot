def solve(data: str) -> str:
    depths = [int(line) for line in data.strip().splitlines() if line.strip()]
    count = sum(1 for i in range(1, len(depths)) if depths[i] > depths[i - 1])
    return str(count)

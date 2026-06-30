def solve(data: str) -> str:
    positions = sorted(map(int, data.strip().split(",")))
    target = positions[len(positions) // 2]
    fuel = sum(abs(p - target) for p in positions)
    return str(fuel)

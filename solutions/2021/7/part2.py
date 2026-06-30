def solve(data: str) -> str:
    positions = list(map(int, data.strip().split(",")))
    lo, hi = min(positions), max(positions)

    def fuel_cost(target: int) -> int:
        total = 0
        for p in positions:
            d = abs(p - target)
            total += d * (d + 1) // 2
        return total

    return str(min(fuel_cost(t) for t in range(lo, hi + 1)))

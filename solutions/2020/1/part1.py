def solve(data: str) -> str:
    nums = [int(line) for line in data.strip().splitlines() if line.strip()]
    seen = set()
    for n in nums:
        complement = 2020 - n
        if complement in seen:
            return str(n * complement)
        seen.add(n)
    raise ValueError("no two entries sum to 2020")

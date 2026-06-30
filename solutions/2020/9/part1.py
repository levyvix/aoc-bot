def solve(data: str) -> str:
    nums = [int(line) for line in data.strip().splitlines()]
    preamble = 25

    for i in range(preamble, len(nums)):
        target = nums[i]
        window = nums[i - preamble : i]
        seen = set(window)
        if not any((target - a) in seen and (target - a) != a for a in window):
            return str(target)

    raise ValueError("no invalid number found")

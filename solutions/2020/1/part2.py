def solve(data: str) -> str:
    nums = [int(line) for line in data.strip().splitlines() if line.strip()]
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 2020:
                    return str(nums[i] * nums[j] * nums[k])
    raise ValueError("no three entries sum to 2020")

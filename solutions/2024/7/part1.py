def solve(data: str) -> str:
    total = 0
    for line in data.strip().splitlines():
        target_s, nums_s = line.split(": ")
        target = int(target_s)
        nums = list(map(int, nums_s.split()))

        def can_reach(acc: int, idx: int) -> bool:
            if idx == len(nums):
                return acc == target
            n = nums[idx]
            return can_reach(acc + n, idx + 1) or can_reach(acc * n, idx + 1)

        if can_reach(nums[0], 1):
            total += target

    return str(total)

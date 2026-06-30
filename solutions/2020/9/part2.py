def _find_invalid(nums: list[int], preamble: int = 25) -> int:
    for i in range(preamble, len(nums)):
        target = nums[i]
        window = nums[i - preamble : i]
        seen = set(window)
        if not any((target - a) in seen and (target - a) != a for a in window):
            return target
    raise ValueError("no invalid number found")


def solve(data: str) -> str:
    nums = [int(line) for line in data.strip().splitlines()]
    target = _find_invalid(nums)

    left = 0
    current = 0
    for right in range(len(nums)):
        current += nums[right]
        while current > target and left < right:
            current -= nums[left]
            left += 1
        if current == target and right - left + 1 >= 2:
            window = nums[left : right + 1]
            return str(min(window) + max(window))

    raise ValueError("no contiguous range found")

def solve(data: str) -> str:
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]
    if not lines:
        return "0"
    width = len(lines[0])

    def rating(numbers: list[str], oxygen: bool) -> int:
        nums = list(numbers)
        for i in range(width):
            if len(nums) == 1:
                break
            ones = sum(1 for n in nums if n[i] == "1")
            zeros = len(nums) - ones
            if ones > zeros:
                keep = "1" if oxygen else "0"
            elif zeros > ones:
                keep = "0" if oxygen else "1"
            else:
                keep = "1" if oxygen else "0"
            nums = [n for n in nums if n[i] == keep]
        return int(nums[0], 2)

    oxygen = rating(lines, oxygen=True)
    co2 = rating(lines, oxygen=False)
    return str(oxygen * co2)

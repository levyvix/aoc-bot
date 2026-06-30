def extrapolate(nums: list[int]) -> int:
    sequences = [list(nums)]
    while len(sequences[-1]) > 1 and not all(x == 0 for x in sequences[-1]):
        prev = sequences[-1]
        sequences.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])

    last_val = 0
    for seq in reversed(sequences):
        last_val = seq[-1] + last_val
    return last_val


def solve(data: str) -> str:
    total = 0
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        nums = [int(x) for x in line.split()]
        total += extrapolate(nums)
    return str(total)

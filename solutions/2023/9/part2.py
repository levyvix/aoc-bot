def extrapolate_backwards(nums: list[int]) -> int:
    sequences = [list(nums)]
    while len(sequences[-1]) > 1 and not all(x == 0 for x in sequences[-1]):
        prev = sequences[-1]
        sequences.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])

    first_val = 0
    for seq in reversed(sequences):
        first_val = seq[0] - first_val
    return first_val


def solve(data: str) -> str:
    total = 0
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        nums = [int(x) for x in line.split()]
        total += extrapolate_backwards(nums)
    return str(total)

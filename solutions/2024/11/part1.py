from collections import Counter


def blink(stones: Counter[int]) -> Counter[int]:
    new: Counter[int] = Counter()
    for n, count in stones.items():
        if n == 0:
            new[1] += count
        elif len(str(n)) % 2 == 0:
            s = str(n)
            mid = len(s) // 2
            new[int(s[:mid])] += count
            new[int(s[mid:])] += count
        else:
            new[n * 2024] += count
    return new


def solve(data: str) -> str:
    stones = Counter(int(x) for x in data.split())
    for _ in range(25):
        stones = blink(stones)
    return str(sum(stones.values()))

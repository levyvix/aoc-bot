from functools import lru_cache


def count_arrangements(springs: str, groups: tuple[int, ...]) -> int:
    @lru_cache(maxsize=None)
    def dp(i: int, g: int, run: int) -> int:
        if i == len(springs):
            if g == len(groups) and run == 0:
                return 1
            if g == len(groups) - 1 and run == groups[g]:
                return 1
            return 0

        ch = springs[i]
        total = 0

        if ch in ".?":
            if run > 0:
                if g < len(groups) and run == groups[g]:
                    total += dp(i + 1, g + 1, 0)
            else:
                total += dp(i + 1, g, 0)

        if ch in "#?":
            if g < len(groups) and run < groups[g]:
                total += dp(i + 1, g, run + 1)

        return total

    return dp(0, 0, 0)


def solve(data: str) -> str:
    total = 0
    for line in data.strip().splitlines():
        springs, groups_str = line.split()
        groups = tuple(int(x) for x in groups_str.split(","))
        total += count_arrangements(springs, groups)
    return str(total)

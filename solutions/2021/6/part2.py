def solve(data: str) -> str:
    counts = [0] * 9
    for timer in map(int, data.strip().split(",")):
        counts[timer] += 1

    for _ in range(256):
        spawning = counts[0]
        counts = counts[1:] + [0]
        counts[6] += spawning
        counts[8] = spawning

    return str(sum(counts))

def count_ways(time: int, record: int) -> int:
    return sum(1 for hold in range(time + 1) if hold * (time - hold) > record)


def solve(data: str) -> str:
    lines = data.strip().splitlines()
    times = list(map(int, lines[0].split(":")[1].split()))
    distances = list(map(int, lines[1].split(":")[1].split()))

    product = 1
    for time, record in zip(times, distances):
        product *= count_ways(time, record)

    return str(product)

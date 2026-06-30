from math import gcd


def solve(data: str) -> str:
    line = data.strip().splitlines()[1]
    buses = []
    for i, token in enumerate(line.split(",")):
        if token != "x":
            buses.append((i, int(token)))

    t = 0
    step = 1
    for offset, bus_id in buses:
        while (t + offset) % bus_id != 0:
            t += step
        step = step // gcd(step, bus_id) * bus_id

    return str(t)

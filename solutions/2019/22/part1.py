def solve(data: str) -> str:
    n = 10007
    pos = 2019

    for line in data.strip().splitlines():
        line = line.strip()
        if line == "deal into new stack":
            pos = (n - 1) - pos
        elif line.startswith("cut"):
            x = int(line.split()[-1])
            pos = (pos - x) % n
        elif line.startswith("deal with increment"):
            inc = int(line.split()[-1])
            pos = (pos * inc) % n

    return str(pos)

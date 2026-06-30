def solve(data: str) -> str:
    total = 0
    for line in data.splitlines():
        if not line:
            continue
        _, reveals = line.split(": ", 1)
        mins = {"red": 0, "green": 0, "blue": 0}
        for reveal in reveals.split("; "):
            for part in reveal.split(", "):
                count, color = part.split()
                mins[color] = max(mins[color], int(count))
        total += mins["red"] * mins["green"] * mins["blue"]
    return str(total)

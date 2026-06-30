def solve(data: str) -> str:
    total = 0
    for group in data.strip().split("\n\n"):
        total += len(set("".join(group.split("\n"))))
    return str(total)

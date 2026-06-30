def solve(data: str) -> str:
    total = 0
    for group in data.strip().split("\n\n"):
        people = group.split("\n")
        common = set(people[0])
        for person in people[1:]:
            common &= set(person)
        total += len(common)
    return str(total)

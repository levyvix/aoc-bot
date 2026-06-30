REQUIRED = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


def solve(data: str) -> str:
    count = 0
    for block in data.strip().split("\n\n"):
        fields = set()
        for token in block.replace("\n", " ").split():
            key, _, _ = token.partition(":")
            fields.add(key)
        if REQUIRED <= fields:
            count += 1
    return str(count)

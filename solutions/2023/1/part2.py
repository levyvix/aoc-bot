WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def first_digit(line: str) -> int:
    for i, ch in enumerate(line):
        if ch.isdigit():
            return int(ch)
        for word, value in WORDS.items():
            if line[i:].startswith(word):
                return value
    raise ValueError(f"no digit found in line: {line!r}")


def last_digit(line: str) -> int:
    for i in range(len(line) - 1, -1, -1):
        if line[i].isdigit():
            return int(line[i])
        for word, value in WORDS.items():
            if line[i:].startswith(word):
                return value
    raise ValueError(f"no digit found in line: {line!r}")


def solve(data: str) -> str:
    total = 0
    for line in data.splitlines():
        if not line:
            continue
        total += first_digit(line) * 10 + last_digit(line)
    return str(total)

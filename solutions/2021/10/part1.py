PAIRS = {")": "(", "]": "[", "}": "{", ">": "<"}
SCORES = {")": 3, "]": 57, "}": 1197, ">": 25137}
OPEN = set("([{<")


def solve(data: str) -> str:
    total = 0
    for line in data.strip().splitlines():
        stack = []
        corrupted = False
        for ch in line.strip():
            if ch in OPEN:
                stack.append(ch)
            elif ch in PAIRS:
                if not stack or stack[-1] != PAIRS[ch]:
                    total += SCORES[ch]
                    corrupted = True
                    break
                stack.pop()
    return str(total)

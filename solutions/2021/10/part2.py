PAIRS = {")": "(", "]": "[", "}": "{", ">": "<"}
CLOSE = {"(": ")", "[": "]", "{": "}", "<": ">"}
OPEN = set("([{<")
SCORES = {")": 1, "]": 2, "}": 3, ">": 4}


def solve(data: str) -> str:
    scores = []
    for line in data.strip().splitlines():
        stack = []
        corrupted = False
        for ch in line.strip():
            if ch in OPEN:
                stack.append(ch)
            elif ch in PAIRS:
                if not stack or stack[-1] != PAIRS[ch]:
                    corrupted = True
                    break
                stack.pop()
        if corrupted or not stack:
            continue
        completion = "".join(CLOSE[ch] for ch in reversed(stack))
        score = 0
        for ch in completion:
            score = score * 5 + SCORES[ch]
        scores.append(score)
    scores.sort()
    return str(scores[len(scores) // 2])

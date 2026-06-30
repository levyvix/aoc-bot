def solve(data: str) -> str:
    lines = data.strip().splitlines()
    template = lines[0]
    rules: dict[str, str] = {}
    for line in lines[2:]:
        pair, insert = line.split(" -> ")
        rules[pair] = insert

    for _ in range(10):
        parts = []
        for i in range(len(template) - 1):
            parts.append(template[i] + rules[template[i : i + 2]])
        parts.append(template[-1])
        template = "".join(parts)

    counts: dict[str, int] = {}
    for ch in template:
        counts[ch] = counts.get(ch, 0) + 1

    values = counts.values()
    return str(max(values) - min(values))

def solve(data: str) -> str:
    lines = data.strip().splitlines()
    template = lines[0]
    rules: dict[str, str] = {}
    for line in lines[2:]:
        pair, insert = line.split(" -> ")
        rules[pair] = insert

    pair_counts: dict[str, int] = {}
    for i in range(len(template) - 1):
        pair = template[i : i + 2]
        pair_counts[pair] = pair_counts.get(pair, 0) + 1

    element_counts: dict[str, int] = {}
    for ch in template:
        element_counts[ch] = element_counts.get(ch, 0) + 1

    for _ in range(40):
        pair_deltas: dict[str, int] = {}
        element_deltas: dict[str, int] = {}
        for pair, count in pair_counts.items():
            insert = rules[pair]
            a, b = pair[0], pair[1]
            pair_deltas[pair] = pair_deltas.get(pair, 0) - count
            pair_deltas[a + insert] = pair_deltas.get(a + insert, 0) + count
            pair_deltas[insert + b] = pair_deltas.get(insert + b, 0) + count
            element_deltas[insert] = element_deltas.get(insert, 0) + count

        for pair, delta in pair_deltas.items():
            new_count = pair_counts.get(pair, 0) + delta
            if new_count == 0:
                pair_counts.pop(pair, None)
            else:
                pair_counts[pair] = new_count

        for ch, delta in element_deltas.items():
            element_counts[ch] = element_counts.get(ch, 0) + delta

    values = element_counts.values()
    return str(max(values) - min(values))

def _parse(data: str):
    rules_section, updates_section = data.strip().split("\n\n")
    rules = []
    for line in rules_section.splitlines():
        left, right = line.split("|")
        rules.append((int(left), int(right)))
    updates = []
    for line in updates_section.splitlines():
        updates.append([int(x) for x in line.split(",")])
    return rules, updates


def _is_valid(pages: list[int], rules: list[tuple[int, int]]) -> bool:
    page_set = set(pages)
    pos = {p: i for i, p in enumerate(pages)}
    for left, right in rules:
        if left in page_set and right in page_set:
            if pos[left] >= pos[right]:
                return False
    return True


def _order_pages(pages: list[int], rules: list[tuple[int, int]]) -> list[int]:
    page_set = set(pages)
    successors: dict[int, list[int]] = {p: [] for p in pages}
    in_degree = {p: 0 for p in pages}

    for left, right in rules:
        if left in page_set and right in page_set:
            successors[left].append(right)
            in_degree[right] += 1

    queue = sorted(p for p in pages if in_degree[p] == 0)
    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)
        for succ in successors[node]:
            in_degree[succ] -= 1
            if in_degree[succ] == 0:
                queue.append(succ)
                queue.sort()

    return result


def solve(data: str) -> str:
    rules, updates = _parse(data)
    total = 0
    for pages in updates:
        if not _is_valid(pages, rules):
            ordered = _order_pages(pages, rules)
            total += ordered[len(ordered) // 2]
    return str(total)

def solve(data: str) -> str:
    rules_section, updates_section = data.strip().split("\n\n")
    rules = []
    for line in rules_section.splitlines():
        left, right = line.split("|")
        rules.append((int(left), int(right)))

    total = 0
    for line in updates_section.splitlines():
        pages = [int(x) for x in line.split(",")]
        page_set = set(pages)
        pos = {p: i for i, p in enumerate(pages)}

        valid = True
        for left, right in rules:
            if left in page_set and right in page_set:
                if pos[left] >= pos[right]:
                    valid = False
                    break

        if valid:
            total += pages[len(pages) // 2]

    return str(total)

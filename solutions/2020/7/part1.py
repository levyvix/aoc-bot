import re


def solve(data: str) -> str:
    contains: dict[str, list[tuple[int, str]]] = {}
    for line in data.strip().splitlines():
        container, rest = line.split(" bags contain ")
        contents: list[tuple[int, str]] = []
        if "no other bags" not in rest:
            for part in rest.rstrip(".").split(", "):
                count, color = part.split(" ", 1)
                color = color.removesuffix(" bag").removesuffix(" bags")
                contents.append((int(count), color))
        contains[container] = contents

    can_contain: dict[str, set[str]] = {}
    for container, items in contains.items():
        for _, color in items:
            can_contain.setdefault(color, set()).add(container)

    seen: set[str] = set()
    queue = ["shiny gold"]
    while queue:
        current = queue.pop()
        for parent in can_contain.get(current, ()):
            if parent not in seen:
                seen.add(parent)
                queue.append(parent)

    return str(len(seen))

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

    def count_bags(color: str) -> int:
        total = 0
        for qty, sub_color in contains[color]:
            total += qty * (1 + count_bags(sub_color))
        return total

    return str(count_bags("shiny gold"))

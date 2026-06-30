def solve(data: str) -> str:
    graph: dict[str, list[str]] = {}
    for line in data.strip().splitlines():
        a, b = line.split("-")
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, []).append(a)

    def is_small(cave: str) -> bool:
        return cave.islower()

    def count_paths(current: str, visited_small: frozenset[str]) -> int:
        if current == "end":
            return 1
        total = 0
        for neighbor in graph.get(current, []):
            if neighbor == "start":
                continue
            if is_small(neighbor) and neighbor in visited_small:
                continue
            new_visited = visited_small
            if is_small(neighbor):
                new_visited = visited_small | {neighbor}
            total += count_paths(neighbor, new_visited)
        return total

    return str(count_paths("start", frozenset()))

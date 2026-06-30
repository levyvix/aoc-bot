def solve(data: str) -> str:
    graph: dict[str, list[str]] = {}
    for line in data.strip().splitlines():
        a, b = line.split("-")
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, []).append(a)

    def is_small(cave: str) -> bool:
        return cave.islower()

    def can_visit_small(visited: dict[str, int], cave: str) -> bool:
        count = visited.get(cave, 0)
        if count == 0:
            return True
        if count == 1:
            return not any(v == 2 for k, v in visited.items() if k != cave)
        return False

    def count_paths(current: str, visited_small: dict[str, int]) -> int:
        if current == "end":
            return 1
        total = 0
        for neighbor in graph.get(current, []):
            if neighbor == "start":
                continue
            if is_small(neighbor):
                if not can_visit_small(visited_small, neighbor):
                    continue
                new_visited = dict(visited_small)
                new_visited[neighbor] = new_visited.get(neighbor, 0) + 1
            else:
                new_visited = visited_small
            total += count_paths(neighbor, new_visited)
        return total

    return str(count_paths("start", {}))

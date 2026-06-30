def parse_graph(data: str) -> dict[str, dict[str, int]]:
    graph: dict[str, dict[str, int]] = {}
    for line in data.strip().splitlines():
        left, right = line.split(": ")
        node = left
        graph.setdefault(node, {})
        for neighbor in right.split():
            graph.setdefault(neighbor, {})
            graph[node][neighbor] = graph[node].get(neighbor, 0) + 1
            graph[neighbor][node] = graph[neighbor].get(node, 0) + 1
    return graph


def stoer_wagner(graph: dict[str, dict[str, int]]) -> tuple[int, int, int]:
    adj = {v: dict(neighbors) for v, neighbors in graph.items()}
    merged = {v: {v} for v in adj}

    best_weight = float("inf")
    best_sizes = (0, 0)

    while len(adj) > 1:
        visited: set[str] = set()
        weights = {v: 0 for v in adj}
        prev = None
        last = None

        for _ in range(len(adj)):
            sel = max((v for v in adj if v not in visited), key=lambda v: weights[v])
            visited.add(sel)
            for u, w in adj[sel].items():
                if u not in visited:
                    weights[u] += w
            prev, last = last, sel

        assert prev is not None and last is not None
        s, t = prev, last
        cut_weight = weights[t]

        if cut_weight < best_weight:
            best_weight = cut_weight
            side_a = len(merged[t])
            side_b = sum(len(merged[v]) for v in adj if v != t)
            best_sizes = (side_a, side_b)

        merged[s] |= merged[t]
        del merged[t]

        for u, w in list(adj[t].items()):
            if u != s:
                adj[s][u] = adj[s].get(u, 0) + w
                adj[u][s] = adj[u].get(s, 0) + w
                adj[u].pop(t, None)
        adj[s].pop(t, None)
        adj[s].pop(s, None)
        adj.pop(t)

    return int(best_weight), best_sizes[0], best_sizes[1]


def solve(data: str) -> str:
    graph = parse_graph(data)
    _cut_weight, size_a, size_b = stoer_wagner(graph)
    return str(size_a * size_b)

def solve(data: str) -> str:
    adj: dict[str, set[str]] = {}
    for line in data.strip().splitlines():
        a, b = line.strip().split("-")
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    triangles: set[frozenset[str]] = set()
    for u, neighbors in adj.items():
        neighbor_list = list(neighbors)
        for i in range(len(neighbor_list)):
            for j in range(i + 1, len(neighbor_list)):
                v, w = neighbor_list[i], neighbor_list[j]
                if w in adj[v]:
                    triangles.add(frozenset((u, v, w)))

    count = sum(
        1 for triangle in triangles if any(node.startswith("t") for node in triangle)
    )
    return str(count)

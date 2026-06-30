def solve(data: str) -> str:
    adj: dict[str, set[str]] = {}
    for line in data.strip().splitlines():
        a, b = line.strip().split("-")
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    best: set[str] = set()

    def bron_kerbosch(r: set[str], p: set[str], x: set[str]) -> None:
        nonlocal best
        if not p and not x:
            if len(r) > len(best):
                best = set(r)
            return

        pivot = max(p | x, key=lambda u: len(adj[u] & p))
        for v in list(p - adj[pivot]):
            neighbors = adj[v]
            bron_kerbosch(r | {v}, p & neighbors, x & neighbors)
            p.remove(v)
            x.add(v)

    bron_kerbosch(set(), set(adj), set())
    return ",".join(sorted(best))

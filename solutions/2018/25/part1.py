def solve(data: str) -> str:
    points = [tuple(map(int, line.split(","))) for line in data.strip().splitlines() if line.strip()]
    n = len(points)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj

    for i in range(n):
        pi = points[i]
        for j in range(i + 1, n):
            pj = points[j]
            if sum(abs(a - b) for a, b in zip(pi, pj)) <= 3:
                union(i, j)

    return str(len({find(i) for i in range(n)}))

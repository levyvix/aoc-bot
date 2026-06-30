def solve(data: str) -> str:
    blocks = data.strip().split("\n\n")
    seeds = list(map(int, blocks[0].split(":")[1].split()))

    maps = []
    for block in blocks[1:]:
        lines = block.strip().splitlines()
        mapping = []
        for line in lines[1:]:
            dest_start, source_start, length = map(int, line.split())
            mapping.append((dest_start, source_start, length))
        maps.append(mapping)

    def apply_map(value: int, mapping: list[tuple[int, int, int]]) -> int:
        for dest_start, source_start, length in mapping:
            if source_start <= value < source_start + length:
                return dest_start + (value - source_start)
        return value

    min_location = float("inf")
    for seed in seeds:
        value = seed
        for mapping in maps:
            value = apply_map(value, mapping)
        min_location = min(min_location, value)

    return str(int(min_location))

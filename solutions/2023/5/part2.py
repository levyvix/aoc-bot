def parse(data: str) -> tuple[list[tuple[int, int]], list[list[tuple[int, int, int]]]]:
    blocks = data.strip().split("\n\n")
    seed_nums = list(map(int, blocks[0].split(":")[1].split()))
    seed_ranges = [
        (seed_nums[i], seed_nums[i + 1]) for i in range(0, len(seed_nums), 2)
    ]

    maps = []
    for block in blocks[1:]:
        lines = block.strip().splitlines()
        mapping = []
        for line in lines[1:]:
            dest_start, source_start, length = map(int, line.split())
            mapping.append((dest_start, source_start, length))
        maps.append(mapping)

    return seed_ranges, maps


def apply_map(
    ranges: list[tuple[int, int]], mapping: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for dest_start, source_start, length in mapping:
        source_end = source_start + length
        next_ranges: list[tuple[int, int]] = []
        for r_start, r_len in ranges:
            r_end = r_start + r_len
            if r_end <= source_start or r_start >= source_end:
                next_ranges.append((r_start, r_len))
                continue
            if r_start < source_start:
                next_ranges.append((r_start, source_start - r_start))
            overlap_start = max(r_start, source_start)
            overlap_end = min(r_end, source_end)
            out.append((dest_start + (overlap_start - source_start), overlap_end - overlap_start))
            if r_end > source_end:
                next_ranges.append((source_end, r_end - source_end))
        ranges = next_ranges
    out.extend(ranges)
    return out


def solve(data: str) -> str:
    ranges, maps = parse(data)
    for mapping in maps:
        ranges = apply_map(ranges, mapping)
    return str(min(start for start, _ in ranges))

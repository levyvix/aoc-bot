def solve(data: str) -> str:
    unique_lengths = {2, 3, 4, 7}
    count = 0
    for line in data.strip().splitlines():
        _, output = line.split(" | ")
        for signal in output.split():
            if len(signal) in unique_lengths:
                count += 1
    return str(count)

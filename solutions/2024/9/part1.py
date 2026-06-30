def solve(data: str) -> str:
    disk: list[int] = []
    file_id = 0
    is_file = True
    for ch in data.strip():
        length = int(ch)
        if is_file:
            disk.extend([file_id] * length)
            file_id += 1
        else:
            disk.extend([-1] * length)
        is_file = not is_file

    left, right = 0, len(disk) - 1
    while left < right:
        while left < right and disk[left] != -1:
            left += 1
        while left < right and disk[right] == -1:
            right -= 1
        if left < right:
            disk[left] = disk[right]
            disk[right] = -1
            left += 1
            right -= 1

    checksum = sum(i * block for i, block in enumerate(disk) if block != -1)
    return str(checksum)

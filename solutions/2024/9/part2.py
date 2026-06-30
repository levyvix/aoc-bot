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

    files: dict[int, tuple[int, int]] = {}
    i = 0
    while i < len(disk):
        if disk[i] != -1:
            fid = disk[i]
            start = i
            while i < len(disk) and disk[i] == fid:
                i += 1
            files[fid] = (start, i - start)
        else:
            i += 1

    for fid in sorted(files.keys(), reverse=True):
        start, size = files[fid]
        dest = None
        pos = 0
        while pos < start:
            if disk[pos] == -1:
                end = pos
                while end < start and disk[end] == -1:
                    end += 1
                if end - pos >= size:
                    dest = pos
                    break
                pos = end
            else:
                pos += 1

        if dest is not None:
            for j in range(size):
                disk[dest + j] = fid
                disk[start + j] = -1

    checksum = sum(i * block for i, block in enumerate(disk) if block != -1)
    return str(checksum)

def hash_string(s: str) -> int:
    value = 0
    for ch in s:
        value = (value + ord(ch)) * 17 % 256
    return value


def solve(data: str) -> str:
    boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]

    for step in data.replace("\n", "").split(","):
        if not step:
            continue
        if step.endswith("-"):
            label = step[:-1]
            box = hash_string(label)
            boxes[box] = [(l, f) for l, f in boxes[box] if l != label]
        else:
            label, focal = step.split("=")
            focal_length = int(focal)
            box = hash_string(label)
            lenses = boxes[box]
            for i, (l, _) in enumerate(lenses):
                if l == label:
                    lenses[i] = (label, focal_length)
                    break
            else:
                lenses.append((label, focal_length))

    total = 0
    for box_num, lenses in enumerate(boxes):
        for slot, (_, focal) in enumerate(lenses, start=1):
            total += (box_num + 1) * slot * focal

    return str(total)

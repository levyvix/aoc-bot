def solve(data: str) -> str:
    lines = data.strip().splitlines()
    dots: set[tuple[int, int]] = set()
    folds: list[tuple[str, int]] = []

    for line in lines:
        if not line:
            continue
        if line.startswith("fold along"):
            axis, value = line.removeprefix("fold along ").split("=")
            folds.append((axis, int(value)))
        else:
            x, y = map(int, line.split(","))
            dots.add((x, y))

    axis, value = folds[0]
    new_dots: set[tuple[int, int]] = set()
    for x, y in dots:
        if axis == "x":
            if x > value:
                x = 2 * value - x
        else:
            if y > value:
                y = 2 * value - y
        new_dots.add((x, y))

    return str(len(new_dots))

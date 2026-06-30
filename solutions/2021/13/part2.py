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

    for axis, value in folds:
        new_dots: set[tuple[int, int]] = set()
        for x, y in dots:
            if axis == "x":
                if x > value:
                    x = 2 * value - x
            else:
                if y > value:
                    y = 2 * value - y
            new_dots.add((x, y))
        dots = new_dots

    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)

    rows: list[str] = []
    for y in range(max_y + 1):
        rows.append("".join("#" if (x, y) in dots else " " for x in range(max_x + 1)))
    while rows and not rows[-1].strip():
        rows.pop()

    font: dict[str, list[str]] = {
        "A": [" ## ", "#  #", "#  #", "####", "#  #", "#  #"],
        "B": ["### ", "#  #", "### ", "#  #", "#  #", "### "],
        "C": [" ## ", "#  #", "#   ", "#   ", "#  #", " ###"],
        "D": ["### ", "#  #", "#  #", "#  #", "#  #", "### "],
        "E": ["####", "#   ", "### ", "#   ", "#   ", "####"],
        "F": ["####", "#   ", "### ", "#   ", "#   ", "#   "],
        "G": [" ## ", "#  #", "#   ", "# ##", "#  #", " ###"],
        "H": ["#  #", "#  #", "####", "#  #", "#  #", "#  #"],
        "I": [" ###", "  # ", "  # ", "  # ", "  # ", " ###"],
        "J": ["  ##", "   #", "   #", "   #", "#  #", " ## "],
        "K": ["#  #", "# # ", "##  ", "# # ", "#  #", "#  #"],
        "L": ["#   ", "#   ", "#   ", "#   ", "#   ", "####"],
        "M": ["#  #", "####", "#  #", "#  #", "#  #", "#  #"],
        "N": ["#  #", "### ", "# # ", "#  #", "#  #", "#  #"],
        "O": [" ###", "#  #", "#  #", "#  #", "#  #", " ###"],
        "P": ["### ", "#  #", "#  #", "### ", "#   ", "#   "],
        "Q": [" ###", "#  #", "#  #", "# ##", "#  #", " ## "],
        "R": ["### ", "#  #", "#  #", "### ", "# # ", "#  #"],
        "S": [" ####", "#    ", " ### ", "    #", "    #", "#### "],
        "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
        "U": ["#  #", "#  #", "#  #", "#  #", "#  #", " ## "],
        "V": ["#  #", "#  #", "#  #", "#  #", " # #", "  # "],
        "W": ["#  #", "#  #", "#  #", "# # ", "## #", "#  #"],
        "X": ["#  #", "#  #", " ## ", " ## ", "#  #", "#  #"],
        "Y": ["#  #", "#  #", " # #", "  #  ", "  #  ", "  #  "],
        "Z": ["####", "   #", "  # ", " #  ", "#   ", "####"],
    }

    gap_cols = [
        x
        for x in range(len(rows[0]))
        if all(x >= len(row) or row[x] == " " for row in rows)
    ]
    starts = [0]
    for col in gap_cols:
        if col > starts[-1]:
            starts.append(col + 1)
    starts = [s for s in starts if s < len(rows[0])]

    letters: list[str] = []
    for i, start in enumerate(starts):
        end = gap_cols[i] if i < len(gap_cols) else len(rows[0])
        block = [row[start:end] for row in rows]
        best = min(
            font,
            key=lambda ch: sum(a != b for a, b in zip(block, font[ch])),
        )
        letters.append(best)

    return "".join(letters)

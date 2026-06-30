def solve(data: str) -> str:
    return _solve_monad(data, find_max=True)


def _parse_blocks(data: str) -> list[tuple[int, int, int]]:
    blocks = []
    lines = data.strip().splitlines()
    for i in range(0, len(lines), 18):
        block = lines[i : i + 18]
        div = int(block[4].split()[2])
        add_x = int(block[5].split()[2])
        add_y = int(block[15].split()[2])
        blocks.append((div, add_x, add_y))
    return blocks


def _step(z: int, w: int, div: int, cx: int, cy: int) -> int:
    r = z % 26
    z = z // div
    if w == r + cx:
        return z
    return z * 26 + w + cy


def _prev_z_in(z_out: int, w: int, div: int, cx: int, cy: int) -> list[int]:
    out: list[int] = []

    if div == 26:
        r = w - cx
        if 0 <= r < 26:
            z_in = z_out * 26 + r
            if _step(z_in, w, div, cx, cy) == z_out:
                out.append(z_in)
    elif div == 1 and z_out % 26 + cx == w:
        if _step(z_out, w, div, cx, cy) == z_out:
            out.append(z_out)

    zm = z_out - w - cy
    if zm >= 0 and zm % 26 == 0:
        m = zm // 26
        if div == 1:
            z_in = m
            if _step(z_in, w, div, cx, cy) == z_out:
                out.append(z_in)
        else:
            for r in range(26):
                if w == r + cx:
                    continue
                z_in = m * 26 + r
                if z_in // 26 == m and _step(z_in, w, div, cx, cy) == z_out:
                    out.append(z_in)

    return out


def _solve_monad(data: str, *, find_max: bool) -> str:
    blocks = _parse_blocks(data)
    digits = range(9, 0, -1) if find_max else range(1, 10)
    states: dict[int, str] = {0: ""}

    for i in range(len(blocks) - 1, -1, -1):
        div, cx, cy = blocks[i]
        new_states: dict[int, str] = {}
        for z_out, suffix in states.items():
            for w in digits:
                for z_in in _prev_z_in(z_out, w, div, cx, cy):
                    candidate = str(w) + suffix
                    if z_in not in new_states:
                        new_states[z_in] = candidate
                    elif find_max and candidate > new_states[z_in]:
                        new_states[z_in] = candidate
                    elif not find_max and candidate < new_states[z_in]:
                        new_states[z_in] = candidate
        states = new_states

    return states[0]

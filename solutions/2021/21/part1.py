from __future__ import annotations


def solve(data: str) -> str:
    lines = data.strip().splitlines()
    pos = [int(line.rsplit(":", 1)[-1].strip()) for line in lines[:2]]
    scores = [0, 0]
    die = 1
    rolls = 0
    player = 0

    while scores[0] < 1000 and scores[1] < 1000:
        move = 0
        for _ in range(3):
            move += die
            die = 1 if die == 100 else die + 1
            rolls += 1

        pos[player] = (pos[player] - 1 + move) % 10 + 1
        scores[player] += pos[player]
        player ^= 1

    loser = scores[1] if scores[0] >= 1000 else scores[0]
    return str(loser * rolls)

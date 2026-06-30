from __future__ import annotations

from functools import lru_cache

ROLL_COUNTS = {s: 0 for s in range(3, 10)}
for a in (1, 2, 3):
    for b in (1, 2, 3):
        for c in (1, 2, 3):
            ROLL_COUNTS[a + b + c] += 1


def solve(data: str) -> str:
    lines = data.strip().splitlines()
    start = tuple(int(line.rsplit(":", 1)[-1].strip()) for line in lines[:2])

    @lru_cache(maxsize=None)
    def play(pos1: int, pos2: int, score1: int, score2: int, player: int) -> tuple[int, int]:
        if score1 >= 21:
            return (1, 0)
        if score2 >= 21:
            return (0, 1)

        wins1 = wins2 = 0
        pos = pos1 if player == 0 else pos2
        score = score1 if player == 0 else score2

        for move, count in ROLL_COUNTS.items():
            new_pos = (pos - 1 + move) % 10 + 1
            new_score = score + new_pos
            if new_score >= 21:
                if player == 0:
                    wins1 += count
                else:
                    wins2 += count
            else:
                if player == 0:
                    w1, w2 = play(new_pos, pos2, new_score, score2, 1)
                else:
                    w1, w2 = play(pos1, new_pos, score1, new_score, 0)
                wins1 += count * w1
                wins2 += count * w2

        return (wins1, wins2)

    p1_wins, p2_wins = play(start[0], start[1], 0, 0, 0)
    return str(max(p1_wins, p2_wins))

def solve(data: str) -> str:
    opp = {"A": 0, "B": 1, "C": 2}
    mine = {"X": 0, "Y": 1, "Z": 2}
    shape_score = [1, 2, 3]
    outcome_score = {
        (0, 0): 3,
        (1, 1): 3,
        (2, 2): 3,
        (0, 2): 6,
        (2, 1): 6,
        (1, 0): 6,
        (2, 0): 0,
        (1, 2): 0,
        (0, 1): 0,
    }
    total = 0
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        o, m = line.split()
        m_val = mine[m]
        o_val = opp[o]
        total += shape_score[m_val] + outcome_score[(m_val, o_val)]
    return str(total)

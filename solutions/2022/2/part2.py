def solve(data: str) -> str:
    opp = {"A": 0, "B": 1, "C": 2}
    outcome_score = {"X": 0, "Y": 3, "Z": 6}
    shape_score = [1, 2, 3]
    total = 0
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        o, desired = line.split()
        o_val = opp[o]
        if desired == "Y":
            m_val = o_val
        elif desired == "Z":
            m_val = (o_val + 1) % 3
        else:
            m_val = (o_val + 2) % 3
        total += shape_score[m_val] + outcome_score[desired]
    return str(total)

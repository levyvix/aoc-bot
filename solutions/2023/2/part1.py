def solve(data: str) -> str:
    limits = {"red": 12, "green": 13, "blue": 14}
    total = 0
    for line in data.splitlines():
        if not line:
            continue
        game_id, reveals = line.split(": ", 1)
        game_num = int(game_id.split()[1])
        possible = True
        for reveal in reveals.split("; "):
            for part in reveal.split(", "):
                count, color = part.split()
                if int(count) > limits[color]:
                    possible = False
                    break
            if not possible:
                break
        if possible:
            total += game_num
    return str(total)

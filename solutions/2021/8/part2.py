def solve(data: str) -> str:
    total = 0
    for line in data.strip().splitlines():
        patterns, output = line.split(" | ")
        signals = [frozenset(p) for p in patterns.split()]
        one = next(s for s in signals if len(s) == 2)
        four = next(s for s in signals if len(s) == 4)
        seven = next(s for s in signals if len(s) == 3)
        eight = next(s for s in signals if len(s) == 7)
        nine = next(s for s in signals if len(s) == 6 and four.issubset(s))
        three = next(s for s in signals if len(s) == 5 and seven.issubset(s))
        five = next(
            s
            for s in signals
            if len(s) == 5 and len(s & one) == 1 and len(s & four) == 3
        )
        two = next(s for s in signals if len(s) == 5 and s not in (three, five))
        six = next(
            s for s in signals if len(s) == 6 and s is not nine and len(s & one) == 1
        )
        zero = next(s for s in signals if len(s) == 6 and s not in (nine, six))

        digit_map = {
            zero: 0,
            one: 1,
            two: 2,
            three: 3,
            four: 4,
            five: 5,
            six: 6,
            seven: 7,
            eight: 8,
            nine: 9,
        }

        value = 0
        for signal in output.split():
            value = value * 10 + digit_map[frozenset(signal)]
        total += value

    return str(total)

CARD_VALUE = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}

TYPE_SCORE = {
    (5,): 6,
    (4, 1): 5,
    (3, 2): 4,
    (3, 1, 1): 3,
    (2, 2, 1): 2,
    (2, 1, 1, 1): 1,
    (1, 1, 1, 1, 1): 0,
}


def hand_key(cards: str) -> tuple:
    jokers = cards.count("J")
    counts: dict[str, int] = {}
    for card in cards:
        if card != "J":
            counts[card] = counts.get(card, 0) + 1

    if not counts:
        type_score = TYPE_SCORE[(5,)]
    else:
        freqs = sorted(counts.values(), reverse=True)
        freqs[0] += jokers
        freqs = sorted(freqs, reverse=True)
        type_score = TYPE_SCORE[tuple(freqs)]

    card_scores = tuple(CARD_VALUE[c] for c in cards)
    return (type_score, card_scores)


def solve(data: str) -> str:
    hands = []
    for line in data.strip().splitlines():
        cards, bid = line.split()
        hands.append((hand_key(cards), int(bid)))

    hands.sort(key=lambda item: item[0])

    total = 0
    for rank, (_, bid) in enumerate(hands, start=1):
        total += rank * bid

    return str(total)

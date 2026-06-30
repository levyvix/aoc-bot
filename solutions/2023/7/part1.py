CARD_VALUE = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
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
    counts = sorted(
        [cards.count(c) for c in set(cards)],
        reverse=True,
    )
    type_score = TYPE_SCORE[tuple(counts)]
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

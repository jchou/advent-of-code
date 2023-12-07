from collections import Counter
from pathlib import Path


# Each of these MUST be defined in order from lowest to highest value
CARD_VALUES = {label: value for value, label in enumerate("23456789TJQKA")}
CARD_VALUES_WITH_WILD_JOKER = {label: value for value, label in enumerate("J23456789TQKA")}
TYPE_VALUES = {label: value for value, label in enumerate([
    "HIGH_CARD",
    "ONE_PAIR",
    "TWO_PAIR",
    "THREE_OF_A_KIND",
    "FULL_HOUSE",
    "FOUR_OF_A_KIND",
    "FIVE_OF_A_KIND",
])}


def get_hand_type(hand: str) -> int:
    cards_by_count = Counter(hand).most_common()
    if cards_by_count[0][1] == 5:
        return TYPE_VALUES["FIVE_OF_A_KIND"]
    elif cards_by_count[0][1] == 4:
        return TYPE_VALUES["FOUR_OF_A_KIND"]
    elif cards_by_count[0][1] == 3:
        if cards_by_count[1][1] == 2:
            return TYPE_VALUES["FULL_HOUSE"]
        else:
            return TYPE_VALUES["THREE_OF_A_KIND"]
    elif cards_by_count[0][1] == 2:
        if cards_by_count[1][1] == 2:
            return TYPE_VALUES["TWO_PAIR"]
        else:
            return TYPE_VALUES["ONE_PAIR"]
    else:
        return TYPE_VALUES["HIGH_CARD"]


def get_hand_value(hand: str, is_joker_wild=False) -> tuple:
    highest_hand_type = get_hand_type(hand)
    if is_joker_wild is True:
        i = 0
        hands = [hand]
        hands_seen = {hand}
        while i < len(hands):
            alt_hand = hands[i]
            for j, card in enumerate(alt_hand):
                if card == "J":
                    for label in "23456789TQKA":
                        new_hand = alt_hand[:j] + label + alt_hand[j + 1:]
                        if new_hand not in hands_seen:
                            highest_hand_type = max(highest_hand_type, get_hand_type(new_hand))
                            hands_seen.add(new_hand)
                            hands.append(new_hand)
            i += 1

    if is_joker_wild is True:
        return (highest_hand_type,) + tuple(CARD_VALUES_WITH_WILD_JOKER[card] for card in hand)
    else:
        return (highest_hand_type,) + tuple(CARD_VALUES[card] for card in hand)


def part1(hands_and_bids: str, is_joker_wild=False) -> int:
    scores_and_bids = []
    for hand_and_bid in hands_and_bids.splitlines():
        hand, bid = hand_and_bid.split()
        scores_and_bids.append((get_hand_value(hand, is_joker_wild=is_joker_wild), int(bid)))
    scores_and_bids.sort()
    return sum(bid * (i + 1) for i, (_, bid) in enumerate(scores_and_bids))


def part2(hands_and_bids: str) -> int:
    return part1(hands_and_bids, is_joker_wild=True)


if __name__ == '__main__':
    input_text = Path("../inputs/7.txt").read_text()
    print(part1(input_text))
    print(part2(input_text))

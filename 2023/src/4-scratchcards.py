from pathlib import Path

input_text = Path("../inputs/4.txt").read_text()
lines = input_text.splitlines()


def part1():
    total = 0
    for line in lines:
        _, all_numbers = line.split(": ")
        winning_numbers, numbers = line.split(" | ")
        num_winners = len(set(winning_numbers.split()).intersection(set(numbers.split())))
        total += 2 ** (num_winners - 1) if num_winners > 0 else 0
    return total


def part2():
    i = 0
    global lines
    card_scores = {}
    card_count = {}
    for line in lines:
        card, all_numbers = line.split(": ")
        card_number = int(card.split()[1])
        winning_numbers, numbers = line.split(" | ")
        card_scores[card_number] = len(set(winning_numbers.split()).intersection(set(numbers.split())))
        card_count[card_number] = 1

    while i < len(card_count):
        new_cards = card_scores[i+1]
        for j in range(new_cards):
            card_count[i+2+j] += 1 * card_count[i+1]
        i += 1

    return sum(card_count.values())


if __name__ == '__main__':
    print(part1())
    print(part2())

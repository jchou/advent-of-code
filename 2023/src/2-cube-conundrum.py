import math
from pathlib import Path

input_text = Path("../inputs/2.txt").read_text()


def part1():
    max_rgb = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    total = 0
    for line in input_text.splitlines():
        # print(line)
        game, sets = line.split(": ")
        game_id = game.split()[1]
        for s in sets.split("; "):
            for t in s.split(", "):
                number, color = t.split()
                if int(number) > max_rgb[color]:
                    # print(f"Game {game_id} is not possible: {color} is {number} > {max_rgb[color]}")
                    break
            else:
                continue
            break
        else:
            total += int(game_id)
            # print(f"Game {game_id} is possible: {total}")

    print(total)


def part2():
    total = 0
    for line in input_text.splitlines():
        # print(line)
        game, sets = line.split(": ")
        rgb = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for s in sets.split("; "):
            for t in s.split(", "):
                number, color = t.split()
                rgb[color] = max(rgb[color], int(number))
        total += math.prod(rgb.values())

    print(total)


if __name__ == '__main__':
    part1()
    part2()

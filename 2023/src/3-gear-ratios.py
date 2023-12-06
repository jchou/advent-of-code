import collections
import math
from pathlib import Path

input_text = Path("../inputs/3.txt").read_text()
lines = input_text.splitlines()
width = len(lines[0])
height = len(lines)


def part1():
    def is_valid(start, end, line_number):
        for y in range(line_number - 1, line_number + 2):
            l = ""
            for x in range(start - 1, end + 2):
                if y < 0 or y >= height:
                    l += "X"
                    continue
                if x < 0 or x >= width:
                    l += "X"
                    continue
                if y == line_number and start <= x <= end:
                    l += lines[y][x]
                    continue
                l += lines[y][x]
                if lines[y][x] != ".":
                    # print(l)
                    return True
            # print(l)
        # print()
        return False

    total = 0
    for line_number, line in enumerate(lines):
        start = None
        for i in range(width):
            if line[i].isdigit():
                if start is None:
                    start = i
                elif i == width - 1:
                    end = i
                    number = int(line[start:end + 1])
                    if is_valid(start, end, line_number):
                        total += number
                        # print(number)
                    start = None
            elif start is not None:
                end = i - 1
                number = int(line[start:end + 1])
                if is_valid(start, end, line_number):
                    total += number
                    # print("FOUND: " + str(number))
                    # print()
                start = None
    print(total)


def part2():
    def collect_gears(start, end, line_number):
        for y in range(line_number - 1, line_number + 2):
            l = ""
            for x in range(start - 1, end + 2):
                if y < 0 or y >= height:
                    l += "X"
                    continue
                if x < 0 or x >= width:
                    l += "X"
                    continue
                if y == line_number and start <= x <= end:
                    l += lines[y][x]
                    continue
                l += lines[y][x]
                if lines[y][x] == "*":
                    gear_symbols[(x, y)].add((line_number, start, end))
                    # print(f"Adding ({line_number}, {start}, {end}) {lines[line_number][start:end+1]} to {(x, y)} {lines[y][x]}")
            # print(l)
        # print()

    gear_symbols = collections.defaultdict(set)
    total = 0
    for line_number, line in enumerate(lines):
        if line_number - 1 >= 0:
            # print(lines[line_number - 1])
            pass
        # print(line)
        if line_number + 1 < height:
            # print(lines[line_number + 1])
            pass
        start = None
        for i in range(width):
            if line[i].isdigit():
                if start is None:
                    start = i
                elif i == width - 1:
                    end = i
                    collect_gears(start, end, line_number)
                    start = None
            elif start is not None:
                end = i - 1
                collect_gears(start, end, line_number)
                start = None

    # print(gear_symbols)
    for coords in [s for s in gear_symbols.values() if len(s) == 2]:
        # print([int(lines[line][x:y+1]) for (line, x, y) in coords])
        total += math.prod(int(lines[line][x:y+1]) for (line, x, y) in coords)
        # print(coords)

    print(total)


if __name__ == '__main__':
    part1()
    part2()

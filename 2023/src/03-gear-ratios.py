"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""

import collections
import math
from pathlib import Path

input_text = Path("../inputs/03.txt").read_text()
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
            line = ""
            for x in range(start - 1, end + 2):
                if y < 0 or y >= height:
                    line += "X"
                    continue
                if x < 0 or x >= width:
                    line += "X"
                    continue
                if y == line_number and start <= x <= end:
                    line += lines[y][x]
                    continue
                line += lines[y][x]
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
        total += math.prod(int(lines[line][x:y + 1]) for (line, x, y) in coords)
        # print(coords)

    print(total)


if __name__ == '__main__':
    part1()
    part2()

import copy
from pathlib import Path

"""
--- Day 13: Point of Incidence ---
With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:

123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789
In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7
This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.

Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?
"""


def get_reflection_summary(island: list[str]) -> list[int]:
    reflections = []
    # print(" \t", end="")
    # for i in range(len(island[0])):
    #     print(f"{i % 10}", end="")
    # print()
    # for i, isle in enumerate(island):
    #     print(f"{i}\t{isle}")

    # Check for horizontal reflection
    for i in range(1, len(island)):
        if island[i - 1] == island[i]:
            steps = 1
            while True:
                if i + steps > len(island) - 1 or i - 1 - steps < 0:
                    # print(f"Horizontal reflection at {i} (+{100 * i})")
                    reflections.append(100 * i)
                    break

                if island[i - 1 - steps] != island[i + steps]:
                    break

                steps += 1

    # Check for vertical reflection
    for x in range(1, len(island[0])):
        column_is_reflection = True
        for y in range(len(island)):
            if island[y][x - 1] != island[y][x]:
                column_is_reflection = False
                break

        steps = 1
        while column_is_reflection:
            if x + steps > len(island[0]) - 1 or x - 1 - steps < 0:
                # print(f""" \t{" " * (x - 1)}><""")
                # print(f"Vertical reflection at {x} (+{x})")
                reflections.append(x)
                break

            for y in range(len(island)):
                if island[y][x - 1 - steps] != island[y][x + steps]:
                    column_is_reflection = False
                    break

            steps += 1

    return reflections


def part1(islands: list[str]) -> int:
    total = 0
    for island in islands:
        total += get_reflection_summary(island.splitlines())[0]

    return total


def part2(islands: list[str]) -> int:
    total = 0
    for island in islands:
        smudged_island = island.splitlines()
        smudged_result = get_reflection_summary(smudged_island)[0]
        # print(f"Smudged result: {smudged_result}\n")
        fixed_island = copy.deepcopy(smudged_island)
        found = False
        for y in range(len(fixed_island)):
            if found is True:
                break

            for x in range(len(smudged_island[0])):
                original_row = fixed_island[y]
                replacement = "." if smudged_island[y][x] == "#" else "#"
                fixed_island[y] = smudged_island[y][:x] + replacement + smudged_island[y][x + 1:]
                results = get_reflection_summary(fixed_island)
                fixed_island[y] = original_row
                if smudged_result in results:
                    results.remove(smudged_result)
                if len(results) > 0:
                    found = True
                    total += results[0]
                    # print(f"New result: {results[0]}\n")
                    break

    return total


if __name__ == '__main__':
    lines = Path("../inputs/13.txt").read_text().split("\n\n")
    print(part1(lines))
    print(part2(lines))

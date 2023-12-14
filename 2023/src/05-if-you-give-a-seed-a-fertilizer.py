"""
--- Day 5: If You Give A Seed A Fertilizer ---
You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
"""

import math
from pathlib import Path


def part1(seeds, maps):
    min_location = math.inf
    for value in seeds:
        # print(f"seed: {value}")
        for mappings in maps:
            # print(f"mappings: {list(mappings)}")
            for mapping in mappings:
                old_value = value
                value = src_to_dst(value, mapping)
                # print(f"\t{old_value} -> {value}")
                if value != old_value:
                    break
        min_location = min(min_location, value)
        # print(f"min_location: {min_location}")
    return min_location


def src_to_dst(value: int, mapping_entry: tuple[int, int, int]):
    delta = value - mapping_entry[1]
    if 0 <= delta < mapping_entry[2]:
        return mapping_entry[0] + delta
    else:
        return value


def part2(ranges, levels):
    for level in levels:
        # print(f"level: {list(level)}")
        next_level_ranges = []
        i = 0
        while i < len(ranges):
            lo, hi = ranges[i]
            # print(f"\trange: {lo}-{hi}")
            match_found = False
            for dst_lo, src_lo, range_length in level:
                src_hi = src_lo + range_length - 1
                dst_hi = dst_lo + range_length - 1
                # print(f"\t\t{src_lo}-{src_hi} -> {dst_lo}-{dst_hi}")

                # range not contained in mapping at all
                if src_hi < lo or src_lo > hi:
                    # print(f"\t\t{lo}-{hi} not in {src_lo}-{src_hi} at all")
                    continue
                # range fully contained in mapping
                if src_lo <= lo and src_hi >= hi:
                    dst_start = dst_lo + (lo - src_lo)
                    next_level_ranges.append((dst_start, dst_start + (hi - lo)))
                    match_found = True
                    # print(f"\t\t{lo}-{hi} fully contained in {src_lo}-{src_hi}")
                    # print(f"\t\t\tO: {dst_start}-{dst_start + (hi - lo)}")
                    break
                # range extends below and above mapping
                elif src_lo > lo and src_hi < hi:
                    ranges.append((lo, src_lo - 1))
                    next_level_ranges.append((dst_lo, dst_hi))
                    ranges.append((src_hi + 1, hi))
                    match_found = True
                    # print(f"\t\t{lo}-{hi} bigger than {src_lo}-{src_hi}")
                    # print(f"\t\t\tX: {lo}-{src_lo}")
                    # print(f"\t\t\tO: {dst_lo}-{dst_hi}")
                    # print(f"\t\t\tX: {src_hi + 1}-{hi}")
                    break
                # range extends below mapping
                elif src_lo > lo:
                    ranges.append((lo, src_lo - 1))
                    next_level_ranges.append((dst_lo, dst_lo + (hi - src_lo)))
                    match_found = True
                    # print(f"\t\t{lo}-{hi} extends below {src_lo}-{src_hi}")
                    # print(f"\t\t\tX: {lo}-{src_lo - 1}")
                    # print(f"\t\t\tO: {dst_lo}-{dst_lo + (hi - src_lo)}")
                    break
                # range extends above mapping
                elif src_hi < hi:
                    dst_start = dst_lo + (lo - src_lo)
                    next_level_ranges.append((dst_start, dst_start + (src_hi - lo)))
                    ranges.append((src_hi + 1, hi))
                    match_found = True
                    # print(f"\t\t{lo}-{hi} extends above {src_lo}-{src_hi}")
                    # print(f"\t\t\tO: {dst_start}-{dst_start + (src_hi - lo)}")
                    # print(f"\t\t\tX: {src_hi + 1}-{hi}")
                    break

            # if no match found, add the identity range for the next level
            if match_found is False:
                # print(f"\tO: IDENTITY {lo}-{hi}")
                next_level_ranges.append((lo, hi))

            # move on to the next range
            i += 1

        # move on to the next level
        ranges = next_level_ranges

    # print(f"ranges: {ranges}")
    return min(lo for lo, _ in ranges)


if __name__ == '__main__':
    input_text = Path("inputs/05.txt").read_text()
    sections = input_text.split("\n\n")
    seeds = tuple(map(int, sections[0].split(": ")[1].split()))
    maps = []
    for section in sections[1:]:
        map_entries = section.splitlines()[1:]
        maps.append(tuple(tuple(map(int, entry.split())) for entry in map_entries))

    print(part1(seeds, maps))

    seed_ranges = list((seeds[i * 2], seeds[i * 2] + seeds[(i * 2) + 1]) for i in range(len(seeds) // 2))
    # print(seed_ranges)
    print(part2(seed_ranges, maps))

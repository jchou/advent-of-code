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
    input_text = Path("inputs/5.txt").read_text()
    sections = input_text.split("\n\n")
    seeds = tuple(map(int, sections[0].split(": ")[1].split()))
    maps = []
    for section in sections[1:]:
        map_entries = section.splitlines()[1:]
        maps.append(tuple(tuple(map(int, entry.split())) for entry in map_entries))

    print(part1(seeds, maps))

    seed_ranges = list((seeds[i*2], seeds[i*2] + seeds[(i*2)+1]) for i in range(len(seeds) // 2))
    # print(seed_ranges)
    print(part2(seed_ranges, maps))

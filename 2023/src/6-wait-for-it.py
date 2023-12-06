from pathlib import Path


def part1(times, distances):
    total = 1
    times = [int(t) for t in times]
    distances = [int(d) for d in distances]
    for t, d in zip(times, distances):
        num_victories = 0
        for n in range(1, t):
            distance = n * (t - n)
            if distance > d:
                num_victories += 1
        # print(f"num_victories: {num_victories}")
        total *= num_victories
    return total


def part2(time, distance):
    return part1([time], [distance])


if __name__ == '__main__':
    input_text = Path("../inputs/6.txt").read_text()
    print(part1(*[t.split()[1:] for t in input_text.splitlines()]))

    time_limit, record_distance = input_text.splitlines()
    print(part2("".join(time_limit.split()[1:]), "".join(record_distance.split()[1:])))

from bisect import bisect


def get_nums_in_str(line):
    return line.strip().split()[1:]


def read_input_part1(file):
    with open(file, 'r') as f:
        race_times = map(int, get_nums_in_str(f.readline()))
        race_dists = map(int, get_nums_in_str(f.readline()))
        for race_time, race_dist in zip(race_times, race_dists):
            yield race_time, race_dist


def read_input_part2(file):
    with open(file, 'r') as f:
        race_time = int("".join(get_nums_in_str(f.readline())))
        race_dist = int("".join(get_nums_in_str(f.readline())))
        return race_time, race_dist


def get_ways_count(race_time, race_dist):
    max_hold_time = race_time // 2
    thr = bisect(range(1, max_hold_time + 1),
                 race_dist,
                 key=lambda hold_time: (race_time - hold_time) * hold_time
                 )
    ways = (max_hold_time - thr) * 2
    if race_time % 2 == 0:
        ways -= 1
    return ways


def part1(file):
    races = read_input_part1(file)
    res = 1
    for race_time, race_dist in races:
        ways = get_ways_count(race_time, race_dist)
        res *= ways
    print(f"Part 1: {res}")


def part2(file):
    race_time, race_dist = read_input_part2(file)
    ways = get_ways_count(race_time, race_dist)
    print(f"Part 2: {ways}")


file = "input.in"
part1(file)
part2(file)

from statistics import median


def read_input():
    file = open('input.in', 'r')
    crabs = list(map(int, file.readline().split(",")))
    return crabs


def calc_tri_number(idx):
    return idx * (idx + 1) / 2


def calc_total_fuel_2(x, crabs):
    return int(sum([calc_tri_number(abs(crab - x)) for crab in crabs]))


def part1():
    crabs = read_input()
    ideal_line = median(crabs)
    total_fuel = int(sum([abs(crab - ideal_line) for crab in crabs]))
    print(f"Part 1: {total_fuel}")


def part2():
    crabs = read_input()
    lowest_crab = min(crabs)
    highest_crab = max(crabs)
    min_fuel = min([calc_total_fuel_2(x, crabs) for x in range(lowest_crab, highest_crab)])
    print(f"Part 2: {min_fuel}")


if __name__ == "__main__":
    part1()
    part2()

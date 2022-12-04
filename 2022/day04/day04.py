def read_input():
    with open("input.in", "r") as f:
        lines = [[tuple(map(int, a.split('-'))) for a in line.strip().split(',')] for line in f.readlines()]
    return lines


def part1():
    pairs = read_input()
    total = 0
    for r1, r2 in pairs:
        if r1[0] > r2[0] or (r1[0] == r2[0] and r1[1] < r2[1]):
            r1, r2 = r2, r1
        if r1[0] <= r2[0] and r1[1] >= r2[1]:
            total += 1
    print(f"Part 1: {total}")


def part2():
    pairs = read_input()
    total = 0
    for r1, r2 in pairs:
        if r1[0] > r2[0]:
            r1, r2 = r2, r1
        if r1[1] >= r2[0]:
            total += 1
    print(f"Part 2: {total}")


part1()
part2()

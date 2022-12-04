def read_input():
    with open("input.in", "r") as f:
        rucksacks = [line.strip() for line in f.readlines()]
    return rucksacks


def item2priority(item):
    if item.islower():
        return ord(item) - 96
    else:
        return ord(item) - 38


def part1():
    rucksacks = read_input()
    rucksacks = [(set(rucksack[:len(rucksack) // 2]), set(rucksack[len(rucksack) // 2:])) for rucksack in rucksacks]
    total_priority = 0
    for rucksack in rucksacks:
        (common_item,) = rucksack[0] & rucksack[1]
        total_priority += item2priority(common_item)
    print(f"Part 1: {total_priority}")


def part2():
    rucksacks = [set(rucksack) for rucksack in read_input()]
    total_priority = 0
    for i in range(0, len(rucksacks), 3):
        (badge,) = rucksacks[i] & rucksacks[i + 1] & rucksacks[i + 2]
        total_priority += item2priority(badge)
    print(f"Part 2: {total_priority}")


part1()
part2()

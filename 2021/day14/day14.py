from collections import defaultdict


def read_input():
    with open("input.in", "r") as file:
        line = file.readline().strip()
        file.readline()
        rules = {rule[0]: rule[1] for rule in [line.strip().split(" -> ") for line in file.readlines()]}
    template = defaultdict(int)
    for i in range(len(line) - 1):
        template[line[i:i+2]] += 1
    return template, rules


def insert_once(template, rules):
    pairs = [(key, value) for key, value in template.items() if value != 0]
    for pair, value in pairs:
        template[pair] -= value
        element = rules[pair]
        template[pair[0] + element] += value
        template[element + pair[1]] += value


def insert_n(template, rules, n):
    for i in range(n):
        insert_once(template, rules)


def get_most_least_common_element(template):
    element_counts = defaultdict(int)
    for pair, value in template.items():
        element_counts[pair[0]] += value
        element_counts[pair[1]] += value
    for element, count in element_counts.items():
        element_counts[element] = -(count // -2)  # Ceiling division by 2
    counts = element_counts.values()
    return max(counts), min(counts)


def part1():
    template, rules = read_input()
    insert_n(template, rules, 10)
    most_common_count, least_common_count = get_most_least_common_element(template)
    print(f"Part 1: {most_common_count - least_common_count}")


def part2():
    template, rules = read_input()
    insert_n(template, rules, 40)
    most_common_count, least_common_count = get_most_least_common_element(template)
    print(f"Part 2: {most_common_count - least_common_count}")


if __name__ == "__main__":
    part1()
    part2()

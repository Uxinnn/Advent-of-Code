from collections import defaultdict


def read_input(file):
    with open(file, 'r') as f:
        for line in f:
            split_line = line.strip().split(':', 1)
            card_id = int(split_line[0].split()[1].strip())
            raw_nums_line = split_line[1].split('|', 1)
            winning_nums_str = raw_nums_line[0].strip().split()
            winning_nums = set(int(num) for num in winning_nums_str)
            candidate_nums_str = raw_nums_line[1].strip().split()
            candidate_nums = set(int(num) for num in candidate_nums_str)
            yield [card_id, winning_nums, candidate_nums]


def part1(file):
    tot_points = 0
    for card_id, winning_nums, candidate_nums in read_input(file):
        match_count = len(winning_nums & candidate_nums)
        if match_count:
            tot_points += 2 ** (match_count - 1)
    print(f"Part 1: {tot_points}")


def part2(file):
    card_counts = defaultdict(lambda: 1)
    for card_id, winning_nums, candidate_nums in read_input(file):
        match_count = len(winning_nums & candidate_nums)
        card_count = card_counts[card_id]
        for delta in range(1, match_count + 1):
            card_counts[card_id + delta] += card_count
    tot_card_count = sum(card_counts.values())
    print(f"Part 2: {tot_card_count}")


file = "input.in"
part1(file)
part2(file)

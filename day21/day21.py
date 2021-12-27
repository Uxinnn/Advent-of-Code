from collections import defaultdict


def read_input():
    positions = []
    with open("input.in", "r") as file:
        for i in range(2):
            positions.append(int(file.readline().strip().split(": ")[1]) - 1)

    return positions


def simulate_round_part1(positions, round_number, player, scores):
    roll_result = ((round_number % 100) * 3) * 3 + 6
    positions[player] = (positions[player] + roll_result) % 10
    scores[player] += positions[player] + 1


def simulate_until_win_part1(positions):
    scores = [0, 0]
    round_number, player = 0, 0
    while scores[(player + 1) % 2] < 1000:
        simulate_round_part1(positions, round_number, player, scores)
        round_number += 1
        player = (player + 1) % 2
    return scores, round_number


def get_part_1_answer(scores, round_number):
    return min(scores) * round_number * 3


def simulate_all_possibilities_part2(positions):
    universes = defaultdict(int)
    universes[(positions[0], 0, positions[1], 0)] += 1
    win_count = [0, 0]
    rolls = defaultdict(int)
    # Count how many universes will a player move by (i+j+k) number of steps
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                rolls[i + j + k] += 1
    player = 0
    while universes:
        updated_universes = defaultdict(int)
        for universe in universes.keys():
            for roll, count in rolls.items():
                # Calculate new scores and positions
                pos0, score0, pos1, score1 = universe
                new_pos = ((pos0 if player == 0 else pos1) + roll) % 10
                new_score = (score0 if player == 0 else score1) + new_pos + 1
                new_universe = (new_pos, new_score, pos1, score1) if player == 0 else (pos0, score0, new_pos, new_score)
                if new_score >= 21:
                    win_count[player] += count * universes[universe]
                else:
                    updated_universes[new_universe] += count * universes[universe]
        universes = updated_universes
        player = (player + 1) % 2  # Toggle between players
    return win_count


def get_part_2_answer(win_count):
    return max(win_count)


def part1():
    positions = read_input()
    scores, round_number = simulate_until_win_part1(positions)
    answer = get_part_1_answer(scores, round_number)
    print(f"Part 1: {answer}")


def part2():
    positions = read_input()
    win_count = simulate_all_possibilities_part2(positions)
    answer = get_part_2_answer(win_count)
    print(f"Part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

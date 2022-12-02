def read_input():
    with open("input.in", "r") as f:
        games = [line.strip().split() for line in f.readlines()]
    return games


def part1():
    shape_points = {'X': 1, 'Y': 2, 'Z': 3}
    outcome_points = {'l': 0, 't': 3, 'w': 6}
    rules = {'A': {'X': 't', 'Y': 'w', 'Z': 'l'},
             'B': {'X': 'l', 'Y': 't', 'Z': 'w'},
             'C': {'X': 'w', 'Y': 'l', 'Z': 't'}
             }

    total_points = 0
    games = read_input()
    for oppo_shape, shape in games:
        outcome = rules[oppo_shape][shape]
        total_points += (shape_points[shape] + outcome_points[outcome])
    print(f"Part 1: {total_points}")


def part2():
    shape_points = {'A': 1, 'B': 2, 'C': 3}
    outcome_points = {'X': 0, 'Y': 3, 'Z': 6}
    rules = {'A': {'X': 'C', 'Y': 'A', 'Z': 'B'},
             'B': {'X': 'A', 'Y': 'B', 'Z': 'C'},
             'C': {'X': 'B', 'Y': 'C', 'Z': 'A'}
             }

    total_points = 0
    games = read_input()
    for oppo_shape, outcome in games:
        shape = rules[oppo_shape][outcome]
        total_points += (shape_points[shape] + outcome_points[outcome])
    print(f"Part 2: {total_points}")


part1()
part2()

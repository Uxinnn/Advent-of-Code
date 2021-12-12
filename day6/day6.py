def read_input():
    file = open('input.in', 'r')
    initial_count = list(map(int, file.readline().strip().split(",")))
    fish_count = [0]*9
    for fish in initial_count:
        fish_count[fish] += 1
    return fish_count


def simulate_1_day(fish_count):
    fish_due = fish_count[0]
    for i in range(1, 9):
        fish_count[i - 1] = fish_count[i]
    fish_count[8] = fish_due
    fish_count[6] += fish_due
    return fish_count


def simulate_n_days(n, fish_count):
    for _ in range(n):
        fish_count = simulate_1_day(fish_count)
    return fish_count


def get_number_of_fish(fish_count):
    return sum(fish_count)


def part1():
    initial_count = read_input()
    fish_count = simulate_n_days(80, initial_count)
    number_of_fish = get_number_of_fish(fish_count)
    print(f"Part 1: {number_of_fish}")


def part2():
    fish_count = read_input()
    fish_count = simulate_n_days(256, fish_count)
    number_of_fish = get_number_of_fish(fish_count)
    print(f"Part 2: {number_of_fish}")


if __name__ == "__main__":
    part1()
    part2()

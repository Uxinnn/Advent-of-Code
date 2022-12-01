def read_input():
    with open("input.in", "r") as file:
        raw_x, raw_y = [raw[2:] for raw in file.read().strip().split(": ")[1].split(', ')]
        x_min, x_max = map(int, raw_x.split(".."))
        y_min, y_max = map(int, raw_y.split(".."))
    return x_min, x_max, y_min, y_max


def find_highest_y_vel_count(bounding_box):
    x_min, x_max, y_min, y_max = bounding_box
    max_heights = []
    count = 0
    for x_vel in range(1, x_max + 1):
        for y_vel in range(y_min, -y_min):
            height = simulate(x_vel, y_vel, bounding_box)
            if height != -1:
                max_heights.append(height)
                count += 1
    return max(max_heights), count


def simulate(x_vel, y_vel, bounding_box):
    x_min, x_max, y_min, y_max = bounding_box
    x, y = 0, 0
    steps = []  # May not need to store all steps, just the highest one
    in_box = False
    while (x <= x_max and y >= y_min) or (x_vel == 0 and y >= y_min):
        steps.append((x, y))
        if x_min <= x <= x_max and y_min <= y <= y_max:
            in_box = True
        x += x_vel
        y += y_vel
        x_vel = x_vel - 1 if x_vel != 0 else 0
        y_vel -= 1
    if in_box:
        return max([step[1] for step in steps])
    else:
        return -1


def part1():
    bounding_box = read_input()
    max_y = find_highest_y_vel_count(bounding_box)[0]
    print(f"Part 1: {max_y}")


def part2():
    bounding_box = read_input()
    count = find_highest_y_vel_count(bounding_box)[1]
    print(f"Part 2: {count}")


if __name__ == "__main__":
    part1()
    part2()

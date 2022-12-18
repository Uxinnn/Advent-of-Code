def read_input(file):
    with open(file, 'r') as f:
        objects = [line.split() for line in f]
        objects = [((int(line[2][:-1].split('=')[-1]), int(line[3][:-1].split('=')[-1])),
                    (int(line[-2][:-1].split('=')[-1]), int(line[-1].split('=')[-1])))
                   for line in objects
                   ]
    return objects


def get_cover(row, sensor, manhattan_dist):
    """
    Get the range of points in the row which is covered by the sensor
    """
    y_diff = abs(row - sensor[1])
    x_range = (sensor[0] - manhattan_dist + y_diff, sensor[0] + manhattan_dist - y_diff)
    if x_range[0] > x_range[1]:
        return None
    return x_range


def combine_ranges(x_ranges):
    """
    Combine overlapping ranges. Minimizes the number of ranges in the list.
    """
    combined_ranges = list()
    x_ranges.sort()
    for x_range in x_ranges:
        if not combined_ranges:
            combined_ranges.append(list(x_range))
            continue
        last_range = combined_ranges[-1]
        if x_range[0] <= last_range[1] < x_range[1] or last_range[1] + 1 == x_range[0]:
            combined_ranges[-1][1] = x_range[1]
        elif x_range[0] > last_range[1]:
            combined_ranges.append(list(x_range))
    return combined_ranges


def get_row_range(row, objects):
    """
    Get the ranges of points in a row which are covered by all sensors.
    """
    x_ranges = list()
    for sensor, beacon in objects:
        manhattan_dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
        x_range = get_cover(row, sensor, manhattan_dist)
        if x_range is not None:
            x_ranges.append(x_range)
    combined_ranges = combine_ranges(x_ranges)
    return combined_ranges


def part1(file):
    objects = read_input(file)
    row = 10 if file == "example.in" else 2000000
    combined_ranges = get_row_range(row, objects)
    positions = sum([r[1] - r[0] for r in combined_ranges])
    print(f"Part 1: {positions}")


def part2(file):
    objects = read_input(file)
    max_coor = 20 if file == "example.in" else 4000000
    min_coor = 0
    multiplier = 4000000
    for y in range(max_coor):
        combined_ranges = get_row_range(y, objects)
        if len(combined_ranges) > 1:
            x = combined_ranges[1][0] - 1
            if min_coor <= x <= max_coor:
                answer = x * multiplier + y
                print(f"Part 2: {answer}")
            return


input_file = "input.in"
part1(input_file)
part2(input_file)

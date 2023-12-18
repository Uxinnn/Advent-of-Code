def read_input(file):
    with open(file, 'r') as f:
        for row in f:
            row = row.strip()
            dirn, count, color = row.split()
            count = int(count)
            color = color[2:-1]
            yield dirn, count, color


def get_new_steps(steps):
    idx_2_dirn = "RDLU"
    for _, _, color in steps:
        count = int(color[:-1], 16)  # First 5 values are hex
        dirn = idx_2_dirn[int(color[-1])]  # Convert last value to direction
        yield dirn, count, None


def get_area_and_perimeter(steps):
    """
    Use shoelace method to find area.
    """
    coor = (0, 0)
    area, perimeter = 0, 0
    for dirn, count, color in steps:
        prev_coor = coor
        if dirn == 'R':
            coor = (coor[0], coor[1] + count)
        elif dirn == 'L':
            coor = (coor[0], coor[1] - count)
        elif dirn == 'U':
            coor = (coor[0] - count, coor[1])
        elif dirn == 'D':
            coor = (coor[0] + count, coor[1])
        perimeter += count
        area += (coor[0] + prev_coor[0]) * (coor[1] - prev_coor[1])
    area = abs(area) // 2
    return area, perimeter


def get_interior_points(area, perimeter):
    interior_points = int(area - perimeter / 2 + 1) + perimeter
    return interior_points


def part1(file):
    steps = read_input(file)
    area, perimeter = get_area_and_perimeter(steps)
    interior_points = get_interior_points(area, perimeter)
    print(f"Part 1: {interior_points}")


def part2(file):
    steps = read_input(file)
    steps = get_new_steps(steps)
    area, perimeter = get_area_and_perimeter(steps)
    interior_points = get_interior_points(area, perimeter)
    print(f"Part 2: {interior_points}")


file = "input.in"
part1(file)
part2(file)

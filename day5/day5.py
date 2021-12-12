def read_input(is_part_1):
    coordinates = []
    with open("input.in", "r") as file:
        while True:
            line = file.readline().strip()
            if line == "":
                break
            coordinate_pair = [tuple(map(int, coor.split(','))) for coor in line.split(" -> ")]
            if is_part_1 and coordinate_pair[0][0] != coordinate_pair[1][0] and \
                    coordinate_pair[0][1] != coordinate_pair[1][1]:
                continue
            if coordinate_pair[0][0] == coordinate_pair[1][0] and coordinate_pair[0][1] > coordinate_pair[1][1]:
                coordinate_pair[0], coordinate_pair[1] = coordinate_pair[1], coordinate_pair[0]
            elif coordinate_pair[0][1] == coordinate_pair[1][1] and coordinate_pair[0][0] > coordinate_pair[1][0]:
                coordinate_pair[0], coordinate_pair[1] = coordinate_pair[1], coordinate_pair[0]
            else:
                if not is_part_1:
                    if coordinate_pair[0][0] > coordinate_pair[1][0]:
                        coordinate_pair[0], coordinate_pair[1] = coordinate_pair[1], coordinate_pair[0]
            # print(coordinate_pair)
            coordinates.append(coordinate_pair)
    return coordinates


def init_coor_dict():
    coor_dict = dict()
    return coor_dict


def mark_coordinates(p1, p2, coor_dict):
    # horizontal line, y is the same
    if p1[1] == p2[1]:
        y = p1[1]
        for x in range(p1[0], p2[0] + 1):
            if (x, y) not in coor_dict.keys():
                coor_dict[(x, y)] = 0
            coor_dict[(x, y)] += 1
    # vertical line, x is the same
    elif p1[0] == p2[0]:
        x = p1[0]
        for y in range(p1[1], p2[1] + 1):
            if (x, y) not in coor_dict.keys():
                coor_dict[(x, y)] = 0
            coor_dict[(x, y)] += 1
    # horizontal line
    else:
        # bottom up
        if p1[1] > p2[1]:
            for i in range(p2[0] - p1[0] + 1):
                x = p1[0] + i
                y = p1[1] - i
                if (x, y) not in coor_dict.keys():
                    coor_dict[(x, y)] = 0
                coor_dict[(x, y)] += 1
        # up bottom
        else:
            for i in range(p2[0] - p1[0] + 1):
                x = p1[0] + i
                y = p1[1] + i
                if (x, y) not in coor_dict.keys():
                    coor_dict[(x, y)] = 0
                coor_dict[(x, y)] += 1
    return coor_dict


def mark_all_coordinates(coordinates, coor_dict):
    for coordinate_pair in coordinates:
        p1 = coordinate_pair[0]
        p2 = coordinate_pair[1]
        coor_dict = mark_coordinates(p1, p2, coor_dict)
    return coor_dict


def get_danger_points(coor_dict):
    total_danger_points = 0
    for coor_count in coor_dict.values():
        if coor_count > 1:
            total_danger_points += 1
    return total_danger_points


def part1():
    coordinates = read_input(True)
    coor_dict = init_coor_dict()
    coor_dict = mark_all_coordinates(coordinates, coor_dict)
    danger_points_count = get_danger_points(coor_dict)
    print(f"Part 1: {danger_points_count}")


def part2():
    coordinates = read_input(False)
    coor_dict = init_coor_dict()
    coor_dict = mark_all_coordinates(coordinates, coor_dict)
    danger_points_count = get_danger_points(coor_dict)
    print(f"Part 2: {danger_points_count}")


if __name__ == "__main__":
    part1()
    part2()

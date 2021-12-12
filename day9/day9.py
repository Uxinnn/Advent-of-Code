def read_input():
    file = open('input.in', 'r')
    height_map = [[10] + [int(i) for i in line.strip()] + [10] for line in file.readlines()]
    height_map = [[10] * len(height_map[0])] + height_map + [[10] * len(height_map[0])]
    return height_map


def get_low_points(height_map):
    low_points = []
    for i in range(1, len(height_map) - 1):
        for j in range(1, len(height_map[0]) - 1):
            value = height_map[i][j]
            if value < height_map[i][j-1] and value < height_map[i][j+1]\
                    and value < height_map[i-1][j] and value < height_map[i+1][j]:
                low_points.append(value)
    return low_points


def get_sum_of_risk_levels(low_points):
    return sum([x + 1 for x in low_points])


def flood_fill(x, y, height_map, size):
    if height_map[x][y] > 8:
        return size
    height_map[x][y] = 9

    size1 = flood_fill(x + 1, y, height_map, size + 1)
    size2 = flood_fill(x - 1, y, height_map, size1)
    size3 = flood_fill(x, y - 1, height_map, size2)
    size4 = flood_fill(x, y + 1, height_map, size3)

    return size4


def get_basin_sizes(height_map):
    sizes = []
    for i in range(1, len(height_map) - 1):
        for j in range(1, len(height_map[0]) - 1):
            if height_map[i][j] < 9:
                size = flood_fill(i, j, height_map, 0)
                sizes.append(size)
    return sizes


def get_answer(sizes):
    sizes.sort()
    largest_3 = sizes[-3:]
    answer = 1
    for size in largest_3:
        answer = answer * size
    return answer


def part1():
    height_map = read_input()
    low_points = get_low_points(height_map)
    sum_of_risk_levels = get_sum_of_risk_levels(low_points)
    print(f"Part 1: {sum_of_risk_levels}")


def part2():
    height_map = read_input()
    sizes = get_basin_sizes(height_map)
    answer = get_answer(sizes)
    print(f"Part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

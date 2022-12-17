"""
Quite a slow implementation...
"""


def read_input(file):
    with open(file, 'r') as f:
        lines = [[tuple(map(int, point.split(','))) for point in line.strip().split(" -> ")] for line in f]
        lines = [(path[i], path[i + 1]) if path[i] < path[i + 1] else (path[i + 1], path[i]) for path in lines for i in range(len(path) - 1)]
    return lines


def get_boundaries(lines):
    max_x, min_x, max_y, min_y = 500, 500, 0, 0
    for p1, p2 in lines:
        max_x = max(max_x, p2[0])
        min_x = min(min_x, p1[0])
        max_y = max(max_y, p2[1])
        min_y = min(min_y, p1[1])
    return max_x, min_x, max_y, min_y


def print_board(lines):
    max_x, min_x, max_y, min_y = get_boundaries(lines)
    board = [['.']*(max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    board[0][500 - min_x] = '+'
    for p1, p2 in lines:
        for j in range(p2[0] - p1[0] + 1):
            board[p2[1] - min_y][p1[0] - min_x + j] = '#'
        for j in range(p2[1] - p1[1] + 1):
            board[p1[1] - min_y + j][p2[0] - min_x] = '#'
    for row in board:
        print(row)


def check_trajectory(sand, lines, old_sands, max_y=None, is_part2=False):
    x, y = sand
    points_to_check = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
    points_status = [0, 0, 0]  # 0 for not blocked, 1 for blocked
    if is_part2 and y == max_y + 1:  # Cannot move further if floor is reached (for part2)
        return [1, 1, 1]
    for i, point_to_check in enumerate(points_to_check):  # Check if point is occupied by old sands
        if point_to_check in old_sands:
            points_status[i] = 1
    for p1, p2 in lines:
        if p1[0] == p2[0]:  # vertical line
            for i, point_to_check in enumerate(points_to_check):
                if point_to_check[0] == p1[0] and p1[1] <= point_to_check[1] <= p2[1]:
                    points_status[i] = 1
        elif p1[1] == p2[1]:  # horizontal line
            for i, point_to_check in enumerate(points_to_check):
                if point_to_check[1] == p1[1] and p1[0] <= point_to_check[0] <= p2[0]:
                    points_status[i] = 1
    return points_status


def move_sand(sand, lines, old_sands, max_y=None, is_part2=False):
    points_status = check_trajectory(sand, lines, old_sands, max_y, is_part2)
    has_moved = False
    if points_status[1] == 0:
        sand[1] += 1
        has_moved = True
    elif points_status[0] == 0:
        sand[1] += 1
        sand[0] -= 1
        has_moved = True
    elif points_status[2] == 0:
        sand[1] += 1
        sand[0] += 1
        has_moved = True
    return has_moved


def is_overboard(sand, max_y):  # Check if sand is going into abyss
    return sand[1] > max_y


def part1(file):
    lines = read_input(file)
    _, _, max_y, _ = get_boundaries(lines)
    old_sands = set()
    sand_counter = 0
    start_x, start_y = 500, 0
    while True:
        sand = [start_x, start_y]
        has_moved = True
        while has_moved:
            has_moved = move_sand(sand, lines, old_sands)
            if is_overboard(sand, max_y):
                print(f"Part 1: {sand_counter}")
                return
        old_sands.add(tuple(sand))
        sand_counter += 1


def part2(file):
    lines = read_input(file)
    _, _, max_y, _ = get_boundaries(lines)
    old_sands = set()
    sand_counter = 0
    start_x, start_y = 500, 0
    while True:
        if (500, 0) in old_sands:
            print(f"Part 2: {sand_counter}")
            return
        sand = [start_x, start_y]
        has_moved = True
        while has_moved:
            has_moved = move_sand(sand, lines, old_sands, max_y=max_y, is_part2=True)
        old_sands.add(tuple(sand))
        sand_counter += 1


input_file = "input.in"
part1(input_file)
part2(input_file)

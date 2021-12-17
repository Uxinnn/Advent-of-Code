import numpy as np
from copy import deepcopy


def read_input():
    with open("input.in", "r") as file:
        grid = np.array([[int(x) for x in line.strip()] for line in file.readlines()])
    return grid


def get_large_grid(grid):
    def plus_n(old_grid, n):
        new_grid = deepcopy(old_grid)
        for i in range(n):
            new_grid = new_grid % 9 + 1
        return new_grid

    vert = np.hstack((grid, plus_n(grid, 1), plus_n(grid, 2), plus_n(grid, 3), plus_n(grid, 4)))
    return np.vstack((vert, plus_n(vert, 1), plus_n(vert, 2), plus_n(vert, 3), plus_n(vert, 4)))


# Each node is (f, g, (x, y))
def a_star_search(grid):
    def calc_manhattan_dist(src, dst):
        return abs(src[0] - dst[0]) + abs(src[1] - dst[1])

    max_x, max_y = len(grid[0]), len(grid)
    not_travelled = [(0, 0, (0, 0))]
    travelled = set()
    goal = (len(grid[0]) - 1, len(grid) - 1)
    while not_travelled:
        current_node = min(not_travelled, key=lambda node: node[0])
        not_travelled.remove(current_node)
        travelled.add(current_node[2])
        if current_node[2] == goal:
            return current_node[0]
        x, y = current_node[2]
        adjacent_coordinates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for adjacent_coordinate in adjacent_coordinates:
            if adjacent_coordinate[0] < 0 or adjacent_coordinate[1] < 0 or \
                    adjacent_coordinate[0] >= max_x or adjacent_coordinate[1] >= max_y:
                continue
            if adjacent_coordinate in travelled:
                continue
            g = current_node[1] + grid[adjacent_coordinate[1]][adjacent_coordinate[0]]
            h = calc_manhattan_dist(adjacent_coordinate, goal)
            adjacent_node = (g + h, g, adjacent_coordinate)
            if adjacent_coordinate in [node[2] for node in not_travelled]:
                old_node = [node for node in not_travelled if node[2] == adjacent_coordinate][0]
                if adjacent_node[0] >= old_node[0]:
                    continue
                else:
                    not_travelled.remove(old_node)
            not_travelled.append(adjacent_node)


def part1():
    grid = read_input()
    lowest_risk = a_star_search(grid)
    print(f"Part 1: {lowest_risk}")


def part2():
    grid = read_input()
    large_grid = get_large_grid(grid)
    lowest_risk = a_star_search(large_grid)
    print(f"Part 2: {lowest_risk}")


if __name__ == "__main__":
    part1()
    part2()

from collections import defaultdict


def read_input():
    with open("input.in", "r") as file:
        dots = defaultdict(int)
        instructions = []
        max_x, max_y = -1, -1
        is_instruction = False
        for line in [line.strip() for line in file.readlines()]:
            if line == "":
                is_instruction = True
                continue
            if not is_instruction:
                x, y = list(map(int, line.split(',')))
                dots[(x, y)] += 1
                max_x = x if max_x < x else y
                max_y = y if max_y < y else y
            else:
                axis, value = line.split()[2].split('=')
                axis = 0 if axis == 'x' else 1
                instructions.append((axis, int(value)))
    return dots, [max_x, max_y], instructions


def fold(dots, max_coordinate, instruction):
    axis, value = instruction
    updated_dots = defaultdict(int)
    if abs(0 - value) > abs(max_coordinate[axis] - value):
        new_max = abs(0 - value) - 1
    else:
        new_max = abs(max_coordinate[axis] - value) - 1
    max_coordinate[axis] = new_max
    for coordinate, dot in dots.items():
        coordinate = list(coordinate)
        if coordinate[axis] != value:
            coordinate[axis] = max_coordinate[axis] - (abs(coordinate[axis] - value) - 1)
            updated_dots[tuple(coordinate)] += dot
    return updated_dots


def print_dots(dots, max_coordinate):
    for j in range(max_coordinate[1] + 1):
        for i in range(max_coordinate[0] + 1):
            if (i, j) not in dots.keys():
                symbol = '.'
            else:
                symbol = '#'
            print(symbol, end=" ")
        print()


def get_number_of_dots(dots):
    return len(dots)


def run_all_instructions(dots, max_coordinate, instructions):
    for instruction in instructions:
        dots = fold(dots, max_coordinate, instruction)
    return dots


def part1():
    dots, max_coordinate, instructions = read_input()
    dots = fold(dots, max_coordinate, instructions[0])
    number_of_dots = get_number_of_dots(dots)
    print(f"Part 1: {number_of_dots}")


def part2():
    dots, max_coordinate, instructions = read_input()
    dots = run_all_instructions(dots, max_coordinate, instructions)
    print("Part 2:")
    print_dots(dots, max_coordinate)


if __name__ == "__main__":
    part1()
    part2()

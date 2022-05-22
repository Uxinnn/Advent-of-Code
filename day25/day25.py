def read_input():
    with open("input.in", "r") as file:
        return [list(line.strip()) for line in file.readlines()]


def move_east(grid):
    can_move = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '>':
                if grid[i][(j + 1) % len(grid[0])] == '.':
                    can_move.append((i, j))
    for i, j in can_move:
        grid[i][(j + 1) % len(grid[0])] = '>'
        grid[i][j] = '.'
    have_moved = bool(can_move)
    return have_moved


def move_south(grid):
    can_move = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'v':
                if grid[(i + 1) % len(grid)][j] == '.':
                    can_move.append((i, j))
    for i, j in can_move:
        grid[(i + 1) % len(grid)][j] = 'v'
        grid[i][j] = '.'
    have_moved = bool(can_move)
    return have_moved


def print_grid(grid):
    for row in grid:
        for coor in row:
            print(coor, end=" ")
        print("\n")


def part1():
    grid = read_input()
    count = 0
    while True:
        have_move_east = move_east(grid)
        have_move_south = move_south(grid)
        count += 1
        if not have_move_east and not have_move_south:
            break
        if count % 1000 == 0:
            print(count)
    print(f"Part 1: {count}")


if __name__ == "__main__":
    part1()

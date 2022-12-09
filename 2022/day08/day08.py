def read_input():
    with open("input.in", 'r') as f:
        grid = [[int(c) for c in line.strip()] for line in f.readlines()]
    return grid


def rotate(grid):
    return list(zip(*grid[::-1]))


def part1():
    grid = read_input()
    visible_trees = set()
    grid_len = len(grid)
    for i in range(4):
        for y, row in enumerate(grid):
            max_height = -1
            for x, c in enumerate(row):
                if c > max_height:
                    if i == 0:
                        visible_trees.add((x, y))
                    elif i == 1:
                        visible_trees.add((y, grid_len-1-x))
                    elif i == 2:
                        visible_trees.add((grid_len-1-x, grid_len-1-y))
                    else:
                        visible_trees.add((grid_len-1-y, x))
                    max_height = c
        grid = rotate(grid)
    print(f"Part 1: {len(visible_trees)}")


def part2():
    grid = read_input()
    max_scenic_score = -1
    row_len = len(grid[0])
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            left_score = 0
            for k in range(j-1, -1, -1):
                left_score += 1
                if row[k] >= c:
                    break
            right_score = 0
            for k in range(j + 1, row_len):
                right_score += 1
                if row[k] >= c:
                    break
            up_score = 0
            for k in range(i-1, -1, -1):
                up_score += 1
                if grid[k][j] >= c:
                    break
            down_score = 0
            for k in range(i + 1, row_len):
                down_score += 1
                if grid[k][j] >= c:
                    break
            scenic_score = left_score * right_score * up_score * down_score
            max_scenic_score = max(max_scenic_score, scenic_score)
    print(f"Part 2: {max_scenic_score}")


part1()
part2()

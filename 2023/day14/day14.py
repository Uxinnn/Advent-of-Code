def read_input(file):
    with open(file, 'r') as f:
        puzzle = [list(row.strip()) for row in f]
        return puzzle


def puzzle_to_key(puzzle):
    """
    Convert puzzle to a string to be used as a unique identifier of the current
    configuration of the puzzle. Used to `run_cycles` to find repeated cycles.
    """
    key = "".join(["".join(row) for row in puzzle])
    return key


def move_rocks(puzzle, max_i, max_j):
    """
    Move rocks up north.
    """
    for j in range(max_j):
        landing_coor = [0, j]  # Where the rock will land when moved up north.
        for i in range(max_i):
            val = puzzle[i][j]
            if val == 'O':
                # Move rock from original coordinate to landing coordinate.
                puzzle[i][j] = '.'
                puzzle[landing_coor[0]][landing_coor[1]] = 'O'
                landing_coor[0] += 1
            elif val == '#':
                # The coordinate directly below the '#' becomes the next
                # land coordinate since '#' are immovable.
                landing_coor[0] = i + 1


def rotate_90(puzzle):
    """
    Get a new puzzle that is rotated 90 degrees clockwise.
    TODO: Probably would be better to do it inplace.
    """
    rotated_puzzle = [list(row)[::-1] for row in zip(*puzzle)]
    return rotated_puzzle


def run_cycles(puzzle, n, max_i, max_j):
    """
    Run n cycles, where each cycle consists of moving rocks up north and then
    rotating the puzzle clockwise 90 degrees, repeated 4 times.
    Cache is used to speed up the runtime since if we land on a puzzle
    configuration we've seen before, we would have found a cycle. Shortcut the
    runtime by calculating how many such cycles will occur, and minus the
    number from n.
    """
    cache = dict()
    while n:
        for _ in range(4):
            move_rocks(puzzle, max_i, max_j)
            puzzle = rotate_90(puzzle)
        # Speed things up
        key = puzzle_to_key(puzzle)
        if key in cache:
            delta = cache[key] - n  # The found cycle is delta in length.
            n -= ((n // delta) * delta)
        else:
            cache[key] = n
        n -= 1
    return puzzle


def get_load(puzzle, max_i):
    tot_load = 0
    for i, row in enumerate(puzzle):
        row_load = row.count('O') * (max_i - i)
        tot_load += row_load
    return tot_load


def part1(file):
    puzzle = read_input(file)
    max_i, max_j = len(puzzle), len(puzzle[0])
    move_rocks(puzzle, max_i, max_j)
    tot_load = get_load(puzzle, max_i)
    print(f"Part 1: {tot_load}")


def part2(file):
    puzzle = read_input(file)
    max_i, max_j = len(puzzle), len(puzzle[0])
    n_cycles = 1000000000
    puzzle = run_cycles(puzzle, n_cycles, max_i, max_j)
    tot_load = get_load(puzzle, max_i)
    print(f"Part 2: {tot_load}")


file = "input.in"
part1(file)
part2(file)

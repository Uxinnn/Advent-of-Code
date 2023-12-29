def read_input(file):
    with open(file, 'r') as f:
        grid = [list(line.strip()) for line in f]
        start = locate_and_replace_S(grid)
        return start, grid


def locate_and_replace_S(grid):
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == 'S':
                grid[i][j] = '.'
                return i, j


def simulate(locs, tot_steps, grid, max_i, max_j, part):
    for i in range(tot_steps):
        new_locs = set()
        for i, j in locs:
            for i2, j2 in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                if (part == 1 and -1 < i2 < max_i and -1 < j2 < max_j
                        and grid[i2][j2] == '.'):
                    new_locs.add((i2, j2))
                elif part == 2 and grid[i2 % max_i][j2 % max_j] == '.':
                    new_locs.add((i2, j2))
        locs = new_locs
    return locs


def part1(file):
    start, grid = read_input(file)
    max_i, max_j = len(grid), len(grid[0])
    tot_steps = 64
    locs = simulate({start}, tot_steps, grid, max_i, max_j, part=1)
    reachable_count = len(locs)
    print(f"Part 1: {reachable_count}")


def part2(file):
    """
    Relationship between number of locations and number of steps is quadratic.
    p = an^2+bn+c
    Use 3 point formula to find coefficients a, b, c.
    Substitute values into quadratic formula to find the coefficients.
    Use coefficients and desired step count n to find number of locations p.
    Done with alot of help from reddit.
    """
    start, grid = read_input(file)
    max_i, max_j = len(grid), len(grid[0])
    reachable_counts = list()
    # These are the 3 points
    for tot_steps in (65, 196, 327):
        locs = simulate({start}, tot_steps, grid, max_i, max_j, part=2)
        reachable_count = len(locs)
        reachable_counts.append(reachable_count)

    # Find coefficients
    # Formulas for a, b, and c are found by hand.
    c = reachable_counts[0]
    b = (4 * reachable_counts[1] -
         3 * reachable_counts[0] -
         reachable_counts[2]
         ) // 2
    a = reachable_counts[1] - reachable_counts[0] - b
    max_steps = 26501365
    x = (max_steps - max_i // 2) // max_i  # number of whole tile lengths
    ans = a * x ** 2 + b * x + c
    print(f"Part 2: {ans}")


file = "input.in"
part1(file)
part2(file)

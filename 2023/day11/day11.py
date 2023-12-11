from bisect import bisect


def read_input(file):
    with open(file, 'r') as f:
        space = [row.strip() for row in f]
        return space


def get_empty_rows_and_cols(space, max_i, max_j):
    empty_rows = list()
    empty_cols = list()
    # Find empty rows first
    for i in range(max_i):
        if space[i].count('.') == max_j:
            empty_rows.append(i)
    # Then find empty columns
    for j in range(max_j):
        empty_count = 0
        for i in range(max_i):
            if space[i][j] == '.':
                empty_count += 1
        if empty_count == max_i:
            empty_cols.append(j)
    return empty_rows, empty_cols


def get_galaxies(space):
    """
    Find all galaxy coordinates.
    """
    galaxies = list()
    for i, row in enumerate(space):
        for j, val in enumerate(row):
            if space[i][j] == '#':
                galaxies.append((i, j))
    return galaxies


def get_expansion_dist(left, right, empty_spaces, expansion_factor):
    """
    Get the extra space between the left and right coordinate that is due to
    the expansion of space.
    """
    expanded_left = bisect(empty_spaces, left)
    expanded_right = bisect(empty_spaces, right)
    expanded_space = abs(expanded_left - expanded_right) * (
                expansion_factor - 1)
    return expanded_space


def get_galaxy_min_dists(galaxies, empty_rows, empty_cols, expansion_factor):
    """
    Get all minimum distances between galaxies after the expansion of space.
    """
    min_dists = list()
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i + 1:]:
            # To calculate distance after expansion: Find the original row and
            # col distance first. Then find how many empty rows are in between
            # the 2 galaxies and multiply the space accordingly. Do the same
            # columns.
            # New distance: row_dist + col_dist + extra_row_dist_from_expansion
            #               + extra_col_dist_from_expansion
            expanded_row_dist = get_expansion_dist(g1[0], g2[0],
                                                   empty_rows,
                                                   expansion_factor
                                                   )
            expanded_col_dist = get_expansion_dist(g1[1], g2[1],
                                                   empty_cols,
                                                   expansion_factor
                                                   )
            original_dist = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
            min_dist = original_dist + expanded_row_dist + expanded_col_dist
            min_dists.append(min_dist)
    return min_dists


def part1(file):
    space = read_input(file)
    max_i, max_j = len(space), len(space[0])
    empty_rows, empty_cols = get_empty_rows_and_cols(space, max_i, max_j)
    # Find all galaxy coordinates
    galaxies = get_galaxies(space)
    # Get pair min
    expansion_factor = 2
    min_dists = get_galaxy_min_dists(galaxies,
                                     empty_rows,
                                     empty_cols,
                                     expansion_factor,
                                     )
    min_dists_sum = sum(min_dists)
    print(f"Part 1: {min_dists_sum}")


def part2(file):
    space = read_input(file)
    max_i, max_j = len(space), len(space[0])
    empty_rows, empty_cols = get_empty_rows_and_cols(space, max_i, max_j)
    # Find all galaxy coordinates
    galaxies = get_galaxies(space)
    # Get pair min
    expansion_factor = 1000000
    min_dists = get_galaxy_min_dists(galaxies,
                                     empty_rows,
                                     empty_cols,
                                     expansion_factor,
                                     )
    min_dists_sum = sum(min_dists)
    print(f"Part 2: {min_dists_sum}")


file = "input.in"
part1(file)
part2(file)

def read_input(file):
    with open(file, 'r') as f:
        puzzle = list()
        for line in f:
            line = line.strip()
            if line:
                puzzle.append(line)
            else:
                yield puzzle
                puzzle = list()
        yield puzzle


def is_rows_valid(row1, row2, smudge=False):
    """
    If smudge is False, simply return whether the 2 rows are the same.
    If smudge is True, return True if there is at most 1 difference in the rows.
    """
    if smudge:
        smudge_found = False
        for v1, v2 in zip(row1, row2):
            if v1 != v2:
                if smudge_found:
                    # Have already found a smudge, rows are not valid since
                    # there are >1 smudges.
                    return False, smudge_found
                else:
                    # First smudge found, still ok. Continue.
                    smudge_found = True
        # All rows are the same with at most 1 smudge found.
        return True, smudge_found
    else:
        return row1 == row2, False


def find_mirror(puzzle, smudge=False, skip_idx=0):
    for i in range(1, len(puzzle)):
        if i == skip_idx:
            # Used for part 2. Skip the index if it is the one that was found
            # in part 1.
            continue
        # Flip top half so rows in the top_half and bot_half that are to be
        # compared have the same index.
        top_half, bot_half = puzzle[:i][::-1], puzzle[i:]
        is_same, smudge_found = True, False
        for row1, row2 in zip(top_half, bot_half):
            # For a top_half and bot_half, check if they are mirror images of
            # each other. If so, return True. Else check other combinations of
            # top_halves and bot_halves.
            is_row_valid, is_row_smudged = is_rows_valid(row1, row2,
                                                         smudge=smudge
                                                         )
            if is_row_valid:
                if smudge and is_row_smudged:
                    if smudge_found:
                        # More than 2 smudges found, mirror is not found.
                        is_same = False
                        break
                    else:
                        # First smudge is found, still ok. Continue
                        smudge_found = True
            else:
                is_same = False
                break
        if is_same:
            # If a mirror is found, return True and the index of the mirror.
            return True, i
    return False, None


def get_mirrors(puzzles, smudge=False, part1_mirrors=None):
    """
    Find mirrors in each puzzle.
    smudge is to toggle between part 1 (False) and part 2 (True).
    """
    mirrors = list()
    for i, puzzle in enumerate(puzzles):
        # Check for horizontal mirrors
        if smudge and part1_mirrors[i][0] == 'h':
            # Find out if we should skip an index when finding mirrors.
            skip_idx = part1_mirrors[i][1]
        else:
            skip_idx = 0
        ret, idx = find_mirror(puzzle, smudge=smudge, skip_idx=skip_idx)
        if ret:
            mirrors.append(('h', idx))
            continue
        # Check for vertical mirrors
        puzzle_T = list(zip(*puzzle))
        if smudge and part1_mirrors[i][0] == 'v':
            # Find out if we should skip an index when finding mirrors.
            skip_idx = part1_mirrors[i][1]
        else:
            skip_idx = 0
        ret, idx = find_mirror(puzzle_T, smudge=smudge, skip_idx=skip_idx)
        if ret:
            mirrors.append(('v', idx))
            continue
        # Exception since there should be a mirror found for each puzzle.
        raise Exception(f"Cannot find mirror for puzzle {i}: {puzzle}.")
    return mirrors


def calculate_response(mirrors):
    res = 0
    for dirn, idx in mirrors:
        if dirn == 'h':
            res += 100 * idx
        else:
            res += idx
    return res


def part1(file):
    puzzles = read_input(file)
    mirrors = get_mirrors(puzzles)
    res = calculate_response(mirrors)
    print(f"Part 1: {res}")


def part2(file):
    puzzles = read_input(file)
    part1_mirrors = get_mirrors(puzzles)
    puzzles = read_input(file)
    mirrors = get_mirrors(puzzles, True, part1_mirrors)
    res = calculate_response(mirrors)
    print(f"Part 2: {res}")


file = "input.in"
part1(file)
part2(file)

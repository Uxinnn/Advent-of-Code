from collections import deque


def read_input(file):
    with open(file, 'r') as f:
        for line in f:
            yield list(line.strip())
        # Extra empty list to allow last line to be processed below since the
        # middle row is the one being processed in focus_rows.
        yield list()


def get_valid_adjacent_coors(focus_rows, i):
    """
    Get adjacent coordinates that are within the bounds of the grid.
    """
    adj_coors = ((0, i - 1), (0, i), (0, i + 1),
                 (1, i - 1), (1, i + 1),
                 (2, i - 1), (2, i), (2, i + 1)
                 )
    for adj_row_idx, adj_i in adj_coors:
        if -1 < adj_i < len(focus_rows[adj_row_idx]):
            yield adj_row_idx, adj_i

def extract_full_int(row, i):
    """
    Obtain the full integer value given the index of one of its characters.
    """
    start, end = i, i + 1
    while start > -1:
        if not row[start - 1].isnumeric():
            break
        start -= 1
    while end < len(row):
        if not row[end].isnumeric():
            break
        end += 1
    num = int("".join(row[start:end]))
    # Replace int indices with '.' to prevent duplicate readings
    for j in range(start, end):
        row[j] = '.'
    return num


def part1(file):
    rows = read_input(file)
    part_num_sum = 0
    # Focus_rows will contain the 3 rows of interest needed to process the
    # middle row (Since to process a single row, we need the rows above & below
    # it only).
    focus_rows = deque([[], [], []])
    for row in rows:
        # Update focus rows to process the next middle row
        focus_rows.popleft()
        focus_rows.append(row)
        # Check middle row
        for i in range(len(focus_rows[1])):
            val = focus_rows[1][i]
            if not val.isnumeric() and val != '.':
                # Found a symbol
                adj_coors = get_valid_adjacent_coors(focus_rows, i)
                for adj_row, adj_i in adj_coors:
                    if focus_rows[adj_row][adj_i].isnumeric():
                        # Found an adjacent number, obtain the whole number
                        num = extract_full_int(focus_rows[adj_row], adj_i)
                        part_num_sum += num
    print(f"Part 1: {part_num_sum}")


def part2(file):
    rows = read_input(file)
    tot_gear_ratio = 0
    # Focus_rows will contain the 3 rows of interest needed to process the
    # middle row (Since to process a single row, we need the rows above & below
    # it only).
    focus_rows = deque([[], [], []])
    for row in rows:
        # Update focus rows to process the next middle row
        focus_rows.popleft()
        focus_rows.append(row)
        # Check middle row
        for i in range(len(focus_rows[1])):
            val = focus_rows[1][i]
            if val == "*":
                # Found a symbol
                adj_nums = list()
                adj_coors = get_valid_adjacent_coors(focus_rows, i)
                for adj_row, adj_i in adj_coors:
                    if focus_rows[adj_row][adj_i].isnumeric():
                        # Found an adjacent number, obtain the whole number
                        num = extract_full_int(focus_rows[adj_row], adj_i)
                        adj_nums.append(num)
                # Calculate gear ratio if exactly 2 adjacent numbers found
                if len(adj_nums) == 2:
                    tot_gear_ratio += adj_nums[0] * adj_nums[1]
    print(f"Part 2: {tot_gear_ratio}")


file = "example.in"
part1(file)
part2(file)

import re


def read_input(file):
    board = list()
    with open(file, 'r') as f:
        for line in f:
            if line[0] in " .#":
                line = line[:-1]
                board.append(line)
            else:
                cmds = line.strip()
                cmds = [int(cmd) if cmd.isnumeric() else cmd for cmd in re.split(r"(\d+)", cmds) if cmd]
    return board, cmds


def get_bounds(board):
    """
    Get extreme bounds of the board, use to find out if coordinate is out of bounds.
    """
    height = len(board)
    width = max(len(row) for row in board)
    bounds = {"vertical": [None for _ in range(width)],
              "horizontal": [None for _ in range(height)],
              }
    for i, row in enumerate(board):
        full_len = len(row)
        main_len = len(row.strip())
        horizontal_start_bound = full_len - main_len
        horizontal_end_bound = full_len - 1
        bounds["horizontal"][i] = [horizontal_start_bound, horizontal_end_bound]
        for j in range(horizontal_start_bound, horizontal_end_bound + 1):
            if bounds["vertical"][j] is None:
                bounds["vertical"][j] = [i, i]
            else:
                bounds["vertical"][j][1] += 1
    return bounds


def strip_board(board):
    """
    Remove leading whitespaces just to save memory space.
    Not too useful in hindsight.
    """
    for i in range(len(board)):
        board[i] = board[i].strip()


def get_leftmost_pt(board):
    """
    Get coordinate of leftmost point to use as starting point.
    CALL THIS BEFORE STRIPPING THE BOARD!
    """
    full_len = len(board[0])
    main_len = len(board[0].strip())
    return [0, full_len - main_len]


def direction2score(direction):
    """
    Convert direction to score for calculating final answer.
    """
    direction_mapper = {(0, 1): 0,  # right
                        (0, -1): 2,  # left
                        (1, 0): 1,  # down
                        (-1, 0): 3,  # up
                        }
    return direction_mapper[direction]


def get_transitions(side_len):
    """
    For part 2, can also be used for part 1 but not coded out.
    Essentially just maps an out of bound point to where it should be and change the direction appropriately.
    """
    transitions = {((side_len, 2 * side_len), (side_len, 3 * side_len - 1), (1, 0)): lambda pt: (
        (pt[1] - side_len, 2 * side_len - 1), (0, -1)),
                   ((side_len, 2 * side_len), (2 * side_len - 1, 2 * side_len), (0, 1)): lambda pt: (
                       (side_len - 1, side_len + pt[0]), (-1, 0)),
                   ((0, 3 * side_len), (side_len - 1, 3 * side_len), (0, 1)): lambda pt: (
                       (3 * side_len - pt[0] - 1, 2 * side_len - 1), (0, -1)),
                   ((2 * side_len, 2 * side_len), (3 * side_len - 1, 2 * side_len), (0, 1)): lambda pt: (
                       (3 * side_len - pt[0] - 1, 3 * side_len - 1), (0, -1)),
                   ((side_len, side_len - 1), (2 * side_len - 1, side_len - 1), (0, -1)): lambda pt: (
                       (2 * side_len, pt[0] - side_len), (1, 0)),
                   ((2 * side_len - 1, 0), (2 * side_len - 1, side_len - 1), (-1, 0)): lambda pt: (
                       (side_len + pt[1], side_len), (0, 1)),
                   ((3 * side_len, side_len), (3 * side_len, 2 * side_len - 1), (1, 0)): lambda pt: (
                       (2 * side_len + pt[1], side_len - 1), (0, -1)),
                   ((3 * side_len, side_len), (4 * side_len - 1, side_len), (0, 1)): lambda pt: (
                       (3 * side_len - 1, pt[0] - 2 * side_len), (-1, 0)),
                   ((0, side_len - 1), (side_len - 1, side_len - 1), (0, -1)): lambda pt: (
                       (3 * side_len - pt[0] - 1, 0), (0, 1)),
                   ((2 * side_len, -1), (3 * side_len - 1, -1), (0, -1)): lambda pt: (
                       (3 * side_len - pt[0] - 1, side_len), (0, 1)),
                   ((-1, side_len), (-1, 2 * side_len - 1), (-1, 0)): lambda pt: ((2 * side_len + pt[1], 0), (0, 1)),
                   ((3 * side_len, -1), (4 * side_len - 1, -1), (0, -1)): lambda pt: (
                       (0, pt[0] - 2 * side_len), (1, 0)),
                   ((-1, 2 * side_len), (-1, 3 * side_len - 1), (-1, 0)): lambda pt: (
                       (4 * side_len - 1, pt[1] - 2 * side_len), (-1, 0)),
                   ((4 * side_len, 0), (4 * side_len, side_len - 1), (1, 0)): lambda pt: (
                       (0, 2 * side_len + pt[1]), (1, 0)),
                   }
    return transitions


def part1(file):
    board, cmds = read_input(file)
    bounds = get_bounds(board)
    pt = get_leftmost_pt(board)
    strip_board(board)
    direction = (0, 1)  # [0, 1]: right, [0, -1]: left, [1, 0]: down, [-1, 0]: up
    i = 0
    for cmd in cmds:
        if isinstance(cmd, str):
            # Change direction
            if direction[0] == 0:
                direction = (direction[1] if cmd == 'R' else -direction[1], 0)
            else:
                direction = (0, direction[0] if cmd == 'L' else -direction[0])
        else:
            # Move
            for _ in range(cmd):
                if direction[0] == 0:  # right or left
                    bound = bounds["horizontal"][pt[0]]
                    new_pt = [pt[0], (pt[1] - bound[0] + direction[1]) % (bound[1] - bound[0] + 1) + bound[0]]
                else:  # up or down
                    bound = bounds["vertical"][pt[1]]
                    new_pt = [(pt[0] - bound[0] + direction[0]) % (bound[1] - bound[0] + 1) + bound[0], pt[1]]
                if board[new_pt[0]][new_pt[1] - bounds["horizontal"][new_pt[0]][0]] == '#':
                    break
                pt = new_pt
            i += 1
    answer = 1000 * (pt[0] + 1) + 4 * (pt[1] + 1) + direction2score(direction)
    print(f"Part 1: {answer}")


def part2(file):
    """
    Note: This part only works for the input structure of the contents in input.in, will not work for example.in!
    Took too long to make this solution so I'm not too inclined to make a solution for a generic input...
    """
    board, cmds = read_input(file)
    side_len = len(board[-1])
    bounds = get_bounds(board)
    pt = get_leftmost_pt(board)
    strip_board(board)
    direction = (0, 1)  # [0, 1]: right, [0, -1]: left, [1, 0]: down, [-1, 0]: up
    transitions = get_transitions(side_len)
    for cmd in cmds:
        if isinstance(cmd, str):
            # Change direction
            if direction[0] == 0:
                direction = (direction[1] if cmd == 'R' else -direction[1], 0)
            else:
                direction = (0, direction[0] if cmd == 'L' else -direction[0])
        else:
            # Move
            for _ in range(cmd):
                new_direction = direction
                if direction[0] == 0:  # right or left
                    new_pt = [pt[0], pt[1] + direction[1]]
                else:  # up or down
                    new_pt = [pt[0] + direction[0], pt[1]]
                for (lower, upper, d_check), pt_map in transitions.items():
                    if lower[0] <= new_pt[0] <= upper[0] and lower[1] <= new_pt[1] <= upper[1] and d_check == direction:
                        new_pt, new_direction = pt_map(new_pt)
                        break
                if board[new_pt[0]][new_pt[1] - bounds["horizontal"][new_pt[0]][0]] == '#':
                    break
                pt = new_pt
                direction = new_direction
    answer = 1000 * (pt[0] + 1) + 4 * (pt[1] + 1) + direction2score(direction)
    print(f"Part 2: {answer}")


input_file = "input.in"
part1(input_file)
part2(input_file)

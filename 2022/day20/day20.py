def read_input(file):
    with open(file, 'r') as f:
        code = [int(num.strip()) for num in f]
    return code


def get_new_idx(i, raw_shift, code_len):
    return (raw_shift + i) % code_len


def move(code, i, zero_idx):
    """
    Used for part 1. Iterate from i onwards until we find a number that has not been visited (indicated by a 1 in its
    tuple's 2nd value). We move this number and then check if we know where 0 is. If so, we check if the movement
    affects the index of 0 and change it if necessary.
    """
    while code[i][1] == 1:  # Find a number that have not been visited
        i += 1
    raw_shift, _ = code[i]
    del code[i]
    new_idx = get_new_idx(i, raw_shift, len(code))
    code.insert(new_idx, (raw_shift, 1))
    if raw_shift == 0:  # We found 0, return its index for tracking
        zero_idx = i
    if zero_idx is not None:  # Update the index of 0 if necessary
        if i < zero_idx < new_idx:
            zero_idx -= 1
        elif i > zero_idx >= new_idx:
            zero_idx += 1
    return i, zero_idx


def brute_force(raw_code, rounds):
    """
    Used for part 2, although can be used for part 1 too. Just a brute force method since my method for part 1 will not
    work since the numbers are moved according to their original positions, not their positions after each round
    (sadly).
    """
    code = list(enumerate(raw_code))
    zero_num = (raw_code.index(0), 0)
    reference = code.copy()
    for _ in range(rounds):
        for num in reference:
            idx = code.index(num)
            del code[idx]
            new_idx = get_new_idx(idx, num[1], len(code))
            code.insert(new_idx, num)
    return code.index(zero_num), code


def part1(file):
    """
    Operates based on the fact that we are moving the numbers based on their original positions from left to right.
    Moving values will not affect the relative positions of values that have not been moved, so we can just iterate
    through the numbers and move the nearest value that have not been visited.
    """
    code = [(num, 0) for num in read_input(file)]  # 0 for not visited, 1 for visited
    i = 0
    zero_idx = None
    while i < len(code) - 1:
        i, zero_idx = move(code, i, zero_idx)
    answer = sum([code[(zero_offset + zero_idx) % len(code)][0] for zero_offset in range(1000, 4000, 1000)])
    print(f"Part 1: {answer}")


def part2(file):
    """
    Brute-forced this out since my method for part 1 will not work here since the order in which values are moved each
    round is according to the original ordering of values, not their current ordering after each round.
    """
    key = 811589153
    code = [num * key for num in read_input(file)]
    zero_idx, code = brute_force(code, 10)
    answer = sum([code[(zero_offset + zero_idx) % len(code)][1] for zero_offset in range(1000, 4000, 1000)])
    print(f"Part 2: {answer}")


input_file = "input.in"
part1(input_file)
part2(input_file)

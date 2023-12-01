from typing import Optional


def read_input(file):
    with open(file, 'r') as f:
        for line in f:
            yield line.strip()


def part1(file):
    cal_sum = 0
    lines = read_input(file)
    for line in lines:
        # Iterate from the front until number is found
        for c in line:
            if c.isnumeric():
                cal_sum += int(c) * 10
                break
        # Iterate from the back until number is found
        for i in range(len(line) - 1, -1, -1):
            if line[i].isnumeric():
                cal_sum += int(line[i])
                break
    print(f"Part 1: {cal_sum}")


def check_num(line: str, i: int) -> Optional[int]:
    """
    Check if the character at index i of the given line is a number or the start of a number word.
    Return number/word value if found.
    """
    letters = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
    if line[i].isnumeric():
        return int(line[i])
    else:
        for letter in letters:
            if line[i:i + len(letter)] == letter:
                return letters[letter]
    return None


def part2(file):
    cal_sum = 0
    lines = read_input(file)
    for line in lines:
        # Iterate forward until number/word is found
        for i in range(len(line)):
            val = check_num(line, i)
            if val:
                cal_sum += val * 10
                break
        # Iterate backwards until number/word is found
        for i in range(len(line) - 1, -1, -1):
            val = check_num(line, i)
            if val:
                cal_sum += val
                break
    print(f"Part 2: {cal_sum}")


file = "input.in"
part1(file)
part2(file)

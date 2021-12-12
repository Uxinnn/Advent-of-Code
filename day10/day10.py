def read_input():
    file = open('input.in', 'r')
    lines = [line.strip() for line in file.readlines()]
    return lines


def get_and_filter_corrupted(lines):
    corrupted_count = {')': 0, ']': 0, '}': 0, '>': 0}
    corrupted_index = []
    for i in range(len(lines)):
        line = lines[i]
        stack = []
        for bracket in line:
            if bracket == '(' or bracket == '[' or bracket == '{' or bracket == '<':
                stack.append(bracket)
            elif (bracket == ')' and stack[-1] == '(') or\
                    (bracket == ']' and stack[-1] == '[') or\
                    (bracket == '}' and stack[-1] == '{') or\
                    (bracket == '>' and stack[-1] == '<'):
                del stack[-1]
            else:
                corrupted_count[bracket] += 1
                corrupted_index.append(i)
                break
    for i in corrupted_index[::-1]:
        del lines[i]
    return corrupted_count


def get_corrupted_score(corrupted_count):
    score = corrupted_count[')'] * 3 + \
            corrupted_count[']'] * 57 + \
            corrupted_count['}'] * 1197 + \
            corrupted_count['>'] * 25137
    return score


def auto_complete(lines):
    completed_lines = []
    for line in lines:
        stack = []
        for bracket in line:
            if bracket == '(' or bracket == '[' or bracket == '{' or bracket == '<':
                stack.append(bracket)
            elif (bracket == ')' and stack[-1] == '(') or \
                    (bracket == ']' and stack[-1] == '[') or \
                    (bracket == '}' and stack[-1] == '{') or \
                    (bracket == '>' and stack[-1] == '<'):
                del stack[-1]
            else:
                print("ERROR")
                break
        completed_lines.append(stack)
    return completed_lines


def get_score(stack):
    points = {'(': 1, '[': 2, '{': 3, '<': 4}
    score = 0
    for bracket in stack[::-1]:
        score *= 5
        score += points[bracket]
    return score


def get_scores(stacks):
    return [get_score(stack) for stack in stacks]


def get_middle_score(scores):
    scores.sort()
    return scores[len(scores)//2]


def part1():
    lines = read_input()
    corrupted_count = get_and_filter_corrupted(lines)
    score = get_corrupted_score(corrupted_count)
    print(f"Part 1: {score}")


def part2():
    lines = read_input()
    _ = get_and_filter_corrupted(lines)
    stacks = auto_complete(lines)
    scores = get_scores(stacks)
    middle_score = get_middle_score(scores)
    print(f"Part 2: {middle_score}")


if __name__ == "__main__":
    part1()
    part2()

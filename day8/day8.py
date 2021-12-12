def read_input():
    file = open('input.in', 'r')
    entries = [line.strip().split(" | ") for line in file.readlines()]
    for i in range(len(entries)):
        entry = entries[i]
        patterns = entry[0].split()
        output = entry[1].split()
        entries[i] = [patterns, output]
    return entries


def get_number_of_1478(entries):
    output_values = [value for entry in entries for value in entry[1]]
    length_of_output_values = [len(value) for value in output_values]
    total_count = length_of_output_values.count(2)\
                  + length_of_output_values.count(4)\
                  + length_of_output_values.count(3)\
                  + length_of_output_values.count(7)
    return total_count


def init_number_map():
    number_map = dict()
    return number_map


def get_1478(patterns, number_map):
    updated_patterns = []
    for pattern in patterns:
        pattern_length = len(pattern)
        if pattern_length == 2:
            number_map[1] = pattern
        elif pattern_length == 4:
            number_map[4] = pattern
        elif pattern_length == 3:
            number_map[7] = pattern
        elif pattern_length == 7:
            number_map[8] = pattern
        else:
            updated_patterns.append(pattern)
    return updated_patterns


def split_length(patterns):
    length_5 = [pattern for pattern in patterns if len(pattern) == 5]
    length_6 = [pattern for pattern in patterns if len(pattern) == 6]
    return length_5, length_6


def get_3(length_5, number_map):
    pattern = None
    for i in range(len(length_5)):
        pattern = length_5[i]
        if len(set(pattern) & set(number_map[1])) == 2:
            break
    number_map[3] = pattern
    length_5.remove(pattern)


def get_9(length_6, number_map):
    pattern = None
    for i in range(len(length_6)):
        pattern = length_6[i]
        if len(set(pattern) & set(number_map[3])) == 5:
            break
    number_map[9] = pattern
    length_6.remove(pattern)


def get_5_2(length_5, number_map):
    pattern5 = None
    pattern2 = None
    for i in range(len(length_5)):
        pattern = length_5[i]
        if len(set(pattern) & set(number_map[9])) == 4:
            pattern2 = pattern
        elif len(set(pattern) & set(number_map[9])) == 5:
            pattern5 = pattern
    number_map[2] = pattern2
    number_map[5] = pattern5
    length_5.remove(pattern2)
    length_5.remove(pattern5)


def get_6_0(length_6, number_map):
    pattern0 = None
    pattern6 = None
    for i in range(len(length_6)):
        pattern = length_6[i]
        if len(set(pattern) & set(number_map[5])) == 5:
            pattern6 = pattern
        elif len(set(pattern) & set(number_map[5])) == 4:
            pattern0 = pattern
    number_map[0] = pattern0
    number_map[6] = pattern6
    length_6.remove(pattern0)
    length_6.remove(pattern6)


def decode_number(values, inv_map):
    number = 0
    for value in values:
        value = ''.join(sorted(value))
        number = number*10 + inv_map[value]
    return number


def decode_all(entries, number_map):
    decoded_numbers = []
    for entry in entries:
        patterns = entry[0]
        values = entry[1]
        updated_patterns = get_1478(patterns, number_map)
        length_5, length_6 = split_length(updated_patterns)
        get_3(length_5, number_map)
        get_9(length_6, number_map)
        get_5_2(length_5, number_map)
        get_6_0(length_6, number_map)
        inv_map = {''.join(sorted(v)): k for k, v in number_map.items()}
        decoded_numbers.append(decode_number(values, inv_map))
    return sum(decoded_numbers)


def part1():
    entries = read_input()
    total_count = get_number_of_1478(entries)
    print(f"Part 1: {total_count}")


def part2():
    entries = read_input()
    number_map = init_number_map()
    sum_of_numbers = decode_all(entries, number_map)
    print(f"Part 2: {sum_of_numbers}")


if __name__ == "__main__":
    part1()
    part2()

def read_input():
    file = open('input.in', 'r')
    lines = [line.strip() for line in file.readlines()]
    return lines


def get_count_at_index(idx, numbers):
    zero_count = 0
    one_count = 0
    for number in numbers:
        if number[idx] == '0':
            zero_count += 1
        else:
            one_count += 1
    return zero_count, one_count


def get_gamma_epsilon(numbers, most_common):
    n = len(numbers[0])
    rate_base2 = ""
    for idx in range(n):
        zero_count, one_count = get_count_at_index(idx, numbers)
        if zero_count > one_count:
            rate_base2 += '0' if most_common else '1'
        else:
            rate_base2 += '1' if most_common else '0'
    rate = int(rate_base2, 2)
    return rate


def get_o2_co2(numbers, is_o2):
    n = len(numbers[0])
    for idx in range(n):
        zero_count, one_count = get_count_at_index(idx, numbers)
        if is_o2:
            value_to_keep = '0' if zero_count > one_count else '1'
        else:
            value_to_keep = '0' if zero_count <= one_count else '1'
        numbers = [number for number in numbers if number[idx] == value_to_keep]
        if len(numbers) == 1:
            break
    rate = int(numbers[0], 2)
    return rate


def part1():
    numbers = read_input()
    gamma = get_gamma_epsilon(numbers, True)
    epsilon = get_gamma_epsilon(numbers, False)
    print(gamma, epsilon, gamma * epsilon)


def part2():
    numbers = read_input()
    o2 = get_o2_co2(numbers, True)
    co2 = get_o2_co2(numbers, False)
    print(o2, co2, o2 * co2)


if __name__ == "__main__":
    part1()
    part2()

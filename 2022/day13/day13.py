def read_input(file):
    with open(file, 'r') as f:
        packets = [eval(line.strip()) for line in f if line.strip() != '']
    return packets


def compare_packets(left, right):
    # Cast int to list if comparing between int and list
    if type(left) == int and type(right) == list:
        left = [left]
    elif type(left) == list and type(right) == int:
        right = [right]
    # Compare each element pair between left and right packets
    for left_element, right_element in zip(left, right):
        if type(left_element) == list or type(right_element) == list:
            val = compare_packets(left_element, right_element)
        else:
            # Both are ints
            val = left_element - right_element
        # If non-zero, return value, else continue checking next element
        if val:
            return val
    return len(left) - len(right)


def part1(file):
    packets = read_input(file)
    answer = sum([i // 2 + 1 for i in range(0, len(packets), 2) if compare_packets(packets[i], packets[i + 1]) < 0])
    print(f"Part 1: {answer}")


def part2(file):
    packets = read_input(file)
    start_idx, end_idx = 1, 2
    start_divider, end_divider = [[2]], [[6]]
    for packet in packets:
        start_packet_diff = compare_packets(packet, start_divider)
        end_packet_diff = compare_packets(packet, end_divider)
        end_idx += 1 if end_packet_diff < 0 else 0
        start_idx += 1 if start_packet_diff < 0 else 0
    print(f"Part 2: {start_idx * end_idx}")


file = "input.in"
part1(file)
part2(file)

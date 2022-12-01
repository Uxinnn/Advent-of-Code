from functools import reduce


def read_input():
    with open("input.in", "r") as file:
        hex_message = file.readline().strip()
    message_size = len(hex_message) * 4
    return bin(int(hex_message, 16))[2:].zfill(message_size)


def decode(message, message_board):
    version = int(message[:3], 2)
    type_id = int(message[3:6], 2)
    if type_id == 4:
        # Literal value
        val, end_idx = decode_literal(message)
        add_to_message_board(version, type_id, message_board, val)
    else:
        sub_message_board = []
        if message[6] == '0':
            sub_packets_length = int(message[7:22], 2) + 22
            end_idx = 22
            add_to_message_board(version, type_id, sub_message_board)
            # decode sub packets with total length defined
            while end_idx < sub_packets_length:
                end_idx += decode(message[end_idx:sub_packets_length], sub_message_board)
            message_board.append(sub_message_board)
        elif message[6] == '1':
            sub_packets_number = int(message[7:18], 2)
            add_to_message_board(version, type_id, sub_message_board)
            packet_start = 18
            # decode sub packets with number of sub packets defined
            while sub_packets_number > 0:
                packet_start += decode(message[packet_start:], sub_message_board)
                sub_packets_number -= 1
            message_board.append(sub_message_board)
            end_idx = packet_start
    return end_idx


def decode_literal(message):
    binary_val = ""
    i = 6
    while True:
        binary_val += message[i + 1:i + 5]
        if message[i] == '0':
            break
        i += 5
    return int(binary_val, 2), i + 5


def add_to_message_board(version, type_id, message_board, literal=0):
    third_param = None
    if type_id == 0:
        third_param = sum
    elif type_id == 1:
        third_param = prod
    elif type_id == 2:
        third_param = min
    elif type_id == 3:
        third_param = max
    elif type_id == 4:
        third_param = literal
    elif type_id == 5:
        third_param = gt
    elif type_id == 6:
        third_param = lt
    elif type_id == 7:
        third_param = eq
    message_board.append((version, type_id, third_param))


def compute_packets(message_board):
    op = message_board[0][2]  # Contains math operator
    for i in range(1, len(message_board)):
        message_board[i] = compute_packets(message_board[i]) if isinstance(message_board[i], list) else message_board[i][2]
    return op(message_board[1:])


def sum_versions(message_board):
    return sum([sum_versions(entry) if isinstance(entry, list) else entry[0] for entry in message_board])


def prod(params):
    return reduce(lambda x, y: x * y, params)


def lt(params):
    return int(params[0] < params[1])


def gt(params):
    return int(params[0] > params[1])


def eq(params):
    return int(params[0] == params[1])


def part1():
    message = read_input()
    message_board = []
    decode(message, message_board)
    version_sum = sum_versions(message_board[0])
    print(f"Part 1: {version_sum}")


def part2():
    message = read_input()
    message_board = []
    decode(message, message_board)
    value = compute_packets(message_board[0])
    print(f"Part 2: {value}")


if __name__ == "__main__":
    part1()
    part2()

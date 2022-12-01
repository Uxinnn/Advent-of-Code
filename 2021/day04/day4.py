LENGTH_OF_BOARD = 5


def read_file():
    with open("input.in", "r") as file:
        numbers = tuple(map(int, file.readline().strip().split(",")))
        file.readline()
        list_of_board = []
        board = []
        for line in file.readlines():
            line = line.strip()
            if line == "":
                list_of_board.append(board)
                board = []
            else:
                board.append(list(map(int, line.split())))
        list_of_board.append(board)
    return numbers, list_of_board


def check_win(shadow_board):
    for row in shadow_board:
        if sum(row) == LENGTH_OF_BOARD:
            return True
    transposed_shadow_board = list(map(list, zip(*shadow_board)))
    for row in transposed_shadow_board:
        if sum(row) == LENGTH_OF_BOARD:
            return True
    return False


# Returns index of board that have won. If no board has won, return -1
def check_all_win(shadow_boards):
    winning_boards = []
    number_of_boards = len(shadow_boards)
    for i in range(number_of_boards):
        shadow_board = shadow_boards[i]
        if check_win(shadow_board):
            winning_boards.append(i)
    return winning_boards


def create_shadow_boards(boards):
    number_of_boards = len(boards)
    return [[[0]*5 for _ in range(LENGTH_OF_BOARD)] for _ in range(number_of_boards)]


def mark_board(number, boards, shadow_boards):
    number_of_boards = len(boards)
    for i in range(number_of_boards):
        for j in range(LENGTH_OF_BOARD):
            for k in range(LENGTH_OF_BOARD):
                if number == boards[i][j][k]:
                    shadow_boards[i][j][k] = 1
    return shadow_boards


def find_winner(numbers, boards, shadow_boards):
    past_numbers = set()
    for number in numbers:
        past_numbers.add(number)
        shadow_boards = mark_board(number, boards, shadow_boards)
        list_of_winning_index = check_all_win(shadow_boards)
        if len(list_of_winning_index) == 0:
            continue
        winner_index = list_of_winning_index[0]
        return number, past_numbers, boards[winner_index]
    return None, None, None


def find_loser(numbers, boards, shadow_boards):
    last_winning_number_index = -1
    last_winner = None
    for i in range(len(numbers)):
        number = numbers[i]
        shadow_boards = mark_board(number, boards, shadow_boards)
        list_of_winning_index = check_all_win(shadow_boards)
        if len(list_of_winning_index) != 0:
            last_winning_number_index = i
            last_winner = boards[list_of_winning_index[-1]]
        list_of_winning_index = list_of_winning_index[::-1]
        for winner_index in list_of_winning_index:
            del boards[winner_index]
            del shadow_boards[winner_index]
    # print(last_winner)
    # print(shadow_boards[winner_index])
    # print(last_winning_number_index, numbers[last_winning_number_index])
    # print(numbers[:last_winning_number_index])
    number = numbers[last_winning_number_index]
    past_numbers = numbers[:last_winning_number_index + 1]
    return number, past_numbers, last_winner


def get_result(number, past_numbers, winning_board):
    # Find sum of all numbers on board
    total_sum = sum([sum(row) for row in winning_board])
    flattened_board = [digit for row in winning_board for digit in row]
    sum_of_unmarked_numbers = total_sum
    for past_number in past_numbers:
        if past_number in flattened_board:
            sum_of_unmarked_numbers -= past_number
    return sum_of_unmarked_numbers * number


def print_boards(boards):
    for i in range(len(boards)):
        board = boards[i]
        print("Index: " + str(i))
        for row in board:
            print(row)
        print("\n")


def part1():
    numbers, boards = read_file()
    shadow_boards = create_shadow_boards(boards)
    number, past_numbers, winning_board = find_winner(numbers, boards, shadow_boards)
    print(f"Part 1 Answer: {get_result(number, past_numbers, winning_board)}")


def part2():
    numbers, boards = read_file()
    shadow_boards = create_shadow_boards(boards)
    number, past_numbers, losing_board = find_loser(numbers, boards, shadow_boards)
    print(f"Part 2 Answer: {get_result(number, past_numbers, losing_board)}")


if __name__ == "__main__":
    part1()
    part2()

import heapq


# Read input into a string
def read_input():
    with open("input.in", "r") as file:
        return ''.join([x for x in file.read() if x in 'ABCD.'])


# Check if the corridor path from source index to destination index is
# blocked. Only for corridor movement.
def blocked(src_idx, dst_idx, puzzle):
    direction = 1 if src_idx < dst_idx else -1
    for corr_idx in range(src_idx + direction, dst_idx + direction, direction):
        if puzzle[corr_idx] != '.':
            return True
    return False


# Implement the move from source index to destination index and return
# an updated puzzle
def do_move(src_idx, dst_idx, puzzle):
    tmp = list(puzzle)
    tmp[src_idx], tmp[dst_idx] = tmp[dst_idx], tmp[src_idx]
    return ''.join(tmp)


# rm_pos: index of the room in the corridor
# returns the possible corridor positions an amphipod can take after it
# moves out of its room.
def get_possible_corr_pos(puzzle, rm_pos, corr_pos):
    return [pos for pos in corr_pos if not blocked(rm_pos, pos, puzzle)]


# Check each amphipod in the corridor if it can move into their room.
# If so, return the move in the form:
# (number of steps needed, source index, destination index)
def push_room(puzzle, rm_len, pos):
    amp2rm_num = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    amp = puzzle[pos]
    rm_num = amp2rm_num[amp]
    rm_pos = (rm_num + 1) * 2
    rm = ''.join([puzzle[11 + (4 * i) + rm_num] for i in range(rm_len)])
    if not blocked(pos, rm_pos, puzzle):
        for i in range(rm_len):  # i represents number of amphipods (of the same type) in the room
            if rm == '.' * (rm_len - i) + amp * i:
                steps = abs(rm_pos - pos) + (rm_len - i)
                dst_idx = 11 + (4 * (rm_len - 1 - i)) + rm_num
                return steps, pos, dst_idx
    return None


# Check if any amphipod in the rooms can move into the corridor.
# if so, return the possible moves the amphipod can make in the form:
# (number of steps needed, source index, destination index)
def pop_room(puzzle, rm_len, corr_pos, rm_idx):
    rm_num2amp = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    amps = ''.join([puzzle[11 + (4 * x) + rm_idx] for x in range(rm_len)])

    # Check if the amphipod in the room can move out
    can_pop_room = not any([amps == '.' * i + rm_num2amp[rm_idx] * (rm_len - i) for i in range(rm_len + 1)])
    if can_pop_room:
        for j in range(rm_len):
            rm_pos = rm_idx + 11 + (4 * j)  # Index of the position in the room
            if puzzle[rm_pos] != '.':
                steps_to_room_front = j + 1
                dst_poses = get_possible_corr_pos(puzzle, (rm_idx + 1) * 2, corr_pos)
                # Moves that the amphipod that moves out of its room can do
                return [(steps_to_room_front + abs((rm_idx + 1) * 2 - pos), rm_pos, pos) for pos in dst_poses]
    return []


# Get all moves that amphipods in the rooms can make
def get_moves_to_corr(puzzle, rm_len, corr_pos):
    moves = [move for i in range(4) for move in pop_room(puzzle, rm_len, corr_pos, i)]
    return moves


# Get all moves that amphipods in the corridor can make
def get_moves_from_corr(puzzle, rm_len, corr_pos):
    moves = [push_room(puzzle, rm_len, i) for i in corr_pos if puzzle[i] != '.']
    moves = [move for move in moves if move is not None]
    return moves


# Convert number of steps to energy required for each move
def steps2energy(moves, puzzle):
    multiplier = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    moves_w_energy = []
    for move in moves:
        amp = puzzle[move[1]]
        energy = multiplier[amp] * move[0]
        moves_w_energy.append((energy, move[1], move[2]))
    return moves_w_energy


# Get all next moves that are possible given a puzzle.
def get_moves(puzzle, rm_len):
    corr_pos = [0, 1, 3, 5, 7, 9, 10]
    # Each move is of the form (number of steps, source position, destination position)
    moves = get_moves_to_corr(puzzle, rm_len, corr_pos) + get_moves_from_corr(puzzle, rm_len, corr_pos)
    # Convert steps in each move to energy required
    moves = steps2energy(moves, puzzle)
    return moves


# Runs dijkstra's algorithm to find the least amount energy required
# to reach the final puzzle pattern solution.
def dijkstra(puzzle):
    rm_len = (len(puzzle) - 11) // 4
    final_pattern = '...........' + 'ABCD' * rm_len
    distances = {}
    heap = [(0, puzzle)]
    while puzzle != final_pattern:
        dist, puzzle = heapq.heappop(heap)
        if puzzle in distances:
            # puzzle have already been visited with lesser energy
            continue
        distances[puzzle] = dist
        # Get neighbours
        moves = get_moves(puzzle, rm_len)
        for m in moves:
            new_puzzle = do_move(m[1], m[2], puzzle)
            if new_puzzle not in distances:
                heapq.heappush(heap, (dist + m[0], new_puzzle))
    return distances[final_pattern]


def part1():
    puzzle = read_input()
    least_energy = dijkstra(puzzle)
    print(f"Part 1: {least_energy}")


def part2():
    puzzle = read_input()
    puzzle = puzzle[:15] + 'DCBADBAC' + puzzle[15:]
    least_energy = dijkstra(puzzle)
    print(f"Part 2: {least_energy}")


if __name__ == "__main__":
    part1()
    part2()

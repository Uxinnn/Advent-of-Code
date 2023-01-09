from heapq import heapify, heappop, heappush


def read_input(file):
    with open(file, 'r') as f:
        raw_grid = [line.strip() for line in f]
    bounds = {"min_x": 0, "max_x": len(raw_grid[0]) - 1, "min_y": 0, "max_y": len(raw_grid) - 1}
    start = (0, raw_grid[0].index('.'))
    end = (bounds["max_y"], raw_grid[bounds["max_y"]].index('.'))
    raw_blizzards = set()
    for i, row in enumerate(raw_grid):
        for j, pt in enumerate(row):
            if pt in '<>^v':
                raw_blizzards.add((i, j, pt))
    return start, end, bounds, raw_blizzards


class BlizzardSimulator:
    def __init__(self, raw_blizzard, bounds):
        self.bounds = bounds
        self.cache = dict()
        self.initial = raw_blizzard

    def get_blizzards(self, timestamp):
        if timestamp in self.cache:
            return self.cache[timestamp]
        blizzards = set()
        for start_blizzard in self.initial:
            i, j, direction = start_blizzard
            delta = timestamp if direction in 'v>' else -timestamp
            if direction in '<>':  # Left or right
                pt = (i,
                      (j - (self.bounds["min_x"] + 1) + delta) % (self.bounds["max_x"] - self.bounds["min_x"] - 1) + (
                                  self.bounds["min_x"] + 1))
            else:  # Up or down
                pt = ((i - (self.bounds["min_y"] + 1) + delta) % (self.bounds["max_y"] - self.bounds["min_y"] - 1) + (
                            self.bounds["min_y"] + 1), j)
            blizzards.add(pt)
        self.cache[timestamp] = blizzards
        return blizzards


def get_moves(pt, bounds, start, end, blizzards):
    y, x = pt
    possible_moves = {(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x), (y, x)}
    moves = list()
    for move in possible_moves:
        new_y, new_x = move
        if (new_y <= bounds["min_y"] or new_y >= bounds["max_y"] or new_x <= bounds["min_x"] or new_x >= bounds["max_x"]) and move != start and move != end:
            # Out of bounds
            continue
        if move in blizzards:
            continue
        moves.append(move)
    return moves


def get_shortest_time(start, end, repeat_time, blizzard_simulator, bounds, initial_timestamp):
    """
    A star search to find path from start to end in the shortest time.
    States in the search is encoded as (state_score, modified_timestamp, pt). Modified timestamp is
    `timestamp % time_it_takes_for_blizzard_to_repeat_itself`.
    """
    states = [(0, initial_timestamp, start)]  # states: (score, timestamp, pt)
    heapify(states)
    visited = set()
    while states:
        _, timestamp, pt = heappop(states)
        # Ran into this state earlier, discard this state since it has been visited
        if (timestamp % repeat_time, pt) in visited:
            continue
        visited.add((timestamp % repeat_time, pt))
        blizzards = blizzard_simulator.get_blizzards((timestamp + 1) % repeat_time)
        moves = get_moves(pt, bounds, start, end, blizzards)
        for move in moves:
            if move == end:  # Reached the end, return how long it took
                return timestamp + 1 - initial_timestamp
            elif ((timestamp + 1) % repeat_time, move) in visited:
                continue
            # Create new state and add it to heap
            new_timestamp = timestamp + 1
            heuristic_score = abs(move[0] - (end[0] - 1)) + abs(move[1] - end[1]) + 1
            state_score = new_timestamp + heuristic_score
            new_state = (state_score, new_timestamp, move)
            heappush(states, new_state)


def part1(file):
    start, end, bounds, raw_blizzards = read_input(file)
    blizzard_simulator = BlizzardSimulator(raw_blizzards, bounds)
    # Blizzard pattern repeats every `repeat_time` minutes, use to reduce blizzard position calculations.
    repeat_time = (bounds["max_x"] - bounds["min_x"] - 1) * (bounds["max_y"] - bounds["min_y"] - 1)
    initial_timestamp = 0
    timestamp = get_shortest_time(start, end, repeat_time, blizzard_simulator, bounds, initial_timestamp)
    print(f"Part 1: {timestamp}")


def part2(file):
    start, end, bounds, raw_blizzards = read_input(file)
    blizzard_simulator = BlizzardSimulator(raw_blizzards, bounds)
    repeat_time = (bounds["max_x"] - bounds["min_x"] - 1) * (bounds["max_y"] - bounds["min_y"] - 1)
    total_time = 0
    initial_timestamp = 0
    for src, dst in ((start, end), (end, start), (start, end)):
        timestamp = get_shortest_time(src, dst, repeat_time, blizzard_simulator, bounds, initial_timestamp)
        total_time += timestamp
        initial_timestamp = total_time
    print(f"Part 2: {total_time}")


input_file = "input.in"
part1(input_file)
part2(input_file)

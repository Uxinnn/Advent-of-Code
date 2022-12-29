"""
Since rocks and jet patterns are periodic, the same pattern and state should probably be repeated over time.
We thus store the state of the whole problem after every rock drop and check if the state has been seen before.
If so, then fast-forward the simulation since a cycle is found (The state returned to the same state after some time).
"""


def read_input(file):
    with open(file, 'r') as f:
        return f.readline().strip()


class RockGenerator:
    """
    Generates the correct rocks for each simulation round.
    """
    def __init__(self):
        self.rocks = [{(0, 0), (1, 0), (2, 0), (3, 0)},
                      {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
                      {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
                      {(0, 0), (0, 1), (0, 2), (0, 3)},
                      {(0, 0), (1, 0), (0, 1), (1, 1)}
                      ]
        self.counter = 0

    def get_rock(self, x_offset, y_offset):
        """
        Gives you the next rock to be used in the next simulation.
        :param x_offset: Shift the rock in the x direction, used to set x starting point of rock.
        :param y_offset: Shift the rock in the y direction, used to set y starting point of rock.
        :return: Rock at the correct starting point.
        """
        rock = set((x + x_offset, y + y_offset) for x, y in self.rocks[self.counter])
        self.counter = (self.counter + 1) % len(self.rocks)
        return rock

    def get_rock_idx(self):
        """
        To allow easy storing of rock generator state.
        """
        return self.counter


class JetGenerator:
    """
    Generates the correct jet for each simulation round.
    """
    def __init__(self, jet_pattern):
        self.jet_pattern = jet_pattern
        self.jet_pattern_length = len(jet_pattern)
        self.counter = 0

    def get_jet_direction(self):
        jet_direction = self.jet_pattern[self.counter]
        self.counter = (self.counter + 1) % self.jet_pattern_length
        return jet_direction

    def get_jet_index(self):
        """
        To allow easy storing of jet generator state.
        """
        return self.counter


class PatternCatcher:
    """
    Stores previous states and checks for repeated states (which indicates a cycle is found).
    """
    def __init__(self):
        self.states = dict()

    def check(self, top_chamber_state, rock_idx, jet_idx, max_height, rocks_passed):
        # Preparing new state
        top_chamber_state = list(top_chamber_state)
        top_chamber_state.sort()
        state = (str(top_chamber_state), rock_idx, jet_idx)

        # Check if new state is repeated
        if state in self.states:
            return self.states[state]
        else:
            # Store state for future checking
            # Max_height and rocks_passed are needed for fast-forwarding of simulation, thus they are stored
            self.states[state] = (max_height, rocks_passed)
            return -1, -1  # negative to indicate not found

    def clear(self):
        self.states.clear()


def clip_chamber_state(chamber_state, max_height, relative=True):
    """
    Get rocks that are at the top 100 places in height.
    :param chamber_state: Full current state.
    :param max_height: Max height of the current state.
    :param relative: Output state in relative distances instead of absolute distances.
                     Used to compare between states.
    :return: State of the chamber of the coordinates in the top 100 y values.
    """
    if relative:
        top_chamber_state = set((x, y - max_height + 100) for x, y in chamber_state if y > max_height - 100)
    else:
        top_chamber_state = set((x, y) for x, y in chamber_state if y > max_height - 100)
    return top_chamber_state


def move_rock(chamber_state, rock, jet_direction):
    # left or right
    updated_rock = set((x - 1 if jet_direction == '<' else x + 1, y) for x, y in rock)
    if (((jet_direction == '<' and min((x for x, y in updated_rock)) > -1) or
         (jet_direction == '>' and max((x for x, y in updated_rock)) < 7)) and
            not updated_rock & chamber_state):
        rock = updated_rock
    # drop
    updated_rock = set((x, y - 1) for x, y in rock)
    if updated_rock & chamber_state or min((y for x, y in updated_rock)) < 0:
        # rest
        return rock, False
    else:
        rock = updated_rock
        return rock, True


def simulate(jet_pattern, num_rocks):
    rock_generator = RockGenerator()
    jet_generator = JetGenerator(jet_pattern)
    pattern_checker = PatternCatcher()
    max_height = -1
    chamber_state = set()
    i = 0
    while i < num_rocks:
        rock = rock_generator.get_rock(2, max_height + 4)
        is_moving = True
        while is_moving:
            jet_direction = jet_generator.get_jet_direction()
            rock, is_moving = move_rock(chamber_state, rock, jet_direction)
        chamber_state.update(rock)
        max_height = max(max_height, max([y for x, y in rock]))
        # Check if cycles
        matched_height, old_i = pattern_checker.check(clip_chamber_state(chamber_state, max_height),
                                                      rock_generator.get_rock_idx(),
                                                      jet_generator.get_jet_index(),
                                                      max_height,
                                                      i,
                                                      )
        if matched_height > 0:
            # Speed up here
            height_interval = max_height - matched_height
            rocks_interval = i - old_i
            num_repeats = (num_rocks - i) // rocks_interval
            i += num_repeats * rocks_interval
            chamber_state = set((x, y + num_repeats * height_interval) for x, y in clip_chamber_state(chamber_state,
                                                                                                      max_height,
                                                                                                      relative=False,
                                                                                                      )
                                )
            max_height += num_repeats * height_interval
            pattern_checker.clear()

        i += 1

    # print(pattern_checker.states)
    return max_height + 1


def part1(file):
    jet_pattern = read_input(file)
    num_rocks = 2022
    max_height = simulate(jet_pattern, num_rocks)
    print(f"Part 1: {max_height}")


def part2(file):
    jet_pattern = read_input(file)
    num_rocks = 1000000000000
    max_height = simulate(jet_pattern, num_rocks)
    print(f"Part 2: {max_height}")


input_file = "input.in"
part1(input_file)
part2(input_file)

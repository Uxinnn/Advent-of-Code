"""
Got quite abit of help from https://www.youtube.com/watch?v=H3PSODv4nf0&t=323s and reddit.
Essentially you have to enumerate through all possible states to find the maximum geodes that can be produced.
Key question to solve is how to optimize the search via branch-and-bound.
"""
import re
from math import ceil


def read_input(file):
    """
    Parses input into blueprints. Blueprints are of the form (ore_bot_cost, clay_bot_cost, obsidian_bot_cost,
    geode_bot_cost). Ore, clay, and obsidian are encoded into indexes 0, 1, and 2 respectively. Each cost field is
    specified in (r_count, r_type), where r_count refers to the amount of resource needed and r_type refers to the type
    of resource needed, encoded as a resource index (0, 1, or 2).
    """
    blueprints = list()
    resource_types = ["ore", "clay", "obsidian"]
    regex_expr = "(\\d+) (\\w+)"
    with open(file, 'r') as f:
        for line in f:
            tmp = [(int(count), resource_types.index(resource)) for count, resource in re.findall(regex_expr, line)]
            blueprint = ((tmp[0],), (tmp[1],), (tmp[2], tmp[3]), (tmp[4], tmp[5]))
            blueprints.append(blueprint)
    return blueprints


def get_max_costs(blueprint):
    """
    For each resource, find the maximum amount needed to create any bot.
    """
    max_costs = [0, 0, 0]
    for bot_bp in blueprint:
        for r_cost, r_type in bot_bp:
            max_costs[r_type] = max(max_costs[r_type], r_cost)
    return max_costs


def get_upper_bound(state):
    """
    Get the maximum possible geodes a state can produce.
    Found by adding an extra geode bot for each remaining time stamp.
    """
    bots, resources, time_left = state
    upper_bound = resources[3] + sum(bots[3] + i for i in range(time_left))
    return upper_bound


def get_max_geodes(blueprint, bots, resources, time_left):
    max_costs = get_max_costs(blueprint)
    states_stack = [(bots, resources, time_left)]
    max_geodes = 0
    visited = set()  # Store previously evaluated states to prevent repeated calculations.
    while states_stack:
        state = states_stack.pop()
        visited.add(state)
        bots, resources, time_left = state
        max_geodes = max(max_geodes, resources[3] + bots[3] * time_left)
        for i, bot_cost in enumerate(blueprint):
            # Optimization 1: We do not need more bots than the maximum amount of resources needed.
            # E.g. If we need at most 4 ore to create any type of bots, then we just need at most 4 ore bots.
            if i != 3 and bots[i] >= max_costs[i]:
                continue

            time_needed = 0
            for r_count, r_type in bot_cost:
                # No bots of a particular resource means that you cannot produce the said resource. This means that
                # other bots that require the said resource cannot be produced either.
                if bots[r_type] == 0:
                    break
                # Finding the time needed to create each bot
                time_needed = max(time_needed, ceil((r_count - resources[r_type]) / bots[r_type]))
            else:
                time_needed += 1  # +1 to account of the time needed to create a bot.
                new_time_left = time_left - time_needed
                if new_time_left <= 0:  # Ran out of time
                    continue
                # Creating new state with updated resources and bots
                new_resources = [resources[j] + bots[j] * time_needed for j in range(4)]
                for r_count2, r_type2 in bot_cost:
                    new_resources[r_type2] -= r_count2
                new_bots = list(bots)
                new_bots[i] += 1
                # Optimization 2: If we cannot possibly spend all the resources we have in the remaining time, then
                # remove all extra resources. This reduces the possible states we have and speed things up.
                # E.g. If we have 5 minutes left and all bots need at most 4 ore to create, but we have 30 ore, then we
                # can spend at most 20 ore in the remaining time. We can thus throw away 10 ore without any
                # consequences.
                for j in range(3):
                    new_resources[j] = min(max_costs[j] * new_time_left, new_resources[j])

                new_state = (tuple(new_bots), tuple(new_resources), new_time_left)
                # Optimization 3: If new state have been seen before, then we have previously calculated how much
                # geodes the state will produce. There is no need to calculate it again. So we can safely ignore this
                # duplicate state.
                if new_state in visited:
                    continue
                # Optimization 4: If the maximum possible number of geodes that can be produce by a state is lesser
                # than the maximum geodes that we know can be produce, then just ignore this state since it cannot
                # possibly create more geodes than our current max.
                # (The upper bound is lesser than our currently known best value, so we can safely ignore this state)
                if get_upper_bound(new_state) < max_geodes:
                    continue

                states_stack.append(new_state)
    return max_geodes


def part1(file):
    blueprints = read_input(file)
    start_bots = (1, 0, 0, 0)
    start_resources = (0, 0, 0, 0)
    start_time = 24
    quality_sum = 0
    for i, blueprint in enumerate(blueprints):
        quality_sum += (i + 1) * get_max_geodes(blueprint, start_bots, start_resources, start_time)
    print(f"Part 1: {quality_sum}")


def part2(file):
    blueprints = read_input(file)[:3]
    start_bots = (1, 0, 0, 0)
    start_resources = (0, 0, 0, 0)
    start_time = 32
    answer = 1
    for blueprint in blueprints:
        answer *= get_max_geodes(blueprint, start_bots, start_resources, start_time)
    print(f"Part 2: {answer}")


input_file = "input.in"
part1(input_file)
part2(input_file)

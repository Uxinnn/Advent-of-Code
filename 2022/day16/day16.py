"""
Valves are encoded as binary numbers to make things faster (1, 10, 100, 1000, ...).
Code will be very slow without removing valves with 0 flow rate since they increase the search space by a lot.
"""


from math import inf


def read_input(file):
    with open(file, 'r') as f:
        lines = [line.strip().split() for line in f]
        valve2idx = {line[1]: 1 << i for i, line in enumerate(lines)}
        flow_rates = {valve2idx[line[1]]: int(line[4][:-1].split('=')[1]) for line in lines}
        tunnels = {valve2idx[line[1]]: list(map(valve2idx.get, [tunnel if tunnel[-1] != ',' else tunnel[:-1]
                                                                for tunnel in line[9:]
                                                                ]))
                   for line in lines
                   }
    return flow_rates, tunnels, valve2idx


def get_travel_costs(tunnels):
    """
    Run floyd warshall algorithm to get the shortest cost path from 1 valve to another.
    """
    valves = tunnels.keys()
    travel_costs = {src: {dst: inf if src != dst else 0 for dst in valves} for src in valves}
    for src, dsts in tunnels.items():
        for dst in dsts:
            travel_costs[src][dst] = 1
    for k in valves:
        for i in valves:
            for j in valves:
                travel_costs[i][j] = min(travel_costs[i][j], travel_costs[i][k] + travel_costs[k][j])
    return travel_costs


def remove_dead_valves(start_valve, flow_rates, travel_costs):
    """
    Remove valves with flow rate of 0 since we would not stop at them.
    Helps to reduce search space (And make the code run in reasonable amounts of time since there are
    alot of valves with 0 flow rate in the input).
    """
    dead_valves = [valve_idx for valve_idx, flow_rate in flow_rates.items() if flow_rate == 0]
    for valve_idx in dead_valves:
        del flow_rates[valve_idx]
        if valve_idx != start_valve:
            del travel_costs[valve_idx]
        for src in travel_costs:
            del travel_costs[src][valve_idx]


def find_flow(src, state, flow, remaining_time, flow_rates, travel_costs, answer):
    """
    Get the maximum possible flow for each state.
    :param src: Valve that we are not at.
    :param state: State of valves (Whether they have been visited or not).
    :param flow: Current accumulated flow.
    :param remaining_time: How much time is left to open other valves.
    :param flow_rates: Dictionary containing flow rates of all valves.
    :param travel_costs: Contains value of shortest cost path from 1 valve to another.
    :param answer: Stores the maximum flow that is possible for each state.
    :return: The parameter answer.
    """
    answer[state] = max(answer.get(state, 0), flow)
    for next_valve in flow_rates:
        updated_remaining_time = remaining_time - travel_costs[src][next_valve] - 1
        if state & next_valve or updated_remaining_time < 1:
            continue
        find_flow(next_valve,
                  state | next_valve,
                  flow + flow_rates[next_valve] * updated_remaining_time,
                  updated_remaining_time,
                  flow_rates,
                  travel_costs,
                  answer,
                  )
    return answer


def part1(file):
    flow_rates, tunnels, valve2idx = read_input(file)
    travel_costs = get_travel_costs(tunnels)
    start_valve, state, flow, remaining_time, answer = "AA", 0, 0, 30, dict()
    src = valve2idx[start_valve]
    remove_dead_valves(src, flow_rates, travel_costs)
    flows = find_flow(src, state, flow, remaining_time, flow_rates, travel_costs, answer)
    max_flow = max(flows.values())
    print(f"Part 1: {max_flow}")


def part2(file):
    flow_rates, tunnels, valve2idx = read_input(file)
    travel_costs = get_travel_costs(tunnels)
    start_valve, state, flow, remaining_time, answer = "AA", 0, 0, 26, dict()
    src = valve2idx[start_valve]
    remove_dead_valves(src, flow_rates, travel_costs)
    flows = find_flow(src, state, flow, remaining_time, flow_rates, travel_costs, answer)
    max_flow = max([flow1 + flow2
                    for state1, flow1 in flows.items()
                    for state2, flow2 in flows.items()
                    if not state1 & state2
                    ])
    print(f"Part 2: {max_flow}")


input_file = "input.in"
part1(input_file)
part2(input_file)

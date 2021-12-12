from collections import defaultdict


def read_input():
    with open("input.in", "r") as file:
        links = defaultdict(set)
        for a, b in [line.strip().split('-') for line in file.readlines()]:
            links[a].add(b)
            links[b].add(a)
    return links


def step(links, connections, full_connections, is_part_1):
    connection, flag = connections.pop()
    last_node = connection[-1]
    for link in links[last_node]:
        if (link == "start") or (link.islower() and (is_part_1 or flag) and link in connection):
            continue
        new_connection = connection.copy()
        new_connection.append(link)
        if link == "end":
            full_connections.add(tuple(new_connection))
            continue
        if is_part_1:
            connections.append([new_connection, flag])
        else:
            if link.islower() and new_connection.count(link) == 2:
                connections.append([new_connection, not flag])
            else:
                connections.append([new_connection, flag])
    return


def list_connections_part1(links, is_part_1):
    connections = [[["start", dst], False] for dst in links["start"]]
    full_connections = set()
    while connections:
        step(links, connections, full_connections, is_part_1)
    return full_connections


def part1():
    links = read_input()
    full_connections = list_connections_part1(links, True)
    print(f"Part 1: {len(full_connections)}")


def part2():
    links = read_input()
    full_connections = list_connections_part1(links, False)
    print(f"Part 2: {len(full_connections)}")


if __name__ == "__main__":
    part1()
    part2()

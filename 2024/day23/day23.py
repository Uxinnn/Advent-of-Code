from collections import defaultdict


def read_input(file):
  with open(file, 'r') as f:
    adj_list = defaultdict(set)
    for line in f.readlines():
      c1, c2 = line.strip().split('-')
      adj_list[c1].add(c2)
      adj_list[c2].add(c1)
  return adj_list


def get_3_lans(adj_list, vertex):
  lans = set()
  pairs = {(vertex, neighbor) for neighbor in adj_list[vertex]}
  for v1, v2 in pairs:
    for neighbor in adj_list[v1]:
      if neighbor != v2 and v2 in adj_list[neighbor]:
        lan = tuple(sorted((v1, v2, neighbor)))
        lans.add(lan)
  return lans


def get_maximal_lans(r, p, x, adj_list, results):
  # bron_kerbosch to get all maximal cliques
  # See: https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
  #      https://github.com/alanmc-zz/python-bors-kerbosch/blob/master/bors-kerbosch.py
  if not p and not x:
    results.append(sorted(r))
    return
  vertices = p.copy()
  for vertex in vertices:
    get_maximal_lans(r | {vertex},
                     p & adj_list[vertex],
                     x & adj_list[vertex],
                     adj_list,
                     results,
                     )
    p.remove(vertex)
    x.add(vertex)


def part1(file):
  adj_list = read_input(file)
  lans = set()
  for vertex in adj_list:
    if vertex[0] == 't':
      lans |= get_3_lans(adj_list, vertex)
  count = len(lans)
  print(f"Part 1: {count}")


def part2(file):
  adj_list = read_input(file)
  results = list()
  get_maximal_lans(set(), set(adj_list.keys()), set(), adj_list, results)
  max_lan = max(results, key=lambda x: len(x))
  passwd = ",".join(max_lan)
  print(f"Part 2: {passwd}")


file = "input.in"
part1(file)
part2(file)

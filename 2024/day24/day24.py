import graphviz


def read_input(file):
  with open(file, 'r') as f:
    line = f.readline().strip()
    init_vals = dict()
    while line:
      wire, val = line.split(': ')
      init_vals[wire] = int(val)
      line = f.readline().strip()
    conns = dict()
    for line in f.readlines():
      line = line.strip().split()
      w1, op, w2, _, w3 = line
      conns[w3] = (op, w1, w2)
  return init_vals, conns


def get_val(wire, vals, conns):
  if wire in vals.keys():
    return vals[wire]
  op, w1, w2 = conns[wire]
  if op == "AND":
    op = lambda x, y: x & y
  elif op == "OR":
    op = lambda x, y: x | y
  else:
    op = lambda x, y: x ^ y
  val = op(get_val(w1, vals, conns), get_val(w2, vals, conns))
  vals[wire] = val
  return val


def simulate(vals, conns):
  for wire in conns.keys():
    get_val(wire, vals, conns)
  z_wires = sorted([wire for wire in conns.keys() if wire[0] == 'z'],
                   reverse=True
                   )
  bits = [vals[wire] for wire in z_wires]
  res = 0
  for bit in bits:
    res = (res << 1) | bit
  return res


def save_adder(conns):
  graph = graphviz.Digraph()
  op2color = {"AND": "green",
              "OR": "blue",
              "XOR": "red",
              }
  for w3, (op, w1, w2) in conns.items():
    color = op2color[op]
    graph.edge(w1, w3, label=op, color=color)
    graph.edge(w2, w3, label=op, color=color)
  graph.render("graph", format="png")


def part1(file):
  vals, conns = read_input(file)
  res = simulate(vals, conns)
  print(f"Part 1: {res}")


def part2(file):
  """
  Solved this manually by looking at the adder diagram and seeing which wire
  is connected wrongly. There's a repeated pattern.
  """
  _, conns = read_input(file)
  # save_adder(conns)
  swap_wires = ["qnw", "qff", "z16", "pbv", "z23", "qqp", "z36", "fbq"]
  swap_wires.sort()
  res = ",".join(swap_wires)
  print(f"Part 2: {res}")


file = "input.in"
part1(file)
part2(file)

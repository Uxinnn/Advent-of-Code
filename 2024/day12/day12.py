def read_input(file):
  with open(file) as f:
    return [line.strip() for line in f.readlines()]


def get_areas(grid, m, n):
  visited = [[0] * n for _ in range(m)]
  areas = list()
  for i in range(m):
    for j in range(n):
      if not visited[i][j]:
        area = flood_fill_area(grid, visited, i, j, m, n, 0)
        areas.append(area)
  return areas


def flood_fill_area(grid, visited, i, j, m, n, area):
  visited[i][j] = 1
  area += 1
  for i2, j2 in ((i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)):
    if -1 < i2 < n and -1 < j2 < m:
      if not visited[i2][j2] and grid[i2][j2] == grid[i][j]:
        area = flood_fill_area(grid, visited, i2, j2, m, n, area)
  return area


def get_perimeters(grid, m, n):
  visited = [[0] * n for _ in range(m)]
  perimeters = list()
  for i in range(m):
    for j in range(n):
      if not visited[i][j]:
        perimeter = flood_fill_perimeter(grid, visited, i, j, m, n, 0)
        perimeters.append(perimeter)
  return perimeters


def flood_fill_perimeter(grid, visited, i, j, m, n, perimeter):
  visited[i][j] = 1
  for i2, j2 in ((i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)):
    if -1 < i2 < n and -1 < j2 < m:
      if visited[i2][j2]:
        if grid[i2][j2] != grid[i][j]:
          perimeter += 1
      else:
        if grid[i2][j2] == grid[i][j]:
          perimeter = flood_fill_perimeter(grid, visited, i2, j2, m, n,
                                           perimeter)
        else:
          perimeter += 1
    else:
      perimeter += 1
  return perimeter


def get_vertices(grid, m, n):
  visited_vertices = [[0] * n for _ in range(m)]
  vertices_grid = get_vertices_grid(grid, m, n)
  vertices = list()
  for i in range(m):
    for j in range(n):
      if not visited_vertices[i][j]:
        vertex = flood_fill_vertices(grid,
                                     vertices_grid,
                                     visited_vertices,
                                     i,
                                     j,
                                     m,
                                     n,
                                     0,
                                     )
        vertices.append(vertex)
  return vertices


def get_vertices_grid(grid, m, n):
  vertices_grid = [[0] * n for _ in range(m)]
  for i in range(m):
    for j in range(n):
      # Check the neighboring positions to see if it is an edge.
      is_edge_neighbors = list()
      for i2, j2 in (i, j + 1), (i + 1, j), (i, j - 1), (i - 1, j):
        is_edge = (i2 < 0 or i2 >= n or j2 < 0 or j2 >= m or
                   grid[i][j] != grid[i2][j2])
        is_edge_neighbors.append(is_edge)
      # 0-th index of every map is a position diagonal to the original.
      edges_mirror_map = {(0, 1): ((i + 1, j + 1), (i, j + 1), (i + 1, j)),
                          (1, 2): ((i + 1, j - 1), (i, j - 1), (i + 1, j)),
                          (2, 3): ((i - 1, j - 1), (i, j - 1), (i - 1, j)),
                          (3, 0): ((i - 1, j + 1), (i, j + 1), (i - 1, j)),
                          }
      for edge_idxes in edges_mirror_map.keys():
        if (not is_edge_neighbors[edge_idxes[0]] or
            not is_edge_neighbors[edge_idxes[1]]
        ):
          # No 2 consecutive edges, no vertex present.
          continue
        # If there are 2 consecutive edges, then a exterior vertex is present.
        # There is an exterior vertex
        vertices_grid[i][j] += 1
        # Check to see if there is an interior vertex too.
        # if True, add vertex count to the position diagonal.
        if is_interior_vertex(grid, m, n, edge_idxes, edges_mirror_map):
          i2, j2 = edges_mirror_map[edge_idxes][0]
          vertices_grid[i2][j2] += 1
  return vertices_grid


def is_interior_vertex(grid, m, n, edge_idxes, edges_mirror_map):
  # Interior vertex only occurs when the 3 positions surrounding an
  # exterior vertex is of the same type.
  diagonal = edges_mirror_map[edge_idxes][0]
  if -1 < diagonal[0] < n and -1 < diagonal[1] < m:
    neighbors = set()
    for i2, j2 in edges_mirror_map[edge_idxes]:
      if -1 < i2 < n and -1 < j2 < m:
        neighbors.add(grid[i2][j2])
    return len(neighbors) == 1
  return False


def flood_fill_vertices(grid, vertices_grid, visited, i, j, m, n, vertex):
  visited[i][j] = 1
  vertex += vertices_grid[i][j]
  for i2, j2 in ((i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)):
    if -1 < i2 < n and -1 < j2 < m:
      if not visited[i2][j2] and grid[i2][j2] == grid[i][j]:
        vertex = flood_fill_vertices(grid,
                                     vertices_grid,
                                     visited,
                                     i2,
                                     j2,
                                     m,
                                     n,
                                     vertex,
                                     )
  return vertex


def part1(file):
  grid = read_input(file)
  m, n = len(grid), len(grid[0])
  areas = get_areas(grid, m, n)
  perimeters = get_perimeters(grid, m, n)
  tot_price = sum([a * p for a, p in zip(areas, perimeters)])
  print(f"Part 1: {tot_price}")


def part2(file):
  grid = read_input(file)
  m, n = len(grid), len(grid[0])
  areas = get_areas(grid, m, n)
  vertices = get_vertices(grid, m, n)
  tot_price = sum([a * p for a, p in zip(areas, vertices)])
  print(f"Part 2: {tot_price}")


file = "input.in"
part1(file)
part2(file)

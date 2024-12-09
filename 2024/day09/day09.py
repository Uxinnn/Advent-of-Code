"""
Got a little lazy to refactor the code to make it easier to read...
"""

def read_input(file):
  with open(file, 'r') as f:
    disk_map = f.readline().strip()
    disk_map = [int(d) for d in disk_map]
    return disk_map


def update_chksum(chksum, i, r, v):
  for j in range(i, i + r):
    chksum += j * v
  return chksum


def part1(file):
  """
  2 pointers method. Whenever theres an empty slot on the left, use the files
  on the right to 'move' them into the slot. Update the slot and files on the
  right accordingly since the slot may be bigger/smaller than the right-most
  file.
  """
  disk_map = read_input(file)
  left, right = 0, len(disk_map) - 1
  i = 0  # Keeps track of the current block position.
  chksum = 0
  while left <= right:
    if left % 2 == 0:
      _id = left // 2
      chksum = update_chksum(chksum, i, disk_map[left], _id)
      i += disk_map[left]
      left += 1
    else:
      # Empty slot, move files from the right.
      _id = right // 2
      if disk_map[left] > disk_map[right]:
        chksum = update_chksum(chksum, i, disk_map[right], _id)
        disk_map[left] -= disk_map[right]
        i += disk_map[right]
        right -= 2
      elif disk_map[left] < disk_map[right]:
        chksum = update_chksum(chksum, i, disk_map[left], _id)
        disk_map[right] -= disk_map[left]
        i += disk_map[left]
        left += 1
      else:
        chksum = update_chksum(chksum, i, disk_map[left], _id)
        i += disk_map[left]
        left += 1
        right -= 2
  print(f"Part 1: {chksum}")


def merge_free_space(disk_map, i):
  if i < len(disk_map) - 2 and disk_map[i + 1][1] is None:
    disk_map[i] = (disk_map[i][0] + disk_map[i + 1][0], None)
    del disk_map[i + 1]
  if i > 0 and disk_map[i - 1][1] is None:
    disk_map[i] = (disk_map[i][0] + disk_map[i - 1][0], None)
    del disk_map[i - 1]


def part2(file):
  """
  for each file on the right, look through the slots on the left and fit in the
  file if possible. Different approach from part 1.
  """
  disk_map = read_input(file)
  disk_map = [(d, i // 2) if i % 2 == 0 else (d, None)
              for i, d in enumerate(disk_map)
              ]
  right = len(disk_map) - 1
  while right > -1:
    r_size, r_id = disk_map[right]
    if r_id is None:
      right -= 1
      continue
    for left in range(right):
      l_size, l_id = disk_map[left]
      if l_id is None:
        disk_map[left] = disk_map[right]
        if l_size > r_size:
          if left < len(disk_map) - 2 and disk_map[left + 1][1] is None:
            disk_map[left + 1] = (disk_map[left + 1][0] + l_size - r_size, None)
          else:
            disk_map.insert(left + 1, (l_size - r_size, None))
            right += 1
          disk_map[right] = (r_size, None)
          merge_free_space(disk_map, right)
          break
        elif l_size == r_size:
          disk_map[right] = (r_size, None)
          merge_free_space(disk_map, right)
          break
    right -= 1
  # Compute checksum
  i = 0
  chksum = 0
  for item in disk_map:
    if item[1] is not None:
      chksum = update_chksum(chksum, i, item[0], item[1])
    i += item[0]
  print(f"Part 2: {chksum}")


file = "input.in"
part1(file)
part2(file)

from functools import cache
#
# with open("input.in", "r") as file:
#     data = file.read().strip()
#
# RECORDS = [
#     (x, tuple(map(int, y.split(","))))
#     for row in data.split("\n")
#     for x, y in [row.split(" ")]
# ]
#
#
# @cache
# def dp(i, j, cur, seq, nums):
#     if i == len(seq):
#         return (j == len(nums) - 1 and nums[j] == cur) or (j == len(nums) and cur == 0)
#     res = 0
#     if seq[i] in "#?":
#         res += dp(i + 1, j, cur + 1, seq, nums)
#     if seq[i] in ".?":
#         if cur == 0:
#             res += dp(i + 1, j, 0, seq, nums)
#         elif cur > 0 and j < len(nums) and nums[j] == cur:
#             res += dp(i + 1, j + 1, 0, seq, nums)
#     return res
#
#
# def part_one():
#     i = 0
#     for seq, nums in RECORDS:
#         x = dp(0, 0, 0, seq, nums)
#         print(i, x)
#         i += 1
#     return sum(dp(0, 0, 0, seq, nums) for seq, nums in RECORDS)
#
#
# def part_two():
#     unfolded = [
#         ("?".join(seq for _ in range(5)), tuple(nums * 5)) for seq, nums in RECORDS
#     ]
#     return sum(dp(0, 0, 0, seq, nums) for seq, nums in unfolded)
#
#
# print(f"Part 1: {part_one()}")  # 7670
# # print(f"Part 2: {part_two()}")  # 157383940585037


def read_input(file):
    with open(file, 'r') as f:
        for line in f:
            row, nums = line.strip().split()
            nums = tuple(map(int, nums.split(',')))
            yield row, nums


def unfold(entry):
    """
    Unfold row by duplicating it 5 times, delimited by an extra '?'.
    Nums is duplicated 5 times too.
    Used in part 2.
    """
    row, nums = entry
    unfolded_row = ((row + '?') * 5)[:-1]
    unfolded_nums = nums * 5
    return unfolded_row, unfolded_nums


@cache
def dfs(row, nums, idx, nums_idx, prev_damaged):
    nums_len = len(nums)
    # Stopping Conditions
    if (nums_idx < nums_len and prev_damaged > nums[nums_idx]) or (nums_idx >= nums_len and prev_damaged > 0):
        return 0
    elif idx == len(row):
        return int(not nums_idx < nums_len)
    # Check what type of character row[idx] is
    if row[idx] == '.':
        if prev_damaged > 0:
            if nums_idx < len(nums) and prev_damaged == nums[nums_idx]:
                # We have gotten the right length of contiguous #, stop the
                # group of # and go to the next value in nums. Reset
                # prev_damaged.
                return dfs(row, nums, idx + 1, nums_idx + 1, 0)
            else:
                # We exceeded the right length of contiguous #, which makes this
                # combination invalid.
                return 0
        else:
            # We currently have no  contiguous #, just continue to next
            # character in row.
            return dfs(row, nums, idx + 1, nums_idx, 0)
    elif row[idx] == '#':
        # Just add or start a contiguous #. Checks for validity will be done
        # when a '.' is reached.
        return dfs(row, nums, idx + 1, nums_idx, prev_damaged + 1)
    else:
        if nums_idx >= nums_len:
            # We ran out of contiguous # groups needed by nums, there should be
            # no more # from this point onwards.
            # Put a '.'
            return dfs(row, nums, idx + 1, nums_idx, 0)
        elif prev_damaged == nums[nums_idx]:
            # We reached the right length for the current contiguous # group.
            # Go to the next value in nums and reset prev_damaged.
            # Put a '.'
            return dfs(row, nums, idx + 1, nums_idx + 1, 0)
        elif 0 < prev_damaged < nums[nums_idx]:
            # We are in the middle of a contiguous # group. Have to continue
            # adding to the group for it to remain valid.
            # Put a '#'
            return dfs(row, nums, idx + 1, nums_idx, prev_damaged + 1)
        else:
            # Either a '.' or '#' is possible, try both.
            way1 = dfs(row, nums, idx + 1, nums_idx, 0)
            way2 = dfs(row, nums, idx + 1, nums_idx, prev_damaged + 1)
            return way1 + way2


def part1(file):
    tot_count = 0
    for row, nums in read_input(file):
        # Add '.' at end of row because validity of # are only checked when a
        # '.' is reached after a contiguous group of #
        count = dfs(row + '.', nums, 0, 0, 0)
        tot_count += count
    print(f"Part 1: {tot_count}")


def part2(file):
    tot_count = 0
    for entry in read_input(file):
        row, nums = unfold(entry)
        # Add '.' at end of row because validity of # are only checked when a
        # '.' is reached after a contiguous group of #
        count = dfs(row + '.', nums, 0, 0, 0)
        tot_count += count
    print(f"Part 2: {tot_count}")


file = "input.in"
part1(file)
part2(file)

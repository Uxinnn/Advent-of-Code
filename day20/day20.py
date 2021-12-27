def read_input():
    img = {"other": '.'}
    with open("input.in", "r") as file:
        algo = file.readline().strip()
        file.readline()
        row = 0
        for line in file.readlines():
            line = line.strip()
            for i in range(len(line)):
                img[(row, i)] = line[i]
            row += 1

    return algo, img


def get_surrounding_pts(pt):
    y, x = pt
    surrounding_pts = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
                       (y, x - 1), (y, x), (y, x + 1),
                       (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)]
    return surrounding_pts


def plot_img(img):
    y_pts = [k[0] for k in img.keys() if k != "other"]
    x_pts = [k[1] for k in img.keys() if k != "other"]
    min_y, max_y, min_x, max_x = min(y_pts), max(y_pts), min(x_pts), max(x_pts)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(img[(y, x)], end=" ")
        print()


def enhance(algo, img):
    enhanced_img = dict()
    enhanced_img["other"] = algo[0] if img["other"] == "." else algo[-1]
    for pt in [key for key in img.keys() if key != "other"]:
        zone_pts = get_surrounding_pts(pt)
        for zone_pt in zone_pts:
            if zone_pt in enhanced_img.keys():
                continue
            surroundings = get_surrounding_pts(zone_pt)
            px_string = ""
            for px in surroundings:
                px_symbol = img["other"] if px not in img.keys() else img[px]
                px_string += '1' if px_symbol == "#" else '0'
            px_ref = int("".join(px_string), 2)
            enhanced_img[zone_pt] = algo[px_ref]
    return enhanced_img


def enhance_n(algo, img, n):
    enhanced_img = img
    for i in range(n):
        enhanced_img = enhance(algo, enhanced_img)
    return enhanced_img


def get_number_of_lit_pixels(img):
    return list(img.values()).count('#')


def part1():
    algo, img = read_input()
    enhanced_img = enhance_n(algo, img, 2)
    number_of_lit_pixels = get_number_of_lit_pixels(enhanced_img)
    print(f"Part 1: {number_of_lit_pixels}")


def part2():
    algo, img = read_input()
    enhanced_img = enhance_n(algo, img, 50)
    number_of_lit_pixels = get_number_of_lit_pixels(enhanced_img)
    print(f"Part 2: {number_of_lit_pixels}")


if __name__ == "__main__":
    part1()
    part2()

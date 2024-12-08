import time


def parse_grid(
    lines: list[str],
) -> tuple[set[tuple[int, int]], dict[str, list[tuple[int, int]]]]:
    locations = set()
    antennas = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            coord = (x, y)
            locations.add(coord)
            val = lines[y][x]
            if val != "." and val != "#":
                if val not in antennas:
                    antennas[val] = []
                antennas[val].append(coord)
    return locations, antennas


def antinode_locations_p1(
    a: tuple[int, int], b: tuple[int, int]
) -> list[tuple[int, int]]:
    return [
        (a[0] + (a[0] - b[0]), a[1] + (a[1] - b[1])),
        (b[0] + (b[0] - a[0]), b[1] + (b[1] - a[1])),
    ]


assert list(sorted(antinode_locations_p1((5, 5), (8, 4)))) == [
    (2, 6),
    (11, 3),
], antinode_locations_p1((5, 5), (8, 4))
assert list(sorted(antinode_locations_p1((8, 4), (5, 5)))) == [
    (2, 6),
    (11, 3),
], antinode_locations_p1((8, 4), (5, 5))


def antinode_locations_p2(
    a: tuple[int, int], b: tuple[int, int], locations: set[tuple[int, int]]
) -> list[tuple[int, int]]:
    result = []
    cur = (a[0], a[1])
    while cur in locations:
        result.append(cur)
        cur = (cur[0] + (a[0] - b[0]), cur[1] + (a[1] - b[1]))
    cur = (b[0], b[1])
    while cur in locations:
        result.append(cur)
        cur = (cur[0] + (b[0] - a[0]), cur[1] + (b[1] - a[1]))
    return result


def solve_p1(lines: list[str]) -> object:
    locations, antennas = parse_grid(lines)
    antinodes = set()
    for locs in antennas.values():
        for i in range(len(locs)):
            for j in range(i + 1, len(locs)):
                a_loc = antinode_locations_p1(locs[i], locs[j])
                for loc in a_loc:
                    if loc in locations:
                        antinodes.add(loc)
    return len(antinodes)


def solve_p2(lines: list[str]) -> object:
    locations, antennas = parse_grid(lines)
    antinodes = set()
    for locs in antennas.values():
        for i in range(len(locs)):
            for j in range(i + 1, len(locs)):
                a_loc = antinode_locations_p2(locs[i], locs[j], locations)
                for loc in a_loc:
                    antinodes.add(loc)
    return len(antinodes)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    start = time.time()
    print(solve_p1(lines))
    print(solve_p2(lines))
    print(f"processed file '{filename}' in {time.time() - start:.2f}s")


# Part 1: 00:47:28
# Part 2: 00:53:47
if __name__ == "__main__":
    process_file("sample.in")
    process_file("input.in")

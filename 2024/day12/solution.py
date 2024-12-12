import time


def parse_grid(lines: list[str]) -> dict[tuple[int, int], str]:
    grid = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            grid[(x, y)] = lines[y][x]
    return grid


def find_region(
    grid: dict[tuple[int, int], str], start: tuple[int, int]
) -> set[tuple[int, int]]:
    target = grid[start]
    region = set()
    to_visit = [start]
    while len(to_visit) > 0:
        cur = to_visit.pop()
        if cur in region or grid.get(cur, None) != target:
            continue
        region.add(cur)
        for xd, yd in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            to_visit.append((cur[0]+xd, cur[1]+yd))
    return region


def find_all_regions(grid: dict[tuple[int, int], str]) -> list[set[tuple[int, int]]]:
    grid = grid.copy()
    regions = []
    while len(grid) > 0:
        start = set(grid.keys()).pop()
        region = find_region(grid, start)
        for c in region:
            del grid[c]
        regions.append(region)
    return regions


def compute_perimeter(region: set[tuple[int, int]]) -> int:
    perimeter = 0
    for x, y in region:
        for xd, yd in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (x + xd, y + yd) not in region:
                perimeter += 1
    return perimeter

def perpendiculars(xd: int, yd: int) -> list[tuple[int, int]]:
    if xd == 0:
        assert yd in (1, -1)
        return [(1, 0), (-1, 0)]
    assert yd == 0
    assert xd in (1, -1)
    return [(0, -1), (0, 1)]

def compute_num_sides(region: set[tuple[int, int]]) -> int:
    num_sides = 0
    for xd, yd in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        to_count = set(region)
        while len(to_count) > 0:
            cur = to_count.pop()
            other_side = (cur[0] + xd, cur[1] + yd)
            if other_side in region:
                # Not an edge.
                continue
            num_sides += 1
            for p in perpendiculars(xd, yd):
                p_cur = (cur[0]+p[0], cur[1]+p[1])
                while p_cur in to_count:
                    to_count.remove(p_cur)
                    other_side = (p_cur[0] + xd, p_cur[1] + yd)
                    if other_side in region:
                        # Not an edge.
                        break
                    p_cur = (p_cur[0]+p[0], p_cur[1]+p[1])
    return num_sides

def solve_p1(lines: list[str]) -> object:
    grid = parse_grid(lines)
    regions = find_all_regions(grid)
    total_price = 0
    for region in regions:
        total_price += len(region) * compute_perimeter(region)
    return total_price


def solve_p2(lines: list[str]) -> object:
    grid = parse_grid(lines)
    regions = find_all_regions(grid)
    total_price = 0
    for region in regions:
        total_price += len(region) * compute_num_sides(region)
    return total_price


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    start = time.time()
    print(solve_p1(lines))
    print(solve_p2(lines))
    print(f"processed file '{filename}' in {time.time() - start:.2f}s")


# Part 1: 00:13:48
# Part 2: 00:37:45
if __name__ == "__main__":
    process_file("sample.in")
    process_file("input.in")

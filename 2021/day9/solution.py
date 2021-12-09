import sys
from typing import *


def is_low_point(grid: List[List[int]], pos: Tuple[int, int]) -> bool:
    x, y = pos
    for xd, yd in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        new_x = x + xd
        new_y = y + yd
        if new_y >= len(grid) or new_y < 0 or new_x >= len(grid[new_y]) or new_x < 0:
            # Out of bounds.
            continue

        if grid[new_y][new_x] <= grid[y][x]:
            return False

    return True


def get_low_points(grid: List[List[int]]) -> List[Tuple[int, int]]:
    result = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if is_low_point(grid, (x, y)):
                result.append((x, y))
    return result


def get_risk_factor(grid: List[List[int]], point: Tuple[int, int]) -> int:
    return grid[point[1]][point[0]] + 1


def compute_basin_size(grid: List[List[int]], low_point: Tuple[int, int]) -> int:
    basin = set()
    to_visit = {low_point}
    assert grid[low_point[1]][low_point[0]] != 9
    while len(to_visit) > 0:
        (x, y) = to_visit.pop()
        for xd, yd in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_x = x + xd
            new_y = y + yd
            if new_y >= len(grid) or new_y < 0 or new_x >= len(grid[new_y]) or new_x < 0:
                # Out of bounds.
                continue
            if (new_x, new_y) in basin:
                continue

            # The only thing to check is that this is not a 9. This relies on the fact that
            # "all other locations will always be part of exactly one basin".
            # i.e., you can't have the following 1x3 grid: 121 because 2 would belong to 2 basins.
            if grid[new_y][new_x] == 9:
                continue


            to_visit.add((new_x, new_y))

        basin.add((x, y))

    return len(basin)


def main(lines: List[str]) -> None:
    grid = []
    for line in lines:
        row = []
        for d in line:
            row.append(int(d))
        if len(grid) > 0:
            assert len(grid[-1]) == len(row)
        grid.append(row)

    low_points = get_low_points(grid)
    print(sum(get_risk_factor(grid, p) for p in low_points))

    basin_sizes = [compute_basin_size(grid, p) for p in low_points]
    product = 1
    for b in sorted(basin_sizes)[len(basin_sizes)-3:]:
        product *= b
    print(product)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

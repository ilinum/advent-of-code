import sys
from collections import defaultdict
from typing import *


def do_iteration_3d(grid: Dict[Tuple[int, int, int], bool]) -> Dict[Tuple[int, int, int], bool]:
    num_active_neighbors = defaultdict(lambda: 0)
    for (x, y, z), v in grid.items():
        if not v:
            continue
        diff = {-1, 0, 1}
        for xd in diff:
            for yd in diff:
                for zd in diff:
                    if xd == 0 and yd == 0 and zd == 0:
                        continue
                    newx = x + xd
                    newy = y + yd
                    newz = z + zd
                    num_active_neighbors[(newx, newy, newz)] += 1

    next_grid = defaultdict(lambda: False)
    for c, v in num_active_neighbors.items():
        if not grid[c]:
            if num_active_neighbors[c] == 3:
                next_grid[c] = True
        elif num_active_neighbors[c] in {2, 3}:
            next_grid[c] = True
    return next_grid


def do_iteration_4d(grid: Dict[Tuple[int, int, int, int], bool]) -> Dict[Tuple[int, int, int, int], bool]:
    num_active_neighbors = defaultdict(lambda: 0)
    for (x, y, z, w), v in grid.items():
        if not v:
            continue
        diff = {-1, 0, 1}
        for xd in diff:
            for yd in diff:
                for zd in diff:
                    for wd in diff:
                        if xd == 0 and yd == 0 and zd == 0 and wd == 0:
                            continue
                        newx = x + xd
                        newy = y + yd
                        newz = z + zd
                        neww = w + wd
                        num_active_neighbors[(newx, newy, newz, neww)] += 1

    next_grid = defaultdict(lambda: False)
    for c, v in num_active_neighbors.items():
        if not grid[c]:
            if num_active_neighbors[c] == 3:
                next_grid[c] = True
        elif num_active_neighbors[c] in {2, 3}:
            next_grid[c] = True
    return next_grid


def part1(lines: List[str]) -> None:
    grid = defaultdict(lambda: False)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[(x, y, 0)] = c == "#"

    for i in range(6):
        grid = do_iteration_3d(grid)

    print(sum(1 for v in grid.values() if v))


def part2(lines: List[str]) -> None:
    grid = defaultdict(lambda: False)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[(x, y, 0, 0)] = c == "#"

    for i in range(6):
        grid = do_iteration_4d(grid)

    print(sum(1 for v in grid.values() if v))


# 00:18:38: Part 1 complete.
# 00:20:40: Both parts complete.
if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    part1(lines)
    part2(lines)

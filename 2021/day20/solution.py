import sys
from collections import defaultdict
from functools import cache
from typing import *


class Grid:
    def __init__(
            self,
            algo: str,
            initial: Dict[Tuple[int, int], str],
    ) -> None:
        self.initial = initial
        self.algo = algo

    @cache
    def get(self, row: int, col: int, iteration: int) -> str:
        # NOTE: You can make the solution a lot more efficient
        # by adding an extra check for if this cell was surrounded
        # by zeroes in the beginning. For those cells, the only
        # thing you need to check if iteration is even or odd.
        if iteration == 0:
            return self.initial[(row, col)]

        num = ""
        for r in (row - 1, row, row + 1):
            for c in (col - 1, col, col + 1):
                num += self.get(r, c, iteration - 1)
        char = self.algo[int(num, 2)]
        return char


def parse_grid(lines: List[str]) -> Grid:
    algo = lines[0].replace("#", "1").replace(".", "0")
    assert len(lines[1]) == 0

    grid_dict = defaultdict(lambda: "0")
    for row, line in enumerate(lines[2:]):
        for col, char in enumerate(line):
            if char == "#":
                grid_dict[(row, col)] = "1"

    return Grid(algo, grid_dict)


def num_lit(grid: Grid, iteration: int) -> int:
    vals = []
    for row in range(-200, 200):
        for col in range(-200, 200):
            vals.append(grid.get(row, col, iteration))

    return len([v for v in vals if v == "1"])


def main(lines: List[str]) -> None:
    grid = parse_grid(lines)
    print(num_lit(grid, 2))
    print(num_lit(grid, 50))


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

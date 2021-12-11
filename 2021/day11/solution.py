import sys
from typing import *


class Grid:
    def __init__(self, lines: List[str]) -> None:
        self.num_flashes = 0
        self.grid = []
        for line in lines:
            row = [int(c) for c in line]
            self.grid.append(row)

        assert all(len(row) == len(self.grid) for row in self.grid), self.grid

    def _process_flash(self, row: int, col: int) -> None:
        dirs = {-1, 0, 1}
        for rd in dirs:
            for cd in dirs:
                if rd == 0 and cd == 0:
                    continue
                nr = row + rd
                nc = col + cd
                if nr < 0 or nr >= len(self.grid):
                    continue
                if nc < 0 or nc >= len(self.grid[nr]):
                    continue
                self.grid[nr][nc] += 1

    def single_step(self) -> None:
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                self.grid[row][col] += 1

        flashed: Set[Tuple[int, int]] = set()
        while True:
            prev_flashes = len(flashed)
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if self.grid[row][col] > 9 and (row, col) not in flashed:
                        flashed.add((row, col))
                        self._process_flash(row, col)
            if len(flashed) == prev_flashes:
                break
        self.num_flashes += len(flashed)
        for (row, col) in flashed:
            self.grid[row][col] = 0

    def all_flashed(self) -> bool:
        for row in self.grid:
            for cell in row:
                if cell != 0:
                    return False
        return True

    def __repr__(self) -> str:
        rows = []
        for row in self.grid:
            rows.append("".join(str(c) for c in row))
        grid = "\n".join(rows)
        return f"flashes: {self.num_flashes}\n{grid}"


def main(lines: List[str]) -> None:
    g = Grid(lines)
    for _ in range(100):
        g.single_step()
    print(g.num_flashes)

    g = Grid(lines)
    first_synchronized_flash = 0
    while not g.all_flashed():
        first_synchronized_flash += 1
        g.single_step()
    print(first_synchronized_flash)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

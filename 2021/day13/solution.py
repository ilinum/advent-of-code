import sys
from typing import *


class Instruction:
    def __init__(self, line: str) -> None:
        assert line.startswith("fold along "), line
        s = line.split()
        assert len(s) == 3
        (d, val) = s[2].split("=")
        self.dir = d
        self.val = int(val)

    def __repr__(self) -> str:
        return str((self.dir, self.val))


class Grid:
    def __init__(self, inner: Set[Tuple[int, int]]) -> None:
        self.inner = inner

    @classmethod
    def parse(cls, lines: List[str]) -> "Grid":
        s = set()
        for line in lines:
            x, y = line.split(",")
            s.add((int(x), int(y)))
        return cls(s)

    def fold(self, instr: Instruction) -> "Grid":
        res = set()
        if instr.dir == "x":
            for (x, y) in self.inner:
                if x < instr.val:
                    res.add((x, y))
                else:
                    assert x > instr.val, "no dots allowed on folds!"
                    diff = x - instr.val
                    res.add((instr.val - diff, y))
        else:
            assert instr.dir == "y", instr.dir
            for (x, y) in self.inner:
                if y < instr.val:
                    res.add((x, y))
                else:
                    assert y > instr.val, "no dots allowed on folds!"
                    diff = y - instr.val
                    res.add((x, instr.val - diff))
        return Grid(res)

    def __repr__(self) -> str:
        max_x = max(x for (x, y) in self.inner)
        min_x = min(x for (x, y) in self.inner)
        max_y = max(y for (x, y) in self.inner)
        min_y = min(y for (x, y) in self.inner)
        rows = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                if (x, y) in self.inner:
                    row.append("#")
                else:
                    row.append(".")
            rows.append("".join(row))
        return str("\n".join(rows))


def parse_input(lines: List[str]) -> Tuple[Grid, List[Instruction]]:
    instr_start = 0
    for i, line in enumerate(lines):
        if len(line) == 0:
            instr_start = i
            break

    grid = Grid.parse(lines[:instr_start])
    assert instr_start + 1 < len(lines)
    instructions = []
    for line in lines[instr_start + 1:]:
        instructions.append(Instruction(line))
    return grid, instructions


def main(lines: List[str]) -> None:
    grid, instructions = parse_input(lines)
    for instruction in instructions:
        grid = grid.fold(instruction)
        print(len(grid.inner))
    """
    ###..####.#..#.####.#....###...##..#..#
    #..#....#.#.#.....#.#....#..#.#..#.#..#
    #..#...#..##.....#..#....#..#.#....####
    ###...#...#.#...#...#....###..#.##.#..#
    #.#..#....#.#..#....#....#....#..#.#..#
    #..#.####.#..#.####.####.#.....###.#..#
    """
    print(grid)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

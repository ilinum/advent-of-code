import sys
from dataclasses import dataclass
from typing import *


@dataclass
class Instruction:
    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int

    instr: str

    def __init__(self, x0: int, x1: int, y0: int, y1: int, z0: int, z1: int, instr: str) -> None:
        assert x0 < x1, (x0, x1)
        assert y0 < y1, (y0, y1)
        assert z0 < z1, (z0, z1)
        assert instr in {"on", "off"}, instr
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1
        self.instr = instr

    @classmethod
    def parse(cls, line: str) -> "Instruction":
        instr, coord = line.split()
        x_i, y_i, z_i = coord.lstrip("on ").split(",")
        x0, x1 = map(int, x_i.lstrip("x=").split(".."))
        y0, y1 = map(int, y_i.lstrip("y=").split(".."))
        z0, z1 = map(int, z_i.lstrip("z=").split(".."))
        return cls(x0, x1, y0, y1, z0, z1, instr)


def part1(instructions: List[Instruction]) -> None:
    p1_instructions = []
    for i in instructions:
        if not any(k < -50 or k > 50 for k in (i.x0, i.x1, i.y0, i.y1, i.z0, i.z1)):
            p1_instructions.append(i)

    enabled = set()
    for i in p1_instructions:
        for x in range(i.x0, i.x1 + 1):
            for y in range(i.y0, i.y1 + 1):
                for z in range(i.z0, i.z1 + 1):
                    if i.instr == "on":
                        enabled.add((x, y, z))
                    else:
                        assert i.instr == "off", i.instr
                        try:
                            enabled.remove((x, y, z))
                        except KeyError:
                            pass
    print(len(enabled))


def main(lines: List[str]) -> None:
    instructions = [Instruction.parse(line) for line in lines]
    part1(instructions)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

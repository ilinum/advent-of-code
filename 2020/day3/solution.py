import sys
from typing import *


def part1(lines: List[str]) -> None:
    print(count_step(3, lines))


def count_step(step: int, lines: List[str]) -> int:
    pos = 0
    count = 0
    for line in lines:
        if line[pos] == "#":
            count += 1
        pos = pos+step
        if pos >= len(line):
            pos = pos-len(line)
    return count

def part2(lines: List[str]) -> None:
    res = count_step(1, lines) * count_step(3, lines) * count_step(5, lines) * count_step(7, lines)
    even = []
    for i, line in enumerate(lines):
        if i % 2 == 0:
            even.append(line)
    res *= count_step(1, even)
    print(res)

# 00:05:23: Part 1 complete.
# 00:07:52: Both parts complete
if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    part1(lines)
    part2(lines)

import sys
from typing import *


def part1(lines: List[str]) -> None:
    entries = list(map(lambda x: int(x), lines))
    for i in range(len(entries)):
        for j in range(len(entries)):
            if i == j:
                continue
            e1 = entries[i]
            e2 = entries[j]
            if e1 + e2 == 2020:
                print(e1 * e2)
                return


def part2(lines: List[str]) -> None:
    entries = list(map(lambda x: int(x), lines))
    for i in range(len(entries)):
        for j in range(len(entries)):
            for k in range(len(entries)):
                if len({i, j, k}) != 3:
                    continue
                e1 = entries[i]
                e2 = entries[j]
                e3 = entries[k]
                if e1 + e2 + e3 == 2020:
                    print(e1 * e2 * e3)
                    return

# 00:02:37: Part 1 complete.
# 00:04:17: Both parts complete.
if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    part1(lines)
    part2(lines)

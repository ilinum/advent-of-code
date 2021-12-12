import sys
from typing import *


def decode(code: str) -> Tuple[int, int]:
    lower = 0
    upper = 128
    for c in code[:7]:
        mid = (lower + upper) // 2
        if c == "B":
            lower = mid
        else:
            assert c == "F", c
            upper = mid

    assert lower + 1 == upper, (lower, upper)
    row = lower

    lower = 0
    upper = 8
    for c in code[7:]:
        mid = (lower + upper) // 2
        if c == "R":
            lower = mid
        else:
            assert c == "L", c
            upper = mid

    assert lower + 1 == upper, (lower, upper)
    col = lower
    return (row, col)


def part1(lines: List[str]) -> None:
    ids = []
    for line in lines:
        row, col = decode(line)
        ids.append(row * 8 + col)

    print(max(ids))


def part2(lines: List[str]) -> None:
    ids = set()
    for line in lines:
        row, col = decode(line)
        ids.add(row * 8 + col)

    full_set = dict()
    for row in range(128):
        if row == 0 or row == 127:
            continue
        for col in range(8):
            id = row * 8 + col
            full_set[(row, col)] = id
    print(set(full_set.values()) - ids)


# 00:18:56: Both parts complete.
if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    part1(lines)
    part2(lines)

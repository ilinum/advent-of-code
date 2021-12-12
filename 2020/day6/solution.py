import sys
from typing import *


def count_union(group: List[str]) -> int:
    s = set()
    for line in group:
        for c in line:
            s.add(c)
    return len(s)


def get_groups(lines: List[str]) -> List[List[str]]:
    groups = []
    group = []
    for line in lines:
        if len(line) == 0:
            groups.append(group)
            group = []
        else:
            group.append(line)
    groups.append(group)
    return groups


def part1(lines: List[str]) -> None:
    groups = get_groups(lines)
    answers = [count_union(group) for group in groups]
    print(sum(answers))


def count_intersection(group: List[str]) -> int:
    group_sets = []
    for g in group:
        group_sets.append(set(g))

    result = group_sets[0]
    for g in group_sets[1:]:
        result = result.intersection(g)
    return len(result)


def part2(lines: List[str]) -> None:
    groups = get_groups(lines)
    answers = [count_intersection(group) for group in groups]
    print(sum(answers))


# 00:05:03: Part 1 complete.
# 00:07:17: Both parts complete.
if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    part1(lines)
    part2(lines)

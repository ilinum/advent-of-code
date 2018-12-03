import sys
from typing import List
import collections


def part2(lines: List[str]) -> str:
    if not lines:
        raise RuntimeError('lines is empty')
    line_len = len(lines[0].strip())
    for index_to_remove in range(line_len):
        seen = set()
        for line in lines:
            line = line.strip()
            stripped = line[:index_to_remove] + line[index_to_remove + 1:]
            if stripped in seen:
                return stripped
            seen.add(stripped)
    raise RuntimeError()


def part1(lines: List[str]) -> int:
    twos = 0
    threes = 0
    for line in lines:
        counter = collections.Counter(line)
        if 2 in counter.values():
            twos += 1
        if 3 in counter.values():
            threes += 1
    return twos * threes


if __name__ == '__main__':
    print(part2(sys.stdin.readlines()))

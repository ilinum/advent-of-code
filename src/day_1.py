import sys
from typing import List


def part1(lines: List[str]) -> int:
    freq = 0
    for line in lines:
        freq += int(line)
    return freq


def part2(lines: List[str]) -> int:
    freq = 0
    seen = set()
    idx = 0
    while freq not in seen:
        seen.add(freq)
        freq += int(lines[idx])
        idx += 1
        if idx == len(lines):
            idx = 0
    return freq


if __name__ == '__main__':
    print(part2(sys.stdin.readlines()))

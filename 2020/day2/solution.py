import sys
from typing import *

def is_valid(policy: str, password: str) -> bool:
    s = policy.split()
    char = s[1]
    counts = s[0].split("-")
    lower = int(counts[0])
    upper = int(counts[1])
    count = 0
    for c in password:
        if c == char:
            count += 1

    if count >= lower and count <= upper:
        return True
    return False

def is_valid2(policy: str, password: str) -> bool:
    s = policy.split()
    char = s[1]
    counts = s[0].split("-")
    lower = int(counts[0])-1
    upper = int(counts[1])-1
    if lower >= len(password) and upper >= len(password):
        return False
    if lower >= len(password):
        return password[upper] == char
    if upper >= len(password):
        return password[lower] == char
    if (password[lower] == char) != (password[upper] == char):
        return True

    return False

def part1(lines: List[str]) -> None:
    count = 0
    for line in lines:
        s = line.split(":")
        policy = s[0].strip()
        pwd = s[1].strip()
        if is_valid(policy, pwd):
            print(f"{line}: valid")
            count += 1
        else:
            print(f"{line}: invalid")
    print(count)


def part2(lines: List[str]) -> None:
    count = 0
    for line in lines:
        s = line.split(":")
        policy = s[0].strip()
        pwd = s[1].strip()
        if is_valid2(policy, pwd):
            print(f"{line}: valid")
            count += 1
        else:
            print(f"{line}: invalid")
    print(count)


# 00:05:11: Part 1 complete
# 00:12:27: Both parts complete.
if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    part1(lines)
    part2(lines)

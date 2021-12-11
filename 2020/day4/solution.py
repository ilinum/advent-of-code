import sys
from typing import *


def part1(lines: List[str]) -> None:
    cur_pass = dict()
    num_valid = 0
    for line in lines:
        if line == "":
            cur_pass["cid"] = "dummy"
            if len(cur_pass) == 8:
                num_valid += 1
            cur_pass = dict()
        else:
            for item in line.split():
                l = item.split(":")
                cur_pass[l[0]] = l[1]
    print(num_valid)


def is_valid(p: Dict[str, str]) -> bool:
    if len(p) != 8:
        return False
    if int(p["byr"]) < 1920 or int(p["byr"]) > 2002:
        return False
    if int(p["iyr"]) < 2010 or int(p["iyr"]) > 2020:
        return False
    if int(p["eyr"]) < 2020 or int(p["eyr"]) > 2030:
        return False
    height = p["hgt"]
    if height.endswith("cm"):
        cm = int(height[:len(height) - 2])
        if cm < 150 or cm > 193:
            return False
    elif height.endswith("in"):
        inches = int(height[:len(height) - 2])
        if inches < 59 or inches > 76:
            return False
    else:
        return False
    hc = p["hcl"]
    if not hc.startswith("#"):
        return False
    if len(hc) != 7:
        return False
    for c in hc[1:]:
        if c not in {"a", "b", "c", "d", "e", "f",
                     "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
            return False

    if p["ecl"] not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
        return False

    pid = p["pid"]
    if len(pid) != 9:
        return False
    try:
        int(pid)
    except ValueError:
        return False
    return True

def part2(lines: List[str]) -> None:
    cur_pass = {"cid": "dummy"}
    num_valid = 0
    for line in lines:
        if line == "":
            cur_pass["cid"] = "dummy"
            if is_valid(cur_pass):
                num_valid += 1
            else:
                print(f"invalid: {cur_pass}")
            cur_pass = {"cid": "dummy"}
        else:
            for item in line.split():
                l = item.split(":")
                cur_pass[l[0]] = l[1]
    if is_valid(cur_pass):
        num_valid += 1
    else:
        print(f"invalid: {cur_pass}")
    print(num_valid)


# 00:04:57: Part 1 complete.
# 00:26:49: Both parts complete.
if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    part1(lines)
    part2(lines)

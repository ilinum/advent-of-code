import sys
from collections import defaultdict
from typing import *


def get_content_rules(lines: List[str]) -> Dict[str, Dict[str, int]]:
    result = {}
    for line in lines:
        split = line.split()
        outer = split[0] + split[1]
        assert outer not in result
        if line.endswith("no other bags."):
            result[outer] = {}
            continue
        contents = " ".join(split[4:]).split(",")
        content_dict = {}
        for content in contents:
            split = content.split()
            quantity = int(split[0])
            bag = split[1] + split[2]
            assert bag not in content_dict
            content_dict[bag] = quantity
        result[outer] = content_dict
    return result


def part1(lines: List[str]) -> None:
    rules = get_content_rules(lines)
    target = "shinygold"
    to_explore = set()
    explored = set()
    total_options = set()
    for outer, rule in rules.items():
        if rule.get(target, 0) > 0:
            to_explore.add(outer)
    while len(to_explore) > 0:
        cur = to_explore.pop()
        explored.add(cur)
        if len(rules.get(cur, [])) > 0:
            total_options.add(cur)

        for outer, contents in rules.items():
            if contents.get(cur, 0) > 0 and outer not in explored:
                to_explore.add(outer)

    print(len(total_options))


def part2(lines: List[str]) -> None:
    rules = get_content_rules(lines)
    target = "shinygold"
    contents = defaultdict(lambda: 0)
    to_find = {target: 1}
    while len(to_find) > 0:
        bag, count = to_find.popitem()
        contents[bag] += count
        c = rules.get(bag)
        for in_bag, in_count in c.items():
            if in_bag not in to_find:
                to_find[in_bag] = 0
            to_find[in_bag] += in_count * count

    del contents[target]
    print(sum(contents.values()))

# 00:19:22: Part 1 complete.
# 00:28:15: Both parts complete.
if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    part1(lines)
    part2(lines)

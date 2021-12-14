import sys
from collections import defaultdict
from typing import *


def main(lines: List[str]) -> None:
    start = lines[0]
    assert len(lines[1]) == 0
    insertion_rules = {}
    for line in lines[2:]:
        (k, v) = line.split(" -> ")
        insertion_rules[k] = v
    pair_counts = defaultdict(lambda: 0)
    for i in range(1, len(start)):
        pair_counts[start[i - 1] + start[i]] += 1

    for step in range(40):
        next_pair_counts = defaultdict(lambda: 0)
        for pair, count in pair_counts.items():
            if pair not in insertion_rules:
                next_pair_counts[pair] = count
            else:
                insertion = insertion_rules[pair]
                next_pair_counts[pair[0] + insertion] += count
                next_pair_counts[insertion + pair[1]] += count
        pair_counts = next_pair_counts

    counts = defaultdict(lambda: 0)
    for pair, count in pair_counts.items():
        counts[pair[0]] += count
        counts[pair[1]] += count

    # For most of the elements we're double counting (as they're included
    # in two pairs). The only ones that are included in a single pair are the
    # ones at the first and last elements. Due to how the algorithm works,
    # the first and last don't change between iterations (because we insert
    # in the middle). Increase their counts before diving everything by two.
    counts[start[0]] += 1
    counts[start[-1]] += 1
    for k, v in counts.items():
        counts[k] = v // 2
    print(max(counts.values()) - min(counts.values()))


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

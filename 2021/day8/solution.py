import sys
from collections import defaultdict
from typing import *


class Display:
    def __init__(self, patterns: str, output: str) -> None:
        self.patterns = [s.strip() for s in patterns.split()]
        self.output = [s.strip() for s in output.split()]


def find_supersets(digits: Set[FrozenSet[str]], target: FrozenSet[str]) -> Set[FrozenSet[str]]:
    result = set()
    for digit in digits:
        if target.issubset(digit):
            result.add(digit)
    return result


def find_subsets(digits: Set[FrozenSet[str]], target: FrozenSet[str]) -> Set[FrozenSet[str]]:
    result = set()
    for digit in digits:
        if digit.issubset(target):
            result.add(digit)
    return result


def filter_by_len(to_filter: Set[FrozenSet[str]], target_len: int) -> Set[FrozenSet[str]]:
    return set(filter(lambda x: len(x) == target_len, to_filter))


def decypher_display(display: Display) -> int:
    cypher: Dict[int, FrozenSet[str]] = dict()
    # Populate using unique numbers.
    len_to_num = {2: 1, 4: 4, 3: 7, 7: 8}
    all_digits = set(frozenset(digit) for digit in display.output + display.patterns)
    for digit in all_digits:
        if len(digit) in len_to_num:
            num = len_to_num[len(digit)]
            if num in cypher:
                assert cypher[num] == digit
            else:
                cypher[num] = digit

    # 9 is the only 6-segment number that contains 4.
    assert len(cypher) == 4, str(cypher)
    nine = filter_by_len(find_supersets(all_digits, cypher[4]), 6)
    assert len(nine) == 1, nine
    cypher[9] = nine.pop()
    # 3 and 5 are the only 5-segment number that contains 9.
    three_five = filter_by_len(find_subsets(all_digits, cypher[9]), 5)
    assert len(three_five) == 2, three_five
    # 3 will contain 1 vs 5 will not.
    three = find_supersets(three_five, cypher[1])
    assert len(three) == 1, three
    cypher[3] = three.pop()
    five = set(digit for digit in three_five if digit != cypher[3])
    assert len(five) == 1, five
    cypher[5] = five.pop()

    # We got: 1, 3, 4, 5, 7, 8, 9
    # Remaining, we have: 2, 6, 0
    # 2 is the last 5-segment number.
    two = set(digit for digit in filter_by_len(all_digits, 5) if digit not in cypher.values())
    assert len(two) == 1, two
    cypher[2] = two.pop()

    # 6 is a superset of 5.
    six = set(digit for digit in find_supersets(all_digits, cypher[5]) if digit not in cypher.values())
    assert len(six) == 1, six
    cypher[6] = six.pop()

    # 0 is the last one left.
    zero = set(digit for digit in all_digits if digit not in cypher.values())
    assert len(zero) == 1, zero
    cypher[0] = zero.pop()

    digit_to_num = dict()
    for num, digit in cypher.items():
        digit_to_num[digit] = num

    assert len(digit_to_num) == len(cypher)

    # Now, decode!
    out = ""
    for digit in display.output:
        n = digit_to_num[frozenset(digit)]
        out += str(n)
    return int(out)


def main(lines: List[str]) -> None:
    displays = []
    for line in lines:
        sig_patterns, output = line.split("|")
        displays.append(Display(sig_patterns, output))

    count_by_num_segments = defaultdict(lambda: 0)
    for display in displays:
        for digit in display.output:
            count_by_num_segments[len(digit)] += 1
    num_segments = {2, 4, 3, 7}
    print(f"part 1: {sum(count_by_num_segments[n] for n in num_segments)}")

    results = []
    for d in displays:
        decoded = decypher_display(d)
        results.append(decoded)
    print(f"part 2 answer: {sum(results)}")


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

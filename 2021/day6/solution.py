import sys
from collections import defaultdict
from typing import *


def get_ages(lines: List[str]) -> Dict[int, int]:
    assert len(lines) == 1
    ages = defaultdict(lambda: 0)
    for num in lines[0].split(","):
        age = int(num)
        assert 0 <= age < 7
        ages[age] += 1
    return ages


def single_iteration(in_ages: Dict[int, int]) -> Dict[int, int]:
    result = defaultdict(lambda: 0)
    for age, count in in_ages.items():
        if age == 0:
            result[8] += count
            result[6] += count
        else:
            result[age - 1] += count
    return result


def main(lines: List[str], num_iterations: int) -> None:
    ages = get_ages(lines)
    for _ in range(num_iterations):
        ages = single_iteration(ages)
    print(sum(ages.values()))


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines, 80)
    main(lines, 256)

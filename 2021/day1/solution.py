import sys
from typing import List


def compute_increases(depths: List[int]) -> int:
    increases = 0
    prev = depths[0]
    for depth in depths[1:]:
        if depth > prev:
            increases += 1
        prev = depth
    return increases


def group_depths(original_depths: List[int], group_size: int) -> List[int]:
    result = []
    assert len(original_depths) > group_size
    group = original_depths[0:group_size]
    for v in original_depths[3:]:
        result.append(sum(group))
        group = group[1:]
        group.append(v)

    result.append(sum(group))
    return result


def main(filename: str) -> None:
    with open(filename, "r") as f:
        lines = f.readlines()
        depths = [int(line.strip()) for line in lines]

    print(f"ungrouped: {compute_increases(depths)}")
    print(f"grouped with size 3: {compute_increases(group_depths(depths, 3))}")


if __name__ == '__main__':
    main(sys.argv[1])

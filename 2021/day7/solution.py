import sys
from typing import *


def fuel_cost_part_1(positions: List[int], target: int) -> int:
    result = 0
    for pos in positions:
        result += abs(target - pos)
    return result


def fuel_cost_part_2(positions: List[int], target: int) -> int:
    result = 0
    for pos in positions:
        distance = abs(target - pos)
        result += distance * (distance + 1) // 2
        # Or, the slow but easy-to-implement version:
        # if distance != 0:
        #     result += sum(range(distance+1))
    return result


def find_best_position(positions: List[int], calculate_fuel_cost: Callable[[List[int], int], int]) -> None:
    positions_to_consider = list(range(min(positions), max(positions)))
    assert len(positions_to_consider) > 0
    best_position = positions_to_consider[0]
    best_score = calculate_fuel_cost(positions_to_consider, best_position)
    for pos in positions_to_consider[1:]:
        score = calculate_fuel_cost(positions, pos)
        if score < best_score:
            best_score = score
            best_position = pos
    print(f"best position is {best_position} with score {best_score}")


def main(lines: List[str]) -> None:
    assert len(lines) == 1
    positions = [int(pos) for pos in lines[0].split(",")]
    find_best_position(positions, fuel_cost_part_1)
    find_best_position(positions, fuel_cost_part_2)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

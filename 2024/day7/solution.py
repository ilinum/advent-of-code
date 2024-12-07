import time
from typing import Callable


def add_op(x: int, y: int) -> int:
    return x + y


def mul_op(x: int, y: int) -> int:
    return x * y


def concat_op(x: int, y: int) -> int:
    return int(str(x) + str(y))


def has_solution(
    target: int,
    cur: int,
    operands: list[int],
    operators: list[Callable[[int, int], int]],
) -> bool:
    if len(operands) == 0:
        return cur == target
    for op in operators:
        if has_solution(target, op(cur, operands[0]), operands[1:], operators):
            return True
    return False


def parse_equations(lines: list[str]) -> list[tuple[int, list[int]]]:
    eqs = []
    for line in lines:
        result_str, operands_str = line.split(":")
        operands = [int(op) for op in operands_str.strip().split()]
        eqs.append((int(result_str), operands))
    return eqs


def solve_p1(lines: list[str]) -> object:
    valid_results = []
    equations = parse_equations(lines)
    for target, operands in equations:
        if has_solution(target, operands[0], operands[1:], [add_op, mul_op]):
            valid_results.append(target)
    return sum(valid_results)


def solve_p2(lines: list[str]) -> object:
    valid_results = []
    equations = parse_equations(lines)
    for target, operands in equations:
        if has_solution(target, operands[0], operands[1:], [add_op, mul_op, concat_op]):
            valid_results.append(target)
    return sum(valid_results)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    start = time.time()
    print(solve_p1(lines))
    print(solve_p2(lines))
    print(f"processed file '{filename}' in {time.time() - start:.2f}s")


# Part 1: 00:07:10
# Part 2: 00:08:09
if __name__ == "__main__":
    process_file("sample.in")
    process_file("input.in")

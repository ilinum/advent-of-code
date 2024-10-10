from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Condition:
    reg: str
    op: str
    val: int


@dataclass
class Instruction:
    reg: str
    op: str
    val: int
    condition: Condition


def eval_condition(cond: Condition, registers: dict[str, int]) -> bool:
    reg_val = registers[cond.reg]
    if cond.op == ">":
        return reg_val > cond.val
    if cond.op == "<":
        return reg_val < cond.val
    if cond.op == "==":
        return reg_val == cond.val
    if cond.op == "!=":
        return reg_val != cond.val
    if cond.op == "<=":
        return reg_val <= cond.val
    if cond.op == ">=":
        return reg_val >= cond.val
    assert False, f"unsupported condition op: {cond.op}"


def apply_instruction(i: Instruction, registers: dict[str, int]) -> None:
    if eval_condition(i.condition, registers):
        val = i.val
        if i.op == "dec":
            val = val * -1
        registers[i.reg] += val


def parse_instructions(lines: list[str]) -> list[Instruction]:
    instructions = []
    for line in lines:
        (reg, op, val, _, cond_reg, cond_op, cond_val) = line.split()
        instructions.append(
            Instruction(reg, op, int(val), Condition(cond_reg, cond_op, int(cond_val)))
        )
    return instructions


def solve_p1(lines: list[str]) -> object:
    instructions = parse_instructions(lines)
    registers = defaultdict(lambda: 0)
    for i in instructions:
        apply_instruction(i, registers)
    return max(registers.values())


def solve_p2(lines: list[str]) -> object:
    instructions = parse_instructions(lines)
    registers = defaultdict(lambda: 0)
    max_value = 0
    for i in instructions:
        apply_instruction(i, registers)
        max_value = max(registers[i.reg], max_value)
    return max_value


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:06:18
# Part 2: 00:06:55
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

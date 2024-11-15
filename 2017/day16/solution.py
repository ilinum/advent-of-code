from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True)
class SpinInstruction:
    size: int


@dataclass(frozen=True)
class SwapIndexInstruction:
    i: int
    j: int


@dataclass(frozen=True)
class SwapNameInstruction:
    a: str
    b: str


Instruction = SpinInstruction | SwapIndexInstruction | SwapNameInstruction


class Programs:
    def __init__(self, s: str) -> None:
        self.programs = [c for c in s]
        self.name_to_index = {self.programs[i]: i for i in range(len(self.programs))}
        self.start = 0

    @staticmethod
    def create(num_programs: int) -> Programs:
        programs = [""] * num_programs
        for instr in range(num_programs):
            programs[instr] = chr(ord('a') + instr)
        return Programs("".join(programs))

    def execute(self, instr: Instruction) -> None:
        if isinstance(instr, SpinInstruction):
            s = instr.size % len(self.programs)
            self.start -= s
            if self.start < 0:
                self.start = len(self.programs) + self.start
        elif isinstance(instr, SwapIndexInstruction):
            i, j = instr.i, instr.j
            adj_i = (i + self.start) % len(self.programs)
            adj_j = (j + self.start) % len(self.programs)
            self.name_to_index[self.programs[adj_i]], self.name_to_index[self.programs[adj_j]] = adj_j, adj_i
            self.programs[adj_i], self.programs[adj_j] = self.programs[adj_j], self.programs[adj_i]
        elif isinstance(instr, SwapNameInstruction):
            a, b = instr.a, instr.b
            i, j = self.name_to_index[a], self.name_to_index[b]
            self.name_to_index[self.programs[i]], self.name_to_index[self.programs[j]] = j, i
            self.programs[i], self.programs[j] = self.programs[j], self.programs[i]
        else:
            assert False, instr

    def __str__(self) -> str:
        return "".join(self.programs[self.start:] + self.programs[:self.start])


def parse_instructions(instructions: list[str]) -> list[Instruction]:
    result = []
    for instr in instructions:
        if instr.startswith("s"):
            s = int(instr[1:])
            result.append(SpinInstruction(s))
        elif instr.startswith("x"):
            i, j = map(int, instr[1:].split("/"))
            result.append(SwapIndexInstruction(i, j))
        elif instr.startswith("p"):
            a, b = instr[1:].split("/")
            result.append(SwapNameInstruction(a, b))
        else:
            assert False, instr
    return result


def solve_p1(lines: list[str]) -> object:
    instructions = parse_instructions(lines[0].split(","))
    num_programs = 16
    programs = Programs.create(num_programs)
    for instr in instructions:
        programs.execute(instr)
    return str(programs)


def run_dances(programs: Programs, num_dances: int, instructions: list[Instruction]) -> None:
    for _ in range(num_dances):
        for instr in instructions:
            programs.execute(instr)


def solve_p2(lines: list[str]) -> object:
    instructions = parse_instructions(lines[0].split(","))
    num_programs = 16
    programs = Programs.create(num_programs)
    num_dances = 1_000_000_000
    batch_size = 100
    batch_cache = {}
    i = 0
    while i < num_dances:
        i += batch_size
        old_str = str(programs)
        if old_str in batch_cache:
            programs = Programs(batch_cache[old_str])
        else:
            run_dances(programs, batch_size, instructions)
            batch_cache[old_str] = str(programs)
    return str(programs)


def process_file(filename: str) -> None:
    start = time.time()
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))
    print(f"finished processing '{filename}' in {time.time() - start:.2f}s")


# Part 1: 00:23:58
# Part 2: 00:58:01
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

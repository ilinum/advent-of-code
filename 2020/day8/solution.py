import sys
from typing import *


class Instruction:
    def __init__(self, cmd: str, val: int) -> None:
        self.cmd = cmd
        self.val = val

    @classmethod
    def from_string(cls, line: str) -> "Instruction":
        s = line.split()
        return Instruction(s[0], int(s[1]))


def parse_instructions(lines: List[str]) -> List[Instruction]:
    result = []
    for line in lines:
        result.append(Instruction.from_string(line))
    return result

class GenericInterpreterError(RuntimeError):
    pass

class InfiniteLoopError(GenericInterpreterError):
    pass


class Interpreter:
    def __init__(self, instrs: List[Instruction]) -> None:
        self.instrs = instrs
        self.pc = 0
        self.acc = 0
        # For infinite loop detection.
        self.visited = set()

    def advance(self) -> None:
        instr = self.instrs[self.pc]
        if instr.cmd == "nop":
            self.pc += 1
            return
        if instr.cmd == "acc":
            self.pc += 1
            self.acc += instr.val
            return
        if instr.cmd == "jmp":
            self.pc += instr.val
            return
        assert False, instr.cmd

    def is_done(self) -> bool:
        return self.pc == len(self.instrs)

    def execute_to_completion(self) -> int:
        while not self.is_done():
            if self.pc >= len(lines) or self.pc < 0:
                raise GenericInterpreterError()
            if self.pc in self.visited:
                raise InfiniteLoopError()
            self.visited.add(self.pc)
            self.advance()
        return self.acc


def part1(lines: List[str]) -> None:
    interpreter = Interpreter(parse_instructions(lines))
    try:
        interpreter.execute_to_completion()
    except InfiniteLoopError:
        print(interpreter.acc)
        return
    assert False, "no infinite loop"


def try_instrs(instrs: List[Instruction]) -> Optional[int]:
    interp = Interpreter(instrs)
    try:
        interp.execute_to_completion()
    except GenericInterpreterError:
        return None
    return interp.acc


def part2(lines: List[str]) -> None:
    instrs = parse_instructions(lines)
    for i in range(len(instrs)):
        instr = instrs[i]
        if instr.cmd == "nop":
            instrs[i] = Instruction("jmp", instr.val)
        elif instr.cmd == "jmp":
            instrs[i] = Instruction("nop", instr.val)
        else:
            continue
        acc = try_instrs(instrs)
        instrs[i] = instr
        if acc is not None:
            print(acc)
            return
    assert False, "no valid combination found"


# 00:04:31: Part 1 complete.
# 00:15:04: Part 2 complete.
if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    part1(lines)
    part2(lines)

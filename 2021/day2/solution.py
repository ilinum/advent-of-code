import sys

def main(filename: str) -> None:
    with open(filename, "r") as f:
        lines = f.readlines()
        instructions = [Instruction(line) for line in lines]

    pos = PositionPart1()
    for instruction in instructions:
        pos.apply(instruction)
    print(f"part 1 result: {pos.depth * pos.horizontal}")
    pos = PositionPart2()
    for instruction in instructions:
        pos.apply(instruction)
    print(f"part 2 result: {pos.depth * pos.horizontal}")



class Instruction:
    def __init__(self, line: str) -> None:
        s = line.strip().split(" ")
        assert len(s) == 2
        self.direction = s[0]
        assert self.direction in {"forward", "down", "up"}
        self.distance = int(s[1])

    def __repr__(self) -> str:
        return f"{self.direction} {self.distance}"


class PositionPart1:
    def __init__(self):
        self.depth = 0
        self.horizontal = 0

    def apply(self, instruction: Instruction) -> None:
        if instruction.direction == "forward":
            self.horizontal += instruction.distance
        elif instruction.direction == "down":
            self.depth += instruction.distance
        elif instruction.direction == "up":
            self.depth -= instruction.distance
        else:
            assert False, instruction.direction


class PositionPart2:
    def __init__(self):
        self.depth = 0
        self.horizontal = 0
        self.aim = 0

    def apply(self, instruction: Instruction) -> None:
        if instruction.direction == "forward":
            self.horizontal += instruction.distance
            self.depth += self.aim * instruction.distance
        elif instruction.direction == "down":
            self.aim += instruction.distance
        elif instruction.direction == "up":
            self.aim -= instruction.distance
        else:
            assert False, instruction.direction


if __name__ == '__main__':
    main(sys.argv[1])

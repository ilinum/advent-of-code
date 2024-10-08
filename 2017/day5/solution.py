def solve_p1(lines: list[str]) -> object:
    instructions = [int(line) for line in lines]
    pc = 0
    num_steps = 0
    while 0 <= pc < len(instructions):
        old_pc = pc
        pc += instructions[pc]
        instructions[old_pc] += 1
        num_steps += 1
    return num_steps


def solve_p2(lines: list[str]) -> object:
    instructions = [int(line) for line in lines]
    pc = 0
    num_steps = 0
    while 0 <= pc < len(instructions):
        old_pc = pc
        pc += instructions[pc]
        if instructions[old_pc] >= 3:
            instructions[old_pc] -= 1
        else:
            instructions[old_pc] += 1
        num_steps += 1
    return num_steps


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:03:34
# Part 2: 00:04:27
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

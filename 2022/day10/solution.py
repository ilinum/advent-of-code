import collections


class CPU:
    def __init__(self, commands: list[str]) -> None:
        self.commands = collections.deque()
        for cmd in commands:
            if cmd.startswith("addx"):
                # Insert an extra noop because addx command takes two cycles.
                self.commands.append("noop")
                self.commands.append(cmd)
            else:
                self.commands.append(cmd)
        self.register = 1
        self.pc = 0

    def tick(self) -> None:
        cmd = self.commands[self.pc]
        self.pc += 1
        match cmd.split():
            case ["noop"]:
                pass
            case ["addx", v]:
                self.register += int(v)
            case _:
                assert False, f"unknown command {cmd}"

    def has_more(self) -> bool:
        return self.pc < len(self.commands)


class Display:
    def __init__(self, width: int) -> None:
        self.width = width
        self.pos = 0
        self.rows = []

    def tick(self, register: int) -> None:
        if self.pos in (register - 1, register, register + 1):
            self.rows.append("#")
        else:
            self.rows.append(".")
        self.pos += 1
        self.pos = self.pos % self.width

    def format(self) -> str:
        rows = []
        i = 0
        while i + self.width <= len(self.rows):
            rows.append("".join(self.rows[i:i + self.width]))
            i += self.width
        return "\n".join(rows)


def solve_p2(lines: list[str], width: int) -> None:
    cpu = CPU(lines)
    display = Display(width=width)
    while cpu.has_more():
        display.tick(cpu.register)
        cpu.tick()
    print(display.format())


def solve_p1(lines: list[str], width: int) -> None:
    cpu = CPU(lines)
    cycle = 1
    strengths = []
    while cpu.has_more():
        cpu.tick()
        cycle += 1
        if (cycle - 20) % width == 0:
            strengths.append(cycle * cpu.register)
    print(sum(strengths))


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    solve_p1(lines, width=40)
    solve_p2(lines, width=40)


# Part 1: 00:10:29
# Part 2: 00:27:30
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

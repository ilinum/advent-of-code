from collections import deque


class Stacks:
    def __init__(self, lines: list[str]) -> None:
        stacks = []
        for line in lines:
            line = line.replace("    ", ".").replace(" ", "").replace("[", "").replace("]", "")
            for i, c in enumerate(line.strip()):
                while len(stacks) <= i:
                    stacks.append(deque())
                if c != ".":
                    stacks[i].appendleft(c)
        self.stacks = stacks

    def move(self, from_stack: int, to_stack: int, count: int = 1) -> None:
        from_idx = from_stack - 1
        to_idx = to_stack - 1
        blocks = []
        for _ in range(count):
            blocks.append(self.stacks[from_idx].pop())
        self.stacks[to_idx].extend(reversed(blocks))

    def __str__(self):
        return str(self.stacks)


def solve_p2(lines: list[str]) -> str:
    i = 0
    for i in range(len(lines)):
        if len(lines[i].strip()) == 0:
            break
    stacks = Stacks(lines[:i - 1])
    for line in lines[i + 1:]:
        s = line.split()
        num, from_stack, to_stack = int(s[1]), int(s[3]), int(s[5])
        stacks.move(from_stack, to_stack, count=num)
    return "".join([s[-1] for s in stacks.stacks])


def solve_p1(lines: list[str]) -> str:
    i = 0
    for i in range(len(lines)):
        if len(lines[i].strip()) == 0:
            break
    stacks = Stacks(lines[:i - 1])
    for line in lines[i + 1:]:
        s = line.split()
        num, from_stack, to_stack = int(s[1]), int(s[3]), int(s[5])
        for _ in range(num):
            stacks.move(from_stack, to_stack)
    return "".join([s[-1] for s in stacks.stacks])


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x, f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:27:52
# Part 2: 00:32:11
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

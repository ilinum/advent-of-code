from collections import deque


def mul(a: int, b: int) -> int:
    return a * b


def add(a: int, b: int) -> int:
    return a + b


class Operation:
    def __init__(self, line: str) -> None:
        assert line.startswith("new=")
        line = line.removeprefix("new=")
        assert "*" in line or "+" in line
        if "*" in line:
            args = line.split("*")
            self.op = mul
        else:
            args = line.split("+")
            self.op = add

        self.arg1, self.arg2 = args
        if self.arg1 != "old":
            self.arg1 = int(self.arg1)
        if self.arg2 != "old":
            self.arg2 = int(self.arg2)

    def apply(self, item: int) -> int:
        arg1 = item if self.arg1 == "old" else self.arg1
        arg2 = item if self.arg2 == "old" else self.arg2
        return self.op(arg1, arg2)


class Test:
    def __init__(self, lines: list[str]) -> None:
        assert lines[0].startswith("Test:divisibleby")
        self.divisible_by = int(lines[0].removeprefix("Test:divisibleby"))
        self.if_true = int(lines[1].removeprefix("Iftrue:throwtomonkey"))
        self.if_false = int(lines[2].removeprefix("Iffalse:throwtomonkey"))

    def monkey_to_throw(self, item: int) -> int:
        if item % self.divisible_by == 0:
            return self.if_true
        else:
            return self.if_false


class Monkey:
    def __init__(self, lines: list[str], divide_by: int) -> None:
        assert len(lines) == 6, lines
        lines = [line.replace(" ", "") for line in lines]
        self.index = int(lines[0].removesuffix(":").removeprefix("Monkey"))
        self.items = deque(int(i) for i in lines[1].removeprefix("Startingitems:").split(","))
        self.op = Operation(lines[2].removeprefix("Operation:"))
        self.test = Test(lines[3:])
        self.divide_by = divide_by
        self.mod_by = 1
        self.items_processed = 0

    def run(self) -> tuple[int, int]:
        assert len(self.items) > 0
        self.items_processed += 1
        item = self.items.pop()
        item = self.op.apply(item)
        item = item // self.divide_by
        item = item % self.mod_by
        return item, self.test.monkey_to_throw(item)


def parse_input(lines: list[str], divide_by: int) -> list[Monkey]:
    buf = []
    result = []
    for line in lines:
        if line == "":
            # There's an empty line between each monkey.
            result.append(Monkey(buf, divide_by=divide_by))
            buf = []
        else:
            buf.append(line)
    if len(buf) > 0:
        result.append(Monkey(buf, divide_by=divide_by))
    # When we get to really large numbers, multiplication gets very expensive.
    # We can do the trick where we mod by the multiplication of all the
    # test conditions, which shouldn't change the result.
    mod_by = 1
    for m in result:
        mod_by *= m.test.divisible_by
    for m in result:
        m.mod_by = mod_by
    return result


def solve(lines: list[str], num_rounds: int, divide_by: int) -> None:
    monkeys = parse_input(lines, divide_by=divide_by)
    for r in range(num_rounds):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                item, target = monkey.run()
                monkeys[target].items.append(item)
    processed = list(reversed(sorted(m.items_processed for m in monkeys)))
    print(processed[0] * processed[1])


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    solve(lines, num_rounds=20, divide_by=3)
    solve(lines, num_rounds=10000, divide_by=1)


# Part 1: 00:34:59
# Part 2: 01:14:04
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

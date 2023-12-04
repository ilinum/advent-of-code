import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def neighbors(self) -> set["Pos"]:
        result = set()
        for x in (self.x - 1, self.x, self.x + 1):
            for y in (self.y - 1, self.y, self.y + 1):
                if x == self.x and y == self.y:
                    continue
                result.add(Pos(x=x, y=y))

        return result


@dataclass(frozen=True)
class Number:
    value: int
    start_x: int
    end_x: int
    y: int

    def positions(self) -> set[Pos]:
        result = set()
        for x in range(self.start_x, self.end_x + 1):
            result.add(Pos(x, self.y))
        return result


def find_numbers(lines: list[str]) -> dict[Pos, Number]:
    numbers = {}
    for y in range(len(lines)):
        line = lines[y]
        cur_num = ""
        for x in range(len(line)):
            c = line[x]
            if c.isnumeric():
                cur_num += c
            elif len(cur_num) > 0:
                num = Number(
                    value=int(cur_num),
                    start_x=x - len(cur_num),
                    end_x=x - 1,
                    y=y,
                )
                for pos in num.positions():
                    numbers[pos] = num
                cur_num = ""

        if len(cur_num) > 0:
            num = Number(
                value=int(cur_num),
                start_x=len(line) - len(cur_num),
                end_x=len(line) - 1,
                y=y,
            )
            for pos in num.positions():
                numbers[pos] = num
    return numbers


def solve_p1(lines: list[str]) -> object:
    numbers = find_numbers(lines)
    symbols: set[Pos] = set()
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            c = line[x]
            if not c.isnumeric() and c != ".":
                symbols.add(Pos(x=x, y=y))

    part_numbers = set()
    for sym in symbols:
        for pos in sym.neighbors():
            if pos in numbers:
                part_numbers.add(numbers[pos])
    return sum(n.value for n in part_numbers)


def solve_p2(lines: list[str]) -> object:
    numbers: dict[Pos, Number] = find_numbers(lines)
    gears: set[Pos] = set()
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            if line[x] == "*":
                gears.add(Pos(x=x, y=y))

    gear_ratios = []
    for gear in gears:
        gear_nums = set()
        for n in gear.neighbors():
            if n in numbers:
                gear_nums.add(numbers[n])
        assert len(gear_nums) in (0, 1, 2)
        if len(gear_nums) == 2:
            (n1, n2) = tuple(gear_nums)
            gear_ratios.append(n1.value * n2.value)
    return sum(gear_ratios)


def process_file(filename: str) -> None:
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:17:58
# Part 2: 00:26:54
if __name__ == '__main__':
    for file in ("sample.in", "input.in"):
        start = time.time()
        print(f"processing '{file}'")
        process_file(file)
        end = time.time()
        print(f"processed '{file}' in {end - start:.2f}s")

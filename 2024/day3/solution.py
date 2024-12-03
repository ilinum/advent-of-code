import re


def eval_line(line: str) -> int:
    p = re.compile(r"mul\(\d\d?\d?,\d\d?\d?\)")
    result = 0
    for match in p.findall(line):
        a, b = match.removeprefix("mul(").removesuffix(")").split(",")
        result += int(a) * int(b)
    return result


def solve_p1(lines: list[str]) -> object:
    result = 0
    for line in lines:
        result += eval_line(line)
    return result


def solve_p2(lines: list[str]) -> object:
    line = "".join(lines)
    splits = line.split("don't()")
    result = eval_line(splits[0])
    for split in splits[1:]:
        enabled = split.split("do()")[1:]
        for e in enabled:
            result += eval_line(e)
    return result


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:09:58
# Part 2: 00:14:19
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

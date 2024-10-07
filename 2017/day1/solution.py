def solve(line: str, advance: int) -> int:
    result = 0
    for i in range(len(line)):
        x = int(line[i])
        y = int(line[(i + advance) % len(line)])
        if x == y:
            result += x
    return result


def solve_p1(lines: list[str]) -> object:
    assert len(lines) == 1
    return solve(lines[0], advance=1)


def solve_p2(lines: list[str]) -> object:
    assert len(lines) == 1
    line = lines[0]
    return solve(line, advance=len(line) // 2)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:04:54
# Part 2: 00:06:40
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

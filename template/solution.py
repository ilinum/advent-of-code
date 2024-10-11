def solve_p1(lines: list[str]) -> object:
    return None


def solve_p2(lines: list[str]) -> object:
    return None


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1:
# Part 2:
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

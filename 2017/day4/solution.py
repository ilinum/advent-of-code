def solve_p1(lines: list[str]) -> object:
    num_valid = 0
    for line in lines:
        p = line.split()
        if len(list(set(p))) == len(list(p)):
            num_valid += 1
    return num_valid


def solve_p2(lines: list[str]) -> object:
    num_valid = 0
    for line in lines:
        p = ["".join(sorted(w)) for w in line.split()]
        if len(list(set(p))) == len(list(p)):
            num_valid += 1
    return num_valid


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:01:02
# Part 2: 00:03:42
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

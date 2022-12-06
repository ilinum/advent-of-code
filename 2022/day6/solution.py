def distinct_contiguous_index(msg: str, num_contiguous: int) -> int:
    assert len(msg) > num_contiguous
    for i in range(num_contiguous, len(msg)):
        chars = msg[i - num_contiguous:i]
        if len(set(chars)) == len(chars):
            return i
    return 0


def solve_p2(lines: list[str]) -> None:
    for line in lines:
        print(distinct_contiguous_index(line, num_contiguous=14))


def solve_p1(lines: list[str]) -> None:
    for line in lines:
        print(distinct_contiguous_index(line, num_contiguous=4))


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    solve_p1(lines)
    solve_p2(lines)


# Part 1: 00:04:21
# Part 2: 00:05:14
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

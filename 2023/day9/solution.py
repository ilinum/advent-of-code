import time


def find_next_seq_number(seq: list[int]) -> int:
    if len(seq) == 0 or all(v == 0 for v in seq):
        return 0
    next_seq = []
    for i in range(1, len(seq)):
        next_seq.append(seq[i] - seq[i - 1])
    return seq[-1] + find_next_seq_number(next_seq)


def solve_p1(lines: list[str]) -> object:
    next_numbers = []
    for line in lines:
        next_numbers.append(find_next_seq_number(list(map(int, line.split()))))
    return sum(next_numbers)


def find_prev_seq_number(seq: list[int]) -> int:
    if len(seq) == 0 or all(v == 0 for v in seq):
        return 0
    next_seq = []
    for i in range(1, len(seq)):
        next_seq.append(seq[i] - seq[i - 1])
    return seq[0] - find_prev_seq_number(next_seq)


def solve_p2(lines: list[str]) -> object:
    prev_numbers = []
    for line in lines:
        prev_numbers.append(find_prev_seq_number(list(map(int, line.split()))))
    return sum(prev_numbers)


def process_file(filename: str) -> None:
    start = time.time()
    print(f"processing '{file}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))
    end = time.time()
    print(f"processed '{file}' in {end - start:.2f}s")


# Part 1: 00:10:55
# Part 2: 00:13:14
if __name__ == '__main__':
    for file in [
        "sample.in",
        "input.in",
    ]:
        process_file(file)

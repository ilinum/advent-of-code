def solve_p1(lines: list[str]) -> object:
    l1, l2 = [], []
    for line in lines:
        (a, b) = line.split()
        l1.append(int(a))
        l2.append(int(b))
    l1.sort()
    l2.sort()
    return sum(abs(a-b) for a, b in zip(l1, l2))

def solve_p2(lines: list[str]) -> object:
    l1 = []
    freqs = {}
    for line in lines:
        (a, b) = line.split()
        l1.append(int(a))
        freqs[int(b)] = freqs.get(int(b), 0) + 1
    return sum(freqs.get(n, 0) * n for n in l1)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:02:22
# Part 2: 00:04:05
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

def solve_p1(lines: list[str]) -> object:
    values = [int(line) for line in lines]
    return sum(values)

def solve_p2(lines: list[str]) -> object:
    values = [int(line) for line in lines]
    seen = set()
    cur = 0
    i = 0
    while cur not in seen:
        seen.add(cur)
        cur += values[i]
        i = (i+1) % len(values)
    return cur



def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:01:52
# Part 2: 00:06:06
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

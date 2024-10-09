def process_reactions(s: str) -> str:
    result = []
    i = 0
    while i < len(s):
        if i == len(s) - 1 or s[i] == s[i + 1] or s[i].lower() != s[i + 1].lower():
            result.append(s[i])
            i += 1
        else:
            i += 2
    return "".join(result)


def reduce_polymer(last: str) -> str:
    processed = process_reactions(last)
    while len(processed) != len(last):
        last = processed
        processed = process_reactions(last)
    return processed


def solve_p1(lines: list[str]) -> object:
    return len(reduce_polymer(lines[0]))


def solve_p2(lines: list[str]) -> object:
    all_chars = set(lines[0].lower())
    lengths = []
    for c in all_chars:
        reduced = reduce_polymer(lines[0].replace(c, "").replace(c.upper(), ""))
        lengths.append(len(reduced))
    return min(lengths)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:09:56
# Part 2: 00:13:41
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

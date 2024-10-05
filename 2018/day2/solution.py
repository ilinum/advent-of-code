def solve_p1(lines: list[str]) -> object:
    id_freqs = []
    for line in lines:
        freqs = {}
        for c in line:
            freqs[c] = freqs.get(c, 0) + 1
        id_freqs.append(freqs)
    num_doubles = 0
    num_triples = 0
    for freqs in id_freqs:
        if 2 in freqs.values():
            num_doubles += 1
        if 3 in freqs.values():
            num_triples += 1
    return num_doubles * num_triples

def common_letters(a: str, b: str) -> str:
    result = []
    for x, y in zip(a, b):
        if x == y:
            result.append(x)
    return "".join(result)

def solve_p2(lines: list[str]) -> object:
    for i in range(len(lines)):
        a = lines[i]
        for b in lines[i+1:]:
            assert len(a) == len(b)
            common = common_letters(a, b)
            if len(common) == len(a)-1:
                return common
    assert False, "no matches found"


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:04:25
# Part 2: 00:11:29
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

def cancel_out_dirs(dirs: list[str]) -> list[str]:
    counts = {
        "n": 0,
        "ne": 0,
        "nw": 0,
        "se": 0,
        "sw": 0,
        "s": 0,
    }
    for d in dirs:
        counts[d] += 1

    for _ in range(2):
        combos = [
            ("ne", "nw", "n"),
            ("se", "sw", "s"),
            ("ne", "s", "se"),
            ("nw", "s", "sw"),
            ("sw", "n", "nw"),
            ("se", "n", "ne"),
        ]
        for (a, b, new) in combos:
            counts[new] += min(counts[a], counts[b])
            if counts[a] >= counts[b]:
                counts[a] -= counts[b]
                counts[b] = 0
            else:
                counts[b] -= counts[a]
                counts[a] = 0

        cancel_out = [("n", "s"), ("ne", "sw"), ("nw", "se")]
        for (a, b) in cancel_out:
            if counts[a] >= counts[b]:
                counts[a] -= counts[b]
                counts[b] = 0
            else:
                counts[b] -= counts[a]
                counts[a] = 0

    new_dirs = []
    for d, count in counts.items():
        new_dirs.extend([d] * count)
    return new_dirs


def solve_p1(lines: list[str]) -> object:
    assert len(lines) > 0
    results = []
    for line in lines:
        dirs = line.split(",")
        shortest = cancel_out_dirs(dirs)
        results.append(len(shortest))
    return results


def solve_p2(lines: list[str]) -> object:
    assert len(lines) > 0
    results = []
    for line in lines:
        dirs = line.split(",")
        distances = []
        for i in range(len(dirs)+1):
            distances.append(len(cancel_out_dirs(dirs[:i])))
        results.append(max(distances))
    return results


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:25:19
# Part 2: 00:27:37
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

def priority(char: str) -> int:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    assert char.lower() in alphabet
    result = alphabet.index(char.lower()) + 1
    if char.isupper():
        result += 26
    return result


def solve_p2(lines: list[str]) -> int:
    scores = []
    assert len(lines) % 3 == 0
    for i in range(0, len(lines), 3):
        assert i + 2 < len(lines)
        group = lines[i:i + 3]
        group_sets = [set(line) for line in group]
        item_intersection = group_sets[0]
        for s in group_sets[1:]:
            item_intersection.intersection_update(s)
        assert len(item_intersection) == 1
        scores.append(priority(item_intersection.pop()))
    return sum(scores)


def solve_p1(lines: list[str]) -> int:
    scores = []
    for line in lines:
        assert len(line) % 2 == 0
        mid = len(line) // 2
        first, second = line[:mid], line[mid:]
        in_both = set(first).intersection(set(second))
        scores.extend(priority(char) for char in in_both)
    return sum(scores)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:08:02
# Part 2: 00:14:23
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

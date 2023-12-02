REPLACEMENTS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

REPLACEMENTS_REVERSED = {
    s[::-1]: d for (s, d) in REPLACEMENTS.items()
}


def find_first_digit(s: str, replacements: dict[str, int]) -> int:
    for i in range(len(s)):
        # Try all possible lengths of digits.
        start = max(0, i - max(len(x) for x in replacements.keys()))
        for lower in range(start, i):
            if s[lower:i] in replacements:
                return replacements[s[lower:i]]
        try:
            return int(s[i])
        except ValueError:
            pass
    raise RuntimeError(f"No digit found: {s}")


def solve(lines: list[str]) -> object:
    values = []
    for line in lines:
        first = find_first_digit(line, REPLACEMENTS)
        last = find_first_digit(line[::-1], REPLACEMENTS_REVERSED)
        values.append(int(str(first) + str(last)))
    return sum(values)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve(lines))


# Part 1: 00:05:00
# Part 2: 00:25:00
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

def parse_elf_calories(lines: list[str]) -> list[int]:
    elf_cal = []
    cur = 0
    for line in lines:
        if len(line) == 0:
            elf_cal.append(cur)
            cur = 0
            continue
        cur += int(line)
    elf_cal.append(cur)
    return list(reversed(sorted(elf_cal)))


def solve(lines: list[str]) -> None:
    elf_cal = parse_elf_calories(lines)
    # Part 1: max calories.
    print(elf_cal[0])
    # Part 2: sum of top 3.
    print(sum(elf_cal[:3]))


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    solve(lines)


# Part 1: 00:03:10
# Part 2: 00:06:00
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

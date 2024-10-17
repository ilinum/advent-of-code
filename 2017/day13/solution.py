import time


def scanner_location(r: int, t: int) -> int:
    cycle_length = (r - 1) * 2
    if t >= cycle_length:
        t = t % cycle_length

    result = 0
    while t > 0 and result < r:
        t -= 1
        result += 1
    while t > 0:
        result -= 1
        t -= 1
    return result


def parse_scanners(lines: list[str]) -> dict[int, int]:
    result = {}
    for line in lines:
        depth, range_str = line.split(": ")
        result[int(depth)] = int(range_str)
    return result


def solve_p1(lines: list[str]) -> object:
    scanners = parse_scanners(lines)
    t = 0
    severities = []
    for d in range(min(scanners), max(scanners) + 1):
        scanner = scanners.get(d, None)
        if scanner is not None and scanner_location(scanner, t) == 0:
            severities.append(d * scanner)
        t += 1
    return sum(severities)


def is_caught(t: int, scanners: dict[int, int]) -> bool:
    for d in range(min(scanners), max(scanners) + 1):
        scanner = scanners.get(d, None)
        if scanner is not None and scanner_location(scanner, t) == 0:
            return True
        t += 1
    return False


def solve_p2(lines: list[str]) -> object:
    scanners = parse_scanners(lines)
    t = 0
    start = time.time()
    while True:
        if t % 100000 == 0:
            print(f"trying t={t}, seconds since start: {time.time() - start:,.2f}s")
        if not is_caught(t, scanners):
            return t
        t += 1


def run_tests() -> None:
    assert scanner_location(2, 0) == 0
    assert scanner_location(2, 1) == 1
    assert scanner_location(2, 2) == 0
    assert scanner_location(2, 3) == 1
    assert scanner_location(2, 4) == 0
    assert scanner_location(2, 5) == 1
    assert scanner_location(2, 6) == 0
    assert scanner_location(4, 6) == 0


def process_file(filename: str) -> None:
    run_tests()
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:18:58
# Part 2: 00:28:40
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

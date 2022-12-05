class Range:
    def __init__(self, s: str) -> None:
        x0, x1 = s.split("-")
        self.x0 = int(x0)
        self.x1 = int(x1)
        assert self.x0 <= self.x1

    def contains(self, other: "Range") -> bool:
        return self.x0 <= other.x0 and self.x1 >= other.x1

    def overlaps(self, other: "Range") -> bool:
        are_disjoint = self.x1 < other.x0 or other.x1 < self.x0
        return not are_disjoint


def solve_p2(lines: list[str]) -> int:
    overlaps = 0
    for line in lines:
        s1, s2 = line.split(",")
        r1, r2 = Range(s1), Range(s2)
        if r1.overlaps(r2):
            overlaps += 1
    return overlaps


def solve_p1(lines: list[str]) -> int:
    fully_contained = 0
    for line in lines:
        s1, s2 = line.split(",")
        r1, r2 = Range(s1), Range(s2)
        if r1.contains(r2) or r2.contains(r1):
            fully_contained += 1
    return fully_contained


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:06:12
# Part 2: 00:08:28
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

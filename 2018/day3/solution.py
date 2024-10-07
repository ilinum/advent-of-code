from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    id: str
    x_start: int
    y_start: int
    x_end: int
    y_end: int

    def overlaps(self, other: "Claim") -> bool:
        x_start = max(self.x_start, other.x_start)
        x_end = min(self.x_end, other.x_end)
        y_start = max(self.y_start, other.y_start)
        y_end = min(self.y_end, other.y_end)
        if x_start >= x_end or y_start >= y_end:
            return False
        return True


def parse_claim(line: str) -> Claim:
    (id_str, location) = line.replace(" ", "").split("@")
    (coordinates, dimensions) = location.split(":")
    (x_start, y_start) = coordinates.split(",")
    (width, height) = dimensions.split("x")
    return Claim(
        id=id_str,
        x_start=int(x_start),
        y_start=int(y_start),
        x_end=int(x_start) + int(width),
        y_end=int(y_start) + int(height),
    )


def solve_p1(lines: list[str]) -> object:
    claims = [parse_claim(line) for line in lines]
    claimed_squares = set()
    double_claimed = set()
    for claim in claims:
        for x in range(claim.x_start, claim.x_end):
            for y in range(claim.y_start, claim.y_end):
                square = (x, y)
                if square in claimed_squares:
                    double_claimed.add((x, y))
                claimed_squares.add((x, y))

    return len(double_claimed)


def solve_p2(lines: list[str]) -> object:
    claims = [parse_claim(line) for line in lines]
    for i in range(len(claims)):
        overlaps = False
        for j in range(len(claims)):
            if i == j:
                continue
            overlaps = claims[i].overlaps(claims[j])
            if overlaps:
                break
        if not overlaps:
            return claims[i].id
    assert False, "no non-overlapping claim found"


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 01:07:01
# Part 2: 01:11:42
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

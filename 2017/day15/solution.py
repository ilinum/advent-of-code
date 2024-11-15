from dataclasses import dataclass


@dataclass
class Generator:
    cur: int
    factor: int
    divisor: int | None = None

    def _next(self) -> int:
        result = (self.cur * self.factor) % 2147483647
        self.cur = result
        return result

    def next(self) -> int:
        if self.divisor is None:
            return self._next()
        r = self._next()
        while r % self.divisor != 0:
            r = self._next()
        return r

def solve_p1(lines: list[str]) -> object:
    assert len(lines) == 2
    generators = [
        Generator(int(lines[0].lstrip("generator a starts with ")), 16807),
        Generator(int(lines[1].lstrip("generator b starts with ")), 48271),
    ]
    num_iterations = 40_000_000
    score = 0
    for i in range(num_iterations):
        vals = [g.next() for g in generators]
        vals = [v & 0xffff for v in vals]
        if len(set(vals)) == 1:
            score += 1
    return score


def solve_p2(lines: list[str]) -> object:
    assert len(lines) == 2
    generators = [
        Generator(int(lines[0].lstrip("generator a starts with ")), 16807, divisor=4),
        Generator(int(lines[1].lstrip("generator b starts with ")), 48271, divisor=8),
    ]
    num_iterations = 5_000_000
    score = 0
    for i in range(num_iterations):
        vals = [g.next() for g in generators]
        vals = [v & 0xffff for v in vals]
        if len(set(vals)) == 1:
            score += 1
    return score


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:27:24
# Part 2: 00:52:39
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

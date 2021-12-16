import sys
from typing import *

RISK_UNKNOWN = -1


class Point:
    def __init__(self, x: int, y: int, risk: int) -> None:
        self.x = x
        self.y = y
        self.risk = risk

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __lt__(self, other) -> bool:
        if not isinstance(other, Point):
            raise RuntimeError()
        return self.risk.__lt__(other.risk)


def compute_risks(grid: List[List[int]], start: Point) -> List[List[int]]:
    min_risk = [[RISK_UNKNOWN] * len(row) for row in grid]
    min_risk[start.y][start.x] = start.risk
    to_visit = {start}
    while len(to_visit) > 0:
        cur = min(to_visit)
        to_visit.remove(cur)
        cur_risk = min_risk[cur.y][cur.x]
        assert cur_risk >= 0, (cur.x, cur.y)
        for xd, yd in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
            if xd == 0 and yd == 0:
                continue
            n = Point(cur.x + xd, cur.y + yd, RISK_UNKNOWN)
            if n.y < 0 or n.y >= len(grid) or n.x < 0 or n.x >= len(grid[n.y]):
                continue
            n.risk = min_risk[n.y][n.x]
            new_risk = cur_risk + grid[n.y][n.x]
            if n.risk == RISK_UNKNOWN or n.risk > new_risk:
                min_risk[n.y][n.x] = new_risk
                n.risk = new_risk
                # Found a lower-risk path to that point! Recompute the risks around.
                to_visit.add(n)

    return min_risk


def format_grid(grid: List[List[int]]) -> str:
    rows = []
    for row in grid:
        rows.append("".join(str(c) for c in row))
    return "\n".join(rows)


def parse_grid(lines: List[str]) -> List[List[int]]:
    grid = []
    for line in lines:
        row = [int(c) for c in line]
        grid.append(row)
    return grid


def get_scaled_value(val: int, factor: int) -> int:
    if val + factor < 10:
        return val + factor
    return (val + factor + 1) % 10


def scale_up(original: List[List[int]], factor: int) -> List[List[int]]:
    result = []
    for orig_row in original:
        new_row = []
        for f in range(factor):
            new_row.extend(get_scaled_value(val, f) for val in orig_row)
        result.append(new_row)

    assert len(original) == len(result)
    assert len(original[0]) * factor == len(result[0])
    for f in range(1, factor):
        for row in result[:len(original)]:
            result.append([get_scaled_value(val, f) for val in row])

    assert len(original) * factor == len(result)
    assert len(original[0]) * factor == len(result[0])
    return result


def main(lines: List[str]) -> None:
    grid = parse_grid(lines)
    risks = compute_risks(grid, Point(0, 0, 0))
    print(risks[-1][-1])

    grid = scale_up(parse_grid(lines), 5)
    risks = compute_risks(grid, Point(0, 0, 0))
    print(risks[-1][-1])


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

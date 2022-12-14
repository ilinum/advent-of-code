import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


def parse_input(lines: list[str]) -> list[list[Coord]]:
    grid = []
    for line in lines:
        line = line.replace(" ", "")
        splits = line.split("->")
        row = []
        for s in splits:
            x, y = s.split(",")
            row.append(Coord(int(x), int(y)))
        grid.append(row)
    return grid


def get_rock_locations(rows: list[list[Coord]]) -> set[Coord]:
    grid: set[Coord] = set()
    for row in rows:
        for i in range(1, len(row)):
            start = row[i - 1]
            end = row[i]
            if start.x == end.x:
                for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                    grid.add(Coord(start.x, y))
            else:
                assert start.y == end.y
                for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
                    grid.add(Coord(x, start.y))
    return grid


def solve_p2(lines: list[str]) -> object:
    rows = parse_input(lines)
    grid = get_rock_locations(rows)
    num_rocks = len(grid)
    max_y = max(c.y for c in grid)
    floor = max_y + 2
    cur = Coord(500, 0)
    while True:
        moved = False
        for new_coord in [
            Coord(cur.x, cur.y + 1),
            Coord(cur.x - 1, cur.y + 1),
            Coord(cur.x + 1, cur.y + 1),
        ]:
            if new_coord not in grid and new_coord.y != floor:
                cur = new_coord
                moved = True
                break
        if not moved:
            if cur in grid:
                break
            grid.add(cur)
            cur = Coord(500, 0)
    num_sands = len(grid) - num_rocks
    return num_sands


def solve_p1(lines: list[str]) -> object:
    rows = parse_input(lines)
    grid = get_rock_locations(rows)
    num_rocks = len(grid)
    max_y = max(c.y for c in grid)
    cur = Coord(500, 0)
    while cur.y < max_y:
        moved = False
        for new_coord in [
            Coord(cur.x, cur.y + 1),
            Coord(cur.x - 1, cur.y + 1),
            Coord(cur.x + 1, cur.y + 1),
        ]:
            if new_coord not in grid:
                cur = new_coord
                moved = True
                break
        if not moved:
            grid.add(cur)
            cur = Coord(500, 0)
    num_sands = len(grid) - num_rocks
    return num_sands


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    print(solve_p1(lines))
    print(solve_p2(lines))


def main() -> None:
    for f in os.listdir():
        if f.endswith("in"):
            process_file(f)


# Part 1: 00:18:12
# Part 2: 00:23:38
if __name__ == '__main__':
    main()

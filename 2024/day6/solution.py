from __future__ import annotations

from dataclasses import dataclass

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
@dataclass(frozen=True)
class Guard:
    loc: tuple[int, int]
    dir_index: int

    def _dir(self) -> tuple[int, int]:
        return DIRS[self.dir_index]

    def advance(self) -> Guard:
        d = self._dir()
        loc = (self.loc[0] + d[0], self.loc[1] + d[1])
        return Guard(loc, self.dir_index)

    def turn(self) -> Guard:
        dir_index = (self.dir_index + 1) % len(DIRS)
        return Guard(self.loc, dir_index)

def has_loop(grid: dict[tuple[int, int], str], guard: Guard) -> bool:
    visited = set()
    while guard.loc in grid:
        next_guard = guard.advance()
        if grid.get(next_guard.loc, ".") == "#":
            guard = guard.turn()
            continue
        if guard in visited:
            return True
        visited.add(guard)
        guard = next_guard
    return False

def parse_grid(lines: list[str]) -> tuple[dict[tuple[int, int], str], Guard]:
    grid = {}
    guard = None
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            c = lines[y][x]
            if c == "^":
                guard = Guard((x, y), dir_index=0)
                c = "."
            assert c in (".", "#")
            grid[(x, y)] = c
    assert guard is not None
    return grid, guard

def solve_p1(lines: list[str]) -> object:
    grid, guard = parse_grid(lines)
    visited = set()
    while guard.loc in grid:
        next_guard = guard.advance()
        if grid.get(next_guard.loc, ".") == "#":
            guard = guard.turn()
            continue
        visited.add(guard.loc)
        guard = next_guard
    return len(visited)


def solve_p2(lines: list[str]) -> object:
    grid, guard = parse_grid(lines)

    count = 0
    for loc in grid:
        if grid[loc] == "#":
            continue
        grid[loc] = "#"
        if has_loop(grid, guard):
            count += 1
        grid[loc] = "."
    return count


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:10:13
# Part 2: 00:15:02
if __name__ == "__main__":
    process_file("sample.in")
    process_file("input.in")

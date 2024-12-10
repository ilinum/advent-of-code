import time


def paths_to_peak(
    grid: dict[tuple[int, int], int], start: tuple[int, int]
) -> set[tuple]:
    to_visit = [(start, tuple())]
    visited = set()
    peaks = set()
    while len(to_visit) > 0:
        cur, path = to_visit.pop()
        if (cur, path) in visited:
            continue
        visited.add((cur, path))
        if grid[cur] == 9:
            peaks.add((cur, path))
        for xd, yd in [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
        ]:
            new_c = (cur[0] + xd, cur[1] + yd)
            if new_c not in grid:
                continue
            if grid[new_c] - grid[cur] == 1:
                to_visit.append((new_c, path + (cur,)))
    return peaks


def accessible_peaks(
    grid: dict[tuple[int, int], int], start: tuple[int, int]
) -> set[tuple[int, int]]:
    return set(loc for loc, _ in paths_to_peak(grid, start))


def parse_grid(lines: list[str]) -> dict[tuple[int, int], int]:
    grid = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            grid[(x, y)] = int(lines[y][x])
    return grid


def solve_p1(lines: list[str]) -> object:
    grid = parse_grid(lines)
    result = 0
    for coord, val in grid.items():
        if val == 0:
            result += len(accessible_peaks(grid, coord))
    return result


def solve_p2(lines: list[str]) -> object:
    grid = parse_grid(lines)
    result = 0
    for coord, val in grid.items():
        if val == 0:
            result += len(paths_to_peak(grid, coord))
    return result


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    start = time.time()
    print(solve_p1(lines))
    print(solve_p2(lines))
    print(f"processed file '{filename}' in {time.time() - start:.2f}s")


# Part 1: 00:08:30
# Part 2: 00:13:07
if __name__ == "__main__":
    process_file("sample.in")
    process_file("input.in")

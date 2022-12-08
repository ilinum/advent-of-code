def in_bounds(grid: list[list[int]], row: int, col: int) -> bool:
    return 0 <= row < len(grid) and 0 <= col < len(grid[row])


def is_visible(grid: list[list[int]], row: int, col: int) -> bool:
    height = grid[row][col]
    for rd, cd in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        cr = row + rd
        cc = col + cd
        visible = True
        while in_bounds(grid, cr, cc) and visible:
            if height <= grid[cr][cc]:
                visible = False
            cr += rd
            cc += cd
        if visible:
            return True
    return False


def scenic_score(grid: list[list[int]], row: int, col: int) -> int:
    height = grid[row][col]
    result = 1
    for rd, cd in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        cr = row + rd
        cc = col + cd
        num_visible = 0
        while in_bounds(grid, cr, cc):
            num_visible += 1
            if height <= grid[cr][cc]:
                break
            cr += rd
            cc += cd
        result *= num_visible

    return result


def solve(lines: list[str]) -> None:
    grid = []
    for line in lines:
        row = []
        for c in line:
            row.append(int(c))
        grid.append(row)
    num_visible = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if is_visible(grid, r, c):
                num_visible += 1
    print(num_visible)
    scores = []
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            scores.append(scenic_score(grid, r, c))
    print(max(scores))


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    solve(lines)


# Part 1: 00:08:48
# Part 2: 00:12:35
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

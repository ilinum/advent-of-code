def count_occurences(grid: list[list[str]], word: list[str]) -> int:
    result = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            for ic, jc in [
                (1, 0),
                (0, 1),
                (1, 1),
                (-1, 0),
                (0, -1),
                (-1, -1),
                (-1, 1),
                (1, -1),
            ]:
                cur = []
                cur_i = i
                cur_j = j
                while (
                    len(cur) < len(word)
                    and 0 <= cur_i < len(grid)
                    and 0 <= cur_j < len(grid[i])
                ):
                    cur.append(grid[cur_i][cur_j])
                    cur_i += ic
                    cur_j += jc
                if cur == word:
                    result += 1
    return result


def solve_p1(lines: list[str]) -> object:
    grid = [list(l) for l in lines]
    return count_occurences(grid, list("xmas"))


def has_x_mas(grid: list[list[str]], i: int, j: int) -> int:
    if grid[i][j] != "a":
        return False
    chars = []
    for new_i, new_j in [
        (i - 1, j - 1),
        (i + 1, j + 1),
        (i - 1, j + 1),
        (i + 1, j - 1),
    ]:
        if new_i < 0 or new_i >= len(grid):
            continue
        if new_j < 0 or new_j >= len(grid[i]):
            continue
        chars.append(grid[new_i][new_j])
    if "".join(sorted(chars)) == "mmss" and grid[i + 1][j + 1] != grid[i - 1][j - 1]:
        return True

    return False


def solve_p2(lines: list[str]) -> object:
    count = 0
    grid = [list(line) for line in lines]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if has_x_mas(grid, i, j):
                count += 1
    return count


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:21:04
# Part 2: 01:04:36
if __name__ == "__main__":
    process_file("sample.in")
    process_file("input.in")

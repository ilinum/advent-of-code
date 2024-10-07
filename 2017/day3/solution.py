def solve_p1(lines: list[str]) -> object:
    assert len(lines) == 1
    num = int(lines[0])
    containing_square = 1
    num_steps_from_mid = 0
    while pow(containing_square, 2) < num:
        containing_square += 2
        num_steps_from_mid += 1

    mid_to_center = containing_square // 2
    assert mid_to_center == num_steps_from_mid
    square_side = containing_square
    max_num = pow(containing_square, 2)
    mids = []
    for i in range(4):
        mids.append(max_num-(square_side//2)-(square_side-1)*i)
    distances_to_mid = [abs(mid-num) for mid in mids]
    shortest_to_mid = min(distances_to_mid)
    return shortest_to_mid + mid_to_center


def sum_around(grid: dict[tuple[int, int], int], x: tuple[int, int]) -> int:
    dirs = [
        (1, 1),
        (1, 0),
        (1, -1),
        (0, 1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
    ]
    result = 0
    for d in dirs:
        result += grid.get((x[0]+d[0], x[1]+d[1]), 0)
    return result

def solve_p2(lines: list[str]) -> object:
    assert len(lines) == 1
    num = int(lines[0])
    grid = {(0, 0): 1}
    last = 1
    location = (1, 0)
    dir_index = 0
    dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    while last <= num:
        last = sum_around(grid, location)
        grid[location] = last

        next_dir_index = (dir_index + 1) % len(dirs)
        next_dir = dirs[next_dir_index]
        next_dir_location = (location[0] + next_dir[0], location[1] + next_dir[1])
        if next_dir_location not in grid:
            dir_index = next_dir_index

        cur_dir = dirs[dir_index]
        location = (location[0]+cur_dir[0], location[1]+cur_dir[1])

    return last


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 01:23:25
# Part 2: 01:42:51
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

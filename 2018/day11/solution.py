import time


def get_cell_power(x: int, y: int, serial: int) -> int:
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power = power * rack_id
    power = (power % 1000) // 100
    power -= 5
    return power


def compute_cell_power(serial: int) -> dict[tuple[int, int, int], int]:
    result = {}
    for x in range(1, 301):
        for y in range(1, 301):
            result[(x, y, 1)] = get_cell_power(x, y, serial)
    return result


def compute_square_power(start_x: int, start_y: int, size: int, cells: dict[tuple[int, int, int], int]) -> int:
    if (start_x, start_y, size) in cells:
        return cells[(start_x, start_y, size)]
    result = compute_square_power(start_x, start_y, size - 1, cells)
    for y in range(start_y, start_y + size):
        result += cells[(start_x + size - 1, y, 1)]
    for x in range(start_x, start_x + size - 1):
        result += cells[(x, start_y + size - 1, 1)]
    cells[(start_x, start_y, size)] = result
    return result


def solve_p1(lines: list[str]) -> object:
    serial = int(lines[0])
    cells = compute_cell_power(serial)
    max_power = compute_square_power(1, 1, 3, cells)
    max_cell = (1, 1)
    for x in range(1, 300 - 2):
        for y in range(1, 300 - 2):
            power = compute_square_power(x, y, 3, cells)
            if power > max_power:
                max_power = power
                max_cell = (x, y)
    return max_cell


def print_cells(cells: dict[tuple[int, int], int]) -> None:
    for x in range(1, 301):
        line = []
        for y in range(1, 301):
            line.append(str(cells[(x, y)]))
        print(",".join(line))


def solve_p2(lines: list[str]) -> object:
    serial = int(lines[0])
    cells = compute_cell_power(serial)
    max_power = compute_square_power(1, 1, 1, cells)
    max_cell = (1, 1, 1)
    start = time.time()
    for size in range(1, 301):
        # This solution is slow, a better approach would be to use summed-area table:
        # https://en.wikipedia.org/wiki/Summed-area_table.
        if size % 50 == 0:
            print(
                f"processed {size} sizes in {time.time() - start}s, that is "
                f"{(size / (time.time() - start)) * 60:,.2f} per minute",
            )
        for x in range(1, 300 - size + 1):
            for y in range(1, 300 - size + 1):
                power = compute_square_power(x, y, size, cells)
                if power > max_power:
                    max_power = power
                    max_cell = (x, y, size)
    return max_cell


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:10:41
# Part 2: 00:47:31
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def new_tail(tail: Point, head: Point) -> Point:
    xd = head.x - tail.x
    yd = head.y - tail.y
    if abs(xd) <= 1 and abs(yd) <= 1:
        # No movement.
        return tail
    # This is very verbose but the code is simple and clear.
    if xd > 0:
        x_move = 1
    elif xd == 0:
        x_move = 0
    else:
        x_move = -1

    if yd > 0:
        y_move = 1
    elif yd == 0:
        y_move = 0
    else:
        y_move = -1
    return Point(tail.x + x_move, tail.y + y_move)


def num_tail_visited(lines: list[str], rope_len: int) -> int:
    rope = [Point(0, 0)] * rope_len
    tail_visited = {rope[-1]}
    for line in lines:
        direction, steps = line.split()
        for _ in range(int(steps)):
            head = rope[0]
            match direction:
                case "U":
                    head = Point(head.x, head.y + 1)
                case "D":
                    head = Point(head.x, head.y - 1)
                case "L":
                    head = Point(head.x - 1, head.y)
                case "R":
                    head = Point(head.x + 1, head.y)
                case _:
                    assert False, f"unknown direction {direction}"
            rope[0] = head
            for i in range(1, len(rope)):
                rope[i] = new_tail(rope[i], rope[i - 1])
            tail_visited.add(rope[-1])
    return len(tail_visited)


def solve(lines: list[str]) -> None:
    print(num_tail_visited(lines, rope_len=2))
    print(num_tail_visited(lines, rope_len=10))


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    solve(lines)


# Part 1: 00:20:42
# Part 2: 00:27:06
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

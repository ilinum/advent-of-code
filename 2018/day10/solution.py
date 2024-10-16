from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    initial_location: tuple[int, int]
    velocity: tuple[int, int]


def parse_points(lines: list[str]) -> dict[tuple[int, int], list[Point]]:
    result = {}
    for line in lines:
        pos_str, vel_str = line.replace(" ", "").split(">velocity=<")
        x, y = pos_str.removeprefix("position=<").split(",")
        vx, vy = vel_str.removesuffix(">").split(",")
        key = (int(x), int(y))
        result[key] = result.get(key, [])
        result[key].append(Point(initial_location=(int(x), int(y)), velocity=(int(vx), int(vy))))
    return result


def advance(points: dict[tuple[int, int], list[Point]]) -> dict[tuple[int, int], list[Point]]:
    result = {}
    for ((x, y), points_at_coord) in points.items():
        for point in points_at_coord:
            new_key = (x + point.velocity[0], y + point.velocity[1])
            result[new_key] = result.get(new_key, [])
            result[new_key].append(point)
    return result


def visualize(points: dict[tuple[int, int], list[Point]], seconds: int) -> None:
    min_x = min(x for (x, y) in points)
    max_x = max(x for (x, y) in points)
    min_y = min(y for (x, y) in points)
    max_y = max(y for (x, y) in points)
    max_size_to_visualize = 80
    if max_x - min_x > max_size_to_visualize or max_y - min_y > max_size_to_visualize:
        # No point visualizing, can't read it anyway.
        return
    print(f"sky at second {seconds}:")
    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            if (x, y) in points:
                line.append("#")
            else:
                line.append(".")
        print("".join(line))
    print("\n---\n")


def solve(lines: list[str]) -> object:
    points = parse_points(lines)
    for seconds in range(100000):
        visualize(points, seconds)
        points = advance(points)
    return None


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    solve(lines)


# Part 1: 00:32:03
# Part 2: 00:33:41
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

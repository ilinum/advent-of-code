import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def taxicab_distance(self, other: 'Coord') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass(frozen=True)
class Square:
    top_left: Coord
    side_length: int


@dataclass(frozen=True)
class Boundaries:
    y_to_x: dict[int: tuple[int, int]]


@dataclass(frozen=True)
class Sensor:
    loc: Coord
    beacon: Coord
    boundaries: Boundaries


def parse_sensor_loc(line: str) -> Coord:
    sens_x, sens_y = line.removeprefix("Sensor at ").replace(" ", "").split(",")
    assert sens_x.startswith("x=")
    assert sens_y.startswith("y=")
    return Coord(int(sens_x.removeprefix("x=")), int(sens_y.removeprefix("y=")))


def parse_beacon_loc(line: str) -> Coord:
    beac_x, beac_y = line.removeprefix(" closest beacon is at ").replace(" ", "").split(",")
    assert beac_x.startswith("x=")
    assert beac_y.startswith("y=")
    return Coord(int(beac_x.removeprefix("x=")), int(beac_y.removeprefix("y=")))


def parse_input(lines: list[str]) -> dict[Coord, Coord]:
    sens_to_beacon = {}
    for line in lines:
        sensor_line, beacon_line = line.split(":")
        sens_to_beacon[parse_sensor_loc(sensor_line)] = parse_beacon_loc(beacon_line)
    return sens_to_beacon


def compute_boundaries(sensor: Coord, distance: int) -> Boundaries:
    assert distance > 0
    y_to_x = {}
    for yd in range(-distance, distance + 1):
        left = distance - abs(yd)
        y = sensor.y + yd
        y_to_x[y] = (sensor.x - left, sensor.x + left)
    return Boundaries(y_to_x)


def solve_p2(lines: list[str], min_x: int, max_x: int, min_y: int, max_y: int) -> object:
    sens_to_beacon = parse_input(lines)
    sensors = [
        Sensor(sens, beacon, compute_boundaries(sens, sens.taxicab_distance(beacon)))
        for sens, beacon in sens_to_beacon.items()
    ]
    y = min_y
    while y <= max_y:
        x = min_x
        while x <= max_x:
            found_bound = False
            for s in sensors:
                if y in s.boundaries.y_to_x:
                    bounds = s.boundaries.y_to_x[y]
                    if bounds[0] <= x <= bounds[1]:
                        # Skip over to next bound.
                        found_bound = True
                        x = bounds[1]
            if not found_bound:
                coord = Coord(x, y)
                for s in sensors:
                    # A sanity check.
                    sensor_distance = s.loc.taxicab_distance(s.beacon)
                    distance_to_loc = s.loc.taxicab_distance(coord)
                    assert distance_to_loc > sensor_distance
                return coord.x * 4000000 + coord.y
            x += 1
        y += 1


def solve_p1(lines: list[str], row: int) -> object:
    sens_to_beacon = parse_input(lines)
    beacons = set(sens_to_beacon.values())
    no_beacon = set()
    for sensor, beacon in sens_to_beacon.items():
        print(f"processing sensor {sensor} beacon {beacon}")
        distance = sensor.taxicab_distance(beacon)
        for y in range(sensor.y - distance, sensor.y + distance + 1):
            yd = sensor.y - y
            if y != row:
                continue
            left = abs(abs(distance) - abs(yd))
            for x in range(sensor.x - left, sensor.x + left + 1):
                c = Coord(x, y)
                assert c.taxicab_distance(sensor) <= distance
                if c not in beacons:
                    no_beacon.add(c)
    return len(no_beacon)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    row = 2000000
    max_x, max_y = 4000000, 4000000
    if filename == "sample.in":
        row = 10
        max_x, max_y = 20, 20
    print(solve_p1(lines, row))
    print(solve_p2(lines, 0, max_x, 0, max_y))


def main() -> None:
    for f in os.listdir():
        if f.endswith("in"):
            process_file(f)


# Part 1: 00:34:30
# Part 2: 12:34:35
if __name__ == '__main__':
    main()

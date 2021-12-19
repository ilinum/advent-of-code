import sys
from dataclasses import dataclass
from typing import *


@dataclass(frozen=True)
class Target:
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def covers_point(self, point: "Point") -> bool:
        if point.x < self.min_x or point.x > self.max_x:
            return False
        if point.y < self.min_y or point.y > self.max_y:
            return False
        return True

    def reachable(self, point: "Point") -> bool:
        if point.x > self.max_x:
            return False
        if point.y < self.min_y:
            return False
        return True


@dataclass
class Velocity:
    x: int
    y: int


@dataclass
class Point:
    x: int
    y: int


def simulate(target: Target, velocity: Velocity) -> Optional[int]:
    location = Point(0, 0)
    max_height = 0
    while True:
        if target.covers_point(location):
            return max_height
        if not target.reachable(location):
            return None
        max_height = max(max_height, location.y)
        location.x += velocity.x
        location.y += velocity.y
        velocity.y -= 1
        if velocity.x < 0:
            velocity.x += 1
        elif velocity.x > 0:
            velocity.x -= 1


def main(lines: List[str]) -> None:
    assert len(lines) == 1
    line = lines[0].lstrip("target area: ")
    (x, y) = line.split(", ")
    (min_x, max_x) = x.lstrip("x=").split("..")
    (min_y, max_y) = y.lstrip("y=").split("..")
    target = Target(int(min_x), int(max_x), int(min_y), int(max_y))
    heights = []
    for x in range(0, 1000):
        for y in range(-1000, 1000):
            velocity = Velocity(x, y)
            cur_max = simulate(target, velocity)
            if cur_max is not None:
                heights.append(cur_max)
    print(max(heights))
    print(len(heights))


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

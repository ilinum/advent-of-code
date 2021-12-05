import sys
from collections import defaultdict
from typing import *


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @classmethod
    def parse_from_str(cls, s: str) -> 'Point':
        split = s.strip().split(",")
        assert len(split) == 2, split
        return cls(int(split[0]), int(split[1]))

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y


class Vector:
    def __init__(self, s: str) -> None:
        str_points = s.split("->")
        assert len(str_points) == 2
        self.start = Point.parse_from_str(str_points[0])
        self.end = Point.parse_from_str(str_points[1])

    def points_covered(self) -> List[Point]:
        if self.start.y < self.end.y:
            y_incr = 1
        elif self.start.y == self.end.y:
            y_incr = 0
        else:
            y_incr = -1
        if self.start.x < self.end.x:
            x_incr = 1
        elif self.start.x == self.end.x:
            x_incr = 0
        else:
            x_incr = -1

        result = []
        cur = Point(self.start.x, self.start.y)
        while cur != self.end:
            result.append(Point(cur.x, cur.y))
            cur.x += x_incr
            cur.y += y_incr
        result.append(Point(cur.x, cur.y))
        return result

    def __repr__(self) -> str:
        return f"{self.start} -> {self.end}"


def read_lines(filename: str) -> List[str]:
    with open(filename, "r") as f:
        return list(map(lambda x: x.strip(), f.readlines()))


def main(filename: str) -> None:
    lines = read_lines(filename)
    vectors = [Vector(line) for line in lines]
    vecs_covering_point: Dict[Point, int] = defaultdict(lambda: 0)
    for vec in vectors:
        for p in vec.points_covered():
            vecs_covering_point[p] += 1
    num_points_multi_covered = 0
    for v in vecs_covering_point.values():
        if v > 1:
            num_points_multi_covered += 1
    print(f"num points covered by multiple covered: {num_points_multi_covered}")


if __name__ == '__main__':
    main(sys.argv[1])

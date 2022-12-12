from collections import deque
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int


def letter_to_height(c: str) -> int:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    match c:
        case "S":
            return 0
        case "E":
            return len(alphabet) - 1
        case _:
            return alphabet.index(c)


class Node:
    def __init__(self, height: int, coord: Coordinates) -> None:
        self.height = height
        self.neighbors: set[Node] = set()
        self.coord = coord
        self.path: list[Node] | None = None

    def __repr__(self) -> str:
        return f"{self.coord}, height: {self.height}, distance: {len(self.path)}"


# I had a small bug with how I converted letters to heights, so I built this method to help me
# visualize.
def visualize(path: List[Node], num_rows: int, num_cols: int) -> None:
    loc_to_node = {}
    for n in path:
        assert n not in loc_to_node
        loc_to_node[n.coord] = n
    rows = []
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            node = loc_to_node.get(Coordinates(c, r), None)
            if node is None:
                row.append(".")
            elif node == path[-1]:
                row.append("E")
            else:
                idx = path.index(node)
                next_node = path[idx + 1]
                if next_node.coord.x == node.coord.x:
                    assert next_node.coord.y != node.coord.y
                    if next_node.coord.y > node.coord.y:
                        row.append("v")
                    else:
                        row.append("^")
                else:
                    assert next_node.coord.y == node.coord.y
                    if next_node.coord.x > node.coord.x:
                        row.append(">")
                    else:
                        row.append("<")
        rows.append("".join(row))
    print("\n".join(rows))


def find_shortest_paths(start: Node) -> None:
    to_visit = deque([start])
    start.path = []
    while len(to_visit) > 0:
        cur = to_visit.popleft()
        path = cur.path + [cur]
        for n in cur.neighbors:
            if n.path is None:
                to_visit.append(n)
                n.path = path
            else:
                # This must have been visited before already with a shorter or equal path.
                assert len(n.path) <= len(path)


def solve(lines: list[str]) -> None:
    coord_to_node = {}
    start = end = None
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            letter = lines[i][j]
            coord = Coordinates(j, i)
            node = Node(letter_to_height(letter), coord)
            if letter == "S":
                start = node
            if letter == "E":
                end = node
            coord_to_node[coord] = node
    assert start is not None
    assert end is not None

    for coord, node in coord_to_node.items():
        for xd, yd in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor_coord = Coordinates(coord.x + xd, coord.y + yd)
            if neighbor_coord in coord_to_node:
                neighbor = coord_to_node[neighbor_coord]
                if node.height + 1 >= neighbor.height:
                    node.neighbors.add(neighbor)

    # Now just find the shortest path!
    find_shortest_paths(start)
    assert start == end.path[0]
    # visualize(end.path + [end], len(lines), len(lines[0]))
    print(f"part one: {len(end.path)}")

    shortest_paths = []
    for node in coord_to_node.values():
        if node.height == 0:
            # Reset previous paths.
            for n in coord_to_node.values():
                n.path = None
            find_shortest_paths(node)
            if end.path is not None:
                shortest_paths.append(len(end.path))
    print(f"part two: {min(shortest_paths)}")


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    solve(lines)


# Part 1: 01:21:22
# Part 2: 01:27:28
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

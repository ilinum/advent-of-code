import dataclasses
import math
import time


class Directions:
    def __init__(self, directions: str) -> None:
        self.directions = directions
        self.index = 0
        assert len(directions) > 0

    def next(self) -> str:
        if self.index == len(self.directions):
            self.index = 0
        result = self.directions[self.index]
        self.index += 1
        return result


@dataclasses.dataclass
class Node:
    name: str
    left: str
    right: str

    def child(self, direction: str) -> str:
        if direction == "L":
            return self.left
        assert direction == "R", direction
        return self.right


def parse_graph(lines: list[str]) -> dict[str, Node]:
    nodes = {}
    for line in lines:
        line = line.replace(" ", "")
        (name, children) = line.split("=")
        (left, right) = children.removeprefix("(").removesuffix(")").split(",")
        assert name not in nodes
        nodes[name] = Node(name, left, right)
    return nodes


def traverse_graph(nodes: dict[str, Node], directions: Directions, start: str, end: str) -> int:
    steps = 0
    while start != end:
        steps += 1
        node = nodes[start]
        start = node.child(directions.next())
    return steps


def solve_p1(lines: list[str]) -> object:
    directions = Directions(lines[0])
    assert len(lines[1]) == 0
    nodes = parse_graph(lines[2:])
    return traverse_graph(nodes, directions, start="AAA", end="ZZZ")


def solve_p2(lines: list[str]) -> object:
    directions = Directions(lines[0])
    assert len(lines[1]) == 0
    nodes = parse_graph(lines[2:])
    steps = 0
    current = [n for n in nodes.keys() if n.endswith("A")]
    hits_at_steps = [[] for _ in range(len(current))]
    # Find the first time each path hits the target node.
    while not all(len(h) > 0 for h in hits_at_steps):
        next_dir = directions.next()
        for i, c in enumerate(current):
            node = nodes[c]
            child = node.child(next_dir)
            if c.endswith("Z"):
                hits_at_steps[i].append(steps)
            current[i] = child
        steps += 1
    # The input is such so that we keep looping, hitting the  same node over and over at
    # multiples of the step count the first time we hit it.
    # So, we just need to find the least common multiple of these!
    return math.lcm(*[h[0] for h in hits_at_steps])


def process_file(filename: str) -> None:
    start = time.time()
    print(f"processing '{file}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    # print(solve_p1(lines))
    print(solve_p2(lines))
    end = time.time()
    print(f"processed '{file}' in {end - start:.2f}s")


# Part 1: 00:13:31
# Part 2: 00:46:52
if __name__ == '__main__':
    for file in [
        "sample.in",
        "input.in",
    ]:
        process_file(file)

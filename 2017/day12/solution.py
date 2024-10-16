from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Node:
    neighbors: list[int]


def parse(lines: list[str]) -> dict[int, Node]:
    result = defaultdict(lambda: Node(neighbors=[]))
    for line in lines:
        (cur, neighbors) = line.replace(" ", "").split("<->")
        for n in neighbors.split(","):
            result[int(cur)].neighbors.append(int(n))
    return result

def find_connected(nodes: dict[int, Node], start: int) -> set[int]:
    seen = set()
    to_visit = {start}
    while len(to_visit) > 0:
        cur = to_visit.pop()
        if cur in seen:
            continue
        seen.add(cur)
        for n in nodes[cur].neighbors:
            to_visit.add(n)
    return seen

def solve_p1(lines: list[str]) -> object:
    nodes = parse(lines)
    return len(find_connected(nodes, 0))


def solve_p2(lines: list[str]) -> object:
    nodes = parse(lines)
    num_groups = 0
    while len(nodes) > 0:
        num_groups += 1
        start = set(nodes.keys()).pop()
        group = find_connected(nodes, start)
        for g in group:
            del nodes[g]
    return num_groups


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:05:25
# Part 2: 00:09:27
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

import sys
import time
from collections import deque
from dataclasses import dataclass
from typing import Optional, Deque


@dataclass
class Node:
    x: int
    y: int
    parent: Optional["Node"]


def in_bounds(x: int, y: int, lines: list[list[str]]) -> bool:
    if y >= len(lines) or y < 0:
        return False
    if x >= len(lines[y]) or x < 0:
        return False
    return True


def get_pipe_neighbors(grid: list[list[str]], cur: Node) -> list[Node]:
    sym = grid[cur.y][cur.x]
    if sym == "|":
        neighbors = [
            Node(cur.x, cur.y - 1, cur),
            Node(cur.x, cur.y + 1, cur),
        ]
    elif sym == "-":
        neighbors = [
            Node(cur.x - 1, cur.y, cur),
            Node(cur.x + 1, cur.y, cur),
        ]
    elif sym == "L":
        neighbors = [
            Node(cur.x, cur.y - 1, cur),
            Node(cur.x + 1, cur.y, cur),
        ]
    elif sym == "J":
        neighbors = [
            Node(cur.x, cur.y - 1, cur),
            Node(cur.x - 1, cur.y, cur),
        ]
    elif sym == "7":
        neighbors = [
            Node(cur.x - 1, cur.y, cur),
            Node(cur.x, cur.y + 1, cur),
        ]
    elif sym == "F":
        neighbors = [
            Node(cur.x + 1, cur.y, cur),
            Node(cur.x, cur.y + 1, cur),
        ]
    elif sym == ".":
        neighbors = []
    else:
        assert False, f"unknown symbol {sym}"

    neighbors = [n for n in neighbors if in_bounds(n.x, n.y, grid) and grid[n.y][n.x] != "."]
    return neighbors


def replace_start(n: Node, lines: list[list[str]]) -> str:
    left = in_bounds(n.x - 1, n.y, lines) and lines[n.y][n.x - 1] in ("-", "L", "F")
    right = in_bounds(n.x + 1, n.y, lines) and lines[n.y][n.x + 1] in ("-", "J", "7")
    top = in_bounds(n.x, n.y - 1, lines) and lines[n.y - 1][n.x] in ("|", "7", "F")
    bottom = in_bounds(n.x, n.y + 1, lines) and lines[n.y + 1][n.x] in ("|", "J", "L")
    if left and right:
        assert not top and not bottom
        return "-"
    if top and bottom:
        assert not left and not right
        return "|"
    if bottom and right:
        assert not top and not left
        return "F"
    if top and left:
        assert not bottom and not right
        return "J"
    if left and bottom:
        assert not top and not right
        return "7"
    if top and right:
        assert not bottom and not left
        return "L"
    assert False


def find_loop_distances(grid: list[list[str]]) -> list[list[int]]:
    distances = [[-1] * len(line) for line in grid]
    to_visit: deque[Node] = deque()
    start = None
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "S":
                start = Node(x, y, parent=None)
                grid[y][x] = replace_start(start, grid)
    assert start is not None
    to_visit.append(start)
    while len(to_visit) > 0:
        cur = to_visit.popleft()
        distance = 0
        if cur.parent is not None:
            distance = distances[cur.parent.y][cur.parent.x] + 1
            assert distance > 0
        old_distance = distances[cur.y][cur.x]
        should_process = old_distance == -1 or old_distance > distance
        if should_process:
            distances[cur.y][cur.x] = distance
            for n in get_pipe_neighbors(grid, cur):
                to_visit.append(n)
    return distances


def solve_p1(lines: list[str]) -> object:
    grid = [list(line) for line in lines]
    distances = find_loop_distances(grid)
    return max(max(d) for d in distances)


def solve_p2(lines: list[str]) -> object:
    return None


def process_file(filename: str) -> None:
    start = time.time()
    print(f"processing '{file}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))
    end = time.time()
    print(f"processed '{file}' in {end - start:.2f}s")


# Part 1: 00:42:00
# Part 2:
if __name__ == '__main__':
    for file in [
        "sample.in",
        "input.in",
    ]:
        process_file(file)

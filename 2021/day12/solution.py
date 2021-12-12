import sys
from typing import *


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.edges: Set[str] = set()

    def add_edge(self, node: str) -> None:
        self.edges.add(node)

    def can_visit_multiple_times(self) -> bool:
        return self.name.isupper()

    def __repr__(self) -> str:
        return self.name


def _is_large(node: str) -> bool:
    return node.isupper()


class Visited:
    def __init__(self, small_caves_to_revisit: int) -> None:
        self.small_caves_to_revisit = small_caves_to_revisit
        self.inner: Set[str] = set()
        self.revisited_small: List[str] = []

    def visit(self, node: str) -> None:
        if _is_large(node):
            return
        if node not in self.inner:
            self.inner.add(node)
            return
        assert self.small_caves_to_revisit > 0, self.small_caves_to_revisit
        self.small_caves_to_revisit -= 1
        self.revisited_small.append(node)

    def remove(self, node: str) -> None:
        if _is_large(node):
            return
        if len(self.revisited_small) > 0 and self.revisited_small[-1] == node:
            self.revisited_small.pop()
            self.small_caves_to_revisit += 1
            return
        self.inner.remove(node)

    def can_visit(self, node: str) -> bool:
        if _is_large(node):
            return True
        if node not in self.inner:
            return True
        if node in {"start", "end"}:
            return False
        return self.small_caves_to_revisit > 0


class Graph:
    def __init__(self, lines: List[str], small_caves_to_revisit: int) -> None:
        nodes = {}
        for line in lines:
            (src, dst) = line.split("-")
            if src not in nodes:
                nodes[src] = Node(src)
            if dst not in nodes:
                nodes[dst] = Node(dst)
            nodes[src].add_edge(dst)
            nodes[dst].add_edge(src)
        self.nodes = nodes
        self.visited = Visited(small_caves_to_revisit)

    def find_all_paths(self,
                       cur: str,
                       paths: List[Tuple],
                       cur_path: Tuple = (),
                       ) -> None:
        if cur == "end":
            paths.append(tuple(cur_path))
            return

        if not self.visited.can_visit(cur):
            return

        cur_path += (cur,)
        self.visited.visit(cur)
        for edge in self.nodes[cur].edges:
            self.find_all_paths(edge, paths, cur_path)
        self.visited.remove(cur)


def main(lines: List[str]) -> None:
    graph = Graph(lines, small_caves_to_revisit=0)
    paths = []
    graph.find_all_paths("start", paths=paths)
    print(len(paths))
    paths = []
    graph = Graph(lines, small_caves_to_revisit=1)
    graph.find_all_paths("start", paths=paths)
    print(len(paths))


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

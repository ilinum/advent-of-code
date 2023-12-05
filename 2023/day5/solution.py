import time
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Range:
    start: int
    size: int

    def end(self) -> int:
        return self.start + self.size

    def intersection(self, other: "Range") -> Optional["Range"]:
        # Non-overlapping ranges.
        if self.end() <= other.start or other.end() <= self.start:
            return None
        if self.start < other.start:
            return Range(other.start, min(self.end(), other.end()) - other.start)
        return Range(self.start, min(self.end(), other.end()) - self.start)

    def subtract(self, other: "Range") -> list["Range"]:
        if self.intersection(other) is None:
            return [self]
        result = []
        if self.start < other.start:
            result.append(Range(self.start, other.start - self.start))
        if other.end() < self.end():
            result.append(Range(other.end(), self.end() - other.end()))
        return result


@dataclass(frozen=True)
class TranslationRange:
    src_start: int
    dest_start: int
    size: int

    def src_range(self) -> Range:
        return Range(self.src_start, self.size)

    def dst_range(self) -> Range:
        return Range(self.dest_start, self.size)


@dataclass
class Edge:
    src_name: str
    dest_name: str
    ranges: list[TranslationRange]


class AlmanacGraph:
    def __init__(self, lines: list[str]) -> None:
        self.edges: dict[str, Edge] = {}
        line_groups: list[list[str]] = [[]]
        for line in lines:
            if len(line) > 0:
                line_groups[-1].append(line)
            else:
                line_groups.append([])
        for group in line_groups:
            assert len(group) > 1
            (source, dest) = group[0].removesuffix(" map:").split("-to-")
            self.edges[source] = Edge(src_name=source, dest_name=dest, ranges=[])
            for ranges in group[1:]:
                (dst_start, src_start, size) = ranges.split()
                self.edges[source].ranges.append(
                    TranslationRange(
                        src_start=int(src_start),
                        dest_start=int(dst_start),
                        size=int(size),
                    ),
                )


def parse_seeds(line: str) -> list[int]:
    (_, seeds_str) = line.split(":")
    return [int(s) for s in seeds_str.strip().split()]


def parse_seed_ranges(line: str) -> list[Range]:
    (_, seeds_str) = line.split(":")
    seeds_ints = [int(s) for s in seeds_str.strip().split()]
    assert len(seeds_ints) % 2 == 0, seeds_ints
    result = []
    for i in range(0, len(seeds_ints), 2):
        result.append(Range(start=seeds_ints[i], size=seeds_ints[i + 1]))
    return result


def walk_graph(graph: AlmanacGraph, value: int, start: str, end: str) -> int:
    if start == end:
        return value
    edge = graph.edges[start]
    for r in edge.ranges:
        if r.src_start <= value < r.src_start + r.size:
            # In range!
            return walk_graph(graph, r.dest_start + value - r.src_start, edge.dest_name, end)
    return walk_graph(graph, value, edge.dest_name, end)


def find_min_end(graph: AlmanacGraph, r: Range, start: str, end: str) -> int:
    if start == end:
        return r.start
    edge = graph.edges[start]
    for tr in edge.ranges:
        intersection = tr.src_range().intersection(r)
        if intersection is not None:
            r1 = Range(tr.dest_start + intersection.start - tr.src_start, size=intersection.size)
            remainder = r.subtract(tr.src_range())
            values = [find_min_end(graph, r1, edge.dest_name, end)]
            for r in remainder:
                values.append(find_min_end(graph, r, start, end))
            return min(values)
    return find_min_end(graph, r, edge.dest_name, end)


def solve_p1(lines: list[str], end: str) -> object:
    seeds = parse_seeds(lines[0])
    graph = AlmanacGraph(lines[2:])
    end_values = []
    for seed in seeds:
        end_values.append(walk_graph(graph, seed, "seed", end))
    return min(end_values)


def solve_p2(lines: list[str], end: str) -> object:
    seeds = parse_seed_ranges(lines[0])
    graph = AlmanacGraph(lines[2:])
    min_values = []
    for s in seeds:
        min_values.append(find_min_end(graph, s, "seed", end))
    return min(min_values)


def process_file(filename: str) -> None:
    start = time.time()
    print(f"processing '{file}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines, end="location"))
    print(solve_p2(lines, end="location"))
    end = time.time()
    print(f"processed '{file}' in {end - start:.2f}s")


# Part 1: 00:30:00
# Part 2: 01:12:00
if __name__ == '__main__':
    for file in [
        "sample.in",
        "input.in",
    ]:
        process_file(file)

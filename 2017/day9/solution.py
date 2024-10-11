from dataclasses import dataclass


@dataclass
class Node:
    depth: int
    garbage_score: int
    size: int
    children: list["Node"]


def parse_group(line: str, depth: int = 1) -> Node:
    assert line[0] == "{"
    i = 1
    children = []
    garbage_score = 0
    while line[i] != "}":
        if line[i] == "!":
            i += 2
        elif line[i] == "<":
            i += 1
            while line[i] != ">":
                if line[i] == "!":
                    i += 1
                else:
                    garbage_score += 1
                i += 1
        elif line[i] == "{":
            child = parse_group(line[i:], depth=depth + 1)
            i += child.size
            children.append(child)
        else:
            i += 1

    return Node(depth=depth, size=i + 1, garbage_score=garbage_score, children=children)


def add_up_depths(node: Node) -> int:
    depths = [add_up_depths(c) for c in node.children]
    return sum(depths) + node.depth


def add_up_garbage_score(node: Node) -> int:
    depths = [add_up_garbage_score(c) for c in node.children]
    return sum(depths) + node.garbage_score


def solve_p1(lines: list[str]) -> object:
    scores = []
    for line in lines:
        root = parse_group(line)
        assert root.size == len(line)
        scores.append(add_up_depths(root))
    return sum(scores)


def solve_p2(lines: list[str]) -> object:
    scores = []
    for line in lines:
        root = parse_group(line)
        assert root.size == len(line)
        scores.append(add_up_garbage_score(root))
    return sum(scores)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:14:24
# Part 2: 00:17:37
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

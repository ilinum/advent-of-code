from dataclasses import dataclass


@dataclass
class Node:
    metadatas: list[int]
    children: list["Node"]


def parse_node(line: list[int]) -> tuple[Node, list[int]]:
    num_children = line[0]
    num_metadatas = line[1]
    line = line[2:]
    children = []
    for _ in range(num_children):
        child, line = parse_node(line)
        children.append(child)
    metadatas = line[:num_metadatas]
    return Node(metadatas, children), line[num_metadatas:]


def get_all_metadatas(node: Node) -> list[int]:
    result = []
    for child in node.children:
        result.extend(get_all_metadatas(child))
    result.extend(node.metadatas)
    return result

def solve_p1(lines: list[str]) -> object:
    line = [int(c) for c in lines[0].split()]
    assert len(lines) == 1
    (root, _) = parse_node(line)
    return sum(get_all_metadatas(root))


def get_value(node: Node) -> int:
    if len(node.children) == 0:
        return sum(node.metadatas)
    result = 0
    for i in node.metadatas:
        if 0 <= (i-1) < len(node.children):
            result += get_value(node.children[i-1])
    return result

def solve_p2(lines: list[str]) -> object:
    line = [int(c) for c in lines[0].split()]
    assert len(lines) == 1
    (root, _) = parse_node(line)
    return get_value(root)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:11:52
# Part 2: 00:14:38
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

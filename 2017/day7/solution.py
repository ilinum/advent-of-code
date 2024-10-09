from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    name: str
    weight: int
    children: list[str]
    cumulative_weight: Optional[int]
    depth: int

    @staticmethod
    def parse_node(line: str) -> "Node":
        (name, remainder) = line.split(" (")
        children = []
        weight_str = remainder
        if "->" in remainder:
            (weight_str, children_str) = remainder.split(" -> ")
            children = children_str.split(", ")
        weight = int(weight_str.removesuffix(")"))
        return Node(name, weight, children, cumulative_weight=None, depth=0)


def compute_depths(nodes: dict[str, Node], node: Node) -> None:
    for child in node.children:
        nodes[child].depth = node.depth + 1
        compute_depths(nodes, nodes[child])


def compute_cumulative_weights(nodes: dict[str, Node], name: str) -> None:
    node = nodes[name]
    weight = node.weight
    for child in node.children:
        compute_cumulative_weights(nodes, child)
        weight += nodes[child].cumulative_weight
    node.cumulative_weight = weight


def parse_graph(lines: list[str]) -> tuple[dict[str, Node], Node]:
    nodes = {}
    for line in lines:
        node = Node.parse_node(line)
        nodes[node.name] = node
    child_to_parent = {}
    for name, node in nodes.items():
        for child in node.children:
            assert child not in child_to_parent
            child_to_parent[child] = node
    root = None
    for node in nodes.values():
        if node.name not in child_to_parent:
            root = node
            break
    root.depth = 0
    compute_depths(nodes, root)
    return nodes, root


def solve_p1(lines: list[str]) -> object:
    _, root = parse_graph(lines)
    return root.name


def find_deepest_unbalanced_node(nodes: dict[str, Node]) -> Node:
    unbalanced_nodes = []
    for node in nodes.values():
        if len(node.children) < 3:
            continue
        children_weights = [nodes[child].cumulative_weight for child in node.children]
        if len(set(children_weights)) > 1:
            assert len(set(children_weights)) == 2
            unbalanced_nodes.append(node)

    deepest_unbalanced = max(unbalanced_nodes, key=lambda node: node.depth)
    return deepest_unbalanced


def solve_p2(lines: list[str]) -> object:
    nodes, root = parse_graph(lines)

    compute_cumulative_weights(nodes, root.name)
    # Only look at deepest unbalanced, since that can break the lower levels.
    unbalanced = find_deepest_unbalanced_node(nodes)
    freqs = {}
    children_weights = [nodes[child].cumulative_weight for child in unbalanced.children]
    for w in children_weights:
        freqs[w] = freqs.get(w, 0) + 1
    common_weight = max(freqs.items(), key=lambda x: x[1])[0]
    node_to_fix = None
    for name in unbalanced.children:
        child = nodes[name]
        if child.cumulative_weight != common_weight:
            node_to_fix = child
            break
    return common_weight - (node_to_fix.cumulative_weight - node_to_fix.weight)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:09:45
# Part 2: 00:40:15
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

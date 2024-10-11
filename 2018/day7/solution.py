from collections import defaultdict


def parse_input(lines: list[str]) -> dict[str, list[str]]:
    result = defaultdict(lambda: [])
    for line in lines:
        line = line.removeprefix("step ").removesuffix(" can begin.")
        (node, edge) = line.split(" must be finished before step ")
        result[node].append(edge)
    return result


def compute_prereqs(nodes: dict[str, list[str]]) -> dict[str, set[str]]:
    result = defaultdict(lambda: set())
    for node, dests in nodes.items():

        for dest in dests:
            result[dest].add(node)
    return result


def find_root_nodes(nodes: dict[str, list[str]], prereqs: dict[str, set[str]]) -> set[str]:
    result = set()
    for node in nodes:
        if len(prereqs[node]) == 0:
            result.add(node)
    return result


def time_to_work(node: str) -> int:
    alphabet = "abcdefghijklmonpqrstuvwxyz"
    return alphabet.index(node) + 1


def solve_p1(lines: list[str]) -> object:
    nodes = parse_input(lines)
    order = []
    prereqs = compute_prereqs(nodes)
    available = find_root_nodes(nodes, prereqs)
    while len(available) > 0:
        cur = min(available)
        available.remove(cur)
        order.append(cur)
        for dst in nodes[cur]:
            prereqs[dst].remove(cur)
            if len(prereqs[dst]) == 0:
                available.add(dst)
    return "".join(order)


def solve_p2(lines: list[str]) -> object:
    num_workers = 5
    wait = 60
    nodes = parse_input(lines)
    prereqs = compute_prereqs(nodes)
    available = find_root_nodes(nodes, prereqs)
    in_progress = defaultdict(lambda: [])
    elapsed = 0
    while len(available) > 0 or len(in_progress) > 0:
        if len(in_progress) < num_workers and len(available) > 0:
            # Assign work!
            cur = min(available)
            available.remove(cur)
            in_progress[elapsed + time_to_work(cur) + wait].append(cur)
        elif elapsed in in_progress:
            finished = in_progress.pop(elapsed)
            for node in finished:
                for dst in nodes[node]:
                    prereqs[dst].remove(node)
                    if len(prereqs[dst]) == 0:
                        available.add(dst)
        else:
            # All workers are busy. Fast forward to next event time.
            elapsed = min(in_progress.keys())


    return elapsed

def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:16:51
# Part 2: 00:35:23
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

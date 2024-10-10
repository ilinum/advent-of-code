from typing import Optional


def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def closest_targets(loc: tuple[int, int], targets: set[tuple[int, int]]) -> Optional[tuple[int, int]]:
    distances = [(distance(loc, c), c) for c in targets]
    distances.sort()
    if distances[0][0] == distances[1][0]:
        return None
    return distances[0][1]

def find_infinite_areas(targets: set[tuple[int, int]]) -> set[tuple[int, int]]:
    result = set()
    all_x = [t[0] for t in targets]
    all_y = [t[1] for t in targets]
    # Every target closest to border is infinite.
    for x in [min(all_x)-1, max(all_x)+1]:
        for y in range(min(all_y)-1, max(all_y) + 2):
            closest = closest_targets((x, y), targets)
            if closest is not None:
                result.add(closest)
    for y in [min(all_y)-1, max(all_y)+1]:
        for x in range(min(all_x)-1, max(all_x)+2):
            closest = closest_targets((x, y), targets)
            if closest is not None:
                result.add(closest)
    return result

def solve_p1(lines: list[str]) -> object:
    targets = {}
    for line in lines:
        (x, y) = line.split(", ")
        targets[int(x), int(y)] = 0
    all_x = [t[0] for t in targets.keys()]
    all_y = [t[1] for t in targets.keys()]
    for x in range(min(all_x), max(all_x) + 1):
        for y in range(min(all_y), max(all_y) + 1):
            closest = closest_targets((x, y), set(targets.keys()))
            if closest is not None:
                targets[closest] += 1
    for r in find_infinite_areas(set(targets.keys())):
        del targets[r]
    return max(targets.values())


def solve_p2(lines: list[str]) -> object:
    targets = {}
    for line in lines:
        (x, y) = line.split(", ")
        targets[int(x), int(y)] = 0
    all_x = [t[0] for t in targets.keys()]
    all_y = [t[1] for t in targets.keys()]
    distances = {}
    for x in range(min(all_x), max(all_x) + 1):
        for y in range(min(all_y), max(all_y) + 1):
            c = (x, y)
            distances[c] = 0
            for target in targets:
                distances[c] += distance(c, target)

    fit_criteria = [c for (c, d) in distances.items() if d < 10000]
    return len(fit_criteria)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:25:09
# Part 2: 00:30:09
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

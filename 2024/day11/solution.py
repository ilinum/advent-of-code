import time


def process_stone(s: int) -> list[int]:
    if s == 0:
        return [1]
    stone_str = str(s)
    if len(stone_str) % 2 == 0:
        mid = len(stone_str) // 2
        return [int(stone_str[:mid]), int(stone_str[mid:])]
    return [s * 2024]


def iteration(stones: list[int]) -> list[int]:
    result = []
    for s in stones:
        result.extend(process_stone(s))
    return result


def solve_p1(lines: list[str]) -> object:
    assert len(lines) == 1
    stones = [int(c) for c in lines[0].split()]
    num_iterations = 25
    for i in range(num_iterations):
        stones = iteration(stones)
    return len(stones)


def num_children_at_depth(
    cur: int, depth: int, cache: dict[tuple[int, int], int]
) -> int:
    if depth == 0:
        return 1
    if (cur, depth) in cache:
        return cache[(cur, depth)]
    children = process_stone(cur)
    result = sum(num_children_at_depth(child, depth - 1, cache) for child in children)
    cache[(cur, depth)] = result
    return result


def solve_p2(lines: list[str]) -> object:
    assert len(lines) == 1
    stones = [int(c) for c in lines[0].split()]
    num_iterations = 75
    cache = {}
    return sum(num_children_at_depth(s, num_iterations, cache) for s in stones)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    start = time.time()
    print(solve_p1(lines))
    print(solve_p2(lines))
    print(f"processed file '{filename}' in {time.time() - start:.2f}s")


# Part 1: 00:07:20
# Part 2: 00:26:04
if __name__ == "__main__":
    process_file("sample.in")
    process_file("input.in")

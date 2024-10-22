def run_generation(plants: set[int], rules: dict[tuple[...], str]) -> set[int]:
    result = set()
    for p in range(min(plants) - 5, max(plants) + 6):
        r = (p - 2 in plants, p - 1 in plants, p in plants, p + 1 in plants, p + 2 in plants)
        if r in rules and rules[r]:
            result.add(p)
    return result


def print_plants(plants: set[int]) -> None:
    p = []
    for i in range(-3, 101):
        p.append("#" if i in plants else ".")
    print("".join(p))


def solve(lines: list[str], num_generations: int) -> object:
    initial_state_str = lines[0].split(": ")[1].strip()
    plants = set()
    for i in range(len(initial_state_str)):
        assert initial_state_str[i] in ("#", ".")
        if initial_state_str[i] == "#":
            plants.add(i)

    rules = {}
    for line in lines[1:]:
        if len(line) == 0:
            continue
        condition_str, result = line.split(" => ")
        condition = []
        for c in condition_str:
            condition.append(c == "#")
        rules[tuple(condition)] = result == "#"

    for gen in range(num_generations):
        plants = run_generation(plants, rules)
        if (gen + 1) % 5000 == 0:
            print(f"gen: {gen + 1}, plants: {sum(plants)}")
    return sum(plants)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve(lines, num_generations=20))
    print(solve(lines, num_generations=100000))


# Part 1: 00:35:28
# Part 2: 00:46:38
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

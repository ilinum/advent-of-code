class Game:
    def __init__(self, line: str) -> None:
        splits = line.split(":")
        assert len(splits) == 2
        self.rounds: list[dict[str, int]] = []
        self.id = int(splits[0].split()[1])
        for r in splits[1].split(";"):
            counts_by_color = get_counts_by_color(r)
            self.rounds.append(counts_by_color)


def get_counts_by_color(round_str: str) -> dict[str, int]:
    result = {}
    for cube in round_str.split(","):
        cube_splits = cube.strip().split()
        assert len(cube_splits) == 2, cube
        result[cube_splits[1].strip()] = int(cube_splits[0])
    return result


def solve_p1(games: list[Game], max_by_color: dict[str, int]) -> object:
    values = []
    for game in games:
        valid = True
        for counts_by_color in game.rounds:
            for color, max_color in max_by_color.items():
                if counts_by_color.get(color, 0) > max_color:
                    valid = False
                    break
        if valid:
            values.append(game.id)
    return sum(values)


def solve_p2(games: list[Game]) -> object:
    values = []
    for game in games:
        max_counts = {}
        for counts_by_color in game.rounds:
            for color, count in counts_by_color.items():
                if max_counts.get(color, 0) < count:
                    max_counts[color] = count
        power = 1
        for count in max_counts.values():
            power *= count
        values.append(power)
    return sum(values)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    games = [Game(line) for line in lines]
    print(solve_p1(games, max_by_color={"red": 12, "green": 13, "blue": 14}))
    print(solve_p2(games))


# Part 1: 00:05:20
# Part 2: 00:17:26
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

import time


class Card:
    def __init__(self, line: str) -> None:
        (winning_str, actual_str) = line.split(":")[1].split("|")
        self.winning = set()
        for w in winning_str.strip().split():
            self.winning.add(int(w))
        self.actual = set()
        for a in actual_str.strip().split():
            self.actual.add(int(a))

    def num_matches(self) -> int:
        return len(self.actual.intersection(self.winning))


def solve_p1(lines: list[str]) -> object:
    card_values = []
    for line in lines:
        matching = Card(line).num_matches()
        if matching > 0:
            card_values.append(pow(2, matching - 1))

    return sum(card_values)


def solve_p2(lines: list[str]) -> object:
    copies_per_card = {
        num: 1 for num in range(len(lines))
    }
    for num in range(len(lines)):
        line = lines[num]
        matching = Card(line).num_matches()
        for w in range(num + 1, num + 1 + matching):
            if w in copies_per_card:
                copies_per_card[w] += copies_per_card[num]

    return sum(copies_per_card.values())


def process_file(filename: str) -> None:
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:07:04
# Part 2: 00:13:25
if __name__ == '__main__':
    for file in ("sample.in", "input.in"):
        start = time.time()
        print(f"processing '{file}'")
        process_file(file)
        end = time.time()
        print(f"processed '{file}' in {end - start:.2f}s")

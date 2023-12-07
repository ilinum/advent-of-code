import functools
import time

CARDS_TO_STRENGTH = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
    "J": 0,
}

HIGH_CARD_MULTIPLIER = 1
ONE_PAIR_MULTIPLIER = HIGH_CARD_MULTIPLIER * 100
TWO_PAIR_MULTIPLIER = ONE_PAIR_MULTIPLIER * 100
THREE_OF_A_KIND_MULTIPLIER = TWO_PAIR_MULTIPLIER * 100
FULL_HOUSE_MULTIPLIER = THREE_OF_A_KIND_MULTIPLIER * 100
FOUR_OF_A_KIND_MULTIPLIER = FULL_HOUSE_MULTIPLIER * 100
FIVE_OF_A_KIND_MULTIPLIER = FOUR_OF_A_KIND_MULTIPLIER * 100


@functools.total_ordering
class Hand:

    def __init__(self, cards: str) -> None:
        self.cards = cards
        assert len(self.cards) == 5
        self.freqs = {}
        for c in self.cards:
            self.freqs[c] = self.freqs.get(c, 0) + 1
        self.strength = self._strength()

    def _strength(self) -> int:
        num_jokers = self.cards.count("J")
        if num_jokers > 0:
            del self.freqs["J"]
            if num_jokers == 5:
                assert len(self.freqs) == 0
                self.freqs["A"] = num_jokers
                num_jokers = 0
        sorted_freqs = list(reversed(sorted(self.freqs.values())))
        sorted_freqs[0] += num_jokers
        if sorted_freqs[0] == 5:
            assert len(self.freqs) == 1
            return 1 * FIVE_OF_A_KIND_MULTIPLIER
        if sorted_freqs[0] == 4:
            assert len(self.freqs) == 2
            return 1 * FOUR_OF_A_KIND_MULTIPLIER
        if sorted_freqs[0] == 3 and sorted_freqs[1] == 2:
            assert len(self.freqs) == 2
            return 1 * FULL_HOUSE_MULTIPLIER
        if sorted_freqs[0] == 3:
            assert len(self.freqs) == 3
            return 1 * THREE_OF_A_KIND_MULTIPLIER
        if sorted_freqs[0] == 2 and sorted_freqs[1] == 2:
            assert len(self.freqs) == 3
            return 1 * TWO_PAIR_MULTIPLIER
        if sorted_freqs[0] == 2:
            assert len(self.freqs) == 4
            return 1 * ONE_PAIR_MULTIPLIER
        assert len(self.freqs) == 5
        return HIGH_CARD_MULTIPLIER

    def compare(self, other: "Hand") -> int:
        cmp = self.strength - other.strength
        if cmp != 0:
            return cmp
        for (s, o) in zip(self.cards, other.cards):
            cmp = CARDS_TO_STRENGTH[s] - CARDS_TO_STRENGTH[o]
            if cmp != 0:
                return cmp
        return 0

    def __gt__(self, other: "Hand") -> bool:
        return self.compare(other) > 0

    def __eq__(self, other: "Hand") -> bool:
        return self.cards == other.cards

    def __repr__(self) -> str:
        return self.cards


def solve(lines: list[str]) -> object:
    hands = []
    hand_to_bid = {}
    for line in lines:
        hand, bid = line.split()
        assert hand not in hand_to_bid, f"duplicate hand {hand}"
        hand_to_bid[hand] = int(bid)
        hands.append(Hand(hand))
    hands.sort()
    winnings = []
    for rank, hand in enumerate(hands, start=1):
        winnings.append(rank * hand_to_bid[hand.cards])
    return sum(winnings)


def process_file(filename: str) -> None:
    start = time.time()
    print(f"processing '{file}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    print(solve(lines))
    end = time.time()
    print(f"processed '{file}' in {end - start:.2f}s")


# Part 1: 00:51:30
# Part 2: 01:01:57
if __name__ == '__main__':
    for file in [
        "sample.in",
        "input.in",
    ]:
        process_file(file)

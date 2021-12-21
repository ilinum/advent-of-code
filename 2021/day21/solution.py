import sys
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from typing import *


class DeterministicDice:
    def __init__(self, max_roll: int):
        self._last = 0
        self.rolls = 0
        self.max = max_roll

    def roll(self) -> int:
        self.rolls += 1
        self._last += 1
        if self._last > self.max:
            self._last = 1
        return self._last


@dataclass(frozen=True)
class Player:
    current: int
    score: int

    def roll(self, roll: int) -> "Player":
        cur = self.current + roll % 10
        if cur > 10:
            cur -= 10
        return Player(cur, self.score + cur)


def part1(p1: Player, p2: Player) -> None:
    d = DeterministicDice(max_roll=1000)
    while True:
        rolls = sum([d.roll() for _ in range(3)])
        p1 = p1.roll(rolls)
        if p1.score >= 1000:
            break
        rolls = sum([d.roll() for _ in range(3)])
        p2 = p2.roll(rolls)
        if p2.score >= 1000:
            break
    print(min(p1.score, p2.score) * d.rolls)


@cache
def all_possible_rolls(num_rolls: int, max_roll: int) -> List[List[int]]:
    if num_rolls == 1:
        return [[r] for r in range(1, max_roll + 1)]
    all_prev_rolls = all_possible_rolls(num_rolls - 1, max_roll)
    result = []
    for roll in range(1, max_roll + 1):
        for prev_rolls in all_prev_rolls:
            result.append(prev_rolls + [roll])
    return result


@cache
def process_incomplete_universe(
        og_p1: Player,
        og_p2: Player,
) -> Tuple[Dict[int, int], Dict[Tuple[Player, Player], int]]:
    possible_rolls = all_possible_rolls(num_rolls=3, max_roll=3)
    wins_by_player = {1: 0, 2: 0}
    non_winning_p1 = []
    for roll1 in possible_rolls:
        p1 = og_p1.roll(sum(roll1))
        if p1.score >= 21:
            wins_by_player[1] += 1
        else:
            non_winning_p1.append(p1)
    universes = defaultdict(lambda: 0)
    for p1 in non_winning_p1:
        for roll2 in possible_rolls:
            p2 = og_p2.roll(sum(roll2))
            if p2.score >= 21:
                wins_by_player[2] += 1
            else:
                universes[(p1, p2)] += 1

    return wins_by_player, universes


def part2(p1: Player, p2: Player) -> None:
    wins_by_player = {1: 0, 2: 0}
    incomplete_universes = dict()
    incomplete_universes[(p1, p2)] = 1
    while len(incomplete_universes) > 0:
        (og_p1, og_p2), original_count = incomplete_universes.popitem()
        wins_this_universe, new_universes = process_incomplete_universe(og_p1, og_p2)
        for p, c in wins_this_universe.items():
            wins_by_player[p] += c * original_count
        for (p1, p2), count in new_universes.items():
            if (p1, p2) in incomplete_universes:
                incomplete_universes[(p1, p2)] += original_count * count
            else:
                incomplete_universes[(p1, p2)] = original_count * count

    print(max(wins_by_player.values()))


def create_players(lines: List[str]) -> Tuple[Player, Player]:
    assert len(lines) == 2
    p1_start = int(lines[0].lstrip("Player 1 starting position: "))
    p2_start = int(lines[1].lstrip("Player 2 starting position: "))
    p1 = Player(p1_start, score=0)
    p2 = Player(p2_start, score=0)
    return p1, p2


def main(lines: List[str]) -> None:
    p1, p2 = create_players(lines)
    part1(p1, p2)
    part2(p1, p2)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

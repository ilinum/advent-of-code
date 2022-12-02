from typing import NewType

Shape = NewType("Shape", int)
ROCK = Shape(1)
PAPER = Shape(2)
SCISSORS = Shape(3)

Outcome = NewType("Outcome", int)
LOSS = Outcome(0)
DRAW = Outcome(3)
WIN = Outcome(6)


def shape_to_play(desired_outcome: Outcome, opponent: Shape) -> Shape:
    to_play = {
        WIN: {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK},
        DRAW: {ROCK: ROCK, PAPER: PAPER, SCISSORS: SCISSORS},
        LOSS: {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER},
    }
    return to_play[desired_outcome][opponent]


def game_outcome(you: Shape, opponent: Shape) -> Outcome:
    outcome = {
        ROCK: {ROCK: DRAW, PAPER: LOSS, SCISSORS: WIN},
        PAPER: {ROCK: WIN, PAPER: DRAW, SCISSORS: LOSS},
        SCISSORS: {ROCK: LOSS, PAPER: WIN, SCISSORS: DRAW},
    }
    return outcome[you][opponent]


def solve_p1(lines: list[str]) -> None:
    score = 0
    for line in lines:
        a, b = line.split()
        opponent = {"A": ROCK, "B": PAPER, "C": SCISSORS}[a]
        you = {"X": ROCK, "Y": PAPER, "Z": SCISSORS}[b]
        score += game_outcome(you, opponent) + you
    print(score)


def solve_p2(lines: list[str]) -> None:
    score = 0
    for line in lines:
        a, b = line.split()
        opponent = {"A": ROCK, "B": PAPER, "C": SCISSORS}[a]
        outcome = {"X": LOSS, "Y": DRAW, "Z": WIN}[b]
        score += outcome
        score += shape_to_play(outcome, opponent)
    print(score)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    solve_p1(lines)
    solve_p2(lines)


# Part 1: 00:07:19
# Part 2: 00:13:03
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

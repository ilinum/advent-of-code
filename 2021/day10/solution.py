import sys
from collections import deque
from typing import *

SCORES_PER_INVALID_CHAR = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

SCORES_PER_INCOMPLETE_CHAR = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

OPEN_TO_CLOSE = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

CLOSE_TO_OPEN = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}


def score_corrupted_line(line: str) -> int:
    stack = deque()
    for c in line:
        if c in OPEN_TO_CLOSE:
            stack.append(c)
        else:
            assert c in CLOSE_TO_OPEN, c
            open = stack.pop()
            if CLOSE_TO_OPEN[c] != open:
                return SCORES_PER_INVALID_CHAR[c]

    return 0


def find_incomplete_symbols(line: str) -> str:
    stack = deque()
    for c in line:
        if c in OPEN_TO_CLOSE:
            stack.append(c)
        else:
            assert c in CLOSE_TO_OPEN, c
            open = stack.pop()
            assert CLOSE_TO_OPEN[c] == open

    result = ""
    while len(stack) > 0:
        result += OPEN_TO_CLOSE[stack.pop()]
    return result


def score_incomplete_line(line: str) -> int:
    symbols = find_incomplete_symbols(line)
    score = 0
    for c in symbols:
        score = score * 5 + SCORES_PER_INCOMPLETE_CHAR[c]
    return score


def main(lines: List[str]) -> None:
    corrupted_score = 0
    non_corrupted_lines = []
    for line in lines:
        score = score_corrupted_line(line)
        if score == 0:
            non_corrupted_lines.append(line)
        corrupted_score += score
    print(corrupted_score)

    incomplete_scores = []
    for line in non_corrupted_lines:
        incomplete_scores.append(score_incomplete_line(line))
    incomplete_scores.sort()
    print(incomplete_scores[len(incomplete_scores) // 2])


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

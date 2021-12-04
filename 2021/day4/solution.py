import sys
from typing import *


class Cell:
    def __init__(self, num: int) -> None:
        self.num = num
        self.marked = False

    def __repr__(self) -> str:
        return f"({self.num}, {self.marked})"


class Board:
    def __init__(self, board_input: List[str]) -> None:
        assert len(board_input) == 5
        self.state: List[List[Cell]] = []
        for i, line in enumerate(board_input):
            row_nums = line.split()
            assert len(row_nums) == 5
            row = []
            for j, num in enumerate(row_nums):
                row.append(Cell(int(num)))
            self.state.append(row)

    def mark(self, to_mark: int) -> None:
        for row in self.state:
            for cell in row:
                if cell.num == to_mark:
                    assert not cell.marked
                    cell.marked = True

    def _all_marked(self, cells: List[Cell]) -> bool:
        return all(cell.marked for cell in cells)

    def is_done(self) -> bool:
        # Check rows.
        for row in self.state:
            if self._all_marked(row):
                return True
        # Check columns.
        for col in range(5):
            cells = []
            for row in self.state:
                cells.append(row[col])
            if self._all_marked(cells):
                return True
        return False

    def sum_unmarked(self) -> int:
        result = 0
        for row in self.state:
            for cell in row:
                if not cell.marked:
                    result += cell.num
        return result

    def __repr__(self) -> str:
        return "\n".join(str(row) for row in self.state)


def main(filename: str) -> None:
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
        # First line is numbers, then empty line, then one 5x5 board.
        assert len(lines) > 7, lines
        numbers = [int(n) for n in lines[0].split(",")]
        i = 1
        board_inputs = []
        while i < len(lines):
            if len(lines[i]) == 0:
                i += 1
                continue
            board_inputs.append(lines[i:i + 5])
            i += 5

        print(f"winning board score is {find_winning_board(numbers, create_boards(board_inputs))}")
        print(f"worst board score is {find_worst_board(numbers, create_boards(board_inputs))}")


def create_boards(inputs: List[List[str]]) -> Set[Board]:
    result = set()
    for board_in in inputs:
        result.add(Board(board_in))
    return result


def find_winning_board(numbers: List[int], boards: Set[Board]) -> int:
    for num in numbers:
        for board in boards:
            board.mark(num)
            if board.is_done():
                return board.sum_unmarked() * num
    assert False, f"no winner: {boards}"


def find_worst_board(numbers: List[int], boards: Set[Board]) -> int:
    for num in numbers:
        to_remove = set()
        for board in boards:
            board.mark(num)
            if board.is_done():
                if len(boards) == 1:
                    return boards.pop().sum_unmarked() * num
                to_remove.add(board)
        for rem in to_remove:
            boards.remove(rem)
        assert len(boards) > 0
    assert False, f"something went wrong: {boards}"


if __name__ == '__main__':
    main(sys.argv[1])

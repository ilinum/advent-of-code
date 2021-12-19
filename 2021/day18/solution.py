import math
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import *


class Number(ABC):
    @abstractmethod
    def magnitude(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def try_explode(
            self,
            depth: int,
    ) -> Optional[Tuple[Optional[int], Optional[int], "Number"]]:
        raise NotImplementedError()

    @abstractmethod
    def try_split(self) -> Optional["Number"]:
        raise NotImplementedError()


def reduce(n: Number) -> Number:
    result = n
    while True:
        exploded = result.try_explode(depth=0)
        if exploded is None:
            break
        result = exploded[2]
    while True:
        split = result.try_split()
        if split is None:
            break
        result = split
        while True:
            exploded = result.try_explode(depth=0)
            if exploded is None:
                break
            result = exploded[2]
    return result


@dataclass(frozen=True)
class Pair(Number):
    left: Number
    right: Number

    def magnitude(self) -> int:
        return self.left.magnitude() * 3 + self.right.magnitude() * 2

    def try_explode(
            self,
            depth: int,
    ) -> Optional[Tuple[Optional[int], Optional[int], Number]]:
        if depth == 4:
            # From puzzle:
            # > Exploding pairs will always consist of two regular numbers.
            assert isinstance(self.left, RegularNumber), self.left
            assert isinstance(self.right, RegularNumber), self.right
            return self.left.val, self.right.val, RegularNumber(0)

        res = self.left.try_explode(depth + 1)
        if res is not None:
            left_num, right_num, child = res
            left = child
            right = self.right
            if right_num is not None:
                if isinstance(self.right, RegularNumber):
                    right = RegularNumber(self.right.val + right_num)
                else:
                    assert isinstance(self.right, Pair)
                    right = self.right.add_to_leftmost(right_num)
            return left_num, None, Pair(left, right)

        res = self.right.try_explode(depth + 1)
        if res is not None:
            left_num, right_num, child = res
            right = child
            left = self.left
            if left_num is not None:
                if isinstance(self.left, RegularNumber):
                    left = RegularNumber(self.left.val + left_num)
                else:
                    assert isinstance(self.left, Pair)
                    left = self.left.add_to_rightmost(left_num)
            return None, right_num, Pair(left, right)

        return None

    def add_to_leftmost(self, num: int) -> Number:
        if isinstance(self.left, RegularNumber):
            return Pair(RegularNumber(self.left.val+num), self.right)
        assert isinstance(self.left, Pair)
        return Pair(self.left.add_to_leftmost(num), self.right)

    def add_to_rightmost(self, num: int) -> Number:
        if isinstance(self.right, RegularNumber):
            return Pair(self.left, RegularNumber(self.right.val+num))
        assert isinstance(self.right, Pair)
        return Pair(self.left, self.right.add_to_rightmost(num))

    def try_split(self) -> Optional[Number]:
        left = self.left.try_split()
        if left is not None:
            return Pair(left, self.right)
        right = self.right.try_split()
        if right is not None:
            return Pair(self.left, right)
        return None

    def __repr__(self) -> str:
        return f"[{str(self.left)},{str(self.right)}]"


@dataclass(frozen=True)
class RegularNumber(Number):
    val: int

    def magnitude(self) -> int:
        return self.val

    def try_explode(
            self,
            depth: int,
    ) -> Optional[Tuple[int, int, Number]]:
        return None

    def try_split(self) -> Optional[Number]:
        if self.val < 10:
            return None
        return Pair(RegularNumber(self.val // 2), RegularNumber(math.ceil(self.val / 2)))

    def __repr__(self) -> str:
        return str(self.val)


def parse_number(line: str) -> Number:
    if line[0] != "[":
        return RegularNumber(int(line))
    assert line[-1] == "]", line
    line = line[1:len(line) - 1]

    num_open = 0
    split_point = None
    for i, c in enumerate(line):
        if c == "[":
            num_open += 1
        elif c == "]":
            num_open -= 1
        if num_open == 0 and c == ",":
            split_point = i
            break
    assert split_point is not None, line
    left = parse_number(line[:split_point])
    right = parse_number(line[split_point + 1:])
    return Pair(left, right)


def add(n1: Number, n2: Number) -> Number:
    result = Pair(n1, n2)
    return reduce(result)


def parse_input(lines: List[str]) -> List[Number]:
    return [parse_number(line) for line in lines]


def main(lines: List[str]) -> None:
    # Part 1.
    nums = parse_input(lines)
    assert len(nums) > 1
    cur_sum = nums[0]
    for num in nums[1:]:
        cur_sum = add(cur_sum, num)
    print(cur_sum.magnitude())

    # Part 2.
    sums = []
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i == j:
                continue
            sums.append(add(nums[i], nums[j]).magnitude())
    print(max(sums))


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

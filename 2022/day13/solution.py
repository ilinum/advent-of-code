import functools
import os
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class ListPacket:
    subpackets: list[Union['ListPacket', 'LiteralPacket']]


@dataclass(frozen=True)
class LiteralPacket:
    val: int


Packet = ListPacket | LiteralPacket


def compare(p1: Packet, p2: Packet) -> int:
    if isinstance(p1, LiteralPacket):
        if isinstance(p2, LiteralPacket):
            if p1.val < p2.val:
                return -1
            if p1.val == p2.val:
                return 0
            return 1
        return compare(ListPacket(subpackets=[p1]), p2)
    if isinstance(p2, LiteralPacket):
        return compare(p1, ListPacket(subpackets=[p2]))
    assert isinstance(p1, ListPacket)
    assert isinstance(p2, ListPacket)
    for s1, s2 in zip(p1.subpackets, p2.subpackets):
        cmp = compare(s1, s2)
        if cmp != 0:
            return cmp
    return compare(LiteralPacket(len(p1.subpackets)), LiteralPacket(len(p2.subpackets)))


def parse_packet(line: str) -> Packet:
    if line.startswith("["):
        assert line.endswith("]")
        line = line[1:len(line) - 1]
        subpackets = []
        buf = ""
        opens = 0
        for c in line:
            if c == "[":
                opens += 1
                buf += c
            elif c == "]":
                opens -= 1
                buf += c
            elif c == "," and opens == 0:
                subpackets.append(parse_packet(buf))
                buf = ""
            else:
                buf += c
        if len(buf) > 0:
            subpackets.append(parse_packet(buf))
        return ListPacket(subpackets=subpackets)
    else:
        return LiteralPacket(int(line))


def solve_p1(lines: list[str]) -> None:
    pairs: list[tuple[Packet, Packet]] = []
    buf = []
    for line in lines:
        if len(line) == 0:
            assert len(buf) == 2, len(buf)
            pairs.append((buf[0], buf[1]))
            buf = []
            continue
        buf.append(parse_packet(line))
    if len(buf) > 0:
        assert len(buf) == 2
        pairs.append((buf[0], buf[1]))

    ordered_indexes = []
    for i in range(len(pairs)):
        if compare(pairs[i][0], pairs[i][1]) < 0:
            ordered_indexes.append(i + 1)
    print(sum(ordered_indexes))


def solve_p2(lines: list[str]) -> None:
    packets = []
    for line in lines:
        if len(line) > 0:
            packets.append(parse_packet(line))
    dividers = [parse_packet("[[2]]"), parse_packet("[[6]]")]
    packets.extend(dividers)
    packets = sorted(packets, key=functools.cmp_to_key(lambda x, y: compare(x, y)))
    divider_idx = [packets.index(d) + 1 for d in dividers]
    result = 1
    for d in divider_idx:
        result *= d
    print(result)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    solve_p1(lines)
    solve_p2(lines)


def main() -> None:
    for f in os.listdir():
        if f.endswith("in"):
            process_file(f)


# Part 1:
# Part 2:
if __name__ == '__main__':
    main()

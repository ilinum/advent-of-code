import io
import sys
from abc import ABC, abstractmethod
from typing import *


class Packet(ABC):
    @abstractmethod
    def version(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def subpackets(self) -> List["Packet"]:
        raise NotImplementedError()

    @abstractmethod
    def compute(self) -> int:
        raise NotImplementedError()


TYPE_ID_LITERAL = 4


class LiteralPacket(Packet):
    def __init__(self, version: int, val: int):
        self._version = version
        self.val = val

    def version(self) -> int:
        return self._version

    def subpackets(self) -> List["Packet"]:
        # Literal packet never has subpackets.
        return []

    def compute(self) -> int:
        return self.val


class OperatorPacket(Packet):
    def __init__(self, version: int, type_id: int, subpackets: List["Packet"]):
        self._version = version
        self.type_id = type_id
        self._subpackets = subpackets

    def version(self) -> int:
        return self._version

    def subpackets(self) -> List["Packet"]:
        return self._subpackets

    def compute(self) -> int:
        values = [p.compute() for p in self.subpackets()]
        if self.type_id == 0:
            return sum(values)
        elif self.type_id == 1:
            # Product.
            result = values[0]
            for p in values[1:]:
                result *= p
            return result
        elif self.type_id == 2:
            return min(values)
        elif self.type_id == 3:
            return max(values)
        elif self.type_id == 5:
            assert len(values) == 2
            return 1 if values[0] > values[1] else 0
        elif self.type_id == 6:
            assert len(values) == 2
            return 1 if values[0] < values[1] else 0
        elif self.type_id == 7:
            assert len(values) == 2
            return 1 if values[0] == values[1] else 0
        else:
            assert False, f"unsupported packet type: {self.type_id}"


def parse_value(bits: io.StringIO) -> int:
    parsed_bits = ""
    cur = bits.read(5)
    while cur[0] == "1":
        parsed_bits += cur[1:]
        cur = bits.read(5)
    parsed_bits += cur[1:]
    return int(parsed_bits, 2)


def parse_packet(bits: io.StringIO) -> Packet:
    version = int(bits.read(3), 2)
    type_id = int(bits.read(3), 2)
    if type_id == TYPE_ID_LITERAL:
        return LiteralPacket(version, parse_value(bits))

    len_type = int(bits.read(1), 2)
    if len_type == 0:
        total_len = int(bits.read(15), 2)
        subpacket_bits = bits.read(total_len)
        subpackets = []
        while "1" in subpacket_bits:
            subpacket_io = io.StringIO(subpacket_bits)
            subpackets.append(parse_packet(subpacket_io))
            subpacket_bits = subpacket_io.read()
    else:
        total_packets = int(bits.read(11), 2)
        subpackets = []
        for _ in range(total_packets):
            subpackets.append(parse_packet(bits))
    return OperatorPacket(version, type_id, subpackets)


def hex_to_binary(line: str) -> str:
    result = []
    for c in line:
        i = int(c, 16)
        result.append(f"{i:04b}")
    return "".join(result)


def get_versions(root: Packet) -> List[int]:
    result = [root.version()]
    for p in root.subpackets():
        result.extend(get_versions(p))
    return result


def main(lines: List[str]) -> None:
    for line in lines:
        root = parse_packet(io.StringIO(hex_to_binary(line)))
        print(sum(get_versions(root)))
        print(root.compute())


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

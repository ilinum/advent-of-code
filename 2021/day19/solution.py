import sys
from dataclasses import dataclass
from typing import *


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int
    z: int

    def manhattan_distance(self, other: "Coordinates") -> int:
        shift = min([self.x, self.y, self.z, other.x, other.y, other.z])
        (x1, y1, z1) = map(lambda k: k + shift, [self.x, self.y, self.z])
        (x2, y2, z2) = map(lambda k: k + shift, [other.x, other.y, other.z])
        return abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1)


@dataclass(frozen=True)
class Scanner:
    beacons: Set[Coordinates]
    location: Optional[Coordinates] = None

    def shift(self, shift: Coordinates) -> "Scanner":
        assert self.location is None, self.location
        beacons = set()
        for b in self.beacons:
            beacons.add(Coordinates(b.x + shift.x, b.y + shift.y, b.z + shift.z))

        result = Scanner(beacons, shift)
        return result


def get_all_rotations(s: Scanner) -> List[Scanner]:
    beacons: List[Set[Coordinates]] = [set() for _ in range(24)]
    for c in s.beacons:
        beacons[0].add(Coordinates(c.x, c.y, c.z))
        beacons[1].add(Coordinates(c.x, -c.z, c.y))
        beacons[2].add(Coordinates(c.x, -c.y, -c.z))
        beacons[3].add(Coordinates(c.x, c.z, -c.y))

        beacons[4].add(Coordinates(-c.x, -c.y, c.z))
        beacons[5].add(Coordinates(-c.x, c.z, c.y))
        beacons[6].add(Coordinates(-c.x, c.y, -c.z))
        beacons[7].add(Coordinates(-c.x, -c.z, -c.y))

        beacons[8].add(Coordinates(c.y, c.z, c.x))
        beacons[9].add(Coordinates(c.y, -c.x, c.z))
        beacons[10].add(Coordinates(c.y, -c.z, -c.x))
        beacons[11].add(Coordinates(c.y, c.x, -c.z))

        beacons[12].add(Coordinates(-c.y, -c.z, c.x))
        beacons[13].add(Coordinates(-c.y, c.x, c.z))
        beacons[14].add(Coordinates(-c.y, c.z, -c.x))
        beacons[15].add(Coordinates(-c.y, -c.x, -c.z))

        beacons[16].add(Coordinates(c.z, c.x, c.y))
        beacons[17].add(Coordinates(c.z, -c.y, c.x))
        beacons[18].add(Coordinates(c.z, -c.x, -c.y))
        beacons[19].add(Coordinates(c.z, c.y, -c.x))

        beacons[20].add(Coordinates(-c.z, -c.x, c.y))
        beacons[21].add(Coordinates(-c.z, c.y, c.x))
        beacons[22].add(Coordinates(-c.z, c.x, -c.y))
        beacons[23].add(Coordinates(-c.z, -c.y, -c.x))
    return [Scanner(b) for b in beacons]


def try_place_scanner(placed: Scanner, to_place: Scanner) -> Optional[Scanner]:
    for i, rot in enumerate(get_all_rotations(to_place)):
        for p1 in rot.beacons:
            for p2 in placed.beacons:
                # Assume these two match.
                shift = Coordinates(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
                shifted = rot.shift(shift)
                intersection = shifted.beacons.intersection(placed.beacons)
                if len(intersection) >= 12:
                    return shifted
    return None


def place_single_scanner(
        placed_scanner: Scanner,
        all_placed_scanners: List[Scanner],
        scanners_to_place: List[Scanner],
) -> Scanner:
    for cur in scanners_to_place:
        maybe_placed = try_place_scanner(placed_scanner, cur)
        if maybe_placed is not None:
            scanners_to_place.remove(cur)
            beacons = set(placed_scanner.beacons)
            beacons.update(maybe_placed.beacons)
            all_placed_scanners.append(maybe_placed)
            return Scanner(beacons, placed_scanner.location)
    assert False, "no progress made in a single iteration"


def place_scanners(scanners: List[Scanner]) -> Scanner:
    assert all(s.location is None for s in scanners)
    placed_scanner = Scanner(scanners[0].beacons, Coordinates(0, 0, 0))
    scanners_to_place = scanners[1:]
    all_placed_scanners = [placed_scanner]
    while len(scanners_to_place) > 0:
        placed_scanner = place_single_scanner(
            placed_scanner,
            all_placed_scanners,
            scanners_to_place,
        )
        print(f"placed a scanner, {len(scanners_to_place)} left.")

    print("Scanner locations: {}".format("\n".join(str(s.location) for s in all_placed_scanners)))
    distances = []
    for i, s1 in enumerate(all_placed_scanners):
        for s2 in all_placed_scanners[i + 1:]:
            distances.append(s1.location.manhattan_distance(s2.location))
    print(max(distances))
    return placed_scanner


def parse_scanner(lines: List[str]) -> Scanner:
    assert len(lines) > 0
    assert lines[0].startswith("---")
    assert lines[0].endswith("---")
    beacons = set()
    for line in lines[1:]:
        (x, y, z) = map(int, line.split(","))
        beacons.add(Coordinates(x, y, z))
    return Scanner(beacons)


def parse_input(lines: List[str]) -> List[Scanner]:
    scanners = []
    start = 0
    for i, line in enumerate(lines):
        if len(line) == 0:
            scanners.append(parse_scanner(lines[start:i]))
            start = i + 1
    scanners.append(parse_scanner(lines[start:]))
    return scanners


def main(lines: List[str]) -> None:
    scanners = parse_input(lines)
    scan = place_scanners(scanners)
    print(len(scan.beacons))


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    main(lines)

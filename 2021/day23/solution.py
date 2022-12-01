import collections
import sys
from typing import *

"""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""


def get_desired_room(cell: str) -> int:
    if cell == "A":
        return 2
    if cell == "B":
        return 4
    if cell == "C":
        return 6
    if cell == "D":
        return 8
    assert False, f"Unknown type {cell}"


class Map:
    def __init__(
            self,
            hallway: List[Optional[str]],
            rooms: Dict[int, List[Optional[str]]],
            energy_used: int
    ):
        for h in hallway:
            assert h in {"A", "B", "C", "D", None}, h
        assert len(rooms) == 4, rooms
        for room in rooms.values():
            assert len(room) == 2
            for bunk in room:
                assert bunk in {"A", "B", "C", "D", None}, bunk
        self.hallway = hallway
        self.rooms = rooms
        self.energy_used = energy_used

    @classmethod
    def parse(cls, lines: List[str]) -> "Map":
        assert len(lines) == 5, lines
        stripped = []
        for line in lines:
            stripped.append(line[1:len(line) - 1])
        lines = stripped
        assert set(lines[0]) == {"#"}
        hallway = lines[1]
        assert set(hallway) == {"."}, hallway
        rooms = {}
        for i, c in enumerate(lines[2]):
            if c != "#" and c != " ":
                rooms[i] = [c]
        for i, c in enumerate(lines[3]):
            if c != "#" and c != " ":
                assert i in rooms, i
                assert len(rooms[i]) == 1
                rooms[i].append(c)

        return Map(hallway=[None] * len(hallway), rooms=rooms, energy_used=0)

    def complete(self) -> bool:
        for cell in {"A", "B", "C", "D"}:
            if set(self.rooms[get_desired_room(cell)]) != {cell}:
                return False
        return True

    def __repr__(self) -> str:
        rows = [str(self.energy_used)]
        rows.append("#" * (len(self.hallway) + 2))
        hallway = [c or "." for c in self.hallway]
        rows.append("#{}#".format("".join(hallway)))
        for bunk_i in range(0, 2):
            cur_bunk = []
            for i in range(len(self.hallway)):
                if i not in self.rooms:
                    cur_bunk.append("#")
                else:
                    cur_bunk.append(self.rooms[i][bunk_i] or ".")
            rows.append("#{}#".format("".join(cur_bunk)))
        rows.append("#" * (len(self.hallway) + 2))
        return "\n".join(rows)


def energy_to_move(cell: str, distance: int) -> int:
    assert distance > 0, distance
    if cell == "A":
        return distance
    if cell == "B":
        return distance * 10
    if cell == "C":
        return distance * 100
    if cell == "D":
        return distance * 1000
    assert False, f"Unknown type {cell}"


def states_after_single_iteration(original: Map) -> List[Map]:
    result = []
    # Try moving any ones in the hallway.
    for i, cur in enumerate(original.hallway):
        if cur is None:
            continue
        # Move into the correct room.
        room_i = get_desired_room(cur)
        start, end = min([room_i, i]), max([room_i, i])
        assert start < end, (start, end)
        counts = collections.defaultdict(lambda: 0)
        for h in original.hallway[start:end + 1]:
            counts[h] += 1
        assert counts[cur] >= 1
        if counts[cur] > 1 or set(counts.keys()) != {cur, None}:
            # Someone is in the way.
            continue
        distance = end - start
        if set(original.rooms[room_i]) != {None}:
            # No space available.
            continue
        # Try placing.
        rooms = dict(original.rooms)
        room = rooms[room_i]
        if room[1] is None:
            room = [room[0], cur]
            distance += 2
        else:
            assert room[0] is None
            room = [cur, room[1]]
            distance += 1
        rooms[room_i] = room
        hallway = list(original.hallway)
        hallway[i] = None
        result.append(
            Map(hallway, rooms, original.energy_used + energy_to_move(cur, distance)),
        )

    for (i, room) in original.rooms.items():
        if set(room) == {None}:
            continue
        move_idx = 0 if room[0] is not None else 1
        cur = room[move_idx]
        if get_desired_room(cur) == i:
            if move_idx == 1:
                continue
            if room[1] == cur:
                continue
        rooms = dict(original.rooms)
        rooms[i] = list(room)
        rooms[i][move_idx] = None
        for j in range(len(original.hallway)):
            if j in original.rooms.keys():
                continue
            start, end = min([i, j]), max([i, j])
            assert start < end, (start, end)
            if set(original.hallway[start:end + 1]) != {None}:
                # Someone is in the way.
                continue
            distance = 1 if move_idx == 0 else 2
            distance += end - start
            hallway = list(original.hallway)
            hallway[j] = cur
            result.append(
                Map(hallway, rooms, original.energy_used + energy_to_move(cur, distance)),
            )
    return result


def part1(map: Map) -> None:
    energies = []
    next_maps = collections.deque()
    next_maps.append(map)
    prev_min = {}
    while len(next_maps) > 0:
        cur = next_maps.popleft()
        # A bad hash function.
        cur_id = str(cur.hallway) + str(cur.rooms)
        prev = prev_min.get(cur_id, cur.energy_used + 1)
        if cur.energy_used >= prev:
            continue
        prev_min[cur_id] = cur.energy_used
        states = states_after_single_iteration(cur)
        if len(states) == 0:
            print(f"final state:\n{cur}")
        for n_state in states:
            if n_state.complete():
                print(f"found complete: {n_state.energy_used}")
                energies.append(n_state.energy_used)
            else:
                # print(f"\n{n_state}\n")
                next_maps.append(n_state)
        # time.sleep(100)
    print(min(energies))


def main(lines: List[str]) -> None:
    map = Map.parse(lines)
    part1(map)


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.rstrip("\n"), f.readlines()))
    main(lines)

from dataclasses import dataclass


@dataclass
class Marble:
    val: int
    next: "Marble"
    prev: "Marble"


def play(players: list[int], largest_marble: int) -> None:
    cur = Marble(val=0, next=None, prev=None)
    cur.next = cur
    cur.prev = cur
    player = 0
    for marble_value in range(1, largest_marble + 1):
        if (marble_value % 23) == 0:
            for _ in range(7):
                cur = cur.prev
            players[player] += marble_value + cur.val
            # Remove the current from the list.
            cur.prev.next = cur.next
            cur.next.prev = cur.prev
            cur = cur.next
        else:
            cur = cur.next
            marble = Marble(marble_value, next=cur.next, prev=cur)
            marble.prev.next = marble
            marble.next.prev = marble
            cur = marble
        player = (player + 1) % len(players)


def solve_p1(lines: list[str]) -> object:
    results = []
    for line in lines:
        splits = line.split()
        num_players = int(splits[0])
        last_marble = int(splits[-2])
        players = [0 for _ in range(num_players)]
        play(players, last_marble)
        results.append(max(players))
    return results


def solve_p2(lines: list[str]) -> object:
    results = []
    for line in lines:
        splits = line.split()
        num_players = int(splits[0])
        last_marble = int(splits[-2])
        players = [0 for _ in range(num_players)]
        play(players, last_marble*100)
        results.append(max(players))
    return results

def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:25:31
# Part 2: 00:26:20
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

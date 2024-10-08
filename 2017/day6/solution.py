def moves_to_cycle(banks: list[int]) -> int:
    seen = set()
    moves = 0
    while tuple(banks) not in seen:
        seen.add(tuple(banks))
        cur_max = max(banks)
        i = 0
        while i < len(banks):
            if banks[i] == cur_max:
                break
            i += 1

        to_redistribute = banks[i]
        banks[i] = 0
        while to_redistribute > 0:
            i = (i+1)%len(banks)
            banks[i] += 1
            to_redistribute -= 1
        moves += 1
    return moves

def solve_p1(lines: list[str]) -> object:
    assert len(lines) == 1
    banks = [int(c) for c in lines[0].split()]
    return moves_to_cycle(banks)

def solve_p2(lines: list[str]) -> object:
    assert len(lines) == 1
    banks = [int(c) for c in lines[0].split()]
    moves_to_cycle(banks)
    return moves_to_cycle(banks)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:07:29
# Part 2: 00:10:56
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

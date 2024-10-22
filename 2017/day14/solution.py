import binascii


def reverse_sublist(nums: list[int], cur_pos: int, size: int):
    sublist = []
    assert size <= len(nums)
    i = cur_pos
    while len(sublist) < size:
        sublist.append(nums[i])
        i = (i + 1) % len(nums)

    for n in reversed(sublist):
        nums[cur_pos] = n
        cur_pos = (cur_pos + 1) % len(nums)


def knot_hash(line: str) -> bytes:
    lengths = [ord(c) for c in line] + [17, 31, 73, 47, 23]
    nums = [i for i in range(256)]
    skip_size = 0
    cur_pos = 0
    for _ in range(64):
        for l in lengths:
            reverse_sublist(nums, cur_pos, l)
            cur_pos = (cur_pos + l + skip_size) % len(nums)
            skip_size += 1
    xord = []
    for i in range(0, len(nums), 16):
        n = nums[i]
        for c in nums[i + 1:i + 16]:
            n = n ^ c
        xord.append(n)
    return binascii.hexlify(bytearray(xord))


def hex_to_binary(h: bytes) -> str:
    return str(bin(int(h, 16))[2:].zfill(128))


def solve_p1(lines: list[str]) -> object:
    assert len(lines) == 1
    key = lines[0]
    num_used = 0
    for row in range(128):
        h = knot_hash(f"{key}-{row}")
        num_used += hex_to_binary(h).count("1")
    return num_used


def solve_p2(lines: list[str]) -> object:
    assert len(lines) == 1
    key = lines[0]
    squares = set()
    for row in range(128):
        h = knot_hash(f"{key}-{row}")
        s = hex_to_binary(h)
        for col in range(128):
            if s[col] == "1":
                squares.add((row, col))
    sq_to_reg = {}
    reg_num = 1
    for sq in squares:
        if sq in sq_to_reg:
            # Already processed.
            continue
        to_visit = {sq}
        while len(to_visit) > 0:
            cur = to_visit.pop()
            if cur in sq_to_reg:
                continue
            sq_to_reg[cur] = reg_num
            for (rc, cc) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (cur[0] + rc, cur[1] + cc)
                if neighbor in squares:
                    to_visit.add(neighbor)
        reg_num += 1
    return len(set(sq_to_reg.values()))


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:19:28
# Part 2: 00:10:56
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

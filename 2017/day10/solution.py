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

def solve_p1(lines: list[str]) -> object:
    assert len(lines) == 1
    lengths = [int(c) for c in lines[0].split(",")]
    nums = [i for i in range(256)]
    skip_size = 0
    cur_pos = 0
    for l in lengths:
        reverse_sublist(nums, cur_pos, l)
        cur_pos = (cur_pos + l + skip_size) % len(nums)
        skip_size += 1
    return nums[0] * nums[1]


def solve_p2(lines: list[str]) -> object:
    assert len(lines) == 1
    lengths = [ord(c) for c in lines[0]] + [17, 31, 73, 47, 23]
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
        for c in nums[i+1:i+16]:
            n = n ^ c
        xord.append(n)
    return binascii.hexlify(bytearray(xord))


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:11:02
# Part 2: 00:26:28
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

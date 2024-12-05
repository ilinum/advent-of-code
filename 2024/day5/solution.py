def is_valid_ordering(full_prereqs: dict[int, set[int]], nums: list[int]) -> bool:
    prereqs = {}
    num_set = set(nums)
    for n, prev_nums in full_prereqs.items():
        if n in num_set:
            prereqs[n] = set()
            for pn in prev_nums:
                if pn in num_set:
                    prereqs[n].add(pn)

    for num in nums:
        if len(prereqs.get(num, set())) > 0:
            return False
        for k in prereqs:
            if num in prereqs[k]:
                prereqs[k].remove(num)

    return True

def solve_p1(lines: list[str]) -> object:
    prereqs = {}
    i = 0
    while i < len(lines) and len(lines[i]) > 0:
        line = lines[i]
        a, b = line.split("|")
        if int(b) not in prereqs:
            prereqs[int(b)] = set()
        prereqs[int(b)].add(int(a))
        i += 1

    i += 1
    middle_pages = []
    while i < len(lines):
        line = lines[i]
        nums = [int(e) for e in line.split(",")]
        if is_valid_ordering(prereqs, nums):
            middle_pages.append(nums[len(nums) // 2])
        i += 1

    return sum(middle_pages)


def reorder(full_prereqs: dict[int, set[int]], nums: list[int]) -> list[int]:
    prereqs = {}
    num_set = set(nums)
    for n in num_set:
        prereqs[n] = set()
    for n, prev_nums in full_prereqs.items():
        if n in num_set:
            for pn in prev_nums:
                if pn in num_set:
                    prereqs[n].add(pn)

    result = []
    possible = []
    for n, prev_nums in prereqs.items():
        if len(prev_nums) == 0:
            possible.append(n)
    while len(possible) > 0:
        num = possible.pop()
        result.append(num)
        for k in prereqs:
            if num in prereqs[k]:
                prereqs[k].remove(num)
                if len(prereqs[k]) == 0:
                    possible.append(k)

    assert len(result) == len(nums), f"{result}, {nums}"
    assert is_valid_ordering(full_prereqs, result)
    return result


def solve_p2(lines: list[str]) -> object:
    prereqs = {}
    i = 0
    while i < len(lines) and len(lines[i]) > 0:
        line = lines[i]
        a, b = line.split("|")
        if int(b) not in prereqs:
            prereqs[int(b)] = set()
        prereqs[int(b)].add(int(a))
        i += 1

    i += 1
    middle_pages = []
    while i < len(lines):
        line = lines[i]
        nums = [int(e) for e in line.split(",")]
        print(f"processing line {i}")
        if not is_valid_ordering(prereqs, nums):
            nums = reorder(prereqs, nums)
            middle_pages.append(nums[len(nums) // 2])
        i += 1

    return sum(middle_pages)



def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:12:23
# Part 2: 00:24:17
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

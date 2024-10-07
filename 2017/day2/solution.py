def solve_p1(lines: list[str]) -> object:
    row_checksums = []
    for line in lines:
        row = list(map(int, line.split()))
        row_checksums.append(max(row) - min(row))
    return sum(row_checksums)

def find_and_divide_without_remainder(nums: list[int]) -> int:
    for i in range(len(nums)-1):
        for j in range(i+1, len(nums)):
            x = nums[i]
            y = nums[j]
            if x % y == 0:
                return x // y
            if y % x == 0:
                return y // x
    assert False, f"No evenly divisible number found: {nums}"

def solve_p2(lines: list[str]) -> object:
    row_result = []
    for line in lines:
        row = list(map(int, line.split()))
        row_result.append(find_and_divide_without_remainder(row))
    return sum(row_result)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:01:39
# Part 2: 00:05:15
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

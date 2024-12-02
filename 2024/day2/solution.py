def is_safe(nums: list[int]) -> bool:
    if len(nums) < 2:
        return True
    sign = nums[1] - nums[0]
    for i in range(1, len(nums)):
        d = nums[i] - nums[i-1]
        if (sign < 0) != (d < 0):
            return False
        d = abs(d)
        if d < 1 or d > 3:
            return False

    return True

def solve_p1(lines: list[str]) -> object:
    result = 0
    for line in lines:
        nums = [int(i) for i in line.split()]
        if is_safe(nums):
            result += 1
    return result


def solve_p2(lines: list[str]) -> object:
    result = 0
    for line in lines:
        nums = [int(i) for i in line.split()]
        if is_safe(nums):
            result += 1
        else:
            for i in range(len(nums)):
                if is_safe(nums[:i] + nums[i+1:]):
                    result += 1
                    break
    return result


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip().lower(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1:
# Part 2:
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

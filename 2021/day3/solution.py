import sys
from typing import List, Dict


def freq_map_by_position(numbers: List[List[int]]) -> Dict[int, Dict[int, int]]:
    result = dict()
    for number in numbers:
        for i, digit in enumerate(number):
            if i not in result:
                result[i] = {0: 0, 1: 0}
            result[i][digit] += 1
    return result


def main(filename: str) -> None:
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
        numbers = []
        for line in lines:
            number = []
            for char in line:
                digit = int(char)
                assert digit in {0, 1}
                number.append(digit)
            numbers.append(number)
    part_1(numbers)
    part_2(numbers)


def part_2(numbers: List[List[int]]) -> None:
    oxy_str = "".join(str(n) for n in oxygen_generator(numbers))
    co2_str = "".join(str(n) for n in co2_scrubber(numbers))
    oxy = int(oxy_str, 2)
    co2 = int(co2_str, 2)
    print(f"oxy: {oxy}, co2: {co2}, result: {co2 * oxy}")


def oxygen_generator(numbers: List[List[int]]) -> List[int]:
    assert len(numbers) > 0
    if len(numbers) == 1:
        return numbers[0]
    freq_map = freq_map_by_position(numbers)
    if freq_map[0][0] > freq_map[0][1]:
        n = 0
    else:
        n = 1
    filtered_nums = [num[1:] for num in numbers if num[0] == n]
    result = [n]
    result.extend(oxygen_generator(filtered_nums))
    return result


def co2_scrubber(numbers: List[List[int]]) -> List[int]:
    assert len(numbers) > 0
    if len(numbers) == 1:
        return numbers[0]
    freq_map = freq_map_by_position(numbers)
    if freq_map[0][0] <= freq_map[0][1]:
        n = 0
    else:
        n = 1
    filtered_nums = [num[1:] for num in numbers if num[0] == n]
    result = [n]
    result.extend(co2_scrubber(filtered_nums))
    return result


def part_1(numbers: List[List[int]]) -> None:
    freq_map = freq_map_by_position(numbers)
    gamma_str = ""
    epsilon_str = ""
    for i in range(len(numbers[0])):
        d = freq_map[i]
        assert len(d) == 2
        if d[0] > d[1]:
            gamma_str += "0"
            epsilon_str += "1"
        else:
            gamma_str += "1"
            epsilon_str += "0"

    gamma = int(gamma_str, 2)
    epsilon = int(epsilon_str, 2)
    print(f"gamma: {gamma}, epsilon: {epsilon}, result: {gamma * epsilon}")


if __name__ == '__main__':
    main(sys.argv[1])

import time


def num_ways_to_win(ms: int, record_distance: int) -> int:
    result = 0
    for hold_time in range(ms):
        speed = hold_time * 1
        remaining = ms - hold_time
        actual_distance = remaining * speed
        if actual_distance > record_distance:
            result += 1
    return result


def solve_p1(lines: list[str]) -> object:
    assert len(lines) == 2, lines
    (time_str, distance_str) = lines
    times = list(map(int, time_str.removeprefix("time:").strip().split()))
    distances = list(map(int, distance_str.removeprefix("distance:").strip().split()))
    assert len(times) == len(distances)
    result = 1
    for (ms, distance) in zip(times, distances):
        result *= num_ways_to_win(ms, distance)
    return result


def solve_p2(lines: list[str]) -> object:
    assert len(lines) == 2, lines
    (time_str, distance_str) = lines
    ms = int(time_str.removeprefix("time:").strip().replace(" ", ""))
    distance = int(distance_str.removeprefix("distance:").strip().replace(" ", ""))
    return num_ways_to_win(ms, distance)


def process_file(filename: str) -> None:
    start = time.time()
    print(f"processing '{file}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))
    end = time.time()
    print(f"processed '{file}' in {end - start:.2f}s")


# Part 1: 00:11:42
# Part 2: 00:13:30
if __name__ == '__main__':
    for file in [
        "sample.in",
        "input.in",
    ]:
        process_file(file)

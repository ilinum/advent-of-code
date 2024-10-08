from dataclasses import dataclass


@dataclass
class MinuteRange:
    start: int
    end: int


@dataclass
class Guard:
    id: int
    asleep_times: list[MinuteRange]


def parse_guard_line(line: str) -> int:
    assert "guard" in line
    (_, guard_sentence) = line.split("] ")
    (_, guard_id, _, _) = guard_sentence.split()
    return int(guard_id.removeprefix("#"))


def parse_time_minutes(line: str) -> int:
    (_, hour_minute) = line.split()
    (_, minute) = hour_minute.split(":")
    return int(minute)


def parse_log(lines: list[str]) -> dict[int, Guard]:
    lines.sort()
    assert "guard" in lines[0]
    cur_guard = parse_guard_line(lines[0])
    result = {cur_guard: Guard(cur_guard, asleep_times=[])}
    sleep_start = None
    for line in lines[1:]:
        if "guard" in line:
            cur_guard = parse_guard_line(line)
            if cur_guard not in result:
                result[cur_guard] = Guard(cur_guard, asleep_times=[])
            continue
        if "falls asleep" in line:
            sleep_start = parse_time_minutes(line.split("] ")[0])
            continue
        assert "wakes up" in line
        sleep_end = parse_time_minutes(line.split("] ")[0])
        result[cur_guard].asleep_times.append(MinuteRange(sleep_start, sleep_end))
    return result


def find_sleepiest_guard(guards: dict[int, Guard]) -> int:
    sleep_duration = {}
    for guard in guards:
        sleep_duration[guard] = 0
        for t in guards[guard].asleep_times:
            sleep_duration[guard] += t.end - t.start

    return max(set(sleep_duration.items()), key=lambda x: x[1])[0]


def most_frequent_sleep_minute(sleep_times: list[MinuteRange]) -> (int, int):
    minute_freq = {x: 0 for x in range(60)}
    for t in sleep_times:
        for m in range(t.start, t.end):
            minute_freq[m] += 1
    return max(set(minute_freq.items()), key=lambda x: x[1])


def solve_p1(lines: list[str]) -> object:
    guards = parse_log(lines)
    sleepiest_guard = find_sleepiest_guard(guards)
    (asleep_minute, _) = most_frequent_sleep_minute(guards[sleepiest_guard].asleep_times)
    return asleep_minute * sleepiest_guard


def solve_p2(lines: list[str]) -> object:
    guards = parse_log(lines)
    guard_most_frequent_sleep_minute = set()
    for guard in guards:
        (minute, times) = most_frequent_sleep_minute(guards[guard].asleep_times)
        guard_most_frequent_sleep_minute.add((guard, minute, times))
    (guard, minute, _) = max(guard_most_frequent_sleep_minute, key=lambda x: x[2])
    return guard * minute


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.lower().strip(), f.readlines()))
    print(solve_p1(lines))
    print(solve_p2(lines))


# Part 1: 00:25:30
# Part 2: 00:30:06
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

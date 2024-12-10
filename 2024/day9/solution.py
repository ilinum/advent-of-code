import time
from collections import deque
from dataclasses import dataclass


@dataclass
class File:
    position: int
    id: int
    size: int

@dataclass
class FreeSpace:
    position: int
    size: int

def solve_p1(lines: list[str]) -> object:
    assert len(lines) == 1
    objects = deque()
    position = 0
    is_file = True
    file_id = 0
    for c in lines[0]:
        n = int(c)
        if is_file:
            objects.append(File(position=position, id=file_id,size=n))
            file_id += 1
        else:
            objects.append(FreeSpace(position=position, size=n))
        position += n
        is_file = not is_file

    checksum = 0
    position = 0
    while len(objects) > 0:
        obj = objects.popleft()
        if isinstance(obj, File):
            while obj.size > 0:
                checksum += position * obj.id
                obj.size -= 1
                position += 1
        else:
            assert isinstance(obj, FreeSpace)
            while len(objects) > 0 and obj.size > 0:
                f = objects[-1]
                if isinstance(f, FreeSpace):
                    objects.pop()
                    continue
                assert isinstance(f, File)
                if f.size > 0:
                    f.size -= 1
                    obj.size -= 1
                    checksum += position * f.id
                    position += 1
                if f.size == 0:
                    objects.pop()

    return checksum

def solve_p2(lines: list[str]) -> object:
    assert len(lines) == 1
    files = []
    spaces = []
    position = 0
    is_file = True
    for c in lines[0]:
        n = int(c)
        if is_file:
            files.append(File(position=position, id=len(files),size=n))
        else:
            spaces.append(FreeSpace(position=position, size=n))
        position += n
        is_file = not is_file
    for f in reversed(files):
        for s in spaces:
            if s.size >= f.size and s.position < f.position:
                f.position = s.position
                s.size -= f.size
                s.position += f.size
                break
    checksum = 0
    for f in files:
        for p in range(f.position, f.position+f.size):
            checksum += f.id * p
    return checksum


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    start = time.time()
    print(solve_p1(lines))
    print(solve_p2(lines))
    print(f"processed file '{filename}' in {time.time() - start:.2f}s")


# Part 1: 00:18:19
# Part 2: 00:46:08
if __name__ == "__main__":
    process_file("sample.in")
    process_file("input.in")

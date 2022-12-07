import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class File:
    size: int


class Directory:
    def __init__(self, parent: Optional['Directory']) -> None:
        self.parent = parent
        self.children: dict[str, 'Directory' | File] = {}


class Command:
    def __init__(self, name: str, args: list[str]) -> None:
        self.name = name
        self.args = args
        self.outputs: list[str] = []


class Executor:
    def __init__(self) -> None:
        self.root = Directory(parent=None)
        self.cwd = self.root

    def execute(self, cmd: Command) -> None:
        match cmd.name:
            case "ls":
                assert len(cmd.args) == 0
                for entry in cmd.outputs:
                    match entry.split():
                        case ["dir", name]:
                            self.cwd.children[name] = Directory(self.cwd)
                        case [size, name]:
                            self.cwd.children[name] = File(int(size))
                        case _:
                            assert False, f"unsupported ls entry: {entry}"
            case "cd":
                assert len(cmd.outputs) == 0
                match cmd.args:
                    case ["/"]:
                        self.cwd = self.root
                    case [".."]:
                        assert self.cwd.parent is not None
                        self.cwd = self.cwd.parent
                    case [name]:
                        child = self.cwd.children[name]
                        assert isinstance(child, Directory), self.cwd
                        self.cwd = child
                    case _:
                        assert False, f"unhandled cd args {cmd.args}"


def populate_sizes(root: Directory, sizes: dict[Directory | File, int]) -> None:
    for c in root.children.values():
        if isinstance(c, File):
            sizes[c] = c.size
        else:
            assert isinstance(c, Directory)
            populate_sizes(c, sizes)
    sizes[root] = sum(sizes[c] for c in root.children.values())


def execute_commands(lines: list[str]) -> Executor:
    cmd: Command | None = None
    executor = Executor()
    for line in lines:
        if line.startswith("$"):
            if cmd is not None:
                executor.execute(cmd)
            _, name, *args = line.split()
            cmd = Command(name, args)
        else:
            assert cmd is not None, line
            cmd.outputs.append(line)
    if cmd is not None:
        executor.execute(cmd)
    return executor


def solve(lines: list[str]) -> None:
    executor = execute_commands(lines)
    sizes = {}
    populate_sizes(executor.root, sizes)
    dir_sizes = [v for k, v in sizes.items() if isinstance(k, Directory)]
    p1_answer = sum(size for size in dir_sizes if size <= 100000)
    print(p1_answer)
    free_space = (70000000 - sizes[executor.root])
    need = 30000000 - free_space
    dir_to_delete_size = sizes[executor.root]
    for size in dir_sizes:
        if need <= size < dir_to_delete_size:
            dir_to_delete_size = size
    print(dir_to_delete_size)


def process_file(filename: str) -> None:
    print(f"processing '{filename}'")
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))
    solve(lines)


# Part 1: 00:25:47
# Part 2: 00:29:58
if __name__ == '__main__':
    process_file("sample.in")
    process_file("input.in")

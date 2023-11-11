# Let's make an interpreter!!!
import typing as typ

from tools import get_input

SAMPLE = [
    'cpy 41 a',
    'inc a',
    'inc a',
    'dec a',
    'jnz a 2',
    'dec a',
]

REAL = get_input(12, 2016)


class Interpreter:
    def __init__(self, lines: typ.List[str], part2: bool = False) -> None:
        self.lines = lines

        self.n_lines = len(lines)

        self.regz: typ.Dict[str, int] = {'a': 0, 'b': 0, 'c': 1 if part2 else 0, 'd': 0}

        self.ip = 0

    def processline(self, line:str) -> None:
        split = line.split()

        if split[0] == 'cpy':
            if split[1].isalpha():
                self.regz[split[2]] = self.regz[split[1]]
            else:
                self.regz[split[2]] = int(split[1])
            self.ip += 1
        elif split[0] == 'inc':
            self.regz[split[1]] += 1
            self.ip += 1
        elif split[0] == 'dec':
            self.regz[split[1]] -= 1
            self.ip += 1
        elif split[0] == 'jnz':
            nz = self.regz[split[1]] if split[1].isalpha() else int(split[1])
            if nz != 0:
                self.ip += int(split[2])
            else:
                self.ip += 1

    def exec1(self) -> None:
        while self.ip >= 0 and self.ip < self.n_lines:
            self.processline(self.lines[self.ip])

    def solve1(self) -> int:
        self.exec1()
        return self.regz['a']
    

if __name__ == "__main__":
    t = Interpreter(SAMPLE)
    print(t.solve1())
    r = Interpreter(REAL)
    print(r.solve1())

    t = Interpreter(SAMPLE, part2=True)
    print(t.solve1())
    r = Interpreter(REAL, part2=True)
    print(r.solve1())
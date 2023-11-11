import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    'nop +0',
    'acc +1',
    'jmp +4',
    'acc +3',
    'jmp -3',
    'acc -99',
    'acc +1',
    'jmp -4',
    'acc +6',
]

REAL = get_input(DAYDAY, 2020)


class Day:
    def __init__(self, lines) -> None:
        self.ip = 0
        self.acc = 0
        self.program = lines
        self.execed = [0 for l in lines]

    def exec(self, k):
        line = self.program[k]
        instr, val = line.split(' ')
        val = int(val)
        if instr == "nop":
            self.ip += 1
        elif instr == "acc":
            self.ip += 1
            self.acc += val
        elif instr == "jmp":
            self.ip += val


    def solve1(self):
        while True:
            if not self.execed[self.ip]:
                self.execed[self.ip] = True
                self.exec(self.ip)
            else:
                return self.acc

    def solve2(self):
        lenp = len(self.program)
        for changed in range(lenp):
            origline = self.program[changed]
            split = origline.split()
            if split[0] == "jmp":
                self.program[changed] = 'nop ' + split[1]
            elif split[0] == "nop":
                self.program[changed] = 'jmp ' + split[1]

            self.ip = 0
            self.acc = 0
            self.execed = [0 for l in self.program]
            while True:
                if self.ip == lenp:
                    return self.acc

                if not self.execed[self.ip]:
                    self.execed[self.ip] = True
                    self.exec(self.ip)
                else:
                    break

            self.program[changed] = origline

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())
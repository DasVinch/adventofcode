from __future__ import annotations

import typing as typ

TEST = [
    'cpy 2 a',
    'tgl a',
    'tgl a',
    'tgl a',
    'cpy 1 a',
    'dec a',
    'dec a'
]

MULTEST = [
    'cpy b c',
    'inc a',
    'dec c',
    'jnz c -2',
    'dec d',
    'jnz d -5',
] # assert a += b * d

from tools import get_input
REAL = get_input(23, 2016)
REALWMUL = get_input(230, 2016)

class Interpreter:
    def __init__(self, lines: typ.List[str], verbose: bool = False, max_instructions: int | None = None) -> None:
        self.lines = lines

        self.n_lines = len(lines)

        self.regz: typ.Dict[str, int] = {'a': 0, 'b': 0, 'c': 0, 'd': 0}

        self.ip = 0

        self.verbose = verbose

        self.max_instructions = max_instructions
        self.exec_count = 0

    def processline(self, line:str) -> None:
        split = line.split()

        if self.verbose:
            print(self.ip, line, self.regz)

        if split[0] == 'out':
            val = self.regz[split[1]] if split[1].isalpha() else int(split[1])
            print(f'OUT {val}')
            self.ip += 1
        elif split[0] == 'mul':
            target = split[1]
            op1 = int(split[2]) if not split[2].isalpha() else self.regz[split[2]]
            reg2 = split[3]
            opz = split[4]
            self.regz[target] += op1 * self.regz[reg2]
            self.regz[reg2] = 0
            self.regz[opz] = 0
            self.ip += 1
        elif split[0] == 'cpy':
            if split[2].isalpha():
                if split[1].isalpha():
                    self.regz[split[2]] = self.regz[split[1]]
                else:
                    self.regz[split[2]] = int(split[1])
                self.ip += 1
        elif split[0] == 'inc':
            if split[1].isalpha():
                self.regz[split[1]] += 1
                self.ip += 1
        elif split[0] == 'dec':
            if split[1].isalpha():
                self.regz[split[1]] -= 1
                self.ip += 1
        elif split[0] == 'jnz':
            nz = self.regz[split[1]] if split[1].isalpha() else int(split[1])
            if nz != 0:
                if split[2].isalpha():
                    self.ip += self.regz[split[2]]
                else:
                    self.ip += int(split[2])
            else:
                self.ip += 1
        elif split[0] == 'tgl':
            # assume self.ip points to the line we're processing
            if split[1].isalpha():
                offset = self.regz[split[1]]
            else:
                offset = int(split[1])

            if self.ip + offset >= 0 and self.ip + offset < self.n_lines:
                instr_split = self.lines[self.ip + offset].split()
                cmd = instr_split[0]
                if cmd == 'inc':
                    instr_split[0] = 'dec'
                elif cmd in ['dec', 'tgl']:
                    instr_split[0] = 'inc'
                elif cmd == 'jnz':
                    instr_split[0] = 'cpy'
                elif cmd in ['cpy']:
                    instr_split[0] = 'jnz'
                else:
                    raise ValueError('asdf')
                self.lines[self.ip + offset] = ' '.join(instr_split)

            self.ip += 1

        self.exec_count += 1
            


    def exec1(self, ipbreak: int | None = None) -> None:
        while self.ip >= 0 and self.ip < self.n_lines:
            if ipbreak is not None and self.ip == ipbreak:
                break
            self.processline(self.lines[self.ip])
            if self.max_instructions and self.exec_count == self.max_instructions:
                print('Max instructions reached.')
                break

    def solve1(self, ipbreak: int | None = None) -> int:
        self.exec1(ipbreak)
        return self.regz['a']

if __name__ == "__main__":

    import time

    i = Interpreter(TEST.copy(), verbose=False)
    s = time.time()
    print(i.solve1(), 1e3 * (time.time() - s))

    i2 = Interpreter(REAL.copy(), verbose=False)
    s = time.time()
    i2.regz['a'] = 7
    print(i2.solve1(ipbreak = None), 1e3*(time.time() - s))

    i3 = Interpreter(REALWMUL.copy(), verbose=False)
    s = time.time()
    i3.regz['a'] = 12
    print(i3.solve1(ipbreak=None), 1e3*(time.time() - s))

    i = Interpreter(MULTEST.copy(), verbose=False, max_instructions = None)
    s = time.time()
    i.regz['a'] = 0
    i.regz['b'] = 1
    i.regz['c'] = 0
    i.regz['d'] = 200
    print(i.solve1(), 1e3*(time.time() - s))
    print(i.regz)

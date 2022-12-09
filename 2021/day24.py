from typing import List
from tools import get_input

BITSPROGRAM = [
    'inp w',
    'add z w',
    'mod z 2',
    'div w 2',
    'add y w',
    'mod y 2',
    'div w 2',
    'add x w',
    'mod x 2',
    'div w 2',
    'mod w 2',
]

MONAD = get_input(24, 2021)

class ALUInterpreter:
    def __init__(self, stdin: List[int], program: List[str]) -> None:
        self.stdin_p = 0
        self.stdin = stdin

        self.regs = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

        self.ip = 0
        self.program = program
        self.lenp = len(self.program)

        self.debug = False

    def reset(self, new_stdin):
        self.stdin = new_stdin
        self.stdin_p = 0
        self.ip = 0
        for k in self.regs:
            self.regs[k] = 0

    def override_regs(self, w, x, y, z):
        self.regs['w'] = w
        self.regs['x'] = x
        self.regs['y'] = y
        self.regs['z'] = z

    def get_reg_tuple(self):
        return tuple(self.regs[c] for c in 'wxyz')

    def print(self, s, end='\n'):
        if self.debug:
            print(s, end=end)

    def interpret(self):
        while self.ip < self.lenp:
            instr = self.program[self.ip]
            ilist = instr.split()
            self.ip += 1

            self.print(instr, end = ' | ')

            if ilist[0] == 'inp':
                self.regs[ilist[1]] = self.stdin[self.stdin_p]
                self.print(f'inp {ilist[1]} <- {self.stdin[self.stdin_p]}')
                self.stdin_p += 1
            else:
                origval = self.regs[ilist[1]]
                self.print(f'{ilist[0]} {ilist[1]} ({origval}) <- ', end='')
                if ilist[0] == 'add':
                    if ilist[2] in 'wxyz':
                        self.regs[ilist[1]] += self.regs[ilist[2]]
                        self.print(f'+ {self.regs[ilist[2]]} = {self.regs[ilist[1]]}')
                    else:
                        self.regs[ilist[1]] += int(ilist[2])
                        self.print(f'+ {int(ilist[2])} = {self.regs[ilist[1]]}')
                elif ilist[0] == 'mul':
                    if ilist[2] in 'wxyz':
                        self.regs[ilist[1]] *= self.regs[ilist[2]]
                        self.print(f'* {self.regs[ilist[2]]} = {self.regs[ilist[1]]}')
                    else:
                        self.regs[ilist[1]] *= int(ilist[2])
                        self.print(f'* {int(ilist[2])} = {self.regs[ilist[1]]}')
                elif ilist[0] == 'div':
                    if ilist[2] in 'wxyz':
                        self.regs[ilist[1]] //= self.regs[ilist[2]]
                        self.print(f'/ {self.regs[ilist[2]]} = {self.regs[ilist[1]]}')
                    else:
                        self.regs[ilist[1]] //= int(ilist[2])
                        self.print(f'/ {int(ilist[2])} = {self.regs[ilist[1]]}')
                elif ilist[0] == 'mod':
                    if ilist[2] in 'wxyz':
                        self.regs[ilist[1]] %= self.regs[ilist[2]]
                        self.print(f'% {self.regs[ilist[2]]} = {self.regs[ilist[1]]}')
                    else:
                        self.regs[ilist[1]] %= int(ilist[2])
                        self.print(f'% {int(ilist[2])} = {self.regs[ilist[1]]}')
                elif ilist[0] == 'eql':
                    if ilist[2] in 'wxyz':
                        self.regs[ilist[1]] = int(self.regs[ilist[1]] == self.regs[ilist[2]])
                        self.print(f'== {self.regs[ilist[2]]} = {self.regs[ilist[1]]}')
                    else:
                        self.regs[ilist[1]] = int(self.regs[ilist[1]] == int(ilist[2]))
                        self.print(f'== {int(ilist[2])} = {self.regs[ilist[1]]}')

    def __str__(self):
        return '\n'.join([
            f"stdin_p : {self.stdin_p}",
            f"stdin   : {self.stdin}",
            f"ip/lines: {self.ip} / {self.lenp}",
            f"w       : {self.regs['w']}",
            f"x       : {self.regs['x']}",
            f"y       : {self.regs['y']}",
            f"z       : {self.regs['z']}",
            ])

SUBMONADS = []
temp = []
for line in MONAD:
    if line.startswith('inp'):
        SUBMONADS.append(temp)
        temp = []
    temp += [line]

SUBMONADS = SUBMONADS[1:] + [temp]

if __name__ == "__main__":

    alu = ALUInterpreter([], MONAD)
    subalus = [ALUInterpreter([], SUBMONADS[ii]) for ii in range(14)]

    states = {0} # w <- inp and x *= 0 don't actually matter. Fuck even y doesn't matter!
    newstates = set()
    for bitpos in range(10):
        for bit in range(1,10):
            for s in states:
                sb = subalus[bitpos] 
                sb.reset([bit])
                sb.override_regs(0,0,0,s)
                sb.interpret()
                z = sb.get_reg_tuple()[-1]
                if z < 26:
                    newstates.add(z)
        states = newstates
        newstates = set()
        print(len(states))
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

# yapf: disable
VALUES_C1DIVC2 = [
    ( 11,   1,   7), #  0 Add digit, unavoidable      1
        ( 14,   1,   8), #  1 Add digit, unavoidable      2
            ( 10,   1,  16), #  2 Add digit, unavoidable      3

                ( 14,   1,   8), #  3 Add digit, unavoidable      4
                ( -8,  26,   3), #  4 Possible remove AND not add -> 3

                ( 14,   1,  12), #  5 Add digit unavoid           -> 4
                (-11,  26,   1), #  6 Drop poss no add            -> 3

                ( 10,   1,   8), #  7 Add unavoid                 -> 4
                ( -6,  26,   8), #  8 Drop poss no add            -> 3
                
            ( -9,  26,  14), #  9 Drop poss no add            -> 2

            ( 12,  1,    4), # 10 Add unavoid                  -> 3
            ( -5,  26,  14), # 11 Drop poss no add            -> 2
        ( -4,  26,  15), # 12 Drop poss no add            -> 1
    ( -9,  26,   6), # 13 Drop poss no add            -> 0
]
# yapf: enable


def aMuchSimplerALUModule(z, stdin, c1, div, c2) -> int:
    # c1 < 0 means we can make X 0 means we have a chance to NOT add a digit
    # div = 26 means we have a chance to drop a digit
    if c1 > 0:
        X = 1
    else:
        # Only the LAST digit of Z matters in the determination of X
        X = (z % 26 + c1) != stdin

    Y = (stdin + c2) * X  # c2 > 0, nonzero iff X == 1

    # if div == 26, z >> 1
    # if X == 1, z << 1
    # add y as new digit
    Z = (z // div) * (25*X + 1) + Y

    return Z




        
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
            #f"stdin_p : {self.stdin_p}",
            #f"stdin   : {self.stdin}",
            #f"ip/lines: {self.ip} / {self.lenp}",
            #f"w       : {self.regs['w']}",
            #f"x       : {self.regs['x']}",
            #f"y       : {self.regs['y']}",
            f"z       : {self.regs['z']} | {base26s(self.regs['z'])}",
            ])


def base26s(n: int):
    if n == 0:
        return 'Z'
    
    s = ''
    while n > 0:
        s = chr(((n % 26- 1)%26 + 65)) + s
        n //= 26

    return s





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

    '''
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
    '''
              
sb = alu
mylist = [9 for _ in range(14)]
# 0
# 1 no impact at all
mylist[2] = 2
mylist[3] = 9
mylist[4] = 9
mylist[5] = 8
mylist[6] = 9
mylist[7] = 7
mylist[8] = 9
mylist[9] = 9
mylist[10] = 9
mylist[11] = 8
mylist[12] = 3
mylist[13] = 9

for b0 in range(1,10):
    for b1 in range(1,10):
        mylist[0] = b0
        mylist[13] = b1
        sb.reset(mylist)
        sb.override_regs(0,0,0,0)
        sb.interpret()
        if sb.regs['z'] == 0:
            break
        print(f"input @ {b0,b1}")
        print(sb)
        print('-------------------')



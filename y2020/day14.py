import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
    'mem[8] = 11',
    'mem[7] = 101',
    'mem[8] = 0',
]

SAMPLE2 = [
'mask = 000000000000000000000000000000X1001X',
'mem[42] = 100',
'mask = 00000000000000000000000000000000X0XX',
'mem[26] = 1',
]

REAL = get_input(DAYDAY, 2020)

class Day:
    def __init__(self, lines) -> None:
        self.lines = lines
        self.mem = {}

    def solve1(self):
        for l in self.lines:
            split = l.split()
            if split[0] == 'mask':
                mask0 = int(split[2].replace('X', '0'),2)
                mask1 = int(split[2].replace('X', '1'),2)
            else:
                self.mem[split[0]] = (int(split[2]) & mask1) | mask0

        return sum([self.mem[v] for v in self.mem])

    def solve2(self):
        for l in self.lines:
            split = l.split()
            if split[0] == 'mask':
                mask = split[2]
                mask0 = int(mask.replace('X', '0'),2)
                count = len([c for c in split[2] if c == 'X'])
                idxs = [k for (k,c) in enumerate(split[2]) if c == 'X']
            else:
                addr = int(split[0].split('[')[1][:-1])
                #print(count, addr, mask)
                for kk in range(2**count):
                    nn = kk
                    for p in range(count):
                        v = nn % 2
                        if v:
                            addr |= 1 << (35-idxs[-p])
                        else:
                            addr &= ~(1 << (35-idxs[-p]))
                        nn //= 2
                    #print('   ', addr)

                    self.mem[addr | mask0] = int(split[2])

        return sum([self.mem[v] for v in self.mem])

if __name__ == "__main__":
    #t = Day(SAMPLE)
    #print(t.solve1())
    t = Day(SAMPLE2)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())
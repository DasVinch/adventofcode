import os
import math
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    '939',
    '7,13,x,x,59,x,31,19',
]

REAL = get_input(DAYDAY, 2020)


class Day:
    def __init__(self, lines) -> None:
        self.arrive = int(lines[0])
        busses = [(k, int(t)) for k, t in enumerate(lines[1].split(',')) if t != 'x']
        self.busses = [b[1] for b in busses]
        self.modulos = [b[1]-b[0] for b in busses]

    def solve1(self):
        nextpass = [b*(self.arrive // b) + b for b in self.busses]

        bn = list(zip(self.busses, nextpass))
        bn.sort(key= lambda x: x[1])
        return bn[0][0]* (bn[0][1] - self.arrive)

    def solve2(self):
        lcmall = 1
        for b in self.busses: # Actually they're all prime.
            lcmall = (b * lcmall) // math.gcd(b, lcmall)
        print('lcm ', lcmall)
        coproducts = [lcmall // b for b in self.busses]

        es = []
        for b, c in zip(self.busses, coproducts):
            es += [c * self.findinversebrutal(c, b)]

        tot = 0
        for e, m in zip(es, self.modulos):
            tot = (tot + e*m) % lcmall

        return tot

    def findinversebrutal(self, k, n):
        for p in range(1, n):
            if (k * p) % n == 1:
                return p


if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())
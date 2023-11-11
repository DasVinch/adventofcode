import os
from tools import get_input
from collections import deque

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = '1 2 -3 3 -2 0 4'.split()

REAL = get_input(DAYDAY, 2022)

class int_p:
    def __init__(self, n: int) -> None:
        self.n = n
        

class Day:
    def __init__(self, lines) -> None:
        self.orig = [int_p(int(nn)) for nn in lines]
        for p in self.orig:
            if p.n == 0:
                self.zero = p
                break
        self.deq = deque(self.orig.copy())
        self.l = len(self.orig)

    def solve1(self):
        for val in self.orig:
            idx = self.deq.index(val)
            self.deq.rotate(-idx % self.l)
            #assert self.deq[0] == val
            self.deq.popleft()
            self.deq.insert(val.n % (self.l-1), val)

        i0 = self.deq.index(self.zero)
        self.deq.rotate(-i0)

        #assert self.deq[0] == 0


        return self.deq[1000 % self.l].n + self.deq[2000 % self.l].n + self.deq[3000 % self.l].n

    def solve2(self, n:int = 10):
        for p in self.orig:
            p.n *= 811589153
        self.deq = deque(self.orig.copy())

        for k in range(n-1):
            _ = self.solve1()
        return self.solve1()

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    print(t.solve2())
    r = Day(REAL)
    print(r.solve1())
    print(r.solve2())
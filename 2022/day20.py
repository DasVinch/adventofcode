import os
from tools import get_input
from collections import deque

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = '1 2 -3 3 -2 0 4'.split()

REAL = get_input(DAYDAY, 2022)


class Day:
    def __init__(self, lines) -> None:
        self.orig = [int(nn) for nn in lines]
        self.deq = deque(self.orig.copy())
        self.l = len(self.orig)

    def solve1(self):
        for val in self.orig:
            idx = self.deq.index(val)
            self.deq.rotate(-idx % self.l)
            #assert self.deq[0] == val
            self.deq.popleft()
            self.deq.insert(val % (self.l-1), val)

        i0 = self.deq.index(0)
        self.deq.rotate(-i0)

        #assert self.deq[0] == 0


        return self.deq[1000 % self.l] + self.deq[2000 % self.l] + self.deq[3000 % self.l]

    def solve2(self, n:int = 10):
        self.orig = [k * 811589153 for k in self.orig]
        self.deq = deque(self.orig.copy())

        for k in range(n-1):
            _ = self.solve1()
        return self.solve1()

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())
import os
from tools import get_input
import numpy as np

import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
    'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
    'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
    'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
    'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
    'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
    'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
    'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
    'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
    'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
    'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
    'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
    'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
    'Sensor at x=20, y=1: closest beacon is at x=15, y=3',
]

REAL = get_input(DAYDAY, 2022)


class Day:

    def __init__(self, lines) -> None:
        self.n = len(lines)
        self.coords = np.zeros((self.n, 4), np.int64)

        for k, l in enumerate(lines):
            self.coords[k] = [int(s) for s in re.findall('-?\d+', l)]

        self.manh = np.abs(self.coords[:, 0] -
                           self.coords[:, 2]) + np.abs(self.coords[:, 1] -
                                                       self.coords[:, 3])

        self.uniquebeacons = np.unique(self.coords[:, 2:], axis=0)

    def solve1(self, whatline: int = 10, fortwo: bool = False):
        minmaxbounds = []

        for nn in range(self.n):
            delta = self.manh[nn] - abs(whatline - self.coords[nn][1])
            if delta >= 0:
                minmaxbounds.append(
                    (self.coords[nn][0] - delta,
                     self.coords[nn][0] + delta))  # [xs + delta, whatline]

        minmaxbounds.sort(key=lambda x: x[0])
        #print(minmaxbounds)

        OKintervals = []
        m, mm = minmaxbounds.pop(0)
        while len(minmaxbounds) > 0:
            #print('loopin')
            #print(m, mm, minmaxbounds)
            m1, mm1 = minmaxbounds.pop(0)
            if mm < m1:
                OKintervals += [(m, mm)]
                m, mm = m1, mm1
            else:
                mm = max(mm, mm1)
        OKintervals += [(m, mm)]

        #print(OKintervals)

        if fortwo:
            return OKintervals
            # No need to subtract existing beacons

        total = 0
        for itvl in OKintervals:
            total += itvl[1] - itvl[0] + 1
            x = np.sum((self.uniquebeacons[:, 1] == whatline)
                       & (self.uniquebeacons[:, 0] >= itvl[0])
                       & (self.uniquebeacons[:, 0] <= itvl[1]))
            #print(x)
            total -= x

        return total

    def solve2(self, size=20):
        from tqdm import trange
        for kk in trange(0, size+1):
            itvls = self.solve1(kk, True)
            m = itvls[0][0]
            mm = itvls[-1][1]
            if m > 0:
                print(f"Found on L edge at {kk}")
                return kk
            if mm < size:
                print(f"Found on R edge at {kk}")
                return size*4000000 + kk
            if len(itvls) > 1:
                for ll in range(len(itvls)-1):
                    if itvls[ll][1] < itvls[ll+1][0] - 1:
                        print(f"Found center at {kk} {itvls[ll][1]+1}")
                        return (itvls[ll][1]+1)*4000000 + kk





if __name__ == "__main__":
    t = Day(SAMPLE)
    print("t1, 10", t.solve1())
    print("t1, 11", t.solve1(11))
    print("t2, 20", t.solve2(20))
    r = Day(REAL)
    print("r1, 2000000", r.solve1(2000000))
    print("r2, 4000000", r.solve2(4000000))
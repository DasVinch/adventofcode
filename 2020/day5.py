import numpy as np
import os
from tools import get_input, make_cmapped_int_matrix

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

mapping = {'F': 0, 'B': 1, 'R':1, 'L':0}
SAMPLE = make_cmapped_int_matrix([
    'BFFFBBFRRR',
    'FFFBBBFRRR',
    'BBFFBBFRLL',
], mapping)

REAL = make_cmapped_int_matrix(get_input(DAYDAY, 2020), mapping)


class Day:
    def __init__(self, mat) -> None:
        self.mat = mat

    def solve1(self):
        self.v = self.mat[:, 0] * 0
        for k in range(self.mat.shape[1]):
            self.v *= 2
            self.v += self.mat[:, k]

        return np.max(self.v)

    def solve2(self):
        self.v.sort()
        for k in range(self.v[0], self.v[-1]+1):
            if self.v[k-self.v[0]] != k:
                return k

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    r = Day(REAL)
    print(r.solve1())
    print(r.solve2())
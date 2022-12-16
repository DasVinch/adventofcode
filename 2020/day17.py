import os
import numpy as np
from tools import get_input, make_cmapped_int_matrix
from tqdm import trange

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

CMAP = {'#': 1, '.': 0}
SAMPLE = make_cmapped_int_matrix([
    '.#.',
    '..#',
    '###',
], CMAP)

REAL = make_cmapped_int_matrix(get_input(DAYDAY, 2020), CMAP)


class Day:

    def __init__(self, mat) -> None:
        self.mat = mat
        self.m = self.mat.shape[0]

        self.outmat = np.zeros((15, self.m + 14, self.m + 14), np.int32)
        self.bigm, self.bign, _ = self.outmat.shape

        self.outmat[7,7:-7,7:-7] = self.mat

        self.outmat4 = np.zeros((15, 15, self.m + 14, self.m + 14), np.int32)
        self.outmat4[7, 7,7:-7,7:-7] = self.mat

    def step(self):
        self.newmat = self.outmat.copy()
        for ii in range(1, self.bigm - 1):
            for jj in range(1, self.bign - 1):
                for kk in range(1, self.bign - 1):
                    howmany = np.sum(self.outmat[ii - 1:ii + 2, jj - 1:jj + 2,
                                                 kk - 1:kk + 2])
                    if self.outmat[ii,jj,kk] == 1 and howmany not in (3,4):
                            self.newmat[ii,jj,kk] = 0
                    elif self.outmat[ii,jj,kk] == 0 and howmany == 3:
                        self.newmat[ii,jj,kk] = 1

        self.outmat = self.newmat

    def step4(self):
        self.newmat4 = self.outmat4.copy()
        for ii in range(1, self.bigm - 1):
            for jj in range(1, self.bigm - 1):
                for kk in range(1, self.bign - 1):
                    for ll in range(1, self.bign - 1):
                        howmany = np.sum(self.outmat4[ii - 1:ii + 2, jj - 1:jj + 2,
                                                    kk - 1:kk + 2, ll-1:ll+2])
                        if self.outmat4[ii,jj,kk,ll] == 1 and howmany not in (3,4):
                                self.newmat4[ii,jj,kk,ll] = 0
                        elif self.outmat4[ii,jj,kk,ll] == 0 and howmany == 3:
                            self.newmat4[ii,jj,kk,ll] = 1

        self.outmat4 = self.newmat4

    def solve1(self):
        for _ in trange(6):
            self.step()

        return np.sum(self.outmat)

    def solve2(self):
        for _ in trange(6):
            self.step4()

        return np.sum(self.outmat4)


if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    print(t.solve2())
    r = Day(REAL)
    print(r.solve1())
    print(r.solve2())
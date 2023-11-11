import os
from tools import get_input, make_cmapped_int_matrix
import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

MAPPING = {'.': 0, 'L': 1, '#': 2}
SAMPLE = make_cmapped_int_matrix([
    'L.LL.LL.LL',
    'LLLLLLL.LL',
    'L.L.L..L..',
    'LLLL.LL.LL',
    'L.LL.LL.LL',
    'L.LLLLL.LL',
    '..L.L.....',
    'LLLLLLLLLL',
    'L.LLLLLL.L',
    'L.LLLLL.LL',
], MAPPING)

REAL = make_cmapped_int_matrix(get_input(DAYDAY, 2020), MAPPING)


class Day:

    def __init__(self, mat) -> None:
        # pad by one
        self.mat = np.c_[-np.ones((mat.shape[0] + 2, 1)),
                         np.r_[-np.ones((1, mat.shape[1])), mat,
                               -np.ones((1, mat.shape[1]))],
                         -np.ones((mat.shape[0] + 2, 1))].astype(np.int32)
        self.rows, self.cols = self.mat.shape

    def solve1(self):
        k = 0
        while True:
            if k >= 1000:
                break
            newmat = self.mat.copy()
            for rr in range(1, self.rows-1):
                for cc in range(1, self.cols-1):
                    if self.mat[rr,cc] == 1:
                        if np.sum(self.mat[rr-1:rr+2, cc-1:cc+2] == 2) == 0:
                            newmat[rr,cc] = 2

                    elif self.mat[rr,cc] == 2:
                        if np.sum(self.mat[rr-1:rr+2, cc-1:cc+2] == 2) >= 5:
                            newmat[rr,cc] = 1
            k += 1
            if np.all(newmat == self.mat):
                return np.sum(newmat == 2)

            self.mat = newmat

    def findneighbors(self):
        self.neighbors = {}
        for rr in range(1, self.rows-1):
            for cc in range(1, self.cols-1):
                nborr = []
                nborc = []
                k = 1
                while self.mat[rr-k, cc] == 0:
                    k += 1
                if self.mat[rr-k, cc] > 0:
                    nborr += [rr-k]
                    nborc += [cc]
                k = 1
                while self.mat[rr+k, cc] == 0:
                    k += 1
                if self.mat[rr+k, cc] > 0:
                    nborr += [rr+k]
                    nborc += [cc]
                k = 1
                while self.mat[rr, cc-k] == 0:
                    k += 1
                if self.mat[rr, cc-k] > 0:
                    nborr += [rr]
                    nborc += [cc-k]
                k = 1
                while self.mat[rr, cc+k] == 0:
                    k += 1
                if self.mat[rr, cc+k] > 0:
                    nborr += [rr]
                    nborc += [cc+k]
                k = 1

                while self.mat[rr+k, cc+k] == 0:
                    k += 1
                if self.mat[rr+k, cc+k] > 0:
                    nborr += [rr+k]
                    nborc += [cc+k]
                k = 1
                while self.mat[rr-k, cc-k] == 0:
                    k += 1
                if self.mat[rr-k, cc-k] > 0:
                    nborr += [rr-k]
                    nborc += [cc-k]
                k = 1
                while self.mat[rr-k, cc+k] == 0:
                    k += 1
                if self.mat[rr-k, cc+k] > 0:
                    nborr += [rr-k]
                    nborc += [cc+k]
                k = 1
                while self.mat[rr+k, cc-k] == 0:
                    k += 1
                if self.mat[rr+k, cc-k] > 0:
                    nborr += [rr+k]
                    nborc += [cc-k]
                self.neighbors[(rr,cc)] = (np.array(nborr, np.int32), np.array(nborc, np.int32))

    def solve2(self):
        self.findneighbors()
        k = 0
        while True:
            if k >= 1000:
                break
            newmat = self.mat.copy()
            for rr in range(1, self.rows-1):
                for cc in range(1, self.cols-1):
                    if self.mat[rr,cc] == 1:
                        if np.sum(self.mat[self.neighbors[(rr,cc)]] == 2) == 0:
                            newmat[rr,cc] = 2

                    elif self.mat[rr,cc] == 2:
                        if np.sum(self.mat[self.neighbors[(rr,cc)]] == 2) >= 5:
                            newmat[rr,cc] = 1
            k += 1
            if np.all(newmat == self.mat):
                return np.sum(newmat == 2)

            self.mat = newmat


if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())
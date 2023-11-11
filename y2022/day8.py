from tools import get_input, make_int_matrix
import numpy as np

SMOL = make_int_matrix([
    '12',
    '34',
])

SAMPLE = make_int_matrix([
    '30373',
    '25512',
    '65332',
    '33549',
    '35390',
])

REAL = make_int_matrix(get_input(8, 2022))

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

class Day8:

    def __init__(self, mat) -> None:
        self.mat = mat
        self.nrows, self.ncols = self.mat.shape

        self.vis = np.empty((self.nrows, self.ncols), dtype='<U4')
        self.vis[:,:] = ''

    def solve1(self):
        for rr in range(self.nrows):
            maxfromleft = -1
            maxfromright = -1
            for cc in range(self.ncols):
                if self.mat[rr, cc] > maxfromleft:
                    self.vis[rr, cc] += LEFT
                    maxfromleft = self.mat[rr, cc]
                else:
                    self.vis[rr, cc] += ' '

                if self.mat[rr, -cc-1] > maxfromright:
                    self.vis[rr, -cc-1] += RIGHT
                    maxfromright = self.mat[rr, -cc-1]
                else:
                    self.vis[rr, -cc-1] += ' '

        for cc in range(self.ncols):
            maxfromup = -1
            maxfromdown = -1
            for rr in range(self.nrows):
                if self.mat[rr, cc] > maxfromup:
                    self.vis[rr, cc] += UP
                    maxfromup = self.mat[rr, cc]
                else:
                    self.vis[rr, cc] += ' '

                if self.mat[-rr-1, cc] > maxfromdown:
                    self.vis[-rr-1, cc] += DOWN
                    maxfromdown = self.mat[-rr-1, cc]
                else:
                    self.vis[-rr-1, cc] += ' '

        return np.sum(self.vis != '    ')

    def solve2(self):
        self.lview = np.zeros_like(self.mat)
        self.rview = np.zeros_like(self.mat)
        self.uview = np.zeros_like(self.mat)
        self.dview = np.zeros_like(self.mat)

        for rr in range(self.nrows):
            lindex = np.zeros(10)
            rindex = np.zeros(10)
            for cc in range(self.ncols):
                self.lview[rr, cc] = lindex[self.mat[rr, cc]]
                self.rview[rr, -cc-1] = rindex[self.mat[rr, -cc-1]]

                lindex[:self.mat[rr, cc]+1] = 0
                rindex[:self.mat[rr, -cc-1]+1] = 0

                lindex += 1
                rindex += 1

        for cc in range(self.ncols):
            uindex = np.zeros(10)
            dindex = np.zeros(10)
            for rr in range(self.nrows):
                self.uview[rr, cc] = uindex[self.mat[rr, cc]]
                self.dview[-rr-1, cc] = dindex[self.mat[-rr-1, cc]]

                uindex[:self.mat[rr, cc]+1] = 0
                dindex[:self.mat[-rr-1, cc]+1] = 0

                uindex += 1
                dindex += 1

        return np.max(self.lview * self.rview * self.uview * self.dview)

if __name__ == "__main__":
    sm = Day8(SMOL)
    print(sm.solve2())
    #print(sm.mat)
    #print(sm.vis)
    test = Day8(SAMPLE)
    print(test.solve2())
    #print(test.mat)
    #print(test.vis)
    r = Day8(REAL)
    print(r.solve2())
from tools import get_input, make_cmapped_int_matrix
import numpy as np

class T:
    EAST = 1
    SOUTH = 2
    EMPTY = 0
CMAP = {'.': T.EMPTY, '>': T.EAST, 'v': T.SOUTH}
SAMPLE = make_cmapped_int_matrix([
    'v...>>.vv>',
    '.vv>>.vv..',
    '>>.>v>...v',
    '>>v>>.>.v.',
    'v>v.vv.v..',
    '>.>>..v...',
    '.vv..>.>v.',
    'v.v..>>v.v',
    '....v..v.>',
], CMAP)

REAL = make_cmapped_int_matrix(get_input(25, 2021), CMAP)


class Day25:
    def __init__(self, mat) -> None:
        self.mat = mat

        self.canmove = np.zeros_like(mat, np.bool)

    def step(self):
        self.canmove[:, :-1] = (self.mat[:, :-1] == T.EAST) & (self.mat[:, 1:] == T.EMPTY)
        self.canmove[:, -1] = (self.mat[:, -1] == T.EAST) & (self.mat[:, 0] == T.EMPTY)

        emove = np.sum(self.canmove)

        self.mat[self.canmove] = T.EMPTY
        self.mat[:, 1:][self.canmove[:, :-1]] = T.EAST
        self.mat[:, 0][self.canmove[:, -1]] = T.EAST

        self.canmove[:-1, :] = (self.mat[:-1, :] == T.SOUTH) & (self.mat[1:, :] == T.EMPTY)
        self.canmove[-1, :] = (self.mat[-1, :] == T.SOUTH) & (self.mat[0, :] == T.EMPTY)

        smove = np.sum(self.canmove)

        self.mat[self.canmove] = T.EMPTY
        self.mat[1:, :][self.canmove[:-1, :]] = T.SOUTH
        self.mat[0, :][self.canmove[-1, :]] = T.SOUTH

        return emove, smove

    def solve1(self):
        e, s = 1, 1
        k = 0
        while e + s > 0:
            e, s = self.step()
            k += 1
        return k

    def print_state(self):
        for row in self.mat:
            for c in row:
                if c == T.EAST:
                    print('>', end='')
                elif c == T.SOUTH:
                    print('v', end='')
                else:
                    print('.', end='')
            print()

if __name__ == "__main__":
    t = Day25(SAMPLE)
    r = Day25(REAL)
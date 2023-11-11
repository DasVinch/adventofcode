import os
from tools import get_input, make_charint_matrix, AbstractDijkstraer
import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = make_charint_matrix([
    'Sabqponm',
    'abcryxxl',
    'accszExk',
    'acctuvwj',
    'abdefghi',
])


REAL = make_charint_matrix(get_input(DAYDAY, 2022))

class Djk(AbstractDijkstraer):
    def __init__(self, mat) -> None:
        self.mat = mat.copy()

        a, b = np.where(mat == ord('S'))
        start = (a[0], b[0])
        self.mat[a, b] = 255
        a, b = np.where(mat == ord('E'))
        end = (a[0], b[0])
        self.mat[a, b] = ord('z')

        super().__init__(start, [end])

    def get_neighbors(self, elem):
        x, y = elem
        neis = []

        if x > 0 and self.mat[x-1, y] <= self.mat[x, y] + 1:
            neis += [((x-1, y),1)]
        if y > 0 and self.mat[x, y-1] <= self.mat[x, y] + 1:
            neis += [((x, y-1),1)]
        if x < self.mat.shape[0]-1 and self.mat[x+1, y] <= self.mat[x, y] + 1:
            neis += [((x+1, y),1)]
        if y < self.mat.shape[1]-1 and self.mat[x, y+1] <= self.mat[x, y] + 1:
            neis += [((x, y+1),1)]

        return neis

# We go backwars and invert the neighboring rules
class Djk2(AbstractDijkstraer):
    def __init__(self, mat) -> None:
        self.mat = mat.copy()

        a, b = np.where(self.mat == ord('S'))
        self.mat[a, b] = ord('a')

        a, b = np.where(self.mat == ord('E'))
        start = (a[0], b[0])
        self.mat[a, b] = ord('z')

        aa, bb = np.where(self.mat == ord('a'))
        endl = []
        for a, b in zip(aa, bb):
            endl += [(a,b)]


        super().__init__(start, endl)

    def get_neighbors(self, elem):
        x, y = elem
        neis = []

        if x > 0 and self.mat[x-1, y] >= self.mat[x, y] - 1:
            neis += [((x-1, y),1)]
        if y > 0 and self.mat[x, y-1] >= self.mat[x, y] - 1:
            neis += [((x, y-1),1)]
        if x < self.mat.shape[0]-1 and self.mat[x+1, y] >= self.mat[x, y] - 1:
            neis += [((x+1, y),1)]
        if y < self.mat.shape[1]-1 and self.mat[x, y+1] >= self.mat[x, y] - 1:
            neis += [((x, y+1),1)]

        return neis

if __name__ == "__main__":
    t = Djk(SAMPLE)
    t.solveWithoutPath()
    print(t.distanceDict[t.targets[0]])
    r = Djk(REAL)
    r.solveWithoutPath()
    print(r.distanceDict[r.targets[0]])
    t = Djk2(SAMPLE)
    t.solveWithoutPath()
    print(min([t.distanceDict[ttar] for ttar in t.targets if ttar in t.distanceDict]))
    r = Djk2(REAL)
    r.solveWithoutPath()
    print(min([r.distanceDict[rtar] for rtar in r.targets if rtar in r.distanceDict]))
    #print(r.distanceDict[r.targets[0]])
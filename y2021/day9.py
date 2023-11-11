from tools import get_input
import numpy as np

SAMPLE = [
    '2199943210',
    '3987894921',
    '9856789892',
    '8767896789',
    '9899965678',
]

import scipy.ndimage as ndi


class Day9:

    def __init__(self, lines) -> None:
        split = [[int(t) for t in s] for s in lines]

        self.mat = np.asarray(split, np.int32)
        self.matpad = np.r_[np.c_[self.mat, 9 + np.zeros(
            (self.mat.shape[0], 1), np.int32)], 9 + np.zeros(
                (1, self.mat.shape[1] + 1), np.int32)]

    def solve1(self) -> int:
        totrisk = 0
        self.whmin = []
        for ii in range(self.matpad.shape[0]):
            for jj in range(self.matpad.shape[1]):
                if ((self.matpad[ii, jj] < self.matpad[ii - 1, jj])
                        and (self.matpad[ii, jj] < self.matpad[ii + 1, jj])
                        and (self.matpad[ii, jj] < self.matpad[ii, jj - 1])
                        and (self.matpad[ii, jj] < self.matpad[ii, jj + 1])):
                    self.whmin += [(ii, jj)]
                    totrisk += self.matpad[ii, jj] + 1

        return totrisk

    def solve2(self) -> int:
        self.basins = [Basin(whm, self.matpad) for whm in self.whmin]
        for b in self.basins:
            b.process()

        self.basins.sort(key=lambda b: b.size, reverse=True)

        return self.basins[0].size * self.basins[1].size * self.basins[2].size


class Basin:

    def __init__(self, init_point, data):
        self.data = data
        self.init = init_point
        self.border = [init_point]
        self.contents = [init_point]
        self.size = 1

    def process(self):
        self.border.sort(key=lambda t: self.data[t[0], t[1]])
        while len(self.border) > 0:
            x, y = self.border.pop()
            for b in [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]:
                if not b in self.contents and self.data[
                        b[0], b[1]] > self.data[x, y] and self.data[b[0],
                                                                    b[1]] < 9:
                    self.contents.append(b)
                    self.size += 1
                    self.border.append(b)


if __name__ == "__main__":
    test = Day9(SAMPLE)
    test.solve1()
    print(test.solve2())
    real = Day9(get_input(9, 2021))
    real.solve1()
    print(real.solve2())
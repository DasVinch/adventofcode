import os
from tools import get_input, make_int_matrix, AbstractDijkstraer

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    '2,2,2',
    '1,2,2',
    '3,2,2',
    '2,1,2',
    '2,3,2',
    '2,2,1',
    '2,2,3',
    '2,2,4',
    '2,2,6',
    '1,2,5',
    '3,2,5',
    '2,1,5',
    '2,3,5',
]

REAL = get_input(DAYDAY, 2022)


class Day:

    def __init__(self, lines) -> None:
        self.data = make_int_matrix(lines, ',')

        self.offsets = -np.min(self.data, axis=0)
        self.size = np.max(self.data, axis=0) + self.offsets + 3

        self.cube = np.zeros(self.size, np.bool)

        for pos in self.data:
            x, y, z = pos + self.offsets + 1
            self.cube[x, y, z] = True

    def solve1(self):
        tot_surf = 0
        for i in range(1, self.cube.shape[0]):
            tot_surf += np.sum(self.cube[i - 1, :, :] ^ self.cube[i, :, :])
        for j in range(1, self.cube.shape[1]):
            tot_surf += np.sum(self.cube[:, j - 1, :] ^ self.cube[:, j, :])
        for k in range(1, self.cube.shape[2]):
            tot_surf += np.sum(self.cube[:, :, k - 1] ^ self.cube[:, :, k])

        return tot_surf

    def solve2(self):
        tot_surf = 0
        xm, ym, zm = self.cube.shape

        pending = [(0, 0, 0)]
        done = set()

        while len(pending) > 0:
            this = pending.pop()
            if this in done:
                continue
            done.add(this)

            for k in range(3):
                for off in [-1, 1]:
                    new = list(this)
                    new[k] += off
                    newt = tuple(new)

                    if (newt[0] < 0 or newt[1] < 0 or newt[2] < 0
                            or newt[0] >= xm or newt[1] >= ym
                            or newt[2] >= zm):
                        continue

                    if self.cube[new[0], new[1], new[2]]:
                        tot_surf += 1
                    elif newt not in done:
                        pending.append(newt)

        return tot_surf


if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    print(t.solve2())
    r = Day(REAL)
    print(r.solve1())
    print(r.solve2())
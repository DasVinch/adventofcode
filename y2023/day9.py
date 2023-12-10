from __future__ import annotations

import os
from tools import get_input
import typing as typ
import numpy as np
from scipy.interpolate import lagrange

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    '0 3 6 9 12 15',
    '1 3 6 10 15 21',
    '10 13 16 21 30 45',
]


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug
        self.values = [[int(t) for t in line.split()] for line in lines]

    def solve1(self) -> int:
        tot = 0
        for serie in self.values:
            n = len(serie)
            diffs = [np.asarray(serie, np.int64)]
            while not np.all(diffs[-1] == 0):
                diffs += [diffs[-1][1:] - diffs[-1][:-1]]
            last_at = 0
            for d in diffs[-1::-1]:
                last_at = d[-1] + last_at
            v = last_at
            if self.debug:
                print(v)
            tot += v

        return tot

    def reverse(self):
        self.values = [v[::-1] for v in self.values]

    def solve2(self) -> int:
        self.reverse()

        t = self.solve1()

        self.reverse()
        return t


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

from __future__ import annotations

import os
from tools import get_input

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2024)

SAMPLE = [
'3   4',
'4   3',
'2   5',
'1   3',
'3   9',
'3   3',
]


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.data = np.asarray([[int(k) for k in l.split()] for l in lines])


    def solve1(self) -> int:
        self.k0 = self.data[:, 0].copy()
        self.k0.sort()
        self.k1 = self.data[:, 1].copy()
        self.k1.sort()

        return sum(np.abs(self.k0 - self.k1))
        

    def solve2(self) -> int:
        self.solve1()
        from collections import Counter
        counts = Counter(self.k1)

        tot = 0
        for t in self.k0:
            tot += t * counts[t]

        return tot


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

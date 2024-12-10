from __future__ import annotations

import os
import tools
from tools import get_input

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2024)

SAMPLE = [
    '7 6 4 2 1',
    '1 2 7 8 9',
    '9 7 6 2 1',
    '1 3 2 4 5',
    '8 6 4 4 1',
    '1 3 6 7 9',
]


class Day:

    def __init__(self, mat: list[str], debug: bool = False) -> None:
        self.data = [[int(t) for t in line.split()] for line in mat]
        
        self.debug = debug

    def solve1(self) -> int:

        val = 0
        for dat in self.data:
            val += self.safe_list(dat)

        return val
        
    def safe_list(self, l: list[int]) -> bool:
        ll = np.asarray(l, np.int32)
        lll = ll[1:] - ll[:-1]
        return all((k>=1 and k <= 3) for k in lll) or all((k<=-1 and k >= -3) for k in lll)

    def solve2(self) -> int:
        val = 0
        for dat in self.data:
            if self.safe_list(dat):
                #if self.debug:
                #    print(dat, 'safe')
                val += 1
                continue
            for k in range(len(dat)):
                if self.safe_list(dat[:k] + dat[k+1:]):
                    if self.debug:
                        print(k, dat, dat[:k] + dat[k+1:], 'safe')
                    val += 1
                    break

        return val


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL, False)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

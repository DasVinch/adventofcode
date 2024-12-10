from __future__ import annotations
import typing as typ
from typing import Set

from tools import get_input
import tools


import numpy as np

import os
from enum import IntEnum

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    '...........',
    '.....###.#.',
    '.###.##..#.',
    '..#.#...#..',
    '....#.#....',
    '.##..S####.',
    '.##..#...#.',
    '.......##..',
    '.##.#.####.',
    '.##..##.##.',
    '...........',
]

CHARMAP = {
    '.': 0,
    '#': 1,
    'S': 2
}
import re

TT: typ.TypeAlias = tuple[int, int]

class Djk(tools.AbstractDijkstraer[TT]):
    def __init__(self, matrix: np.ndarray, start: TT, targets: set[TT]) -> None:
        super().__init__(start, targets)
        self.matrix = matrix
        self.xm, self.ym = matrix.shape


    def get_neighbors(self, elem: TT) -> set[tuple[TT, int]]:
        
        nset: set[TT] = set()

        x,y = elem
        if x > 0 and self.matrix[x-1][y] == 0:
            nset.add((x-1, y))
        if x < self.xm-1 and self.matrix[x+1][y] == 0:
            nset.add((x+1, y))
        if y > 0 and self.matrix[x][y-1] == 0:
            nset.add((x, y-1))
        if y < self.ym - 1 and self.matrix[x][y+1] == 0:
            nset.add((x, y+1))

        return {(n,1) for n in nset}


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.dat = tools.make_cmapped_int_matrix(lines, CHARMAP)

        whs = np.where(self.dat == CHARMAP['S'])
        self.start = whs[0][0], whs[1][0]

        self.debug = debug

    def solve1(self, nmax: int = 64) -> int:

        self.p1djk = Djk(self.dat, self.start, set())
        self.p1djk.solveWithoutPath()

        if self.debug:
            self.mat_after = self.dat.copy()
            for (a,b), (dist,_) in self.p1djk.distanceDict.items():
                if dist <= nmax and ((dist % 2) == (nmax % 2)):
                    self.mat_after[a,b] = 3 


        return len([dist for (n,(dist,_)) in self.p1djk.distanceDict.items() if (dist <= nmax and dist % 2 == 0)])
    
    def solve2(self, nmax: int = 26_501_365):
        self.solve1(nmax = 256)
        full_tile_even = len([dist for (n,(dist,_)) in self.p1djk.distanceDict.items() if dist % 2 == 0])
        full_tile_odd = len([dist for (n,(dist,_)) in self.p1djk.distanceDict.items() if dist % 2 == 1])



        # 4 tiles to get in from the middle of a side (and watch parity)
        # 4 * N tiles to get in from a corner (and watch parity)
        # N**2 tiles completed (watch parity!)


        return 0



if __name__ == "__main__":

    t = Day(SAMPLE, True)

    print(f'Test p1: {t.solve1(6)}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

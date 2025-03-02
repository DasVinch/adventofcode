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

CHARMAP = {'.': 0, '#': 1, 'S': 2}
import re

TT: typ.TypeAlias = tuple[int, int]


class Djk(tools.AbstractDijkstraer[TT]):

    def __init__(self, matrix: np.ndarray, start: TT,
                 targets: set[TT]) -> None:
        super().__init__(start, targets)
        self.matrix = matrix
        self.xm, self.ym = matrix.shape

    def get_neighbors(self, elem: TT) -> set[tuple[TT, int]]:

        nset: set[TT] = set()

        x, y = elem
        if x > 0 and self.matrix[x - 1][y] == 0:
            nset.add((x - 1, y))
        if x < self.xm - 1 and self.matrix[x + 1][y] == 0:
            nset.add((x + 1, y))
        if y > 0 and self.matrix[x][y - 1] == 0:
            nset.add((x, y - 1))
        if y < self.ym - 1 and self.matrix[x][y + 1] == 0:
            nset.add((x, y + 1))

        return {(n, 1) for n in nset}


class DjkPeriodic(tools.AbstractDijkstraer[TT]):

    def __init__(self, matrix: np.ndarray, start: TT, targets: set[TT],
                 max_depth) -> None:
        super().__init__(start, targets, max_depth=max_depth)
        self.matrix = matrix
        self.xm, self.ym = matrix.shape

    def get_neighbors(self, elem: TT) -> set[tuple[TT, int]]:

        nset: set[TT] = set()

        x, y = elem
        xm, ym = self.xm, self.ym

        if self.matrix[(x - 1) % xm][y % ym] % 2 == 0:
            nset.add(((x - 1), y))
        if self.matrix[(x + 1) % xm][y % ym] % 2 == 0:
            nset.add(((x + 1), y))
        if self.matrix[x % xm][(y - 1) % ym] % 2 == 0:
            nset.add((x, (y - 1)))
        if self.matrix[x % xm][(y + 1) % ym] % 2 == 0:
            nset.add((x, (y + 1)))

        return {(n, 1) for n in nset}


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
            for (a, b), (dist, _) in self.p1djk.distanceDict.items():
                if dist <= nmax and ((dist % 2) == (nmax % 2)):
                    self.mat_after[a, b] = 3

        return len([
            dist for (n, (dist, _)) in self.p1djk.distanceDict.items()
            if (dist <= nmax and dist % 2 == 0)
        ])

    def solve1_periodic(self, nmax: int = 64) -> int:

        self.p1djk = DjkPeriodic(self.dat, self.start, set(), nmax + 1)
        self.p1djk.solveWithoutPath()

        if self.debug:
            self.mat_after = self.dat.copy()
            for (a, b), (dist, _) in self.p1djk.distanceDict.items():
                if dist <= nmax and ((dist % 2) == (nmax % 2)):
                    self.mat_after[a, b] = 3

        return len([
            dist for (n, (dist, _)) in self.p1djk.distanceDict.items()
            if (dist <= nmax and dist % 2 == nmax % 2)
        ])

    def solve2(self, n_steps: int = 12345):
        

        size = self.dat.shape[0] + self.dat.shape[1]
        mod = n_steps % size
        iters = n_steps // size

        if iters < 4:
            return self.solve1_periodic(n_steps)

        x = []
        y = []
        for i in range(2):
            x += [i]
            y += [self.solve1_periodic(size * i + mod)]
            print(x[-1], y[-1])

        pprev = None
        while True:
            i += 1
            x += [i]
            y += [self.solve1_periodic(size * i + mod)]
            print(x[-1], y[-1])
            p = np.round(np.polyfit(x[-3:], y[-3:], 2)).astype(np.int64)
            
            if pprev is not None and np.all(p == pprev):
                print(p)
                break

            pprev = p

        return int(np.polyval(p, [iters])[0])


if __name__ == "__main__":

    t0 = Day(['...','.S.','...'], True)
    t0.solve1_periodic(1)

    t = Day(SAMPLE, True)

    print(f'Test p1: {t.solve1(6)}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    t.debug = False
    print(f'Test Pp1 (6): {t.solve1_periodic(6)}')
    print(f'Test Pp1 (10): {t.solve1_periodic(10)}')
    print(f'Test Pp1 (100): {t.solve1_periodic(100)}')
    
    # 621494507864558 IS WRONG
    # 621494544278648

    print(f'Test p2 (5000): {t.solve2(5000)}')
    print(f'Real p2: {r.solve2(26501365)}')

"""
..x..
.x.x.
x.x.x
.x.x.
..x..
"""
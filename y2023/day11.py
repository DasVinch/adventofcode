from __future__ import annotations

import os
import typing as typ
from tools import get_input
import tools

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

CMAP = {'.': 0, '#': 1}
REAL = tools.make_cmapped_int_matrix(get_input(DAYDAY, 2023), CMAP)

SAMPLE = tools.make_cmapped_int_matrix([
    '...#......',
    '.......#..',
    '#.........',
    '..........',
    '......#...',
    '.#........',
    '.........#',
    '..........',
    '.......#..',
    '#...#.....',
], CMAP)

import itertools


def cosmo_dist(a: int, b: int, skips: np.ndarray, expand: int = 2) -> int:
    if a == b:
        return 0
    if b < a:
        return cosmo_dist(b, a, skips, expand=expand)

    r = b - a + np.sum((skips > a) & (skips < b)) * (expand - 1)
    return r


class Day:

    def __init__(self, map: np.ndarray, debug: bool = False) -> None:
        self.debug = debug
        self.map = map

        self.prep()

    def prep(self):
        self.galaxies = set(zip(*np.where(self.map == 1)))
        self.nullrows = np.where(np.all(self.map == 0, axis=1))[0]
        self.nullcols = np.where(np.all(self.map == 0, axis=0))[0]

    def cosmological_manhattan(self,
                               g1: tuple[int, int],
                               g2: tuple[int, int],
                               expand=2) -> int:
        return cosmo_dist(g1[0], g2[0], self.nullrows, expand=expand) +\
               cosmo_dist(g1[1], g2[1], self.nullcols, expand=expand)

    def solve1(self) -> int:

        tot = 0

        for g1, g2 in itertools.combinations(self.galaxies, 2):
            v = self.cosmological_manhattan(g1, g2)
            tot += v

        return tot

    def solve2(self, expand: int = 1_000_000) -> int:
        tot = 0

        for g1, g2 in itertools.combinations(self.galaxies, 2):
            v = self.cosmological_manhattan(g1, g2, expand=expand)
            tot += v

        return tot


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2(expand=10)}')
    print(f'Test p2: {t.solve2(expand=100)}')
    print(f'Real p2: {r.solve2()}')

from __future__ import annotations

import os
from tools import get_input
import tools

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tools.make_char_matrix(get_input(DAYDAY, 2024))

SAMPLE = tools.make_char_matrix([
    '............',
    '........0...',
    '.....0......',
    '.......0....',
    '....0.......',
    '......A.....',
    '............',
    '............',
    '........A...',
    '.........A..',
    '............',
    '............',
])


class Day:

    def __init__(self, mat: np.ndarray, debug: bool = False) -> None:
        self.debug = debug

        self.mat = mat
        self.m, self.n = self.mat.shape

        self.keys = list(np.unique(mat))
        self.keys.remove('.')

        self.keyaddr: dict[str, list[tuple[int,int]]] = {}

        for k in self.keys:
            x,y = np.where(self.mat == k)

            self.keyaddr[k] = list(zip(x,y))

    def solve1(self) -> int:

        self.anti1: set[tuple[int,int]] = set()

        import itertools

        for k in self.keys:
            for ant_a, ant_b in itertools.permutations(self.keyaddr[k], 2):
                x = 2 * ant_a[0] - ant_b[0]
                y = 2 * ant_a[1] - ant_b[1]
                if x >= 0 and y >= 0 and x < self.m and y < self.n:
                    self.anti1.add((x,y))

        return len(self.anti1)
        

    def solve2(self) -> int:

        self.anti2: set[tuple[int,int]] = set()

        import itertools

        for k in self.keys:
            for ant_a, ant_b in itertools.permutations(self.keyaddr[k], 2):
                
                idx = 0
                while True:
                    x = ant_b[0] + idx * (ant_a[0] - ant_b[0])
                    y = ant_b[1] + idx * (ant_a[1] - ant_b[1])
                    if x >= 0 and y >= 0 and x < self.m and y < self.n:
                        self.anti2.add((x,y))
                        idx += 1
                    else:
                        break

        return len(self.anti2)


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

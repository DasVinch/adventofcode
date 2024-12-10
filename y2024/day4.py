from __future__ import annotations

import os
import tools
from tools import get_input

import typing as typ
import numpy as np

import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tools.make_char_matrix(get_input(DAYDAY, 2024))

SAMPLE = tools.make_char_matrix([
    'MMMSXXMASM',
    'MSAMXMSMSA',
    'AMXSXMAAMM',
    'MSAMASMSMX',
    'XMASAMXAMM',
    'XXAMMXXAMA',
    'SMSMSASXSS',
    'SAXAMASAAA',
    'MAMMMXMMMM',
    'MXMXAXMASX',
])

class Day:

    def __init__(self, mat: np.ndarray, debug: bool = False) -> None:
        self.debug = debug
        self.mat = mat
        self.shape = mat.shape

    def solve1(self) -> int:
        m, n = self.shape
        count = 0
        M = self.mat
        for ii in range(m):
            for jj in range(n):
                if M[ii,jj] != 'X':
                    continue
                if ii + 3 < m:
                    if M[ii+1,jj] == 'M' and M[ii+2,jj] == 'A' and M[ii+3,jj] == 'S':
                        count += 1
                    if jj + 3 < n and M[ii+1,jj+1] == 'M' and M[ii+2,jj+2] == 'A' and M[ii+3,jj+3] == 'S':
                        count += 1
                    if jj >= 3 and M[ii+1,jj-1] == 'M' and M[ii+2,jj-2] == 'A' and M[ii+3,jj-3] == 'S':
                        count += 1

                if ii >= 3:
                    if M[ii-1,jj] == 'M' and M[ii-2,jj] == 'A' and M[ii-3,jj] == 'S':
                        count += 1
                    if jj + 3 < n and M[ii-1,jj+1] == 'M' and M[ii-2,jj+2] == 'A' and M[ii-3,jj+3] == 'S':
                        count += 1
                    if jj >= 3 and M[ii-1,jj-1] == 'M' and M[ii-2,jj-2] == 'A' and M[ii-3,jj-3] == 'S':
                        count += 1

                if jj + 3 < n and M[ii,jj+1] == 'M' and M[ii,jj+2] == 'A' and M[ii,jj+3] == 'S':
                    count += 1
                if jj >= 3 and M[ii,jj-1] == 'M' and M[ii,jj-2] == 'A' and M[ii,jj-3] == 'S':
                    count += 1

        return count
                


    def solve2(self) -> int:
        m, n = self.shape
        count = 0
        M = self.mat
        for ii in range(1, m-1):
            for jj in range(1, n-1):
                if M[ii,jj] != 'A':
                    continue
                l = [M[ii-1,jj-1], M[ii+1,jj-1], M[ii-1,jj+1], M[ii+1,jj+1]]
                if l.count('M') == 2 and l.count('S') == 2 and l[0] != l[-1]:
                    count += 1

        return count


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL, False)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

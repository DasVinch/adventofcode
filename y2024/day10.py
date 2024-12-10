from __future__ import annotations

import os
import tools

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tools.make_int_matrix(tools.get_input(DAYDAY, 2024))

SAMPLE = tools.make_int_matrix([
    '89010123',
    '78121874',
    '87430965',
    '96549874',
    '45678903',
    '32019012',
    '01329801',
    '10456732',
])

import numpy.typing as npt

import functools

class Day:

    def __init__(self, mat: npt.NDArray[np.int_], debug: bool = False) -> None:
        self.debug = debug
        self.mat = mat

    def solve1(self) -> int:
        zii, zjj = np.where(self.mat == 0)

        self.arch = {}

        tot_scores = 0
        for zi, zj in zip(zii, zjj):
            s = self.score_of_tile(zi, zj)
            if self.debug:
                self.arch[(zi,zj)] = s
            tot_scores += len(s)

        return tot_scores

    def solve2(self) -> int:
        zii, zjj = np.where(self.mat == 0)

        self.arch = {}

        tot_scores = 0
        for zi, zj in zip(zii, zjj):
            s = self.score_of_tile2(zi, zj)
            if self.debug:
                self.arch[(zi,zj)] = s
            tot_scores += s

        return tot_scores

    @functools.cache
    def score_of_tile(self, ii: int, jj: int) -> set[tuple[int, int]]:
        mat = self.mat
        m, n = mat.shape
        val = mat[ii,jj]

        s = set()

        if val == 9:
            return {(ii, jj)}
        
        if ii > 0 and mat[ii-1, jj] == val+1:
            s.update(self.score_of_tile(ii-1, jj))
        if jj > 0 and mat[ii, jj-1] == val+1:
            s.update(self.score_of_tile(ii, jj-1))
        if ii < m-1 and mat[ii+1, jj] == val+1:
            s.update(self.score_of_tile(ii+1, jj))
        if jj < n-1 and mat[ii, jj+1] == val+1:
            s.update(self.score_of_tile(ii, jj+1))

        return s

    @functools.cache
    def score_of_tile2(self, ii: int, jj: int) -> int:
        mat = self.mat
        m, n = mat.shape
        val = mat[ii,jj]


        if val == 9:
            return 1
        
        s = 0
        if ii > 0 and mat[ii-1, jj] == val+1:
            s += self.score_of_tile2(ii-1, jj)
        if jj > 0 and mat[ii, jj-1] == val+1:
            s += self.score_of_tile2(ii, jj-1)
        if ii < m-1 and mat[ii+1, jj] == val+1:
            s += self.score_of_tile2(ii+1, jj)
        if jj < n-1 and mat[ii, jj+1] == val+1:
            s += self.score_of_tile2(ii, jj+1)

        return s



if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

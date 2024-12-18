from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
    '5,4',
    '4,2',
    '4,5',
    '3,0',
    '2,1',
    '6,3',
    '2,4',
    '1,5',
    '0,6',
    '3,3',
    '2,6',
    '5,1',
    '1,2',
    '5,5',
    '2,5',
    '6,5',
    '1,4',
    '0,4',
    '6,4',
    '1,1',
    '6,1',
    '1,0',
    '0,5',
    '1,6',
    '2,0',
]

class Djk(tl.AbstractDijkstraer[tuple[int,int]]):
    def __init__(self, mat:np.ndarray, start: tuple[int, int], targets: typ.Set[tuple[int, int]]) -> None:
        super().__init__(start, targets)

        self.mat = mat
        

    def get_neighbors(self, elem: tuple[int, int]) -> set[tuple[tuple[int, int], int]]:
        m, n = self.mat.shape
        i, j = elem

        neighs: set[tuple[tuple[int,int], int]] = set()

        if i > 0 and self.mat[i-1,j] != '#':
            neighs.add(((i-1,j),1))

        if j > 0 and self.mat[i,j-1] != '#':
            neighs.add(((i,j-1),1))

        if i < m-1 and self.mat[i+1,j] != '#':
            neighs.add(((i+1,j),1))

        if j < n-1 and self.mat[i,j+1] != '#':
            neighs.add(((i,j+1),1))

        return neighs

class Day:

    def __init__(self, lines: list[str], shape:tuple[int,int], debug: bool = False) -> None:
        self.debug = debug

        self.m, self.n = shape

        self.px = []

        for l in lines:
            a,b = l.split(',')
            self.px += [(int(a), int(b))]



    def solve1(self, fall: int) -> int:
        
        self.mat1 = np.zeros((self.m,self.n), dtype='<U1')
        self.mat1[:,:] = ' '
        for i,j in self.px[:fall]:
            self.mat1[i,j] = '#'


        djk = Djk(self.mat1, (0,0), {(self.m-1,self.n-1)})

        return djk.solveWithoutPath()
        

    def solve2(self) -> int:

        return 0


if __name__ == "__main__":
    t = Day(SAMPLE, (7,7), True)
    print(f'Test p1: {t.solve1(12)}')

    r = Day(REAL, (71,71))
    print(f'Real p1: {r.solve1(1024)}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)
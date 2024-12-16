from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLES = [
    [
        'AAAA',
        'BBCD',
        'BBCC',
        'EEEC',
    ],
    [
        'OOOOO',
        'OXOXO',
        'OOOOO',
        'OXOXO',
        'OOOOO',
    ],
    [
        'RRRRIICCFF',
        'RRRRIICCCF',
        'VVRRRCCFFF',
        'VVRCCCJFFF',
        'VVVVCJJCFE',
        'VVIVCCJJEE',
        'VVIIICJJEE',
        'MIIIIIJJEE',
        'MIIISIJEEE',
        'MMMISSJEEE',
    ],
]

CHARMAP = {chr(n): n for n in range(ord('A'), ord('Z') + 1)}


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug
        self.mat = tl.make_cmapped_int_matrix(lines, CHARMAP)

    def solve1(self) -> int:
        from skimage.morphology import label

        self.labels, self.n_labels = label(self.mat, return_num=True, connectivity=1)

        area: dict[int, int] = {}
        peri: dict[int, int] = {}

        for k in range(1, self.n_labels+1):
            area[k] = 0
            peri[k] = 0

        m, n = self.mat.shape

        for ii in range(m):
            for jj in range(n):
                lab = self.labels[ii, jj]
                area[lab] += 1

                if ii == 0 or self.labels[ii-1, jj] != lab:
                    peri[lab] += 1
                if ii == m-1 or self.labels[ii+1, jj] != lab:
                    peri[lab] += 1
                if jj == 0 or self.labels[ii, jj-1] != lab:
                    peri[lab] += 1
                if jj == n-1 or self.labels[ii, jj+1] != lab:
                    peri[lab] += 1

        total = 0
        for k in range(1, self.n_labels+1):
            total += area[k] * peri[k]

        self.area = area
        self.peri = peri

        return total


    def solve2(self) -> int:

        from skimage.morphology import label

        m, n = self.mat.shape
        
        self.bigger_mat = np.zeros((m+2, n+2), dtype=self.mat.dtype)
        self.bigger_mat[1:-1, 1:-1] = self.mat

        self.labels, self.n_labels = label(self.bigger_mat, background=0, return_num=True, connectivity=1)
        l = self.labels
        cornermat = (self.labels * 0).astype(np.uint8)

        area: dict[int, int] = {}
        corners: dict[int, int] = {}

        for k in range(1, self.n_labels+1):
            area[k] = 0
            corners[k] = 0

        for ii in range(1,m+1):
            for jj in range(1,n+1):
                lab = self.labels[ii, jj]
                area[lab] += 1

                # It's an outer corner
                if (l[ii-1, jj] != lab and l[ii, jj+1] != lab):
                    corners[lab] += 1
                    cornermat[ii,jj] |= 0x1
                if (l[ii, jj+1] != lab and l[ii+1, jj] != lab):
                    corners[lab] += 1
                    cornermat[ii,jj] |= 0x2
                if (l[ii+1, jj] != lab and l[ii, jj-1] != lab):
                    corners[lab] += 1
                    cornermat[ii,jj] |= 0x4
                if (l[ii, jj-1] != lab and l[ii-1, jj] != lab):
                    corners[lab] += 1
                    cornermat[ii,jj] |= 0x8
                # It's an inner corner
                if (l[ii+1, jj+1] != lab and l[ii+1, jj] == lab and l[ii, jj+1] == lab):
                    corners[lab] += 1
                    cornermat[ii,jj] |= 0x10
                if (l[ii-1, jj+1] != lab and l[ii-1, jj] == lab and l[ii, jj+1] == lab):
                    corners[lab] += 1
                    cornermat[ii,jj] |= 0x20
                if (l[ii-1, jj-1] != lab and l[ii-1, jj] == lab and l[ii, jj-1] == lab):
                    corners[lab] += 1
                    cornermat[ii,jj] |= 0x40
                if (l[ii+1, jj-1] != lab and l[ii+1, jj] == lab and l[ii, jj-1] == lab):
                    corners[lab] += 1
                    cornermat[ii,jj] |= 0x80



        total = 0
        for k in range(1, self.n_labels+1):
            total += area[k] * corners[k]

        self.area2 = area
        self.corn2 = corners

        self.cornermat = cornermat

        return total


if __name__ == "__main__":
    ts = []
    for SAMPLE in SAMPLES:
        t = Day(SAMPLE, True)
        print(f'Test p1: {t.solve1()}')
        ts += [t]

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    for t in ts:
        print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)
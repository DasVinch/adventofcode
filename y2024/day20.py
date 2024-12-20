from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
    '###############',
    '#...#...#.....#',
    '#.#.#.#.#.###.#',
    '#S#...#.#.#...#',
    '#######.#.#.###',
    '#######.#.#...#',
    '#######.#.###.#',
    '###..E#...#...#',
    '###.#######.###',
    '#...###...#...#',
    '#.#####.#.###.#',
    '#.#...#.#.#...#',
    '#.#.#.#.#.#.###',
    '#...#...#...###',
    '###############',
]
'''
SAMPLE = [
    '#######',
    '#S.#.E#',
    '#######',
]
'''

from dataclasses import dataclass


@dataclass(frozen=True)
class Pos:
    i: int
    j: int
    cheat_enter: tuple[int, int] | None
    cheat_exit: tuple[int, int] | None


class Djk(tl.AbstractDijkstraer[Pos]):

    def __init__(self, mat: np.ndarray, start: tuple[int, int],
                 targets: set[tuple[int, int]], target_ij: tuple[int,
                                                                 int]) -> None:
        self.targets_onlycoords = targets
        self.targets = {Pos(t[0], t[1], None, None) for t in targets}

        s3 = (*start, 0)
        super().__init__(Pos(start[0], start[1], None, None), self.targets)

        self.mat = mat
        self.ij = target_ij

        self.disable_cheats = False

    def validate_target(self, elem: Pos) -> bool:
        return (elem.i, elem.j) in self.targets_onlycoords

    def get_neighbors(self, elem: Pos) -> set[tuple[Pos, int]]:
        m, n = self.mat.shape
        e = elem

        neighs: set[tuple[Pos, int]] = set()

        if e.i > 0 and self.mat[e.i - 1, e.j] != '#':
            if e.cheat_enter is not None and e.cheat_exit is None:
                neighs.add((Pos(e.i - 1, e.j, e.cheat_enter,
                                (e.i - 1, e.j)), 1))
            else:
                neighs.add((Pos(e.i - 1, e.j, e.cheat_enter, e.cheat_exit), 1))

        if e.j > 0 and self.mat[e.i, e.j - 1] != '#':
            if e.cheat_enter is not None and e.cheat_exit is None:
                neighs.add((Pos(e.i, e.j - 1, e.cheat_enter,
                                (e.i, e.j - 1)), 1))
            else:
                neighs.add((Pos(e.i, e.j - 1, e.cheat_enter, e.cheat_exit), 1))

        if e.i < m - 1 and self.mat[e.i + 1, e.j] != '#':
            if e.cheat_enter is not None and e.cheat_exit is None:
                neighs.add((Pos(e.i + 1, e.j, e.cheat_enter,
                                (e.i + 1, e.j)), 1))
            else:
                neighs.add((Pos(e.i + 1, e.j, e.cheat_enter, e.cheat_exit), 1))

        if e.j < n - 1 and self.mat[e.i, e.j + 1] != '#':
            if e.cheat_enter is not None and e.cheat_exit is None:
                neighs.add((Pos(e.i, e.j + 1, e.cheat_enter,
                                (e.i, e.j + 1)), 1))
            else:
                neighs.add((Pos(e.i, e.j + 1, e.cheat_enter, e.cheat_exit), 1))

        if self.disable_cheats:
            return neighs

        if e.cheat_enter is None:  # CHEAT!
            if e.i > 0 and self.mat[e.i - 1, e.j] == '#':
                neighs.add((Pos(e.i - 1, e.j, (e.i - 1, e.j), None), 1))

            if e.j > 0 and self.mat[e.i, e.j - 1] == '#':
                neighs.add((Pos(e.i, e.j - 1, (e.i, e.j - 1), None), 1))

            if e.i < m - 1 and self.mat[e.i + 1, e.j] == '#':
                neighs.add((Pos(e.i + 1, e.j, (e.i + 1, e.j), None), 1))

            if e.j < n - 1 and self.mat[e.i, e.j + 1] == '#':
                neighs.add((Pos(e.i, e.j + 1, (e.i, e.j + 1), None), 1))

        return neighs

    def intercept_elem(self, elem: Pos) -> None:
        if (elem.i, elem.j) == self.ij:
            print(self.ij, self.multiDistanceDict.get(elem, None))


def unpack_wh2(boolmat):
    return tuple(w[0] for w in np.where(boolmat))


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.mat = tl.make_char_matrix(lines)

        self.start = unpack_wh2(self.mat == 'S')
        self.end = unpack_wh2(self.mat == 'E')

        self.djk0 = Djk(self.mat, self.start, set(), self.end)
        self.djk0.disable_cheats = True
        self.djk0.solveWithoutPath()

        mm = np.zeros(self.mat.shape, np.float64)
        mm[:, :] = np.nan
        for p, it in self.djk0.distanceDict.items():
            mm[p.i, p.j] = it[0]
        self.mm = mm

    def solve1(self) -> int:
        mm = self.mm

        self.diffs = [
            np.abs(mm[2:, :] - mm[:-2, :]),
            np.abs(mm[:, 2:] - mm[:, :-2]),
            np.abs(mm[1:, 1:] - mm[:-1, :-1]),
            np.abs(mm[1:, :-1] - mm[:-1, 1:])
        ]

        for d in self.diffs:
            d -= 2
            d[d<=0.0] = np.nan

        return sum([np.sum(d>=100) for d in self.diffs])

    def solve2(self) -> int:
        
        mm = self.mm
        min_cut = 1
        max_cut = 20

        self.diffs2: dict[tuple[int,int], np.ndarray] = {}
        for i in range(max_cut + 1):
            for j in range(-max_cut, max_cut+1):
                if (abs(i) + abs(j) < min_cut or abs(i) + abs(j) > max_cut or
                (-i,-j) in self.diffs2):
                    continue
                if i == 0:
                    if j > 0:
                        self.diffs2[(i,j)] = np.abs(mm[:, j:] - mm[:, :-j])
                    elif j < 0:
                        self.diffs2[(i,j)] = np.abs(mm[:, :j] - mm[:, -j:])
                elif i > 0:
                    if j > 0:
                        self.diffs2[(i,j)] = np.abs(mm[i:, j:] - mm[:-i, :-j])
                    elif j < 0:
                        self.diffs2[(i,j)] = np.abs(mm[i:, :j] - mm[:-i, -j:])
                    elif j == 0:
                        self.diffs2[(i,j)] = np.abs(mm[i:, :] - mm[:-i, :])

        for (i,j), d in self.diffs2.items():
            d -= np.abs(i) + np.abs(j)
            d[d<=0.0] = np.nan

        return sum([np.sum(d >= 100) for d in self.diffs2.values()])



        
        return 0


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)

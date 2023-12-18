from __future__ import annotations
from typing import Set

from tools import get_input
import tools

import numpy as np

import os
from enum import IntEnum

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    '2413432311323',
    '3215453535623',
    '3255245654254',
    '3446585845452',
    '4546657867536',
    '1438598798454',
    '4457876987766',
    '3637877979653',
    '4654967986887',
    '4564679986453',
    '1224686865563',
    '2546548887735',
    '4322674655533',
]

SAMPLE2 = [
    '111111111111',
    '999999999991',
    '999999999991',
    '999999999991',
    '999999999991',
]


class Dir(IntEnum):
    U = 0
    D = 1
    L = 2
    R = 3

    @classmethod
    def turnDirs(cls, dir: Dir) -> list[Dir]:
        return {
            cls.U: (cls.L, cls.R),
            cls.D: (cls.L, cls.R),
            cls.L: (cls.U, cls.D),
            cls.R: (cls.U, cls.D),
        }[dir]


from dataclasses import dataclass


@dataclass
class CartState:
    pos: tuple[int, int]
    dir: Dir
    since: int

    def __hash__(self):
        return hash((self.pos, self.dir, self.since))

    def __eq__(self, oth: CartState):
        '''
        Should be equal IF same pos and same moving capabilities
        '''
        return (self.pos == oth.pos and self.dir == oth.dir
                and self.since == oth.since)


class Djk(tools.AbstractDijkstraer[CartState]):

    def __init__(self, grid: np.ndarray, start: CartState,
                 targets: Set) -> None:
        super().__init__(start, targets)

        self.grid = grid
        self.gshape = grid.shape

    def get_neighbors(self, elem: CartState) -> Set[tuple[CartState, int]]:
        d1, d2 = Dir.turnDirs(elem.dir)

        # Rotate
        neighbs: Set[tuple[CartState, int]] = set()

        # Move straight
        if elem.since < 3:
            x, y = elem.pos
            if elem.dir == Dir.U and x > 0:
                neighbs.add((CartState((x - 1, y), elem.dir,
                                       elem.since + 1), self.grid[x - 1, y]))
            if elem.dir == Dir.D and x < self.gshape[0] - 1:
                neighbs.add((CartState((x + 1, y), elem.dir,
                                       elem.since + 1), self.grid[x + 1, y]))
            if elem.dir == Dir.L and y > 0:
                neighbs.add((CartState((x, y - 1), elem.dir,
                                       elem.since + 1), self.grid[x, y - 1]))
            if elem.dir == Dir.R and y < self.gshape[1] - 1:
                neighbs.add((CartState((x, y + 1), elem.dir,
                                       elem.since + 1), self.grid[x, y + 1]))

        x, y = elem.pos
        # Rotate up
        if elem.dir in [Dir.L, Dir.R] and x > 0:
            neighbs.add((CartState((x - 1, y), Dir.U, 1), self.grid[x - 1, y]))
        # Rotate down
        if elem.dir in [Dir.L, Dir.R] and x < self.gshape[0] - 1:
            neighbs.add((CartState((x + 1, y), Dir.D, 1), self.grid[x + 1, y]))
        # Rotate left
        if elem.dir in [Dir.U, Dir.D] and y > 0:
            neighbs.add((CartState((x, y - 1), Dir.L, 1), self.grid[x, y - 1]))
        # Rotate right
        if elem.dir in [Dir.U, Dir.D] and y < self.gshape[1] - 1:
            neighbs.add((CartState((x, y + 1), Dir.R, 1), self.grid[x, y + 1]))

        return neighbs

    def validate_target(self, elem: CartState) -> bool:
        x, y = elem.pos
        xg, yg = self.gshape
        return x == xg - 1 and y == yg - 1


class Djk2(tools.AbstractDijkstraer[CartState]):

    def __init__(self, grid: np.ndarray, start: CartState,
                 targets: Set) -> None:
        super().__init__(start, targets)

        self.grid = grid
        self.gshape = grid.shape

    def get_neighbors(self, elem: CartState) -> Set[tuple[CartState, int]]:

        # Rotate
        neighbs: Set[tuple[CartState, int]] = set()

        # Special rot on start state
        if elem.pos == (0, 0) and elem.since == 0:
            neighbs.update({(CartState((0, 0), Dir.D, 0), 0),
                            (CartState((0, 0), Dir.R, 0), 0)})

        # Move straight
        if elem.since < 10:
            x, y = elem.pos
            if elem.dir == Dir.U and x > 0:
                neighbs.add((CartState((x - 1, y), elem.dir,
                                       elem.since + 1), self.grid[x - 1, y]))
            if elem.dir == Dir.D and x < self.gshape[0] - 1:
                neighbs.add((CartState((x + 1, y), elem.dir,
                                       elem.since + 1), self.grid[x + 1, y]))
            if elem.dir == Dir.L and y > 0:
                neighbs.add((CartState((x, y - 1), elem.dir,
                                       elem.since + 1), self.grid[x, y - 1]))
            if elem.dir == Dir.R and y < self.gshape[1] - 1:
                neighbs.add((CartState((x, y + 1), elem.dir,
                                       elem.since + 1), self.grid[x, y + 1]))

        x, y = elem.pos
        # Rotate up
        if elem.since >= 4:
            if elem.dir in [Dir.L, Dir.R] and x > 0:
                neighbs.add((CartState((x - 1, y), Dir.U, 1), self.grid[x - 1,
                                                                        y]))
            # Rotate down
            if elem.dir in [Dir.L, Dir.R] and x < self.gshape[0] - 1:
                neighbs.add((CartState((x + 1, y), Dir.D, 1), self.grid[x + 1,
                                                                        y]))
            # Rotate left
            if elem.dir in [Dir.U, Dir.D] and y > 0:
                neighbs.add((CartState((x, y - 1), Dir.L,
                                       1), self.grid[x, y - 1]))
            # Rotate right
            if elem.dir in [Dir.U, Dir.D] and y < self.gshape[1] - 1:
                neighbs.add((CartState((x, y + 1), Dir.R,
                                       1), self.grid[x, y + 1]))

        return neighbs

    def validate_target(self, elem: CartState) -> bool:
        x, y = elem.pos
        xg, yg = self.gshape
        return x == xg - 1 and y == yg - 1 and elem.since >= 4


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.lines = lines

        self.grid = tools.make_int_matrix(self.lines)

        self.grid_shape = (len(self.lines), len(self.lines[0]))

    def solve1(self) -> int:
        djk = Djk(self.grid, CartState((0, 0), Dir.R, 0), set())
        djk.solveWithoutPath()

        x, y = self.grid_shape
        x -= 1
        y -= 1

        targ = [c for c in djk.distanceDict if c.pos == (x, y)][0]
        tscore = [
            djk.distanceDict[c][0] for c in djk.distanceDict if c.pos == (x, y)
        ]

        track = djk.show_track(targ)

        mat = np.zeros((x + 1, y + 1), bool)
        for e in track:
            mat[e.pos] = True

        tools.print_bool_matrix(mat)

        return min(tscore)

    def solve2(self) -> int:
        # WARNING CAN USE Dir.D or Dir.R - getNeighbors wouldn't allow a rotation on
        # the start state. It should.
        djk = Djk2(self.grid, CartState((0, 0), Dir.R, 0), set())
        djk.solveWithoutPath()

        x, y = self.grid_shape
        x -= 1
        y -= 1

        tall = [(c, djk.distanceDict[c][0]) for c in djk.distanceDict
                if djk.validate_target(c)]
        tscore = [c[1] for c in tall]

        min_score = min(tscore)

        targ = tall[tscore.index(min_score)][0]

        import pdb
        pdb.set_trace()
        track = djk.show_track(targ)

        mat = np.zeros((x + 1, y + 1), bool)
        for e in track:
            mat[e.pos] = True

        tools.print_bool_matrix(mat)

        return min(tscore)


if __name__ == "__main__":

    t = Day(SAMPLE, True)

    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    t2 = Day(SAMPLE2, True)

    print(f'Test p1: {t.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Test2 p2: {t2.solve2()}')
    print(f'Real p2: {r.solve2()}')

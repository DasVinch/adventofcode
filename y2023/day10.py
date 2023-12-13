from __future__ import annotations

import os
import typing as typ
from tools import get_input
import tools

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tools.make_char_matrix(get_input(DAYDAY, 2023))

SAMPLE = tools.make_char_matrix([
    '7-F7-',
    '.FJ|7',
    'SJLL7',
    '|F--J',
    'LJ.LJ',
])

SAMPLE2 = tools.make_char_matrix([
    'FF7FSF7F7F7F7F7F---7',
    'L|LJ||||||||||||F--J',
    'FL-7LJLJ||||||LJL-77',
    'F--JF--7||LJLJ7F7FJ-',
    'L---JF-JLJ.||-FJLJJ7',
    '|F|F-JF---7F7-L7L|7|',
    '|FFJF7L7F-JF7|JL---7',
    '7-L-JL7||F7|L7F-7F7|',
    'L.L7LFJ|||||FJL7||LJ',
    'L7JLJL-JLJLJL--JLJ.L',
])


class Djk(tools.AbstractDijkstraer[tuple[int, int]]):

    def __init__(self, map: np.ndarray, start: tuple[int, int],
                 targets: set[tuple[int, int]]) -> None:
        super().__init__(start, targets)

        self.map = map
        self.ms = map.shape

    def get_neighbors(
            self, elem: tuple[int, int]) -> set[tuple[tuple[int, int], int]]:
        x, y = elem
        mark = self.map[x, y]

        neighbs: set[tuple[tuple[int, int], int]] = set()

        if x > 0 and mark in '|LJS' and self.map[x - 1, y] in '|F7S':
            neighbs.add(p1(x - 1, y))
        if x < self.ms[0] and mark in '|F7S' and self.map[x + 1, y] in '|LJS':
            neighbs.add(p1(x + 1, y))

        if y > 0 and mark in '-7JS' and self.map[x, y - 1] in '-FLS':
            neighbs.add(p1(x, y - 1))
        if y < self.ms[1] and mark in '-FLS' and self.map[x, y + 1] in '-7JS':
            neighbs.add(p1(x, y + 1))

        return neighbs


def vconn(t: str, b: str) -> bool:
    return not ((t in 'F7|') and (b in '|JL'))


def hconn(l: str, r: str) -> bool:
    return not ((l in '-LF') and (r in '-7J'))


def p1(x: int, y: int) -> tuple[tuple[int, int], typ.Literal[1]]:
    return ((x, y), 1)


class DualDjk(tools.AbstractDijkstraer[tuple[int, int]]):

    def __init__(self, map: np.ndarray, start: tuple[int, int],
                 targets: set[tuple[int, int]]) -> None:
        super().__init__(start, targets)

        self.map = map
        self.ms = map.shape

    def get_neighbors(
            self, elem: tuple[int, int]) -> set[tuple[tuple[int, int], int]]:
        x, y = elem

        neighbs: set[tuple[tuple[int, int], int]] = set()

        if hconn(self.map[x, y], self.map[x, y + 1]) and x - 1 >= 0:  # up
            neighbs.add(p1(x - 1, y))
        if hconn(self.map[x + 1, y],
                 self.map[x + 1, y + 1]) and x + 1 < self.ms[0] - 1:  # down
            neighbs.add(p1(x + 1, y))

        if vconn(self.map[x, y], self.map[x + 1, y]) and y - 1 >= 0:  # left
            neighbs.add(p1(x, y - 1))
        if vconn(self.map[x, y + 1],
                 self.map[x + 1, y + 1]) and y + 1 < self.ms[1] - 1:  # right
            neighbs.add(p1(x, y + 1))

        return neighbs


class Day:

    def __init__(self,
                 map: np.ndarray,
                 replacer: str,
                 debug: bool = False) -> None:
        self.debug = debug
        self.map = map
        self.replacer = replacer

        where_s = np.where(self.map == 'S')
        self.xs, self.ys = where_s[0][0], where_s[1][0]
        self.map[self.xs, self.ys] = self.replacer

    def solve1(self) -> int:

        djk = Djk(self.map, (self.xs, self.ys), set())

        djk.solveWithoutPath()

        if self.debug:
            print(djk.distanceDict)

        return max(djk.distanceDict.values())

    def solve2(self) -> int:
        djk = Djk(self.map, (self.xs, self.ys), set())
        djk.solveWithoutPath()

        self.map_pad = np.zeros((self.map.shape[0] + 2, self.map.shape[1] + 2),
                                self.map.dtype)
        self.map_pad[1:-1, 1:-1] = self.map
        self.map_pad[0, :] = '.'
        self.map_pad[:, 0] = '.'
        self.map_pad[-1, :] = '.'
        self.map_pad[:, -1] = '.'

        self.map2 = np.zeros_like(self.map_pad, dtype=bool)
        for x, y in djk.distanceDict:
            self.map2[x + 1, y + 1] = True

        if self.debug:
            tools.print_bool_matrix(self.map2)

        self.map_pad[~self.map2] = '.'  # Remove strays.

        dualdjk = DualDjk(self.map_pad, (0, 0), set())
        dualdjk.solveWithoutPath()

        self.can_map = self.map2[:-1, :-1].copy()
        self.can_map[:] = False

        for x, y in dualdjk.distanceDict:
            self.can_map[x, y] = True

        # Now solve for the interior!
        a, b = np.where(~self.can_map)

        dualdjk = DualDjk(self.map_pad, (a[0], b[0]), set())
        dualdjk.solveWithoutPath()

        self.can_map2 = self.can_map.copy()
        self.can_map2[:] = False

        for x, y in dualdjk.distanceDict:
            self.can_map2[x, y] = True

        full_tiles = (self.can_map2[:-1, :-1] & self.can_map2[:-1, 1:]
                      & self.can_map2[1:, :-1] & self.can_map2[1:, 1:])

        return np.sum(full_tiles)


if __name__ == "__main__":
    t = Day(SAMPLE, 'F', True)
    print(f'Test p1: {t.solve1()}')

    t2 = Day(SAMPLE2, '7', True)
    print(f'Test2 p1: {t2.solve1()}')
    print(f'Test2 p2: {t2.solve2()}')

    r = Day(REAL, '|')
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

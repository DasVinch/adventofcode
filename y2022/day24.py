from __future__ import annotations

import os
from typing import Set
from tools import get_input
import tools
import math

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2022)

SAMPLE = [
    '#.######',
    '#>>.<^<#',
    '#.<..<<#',
    '#>v.><>#',
    '#<^v^^>#',
    '######.#',
]

from tools import AbstractDijkstraer
from dataclasses import dataclass
from enum import IntEnum


class BzDir(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


@dataclass
class Blizzard:
    start_pos: tuple[int, int]
    dir: BzDir

    def compute_pos(self, time: int, shape: tuple[int,
                                                  int]) -> tuple[int, int]:
        x, y = self.start_pos
        match self.dir:
            case BzDir.UP:
                return (((x - 1) - time) % (shape[0]-2) + 1, y)
            case BzDir.DOWN:
                return (((x - 1) + time) % (shape[0]-2) + 1, y)
            case BzDir.LEFT:
                return (x, ((y - 1) - time) % (shape[1]-2) + 1)
            case BzDir.RIGHT:
                return (x, ((y - 1) + time) % (shape[1]-2) + 1)
            
    def __hash__(self):
        return hash((*self.start_pos, self.dir))
    
    def __eq__(self, oth: Blizzard) -> bool:
        return self.start_pos == oth.start_pos and self.dir == oth.dir


class Djk(AbstractDijkstraer[tuple[int, int, int]]):

    def __init__(self, bz_list: list[Blizzard], shape: tuple[int, int],
                 start: tuple[int, int, int],
                 targets: Set[tuple[int, int, int]],
                 reverse: bool = False) -> None:

        self.shape = shape
        self.bz_list = bz_list

        self.bz_byrow: dict[int, set[Blizzard]] = {}
        self.bz_bycol: dict[int, set[Blizzard]] = {}
        for bz in bz_list:
            x, y = bz.start_pos
            if not x in self.bz_byrow:
                self.bz_byrow[x] = set()
            self.bz_byrow[x].add(bz)
            if not y in self.bz_bycol:
                self.bz_bycol[y] = set()
            self.bz_bycol[y].add(bz)

        self.max_x_yet = 0

        self.time_loop = math.lcm(shape[0] - 2, shape[1] - 2)

        self.reverse = reverse

        super().__init__(start, targets)

    def get_neighbors(self, elem: tuple[int, int, int]) \
                                -> Set[tuple[tuple[int, int, int], int]]:

        x, y, t = elem
        if y > self.max_x_yet:
            print(f'New max y {y}')
            self.max_x_yet = y

        neighbs: set[tuple[int,int,int]] = set()

        # Compute relevant blizzards at t+1
        future_bzs = set()
        if x-1 in self.bz_byrow:
            future_bzs.update({bz.compute_pos(t+1, self.shape) for bz in self.bz_byrow[x-1]})
        if x in self.bz_byrow:
            future_bzs.update({bz.compute_pos(t+1, self.shape) for bz in self.bz_byrow[x]})
        if x+1 in self.bz_byrow:
            future_bzs.update({bz.compute_pos(t+1, self.shape) for bz in self.bz_byrow[x+1]})
        if y-1 in self.bz_bycol:
            future_bzs.update({bz.compute_pos(t+1, self.shape) for bz in self.bz_bycol[y-1]})
        if y in self.bz_bycol:
            future_bzs.update({bz.compute_pos(t+1, self.shape) for bz in self.bz_bycol[y]})
        if y+1 in self.bz_bycol:
            future_bzs.update({bz.compute_pos(t+1, self.shape) for bz in self.bz_bycol[y+1]})
        
        good_future_bzs = {(xb,yb) for xb, yb in future_bzs if (abs(xb-x) <= 1 and abs(yb-y) <= 1)}

        if x == self.shape[0] - 2 and y == self.shape[1] - 2:
            neighbs.add((x+1, y, (t+1) % self.time_loop)) # The exit
        if self.reverse and x == 1 and y == 1:
            neighbs.add((x-1, y, (t+1) % self.time_loop)) # The exit
        
        if (x,y) == (0,1):
            # Treat start separately so we don't need
            # to do as much boundary checking later.
            neighbs.add((0,1,(t+1) % self.time_loop))
            if not (1,1) in good_future_bzs:
                neighbs.add((1,1,(t+1) % self.time_loop))
            return {(n,1) for n in neighbs}
        
        if (x,y) == (self.shape[0]-1,self.shape[0]-2):
            # Treat start but when start is the end
            neighbs.add((self.shape[0]-1,self.shape[0]-2,(t+1) % self.time_loop))
            if not (1,1) in good_future_bzs:
                neighbs.add((self.shape[0]-2,self.shape[0]-2,(t+1) % self.time_loop))
            return {(n,1) for n in neighbs}

        # Can wait?
        if not (x,y) in good_future_bzs:
            neighbs.add((x,y,(t+1) % self.time_loop))
        # Down
        if not (x+1,y) in good_future_bzs and x+1 < self.shape[0]-1:
            neighbs.add((x+1,y,(t+1) % self.time_loop))
        # Up
        if not (x-1,y) in good_future_bzs and x-1 > 0:
            neighbs.add((x-1,y,(t+1) % self.time_loop))

        # Right
        if not (x,y+1) in good_future_bzs and y+1 < self.shape[1]-1:
            neighbs.add((x,y+1,(t+1) % self.time_loop))
        # Left
        if not (x,y-1) in good_future_bzs and y-1 > 0:
            neighbs.add((x,y-1,(t+1) % self.time_loop))

        return {(n,1) for n in neighbs}
    
    def validate_target(self, elem: tuple[int, int, int]) -> bool:
        x, y, _ = elem
        if self.reverse:
            return x == 0 and y == 1
        else:
            return x == self.shape[0] - 1 and y == self.shape[1] - 2

def parse_blizzards(lines: list[str]) -> list[Blizzard]:
    bzs: list[Blizzard] = []
    for ii, line in enumerate(lines):
        for jj, c in enumerate(line):
            if c in '<>^v':
                dir = {
                    '<': BzDir.LEFT,
                    '>': BzDir.RIGHT,
                    '^': BzDir.UP,
                    'v': BzDir.DOWN,
                }[c]
                bzs += [Blizzard((ii,jj), dir)]
    
    return bzs

class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.bzs = parse_blizzards(lines)

        self.shape = (len(lines), len(lines[0]))


    def solve1(self) -> int:
        djk = Djk(self.bzs, self.shape, (0, 1, 0), None)

        djk.solveWithoutPath()

        solution = {djk.distanceDict[t][0] for t in djk.distanceDict
                    if t[0] == self.shape[0] - 1 and t[1] == self.shape[1] - 2}.pop()

        return solution

    def solve2(self) -> int:
        djk = Djk(self.bzs, self.shape, (0, 1, 0), None)
        djk.solveWithoutPath()
        solution_a = {djk.distanceDict[t][0] for t in djk.distanceDict
                    if t[0] == self.shape[0] - 1 and t[1] == self.shape[1] - 2}.pop()
        print(f'Solution_a: {solution_a}')
        
        
        djk = Djk(self.bzs, self.shape, (self.shape[0] - 1, self.shape[1] - 2, solution_a), None, reverse=True)
        djk.solveWithoutPath()
        solution_b = {djk.distanceDict[t][0] for t in djk.distanceDict
                    if t[0] == 0 and t[1] == 1}.pop() + solution_a
        print(f'Solution_b: {solution_b}')
        
        djk = Djk(self.bzs, self.shape, (0, 1, solution_b), None)
        djk.solveWithoutPath()
        solution_c = {djk.distanceDict[t][0] for t in djk.distanceDict
                    if t[0] == self.shape[0] - 1 and t[1] == self.shape[1] - 2}.pop() + solution_b
        print(f'Solution_c: {solution_c}')

        return solution_c


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')
    print(f'Test p2: {t.solve2()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')
    print(f'Real p2: {r.solve2()}')

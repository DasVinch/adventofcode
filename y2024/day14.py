from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
    'p=0,4 v=3,-3',
    'p=6,3 v=-1,-3',
    'p=10,3 v=-1,2',
    'p=2,0 v=2,-1',
    'p=0,0 v=1,3',
    'p=3,0 v=-2,-2',
    'p=7,6 v=-1,-3',
    'p=3,0 v=-1,-2',
    'p=9,3 v=2,3',
    'p=7,3 v=-1,2',
    'p=2,4 v=2,-3',
    'p=9,5 v=-3,-3',
]

import re

RE = r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)'

from dataclasses import dataclass

@dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int

    def move(self, modx: int, mody: int) -> None:
        self.px = (self.px + self.vx) % modx
        self.py = (self.py + self.vy) % mody


class Day:

    def __init__(self, lines: list[str], debug: bool, height: int, width: int) -> None:
        self.debug = debug

        self.h = height
        self.w = width

        self.lines = lines

        self.robots: list[Robot]
        self._init_robots()

    def _init_robots(self) -> None:
        
        self.robots = []

        for l in self.lines:
            g = re.match(RE, l).groups()
            self.robots += [Robot(*(int(gg) for gg in g))]


    def solve1(self) -> int:
        self._init_robots()

        for k in range(100):
            for r in self.robots:
                r.move(self.h, self.w)

        q = [0,0,0,0]
        for r in self.robots:
            if r.px < self.h // 2 and r.py < self.w // 2:
                q[0] += 1
            elif r.px < self.h // 2 and r.py > self.w // 2:
                q[1] += 1
            elif r.px > self.h // 2 and r.py < self.w // 2:
                q[2] += 1
            elif r.px > self.h // 2 and r.py > self.w // 2:
                q[3] += 1

        return q[0] * q[1] * q[2] * q[3]

        return 0
        

    def solve2(self) -> int:
        self._init_robots()
        mat = np.zeros((self.h, self.w), dtype=np.bool_)

        # one axis: 12 + k*101
        # oth axis: 88 + k*103

        # 6577... chinese remainders ftw.

        for i in range(1, 100000):
            mat[:,:] = 0
            for r in self.robots:
                r.move(self.h, self.w)
                mat[r.px, r.py] = True
            
            if i % 101 == 12 or i % 103 == 88:
                tl.print_bool_matrix(mat)
                input(i)


        return 0


if __name__ == "__main__":
    t = Day(SAMPLE, True, 11, 7)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL, False, 101, 103)
    print(f'Real p1: {r.solve1()}')

    #print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)
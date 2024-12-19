from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
'r, wr, b, g, bwu, rb, gb, br',
'',
'brwrr',
'bggr',
'gbbr',
'rrbgbr',
'ubwu',
'bwurrg',
'brgr',
'bbrgwb',
]

import functools




class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.towels = lines[0].split(', ')

        self.patterns = lines[2:]


    def solve1(self) -> int:
        return sum([self.solvepattern(p) for p in self.patterns])


    @functools.cache
    def solvepattern(self, pattern: str) -> bool:
        if len(pattern) == 0:
            return True

        return any([
            pattern.startswith(t) and self.solvepattern(pattern.removeprefix(t))
            for t in self.towels
        ])
    
    @functools.cache
    def countpattern(self, pattern: str) -> int:
        if len(pattern) == 0:
            return 1

        return sum([
            self.countpattern(pattern.removeprefix(t))
            for t in self.towels if pattern.startswith(t)
        ])

    def solve2(self) -> int:

        return sum([self.countpattern(p) for p in self.patterns])


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)
from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)[0]

SAMPLE = '0 1 10 99 999'
SAMPLE2 = '125 17'

from dataclasses import dataclass

def countdigits(v):
    if v < 10:
        return 1
    return 1 + countdigits(v // 10)


class Stone(int):

    def copy(self) -> Stone:
        return Stone(self)

    def op(self) -> list[Stone]:
        if self == 0:
            return [Stone(1)]
        
        k = countdigits(self)
        if k % 2 == 0:
            l = 10 ** (k//2)
            return [Stone(self // l), Stone(self % l)]

        return [Stone(self * 2024)]

import itertools, functools

def blink(stones: typ.Iterable[Stone]) -> typ.Iterable[Stone]:
    return itertools.chain.from_iterable((s.op() for s in stones))

@functools.cache
def blink_but_count(val: Stone, n: int) -> int:
    if n == 0:
        return 1
    
    return sum([blink_but_count(s, n-1) for s in val.op()])


class Day:

    def __init__(self, line: str, debug: bool = False) -> None:
        self.debug = debug

        self.og_stones = [Stone(int(s)) for s in line.split()]

    def solve1(self) -> int:

        st = [s.copy() for s in self.og_stones]

        for k in range(25):
            st = blink(st)
        
        return len(list(st))
        

    def solve2(self, n: int = 75) -> int:

        st = [s.copy() for s in self.og_stones]

        c = 0
        from tqdm import trange, tqdm
        
        return sum([blink_but_count(s, n) for s in self.og_stones])


if __name__ == "__main__":
    t = Day(SAMPLE2, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(f'Runtime real part2: {time.time() - s:.4f} s')
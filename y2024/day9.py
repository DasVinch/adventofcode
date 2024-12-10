from __future__ import annotations

import os
import tools
from tools import get_input

import typing as typ
import numpy as np

import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2024)[0]

SAMPLE = '2333133121414131402'


class Day:

    def __init__(self, line: str, debug: bool = False) -> None:
        self.debug = debug

        self.line = line
        self.comp = [int(c) for c in line]

        self.buff = [-1] * sum(self.comp)
        
        self.p_end = 0
        self.p_first_void = None

        p_fill = 0
        counter = 0
        stat = True

        for c in self.comp:
            if not stat:
                stat = True
                counter += 1
                if  c > 0:
                    if self.p_first_void is None:
                        self.p_first_void = p_fill

            else:
                for k in range(c):
                    self.buff[p_fill+k] = counter
                stat = False
            
            p_fill += c

        self.p_end = p_fill - 1 # Last full

    def solve1(self) -> int:
        assert isinstance(self.p_first_void, int)
        while self.p_end >= self.p_first_void:
            self.buff[self.p_first_void] = self.buff[self.p_end]
            self.buff[self.p_end] = -1
            while self.buff[self.p_end] == -1:
                self.p_end -= 1
            while self.buff[self.p_first_void] >= 0:
                self.p_first_void += 1

        chk = 0
        for kk, val in enumerate(self.buff):
            if val > 0:
                chk += kk*val
        
        return chk


    def solve2(self) -> int:
        tupleized: list[tuple[int,int,int]] = [] # len, id, pos
        pos = 0
        for k, c in enumerate(self.comp):
            if k % 2 == 0: # file
                tupleized += [(c, k // 2, pos)]
            else:
                tupleized += [(c, -1, pos)]
            pos += c
        self.tp = tupleized

        tupleized_iter = tupleized.copy()

        for (length, idx, pos) in tupleized_iter[::-1]:
            if idx == -1:
                continue
            for kk, (length2, idx2, pos2) in enumerate(tupleized):
                if pos2 >= pos:
                    break
                if idx2 == -1 and length2 >= length:
                    tupleized = tupleized[:kk] + [
                        (0, -1, pos2),
                        (length, idx, pos2),
                        (length2 - length, -1, pos2 + length)
                    ] + tupleized[kk+1:]
                    tupleized.remove((length, idx, pos))
                    break

        self.tp = tupleized

        return _checksum_from_tupleized(tupleized)

def _checksum_from_tupleized(tupleized: list[tuple[int,int,int]]) -> int:
    checksum: int = 0
    for length, idx, pos in tupleized:
        if idx >= 0:
            for k in range(pos, pos + length):
                checksum += k * idx

    return checksum

        


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL, False)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

from __future__ import annotations
import typing as typ
from typing import Set

from tools import get_input
import tools


import numpy as np

import os
from enum import IntEnum

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    '1,0,1~1,2,1',
    '0,0,2~2,0,2',
    '0,2,3~2,2,3',
    '0,0,4~0,2,4',
    '2,0,5~2,2,5',
    '0,1,6~2,1,6',
    '1,1,8~1,1,9',
]

import re

RE_BLOCK = '^(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)$'


from dataclasses import dataclass

@dataclass(frozen=True)
class Block:
    x0: int
    y0: int
    z0: int
    x1: int
    y1: int
    z1: int

    @classmethod
    def parseblock(cls, line: str) -> Block:
        return Block(*re.match(RE_BLOCK, line).groups())

class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.lines = lines

        self.debug = debug

        self.blocks = {kk: Block.parseblock(line) for (kk, line) in enumerate(self.lines)}

    def solve1(self, nmax: int = 64) -> int:

        hz_blocks_by_height = {b.z0: (k, b) for (k,b) in self.blocks.items() if b.z0 == b.z1}
        vert_block_by_floor = {b.z0: (k, b) for (k,b) in self.blocks.items() if b.z0 != b.z1}

        abovers_idx: dict[int,int] = {}

        for kk, block in self.blocks.items():
            

        return 0

    def solve2(self) -> int:
        return 0



if __name__ == "__main__":

    t = Day(SAMPLE, True)

    print(f'Test p1: {t.solve1(6)}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

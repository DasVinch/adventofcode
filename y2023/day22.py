from __future__ import annotations
import typing as typ

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
        b = Block(*re.match(RE_BLOCK, line).groups())  # type: ignore
        return b

    def is_single(self) -> bool:
        return self.x0 == self.x1 and self.y0 == self.y1 and self.z0 == self.z1

    def is_x_block(self) -> bool:
        return self.x1 > self.x0

    def is_y_block(self) -> bool:
        return self.y1 > self.y0

    def is_z_block(self) -> bool:
        return self.z1 > self.z0


class BlockNode:

    def __init__(self, b: Block):
        self.block = b
        self.minimal_superblocks: list[BlockNode] = []
        self.minimal_subblocks: list[BlockNode] = []

    def is_other_superblock(self, other: BlockNode) -> bool:
        return self.is_other_direct_superblock(other) or any([
            sub.is_other_superblock(other) for sub in self.minimal_superblocks
        ])

    def is_other_direct_superblock(self, other: BlockNode) -> bool:
        sb, ob = self.block, other.block
        # implement order --- painnnnn

        if sb.is_single() or sb.is_z_block():
            if ob.is_single() or ob.is_z_block():
                return ob.x0 == sb.x0 and ob.y0 == sb.y0 and ob.z0 > sb.z1
            elif ob.is_x_block():
                return ob.x0 <= sb.x0 and ob.x1 >= sb.x0 and ob.y0 == sb.y0 and ob.z0 > sb.z1
            elif ob.is_y_block():
                return ob.y0 <= sb.y0 and ob.y1 >= sb.y0 and ob.x0 == sb.x0 and ob.z0 > sb.z1

        elif sb.is_x_block():
            if ob.is_single() or ob.is_z_block():
                return ob.x0 <= sb.x1 and ob.x1 >= sb.x0 and ob.y0 == sb.y0 and ob.z0 >= sb.z1
            elif ob.is_x_block():
                return ob.x1 >= sb.x0 and ob.x0 <= sb.x1 and ob.y0 == sb.y0 and ob.z0 >= sb.z1
            elif ob.is_y_block():
                return ob.x0 >= sb.x0 and ob.x0 <= sb.x1 and sb.y0 >= ob.y0 and sb.y0 <= ob.y1 and sb.z0 < ob.z1

        elif sb.is_y_block():
            if ob.is_single() or ob.is_z_block():
                return ob.y0 <= sb.y1 and ob.y1 >= sb.y0 and ob.x0 == sb.x0 and ob.z0 >= sb.z1
            elif ob.is_x_block():
                return ob.y0 >= sb.y0 and ob.y0 <= sb.y1 and sb.x0 >= ob.x0 and sb.x0 <= ob.x1 and sb.z0 < ob.z1
            elif ob.is_y_block():
                return ob.y1 >= sb.y0 and ob.y0 <= sb.y1 and ob.x0 == sb.x0 and ob.z0 >= sb.z1

        raise ValueError('Unexpected location')

    def is_other_minimal_superblock(self, other: BlockNode) -> bool:
        return self.is_other_superblock(other) and not any(
            [bb.is_other_superblock(other) for bb in self.minimal_superblocks])


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.lines = lines

        self.debug = debug

        self.blocks = {
            kk: BlockNode(Block.parseblock(line))
            for (kk, line) in enumerate(self.lines)
        }

    def test(self):
        for b1, bb1 in self.blocks.items():
            for b2, bb2 in self.blocks.items():

                print(chr(b1 + 65), chr(b2 + 65), bb1.is_other_superblock(bb2))

    def solve1(self, nmax: int = 64) -> int:

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

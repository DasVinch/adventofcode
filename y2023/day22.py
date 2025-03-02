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

T = [
    '0,0,0~0,0,0',
    '0,0,1~0,0,1',
    '0,1,0~0,1,1',
    '0,0,2~0,1,2',
]
T2 =[
'0,0,1~0,1,1',
'1,1,1~1,1,1',
'0,0,2~0,0,2',
'0,1,2~1,1,2',
]
T3 = [
'0,0,1~1,0,1',
'0,1,1~0,1,2',
'0,0,5~0,0,5',
'0,0,4~0,1,4',
]

# A -> B \> D -> F -> G
#   \> C /> E /

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
    
    line: str | None = None

    @classmethod
    def parseblock(cls, line: str) -> Block:
        b = Block(
            *(int(t)
              for t in re.match(RE_BLOCK, line).groups()), line=line)  # type: ignore
        return b

    def __repr__(self) -> str:
        return self.line if self.line else 'None'

    def is_single(self) -> bool:
        return self.x0 == self.x1 and self.y0 == self.y1 and self.z0 == self.z1

    def is_x_block(self) -> bool:
        if self.x1 > self.x0:
            assert self.y0 == self.y1 and self.z0 == self.z1
            return True
        return False

    def is_y_block(self) -> bool:
        if self.y1 > self.y0:
            assert self.x0 == self.x1 and self.z0 == self.z1
            return True
        return False

    def is_z_block(self) -> bool:
        if self.z1 > self.z0:
            assert self.x0 == self.x1 and self.y0 == self.y1
            return True
        return False

    def is_other_above(self, other: Block) -> bool:
        s, o = self, other
        # implement order --- painnnnn

        if s.is_single() or s.is_z_block():
            if o.is_single() or o.is_z_block():
                return o.x0 == s.x0 and o.y0 == s.y0 and o.z0 > s.z1
            elif o.is_x_block():
                return o.x0 <= s.x0 and o.x1 >= s.x0 and o.y0 == s.y0 and o.z0 > s.z1
            elif o.is_y_block():
                return o.y0 <= s.y0 and o.y1 >= s.y0 and o.x0 == s.x0 and o.z0 > s.z1

        elif s.is_x_block():
            if o.is_single() or o.is_z_block():
                return o.x0 <= s.x1 and o.x1 >= s.x0 and o.y0 == s.y0 and o.z0 > s.z1
            elif o.is_x_block():
                return o.x1 >= s.x0 and o.x0 <= s.x1 and o.y0 == s.y0 and o.z0 > s.z1
            elif o.is_y_block():
                return o.x0 >= s.x0 and o.x0 <= s.x1 and s.y0 >= o.y0 and s.y0 <= o.y1 and o.z0 > s.z1

        elif s.is_y_block():
            if o.is_single() or o.is_z_block():
                return o.y0 <= s.y1 and o.y1 >= s.y0 and o.x0 == s.x0 and o.z0 > s.z1
            elif o.is_x_block():
                return o.y0 >= s.y0 and o.y0 <= s.y1 and s.x0 >= o.x0 and s.x0 <= o.x1 and o.z0 > s.z1
            elif o.is_y_block():
                return o.y1 >= s.y0 and o.y0 <= s.y1 and o.x0 == s.x0 and o.z0 > s.z1

        raise ValueError('Unexpected location')


class Day():

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.lines = lines

        self.debug = debug

        blocklist = [Block.parseblock(line) for line in self.lines]
        blocklist.sort(key=lambda b: b.z0, reverse=True)

        self.blocks = {
            kk: b
            for (kk, b) in enumerate(blocklist)
        }

        self.block_children: dict[int, set[int]] = {}

        for bid, b in self.blocks.items():
            self._insert_block(bid, b)

        self.descendency: dict[tuple[int, int, int | None], bool] = {}

        #print(self.block_children)

        self._make_minimalized_graph()
        
        self.block_children_inv: dict[int, set[int]] = {}
        self._make_inverted_graph()

        self._remove_levitating_parenthoods()



    def _insert_block(self, b_id: int, b: Block):
        assert b_id not in self.block_children
        new_superset: set[int] = set()

        for ob_id in self.block_children:
            ob = self.blocks[ob_id]
            if b.is_other_above(ob):
                new_superset.add(ob_id)
            if ob.is_other_above(b):
                self.block_children[ob_id].add(b_id)

        self.block_children[b_id] = new_superset

        # self._make_minimalized_graph() Keep the graph minimal! But be efficient about it!

    def _make_minimalized_graph(self):
        for ob_id in self.block_children:
            old_superblock_set = self.block_children[ob_id].copy()
            for sub_id in old_superblock_set:
                if self.would_b_be_above_a_omitting_direct_to_c(ob_id, sub_id, sub_id):
                    self.block_children[ob_id].remove(sub_id)
                    print(f'Removing link {ob_id} {sub_id}')

    def _remove_levitating_parenthoods(self):
        # Handles cases like T3 when a block is indeed above another block but a gap remains
        # Because a taller stack exists elsewhere

        heights: dict[int, int] = {}
        nodes = [id for id in self.block_children]
        
        nodes.sort(key = lambda n: len(self.block_children_inv[n]))

        while len(nodes):
            n = nodes.pop(0)
            if len(self.block_children_inv[n]) == 0:
                heights[n] = 0
                continue

            if not all([sub in heights for sub in self.block_children_inv[n]]):
                nodes.append(n)
                continue

            parent_heights = set()
            for p_id in self.block_children_inv[n]:
                p_block = self.blocks[p_id]
                parent_heights.add(heights[p_id] + p_block.z1 - p_block.z0 + 1)

            if len(parent_heights) == 1:
                heights[n] = parent_heights.pop()
                continue

            max_height = max(parent_heights)
            heights[n] = max_height

            parent_copy = self.block_children_inv[n].copy()
            for p_id in parent_copy:
                p_block = self.blocks[p_id]
                if heights[p_id] + p_block.z1 - p_block.z0 + 1 < max_height:
                    self.block_children[p_id].remove(n)
                    self.block_children_inv[n].remove(p_id)

    def _make_inverted_graph(self):
        for ob_id in self.block_children:
            self.block_children_inv[ob_id] = set()

        for ob_id in self.block_children:
            supporting_set: set[int] = set()
            for sub_id in self.block_children[ob_id]:
                self.block_children_inv[sub_id].add(ob_id)

    def would_b_be_above_a_omitting_direct_to_c(self,
                      a: int,
                      b: int,
                      c: int | None = None) -> bool:
        if (a, b, c) in self.descendency:
            return self.descendency[(a,b,c)]
        
        if (c is None or b != c) and b in self.block_children[a]:
            self.descendency[(a,b,c)] = True
            #print(a,b,c,True)
            return True

        for subblock in self.block_children[a]:
            if subblock == c:
                continue
            if self.would_b_be_above_a_omitting_direct_to_c(subblock, b, None):
                self.descendency[(a,b,c)] = True
                #print(a,b,c,True)
                return True
        
        self.descendency[(a,b,c)] = False
        #print(a,b,c,False)
        return False

    def solve1(self) -> int:
        safe_set = set()
        for b_id in self.blocks:
            if all([
                    len(self.block_children_inv[bb_id]) > 1
                    for bb_id in self.block_children[b_id]
            ]):
                safe_set.add(b_id)
                print(b_id, self.blocks[b_id], [(bb_id, self.block_children_inv[bb_id]) for bb_id in self.block_children[b_id]])

        return len(safe_set)

    def wouldfall(self, b_id: int, missing: set[int]) -> None:
        
        missing.add(b_id)

        for child in self.block_children[b_id]:
            if len(self.block_children_inv[child] - missing) == 0:
                self.wouldfall(child, missing)

    def solve2(self) -> int:
        total = 0
        for b_id in self.blocks:
            m = set()
            self.wouldfall(b_id, m)
            total += len(m) - 1
        return total


if __name__ == "__main__":

    t = Day(SAMPLE, True)

    print(f'Test p1: {t.solve1()}')

    t1 = Day(T)
    t2 = Day(T2)
    t3 = Day(T3)
    print(f't1: {t1.solve1()}')
    print(f't2: {t2.solve1()}')
    print(f't3: {t3.solve1()}')
    
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

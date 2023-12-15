from __future__ import annotations

import os
from tools import get_input
import tools

import re

from tqdm import tqdm

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
]

def hashme(s: str) -> int:
    v = 0
    for c in s:
        v = ((v + ord(c)) * 17) % 256
    return v

from dataclasses import dataclass
@dataclass
class Lens:
    s: str
    v: int


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.bits = lines[0].split(',')


    def solve1(self) -> int:
        return sum([hashme(s) for s in self.bits])

            

    def solve2(self, n = None) -> int:
        if n is None:
            n = len(self.bits)

        self.lenspos: list[list[str]] = [[] for _ in range(256)]
        self.lensmap: dict[str, int] = {}

        re_minus = '([a-z]+)-'
        re_eq = '([a-z]+)=(\d+)'

        for lensbit in self.bits[:n]:
            if m := re.match(re_minus, lensbit):
                lens = m.groups()[0]
                box_id = hashme(lens)
                if lens in self.lenspos[box_id]:
                    self.lenspos[box_id].remove(lens)
                if lens in self.lensmap:
                    del self.lensmap[lens]
            if m := re.match(re_eq, lensbit):
                lens, focal = m.groups()
                box_id = hashme(lens)
                self.lensmap[lens] = int(focal)
                if not lens in self.lenspos[box_id]:
                    self.lenspos[box_id].append(lens)

        # Compute power
        tot = 0
        for ii, contents in enumerate(self.lenspos):
            for jj, label in enumerate(contents):
                tot += (ii+1) * (jj+1) * self.lensmap[label]

        return tot


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

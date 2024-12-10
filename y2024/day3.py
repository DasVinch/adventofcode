from __future__ import annotations

import os
import tools
from tools import get_input

import typing as typ

import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = ''.join(get_input(DAYDAY, 2024))

SAMPLE = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
SAMPLE2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


class Day:

    def __init__(self, line: str, debug: bool = False) -> None:
        self.debug = debug
        self.line = line

    def solve1(self) -> int:
        self.reg = re.compile(r'mul\((\d\d?\d?),(\d\d?\d?)\)')
        it = self.reg.finditer(self.line)
        acc = 0
        for m in it:
            gs = m.groups()
            acc += int(gs[0]) * int(gs[1])
        return acc

    def solve2(self) -> int:
        self.reg = re.compile(r'(?:mul\((\d\d?\d?),(\d\d?\d?)\)|(do)\(\)|(don\'t)\(\))')
        do = True
        it = self.reg.finditer(self.line)
        acc = 0
        for m in it:
            if self.debug:
                print(m.group())
            gs = m.groups()
            if gs[2]: # do:
                do = True
            elif gs[3]:
                do = False
            else:
                if do:
                    acc += int(gs[0]) * int(gs[1])
        return acc


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL, False)
    print(f'Real p1: {r.solve1()}')

    t2 = Day(SAMPLE2, True)
    print(f'Test p2: {t2.solve2()}')
    print(f'Real p2: {r.solve2()}')

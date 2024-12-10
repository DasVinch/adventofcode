from __future__ import annotations

import os
from tools import get_input

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2024)

SAMPLE = [
    '190: 10 19',
    '3267: 81 40 27',
    '83: 17 5',
    '156: 15 6',
    '7290: 6 8 6 15',
    '161011: 16 10 13',
    '192: 17 8 14',
    '21037: 9 7 18 13',
    '292: 11 6 16 20',
]


def intcat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def eval_with_acc(res: int,
                  acc: int,
                  vals: list[int],
                  ok_intcat: bool = False) -> bool:
    if len(vals) == 0:
        return acc == res
    if not ok_intcat:
        return (eval_with_acc(res, acc + vals[0], vals[1:])
                or eval_with_acc(res, acc * vals[0], vals[1:]))
    else:
        return (eval_with_acc(res, acc + vals[0], vals[1:], True)
                or eval_with_acc(res, acc * vals[0], vals[1:], True)
                or eval_with_acc(res, intcat(acc, vals[0]), vals[1:], True))


def eval_init(res: int, vals: list[int], ok_intcat: bool = False) -> bool:
    if len(vals) == 0:
        return False
    if len(vals) == 1:
        return res == vals[0]

    return eval_with_acc(res, vals[0], vals[1:], ok_intcat=ok_intcat)


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.eqn = []
        for line in lines:
            a, b = line.split(':')
            vals = [int(bb) for bb in b.strip().split()]
            self.eqn += [(int(a), vals)]

    def solve1(self) -> int:

        tot = 0

        for eq in self.eqn:
            if eval_init(*eq):
                tot += eq[0]
                if self.debug:
                    print(eq)

        return tot

    def solve2(self) -> int:

        tot = 0

        for eq in self.eqn:
            if eval_init(*eq, ok_intcat=True):
                tot += eq[0]
                if self.debug:
                    print(eq)

        return tot


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

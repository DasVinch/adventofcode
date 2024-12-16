from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
    'Button A: X+94, Y+34',
    'Button B: X+22, Y+67',
    'Prize: X=8400, Y=5400',
    '',
    'Button A: X+26, Y+66',
    'Button B: X+67, Y+21',
    'Prize: X=12748, Y=12176',
    '',
    'Button A: X+17, Y+86',
    'Button B: X+84, Y+37',
    'Prize: X=7870, Y=6450',
    '',
    'Button A: X+69, Y+23',
    'Button B: X+27, Y+71',
    'Prize: X=18641, Y=10279',
]

import re

RE_A = r'Button A: X\+(\d+), Y\+(\d+)'
RE_B = r'Button B: X\+(\d+), Y\+(\d+)'
RE_P = r'Prize: X=(\d+), Y=(\d+)'

from dataclasses import dataclass
import math


@dataclass
class Game:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int


def modified_gcd(a, b, x=0, y=0):
    if b == 0:
        x = 1
        y = 0
        return [a, x, y]
    x1 = 0
    y1 = 0
    d, x1, y1 = modified_gcd(b, a % b, x1, y1)
    x = y1
    y = x1 - y1 * (a // b)
    return [d, x, y]


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.games = []

        for k, l in enumerate(lines):
            if k % 4 == 0:
                ax, ay = re.match(RE_A, l).groups()
            elif k % 4 == 1:
                bx, by = re.match(RE_B, l).groups()
            elif k % 4 == 2:
                px, py = re.match(RE_P, l).groups()
                self.games.append(
                    Game(int(ax), int(ay), int(bx), int(by), int(px), int(py)))

    def solve1(self) -> int:

        price = 0
        for g in self.games:
            price_this_game = -1
            for a in range(101):
                for b in range(101):
                    if (g.ax * a + g.bx * b == g.px
                            and g.ay * a + g.by * b == g.py):
                        p = 3 * a + b
                        if price_this_game == -1 or p < price_this_game:
                            price_this_game = p
            if price_this_game > 0:
                price += price_this_game

        return price

    def solve2(self) -> int:
        K = 10000000000000
        #K = 0
        big_games = [
            Game(g.ax, g.ay, g.bx, g.by, g.px + K, g.py + K)
            for g in self.games
        ]

        cost = 0

        for g in big_games:
            
            mat = np.array([[g.ax, g.ay], [g.bx, g.by]], np.int64)
            det = mat[0,0] * mat[1,1] - mat[1,0] * mat[0,1]
            
            if det == 0:
                import pdb; pdb.set_trace()

            cof = np.array([[mat[1,1], -mat[1,0]], [-mat[0,1], mat[0,0]]], np.int64)

            targ = np.array([g.px, g.py], np.int64)

            res = (cof @ targ) / det

            res0 = (g.by * g.px - g.bx * g.py)
            res1 = (-g.ay * g.px + g.ax * g.py)

            if res0 % det == 0 and res1 % det == 0:
                cost += 3 * res0 // det + res1 // det

        return cost


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)

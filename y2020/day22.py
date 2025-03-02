from __future__ import annotations
import typing as typ

from tools import get_input
import tools

import numpy as np

import os
from enum import IntEnum

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = [[
    29, 21, 38, 30, 25, 7, 2, 36, 16, 44, 20, 12, 45, 4, 31, 34, 33, 42, 50,
    14, 39, 37, 11, 43, 18
],
        [
            32, 24, 10, 41, 13, 3, 6, 5, 9, 8, 48, 49, 46, 17, 22, 35, 1, 19,
            23, 28, 40, 26, 47, 15, 27
        ]]

SAMPLE = [[9, 2, 6, 3, 1], [5, 8, 4, 7, 10]]

class Game:

    def __init__(self, p1: list[int], p2: list[int]):
        self.p1 = p1
        self.p2 = p2

        self.game_history: set[tuple[tuple[int,...], tuple[int,...]]] = set()

    def play_one(self):
        c1 = self.p1.pop(0)
        c2 = self.p2.pop(0)
        if c1 > c2:
            self.p1.append(c1)
            self.p1.append(c2)
        else:
            self.p2.append(c2)
            self.p2.append(c1)

    def play_until(self):
        while len(self.p1) > 0 and len(self.p2) > 0:
            self.play_one()

    def score(self):
        win = self.p1 if len(self.p1) > 0 else self.p2
        total = 0
        for w, k in zip(win[::-1], range(1, len(win)+1)):
            total += w * k
        return total

    def play_all_recursive(self) -> int:
        while len(self.p1) > 0 and len(self.p2) > 0:
            t1, t2 = tuple(self.p1), tuple(self.p2)
            if (t1, t2) in self.game_history:
                return 1 # And p1 wins
            self.game_history.add((t1,t2))

            c1 = self.p1.pop(0)
            c2 = self.p2.pop(0)

            if len(self.p1) >= c1 and len(self.p2) >= c2:
                rec_subgame = Game(self.p1[:c1], self.p2[:c2])
                winner = rec_subgame.play_all_recursive()
            else:
                winner = 1 if c1 > c2 else 2

            if winner == 1:
                self.p1.append(c1)
                self.p1.append(c2)
            else:
                self.p2.append(c2)
                self.p2.append(c1)

        return 1 if len(self.p1) > 0 else 2


class Day():

    def __init__(self, p1: list[int], p2: list[int], debug: bool = False) -> None:
        self.p1 = p1
        self.p2 = p2

        self.debug = debug

    def solve1(self) -> int:
        game = Game(self.p1.copy(), self.p2.copy())
        game.play_until()
        return game.score()

    def solve2(self) -> int:
        game = Game(self.p1.copy(), self.p2.copy())
        _ = game.play_all_recursive()
        return game.score()


if __name__ == "__main__":

    t = Day(*SAMPLE, True)

    print(f'Test p1: {t.solve1()}')

    r = Day(*REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = [int(t) for t in '389547612']

SAMPLE = [int(t) for t in '389125467']

from dataclasses import dataclass

@dataclass
class Dequp:
    label: int
    cw: Dequp
    ccw: Dequp

    def insert_cw(self, dequp: Dequp) -> None:
        dequp.cw = self.cw
        dequp.ccw = self
        dequp.cw.ccw = dequp
        self.cw = dequp

    def insert_ccw(self, dequp: Dequp) -> None:
        dequp.ccw = self.ccw
        dequp.cw = self
        dequp.ccw.cw = dequp
        self.ccw = dequp


    def pop_cw(self) -> Dequp:
        pop = self.cw
        self.cw = pop.cw
        self.cw.ccw = self

        pop.cw = None
        pop.ccw = None
        return pop

    def __repr__(self)-> str:
        return f'Dequp(label={self.label}, cw={self.cw.label}, ccw={self.ccw.label})'


def make_move(dict_dequps: dict[int, Dequp], current_dequp: Dequp) -> Dequp:
    p1 = current_dequp.pop_cw()
    p2 = current_dequp.pop_cw()
    p3 = current_dequp.pop_cw()

    total_cups = len(dict_dequps)
    k = 0
    while True:
        k += 1
        dest_cup = dict_dequps[((current_dequp.label - 1 - k) % total_cups) + 1]
        if dest_cup not in [p1, p2, p3]:
            break

    dest_cup.insert_cw(p3)
    dest_cup.insert_cw(p2)
    dest_cup.insert_cw(p1)

    return current_dequp.cw

class Day:
    def __init__(self, cups: list[int], init_for_p2: bool = False):
        self.dict_dequps: dict[int, Dequp] = {c: Dequp(c, None, None) for c in cups}

        if init_for_p2:
            dd = {k: Dequp(k, None, None) for k in range(len(cups)+1, 1_000_001)}
            self.dict_dequps.update(dd)

        for k in range(len(cups) - 1):
            self.dict_dequps[cups[k]].cw = self.dict_dequps[cups[k+1]]
            self.dict_dequps[cups[k+1]].ccw = self.dict_dequps[cups[k]]

        if not init_for_p2:
            self.dict_dequps[cups[0]].ccw = self.dict_dequps[cups[-1]]
            self.dict_dequps[cups[-1]].cw = self.dict_dequps[cups[0]]
        else:
            for k in range(len(cups)+1, 1_000_000):
                self.dict_dequps[k].cw = self.dict_dequps[k+1]
                self.dict_dequps[k+1].ccw = self.dict_dequps[k]

            self.dict_dequps[cups[0]].ccw = self.dict_dequps[1_000_000]
            self.dict_dequps[cups[-1]].cw = self.dict_dequps[len(cups)+1]
            self.dict_dequps[len(cups)+1].ccw = self.dict_dequps[cups[-1]]
            self.dict_dequps[1_000_000].cw = self.dict_dequps[cups[0]]

        self.current_cup = self.dict_dequps[cups[0]]

        for label, cup in self.dict_dequps.items():
            assert cup.cw
            assert cup.ccw

    def solve1(self, moves: int = 100) -> str:
        current_cup = self.current_cup
        for _ in range(moves):
            current_cup = make_move(self.dict_dequps, current_cup)

        cup = self.dict_dequps[1].cw
        s = []
        for _ in range(len(self.dict_dequps)-1):
            s += [str(cup.label)]
            cup = cup.cw

        return ''.join(s)
        
    def solve2(self, moves: int = 10_000_000):
        current_cup = self.current_cup
        from tqdm import trange
        for _ in trange(moves):
            current_cup = make_move(self.dict_dequps, current_cup)

        return self.dict_dequps[1].cw.label * self.dict_dequps[1].cw.cw.label

if __name__ == '__main__':

    print(f'Test p1 (10): {Day(SAMPLE).solve1(10)}')
    print(f'Test p1 (100): {Day(SAMPLE).solve1()}')

    print(f'Real p1: {Day(REAL).solve1()}')

    tp2 = Day(SAMPLE, init_for_p2=True)
    print(f'Test p2: {tp2.solve2()}')

    s = time.time()
    print(f'Real p2: {Day(REAL, init_for_p2=True).solve2()}')
    print(time.time() - s)
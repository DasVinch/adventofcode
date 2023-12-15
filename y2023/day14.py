from __future__ import annotations

import os
from tools import get_input
import tools

from tqdm import tqdm

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

MAPPER = {
    '.': 0,
    '#': 1,
    'O': 2,
}

REAL = tools.make_cmapped_int_matrix(get_input(DAYDAY, 2023), MAPPER)

SAMPLE = tools.make_cmapped_int_matrix([
    'O....#....',
    'O.OO#....#',
    '.....##...',
    'OO.#O....O',
    '.O.....O#.',
    'O.#..O.#.#',
    '..O..#O..O',
    '.......O..',
    '#....###..',
    '#OO..#....',
], MAPPER)


def array_roll_in_place(x: np.ndarray) -> None:
    next_roll = 0
    for ptr in range(0, len(x)):
        if x[ptr] == 1: # block
            next_roll = ptr + 1
        if x[ptr] == 2:
            x[ptr] = 0
            x[next_roll] = 2
            next_roll += 1

def array_roll_in_place_rev(x: np.ndarray) -> None:
    next_roll = len(x)-1
    for ptr in range(len(x)-1, -1, -1):
        if x[ptr] == 1: # block
            next_roll = ptr - 1
        if x[ptr] == 2:
            x[ptr] = 0
            x[next_roll] = 2
            next_roll -= 1

class Day:

    def __init__(self, mat: np.ndarray, debug: bool = False) -> None:
        self.debug = debug
        self.mat = mat
        self.mat_bak = self.mat.copy()

    def reset(self):
        self.mat = self.mat_bak.copy()

    def roll_north(self):
        for cc in range(self.mat.shape[1]):
            array_roll_in_place(self.mat[:,cc])

    def roll_west(self):
        for rr in range(self.mat.shape[0]):
            array_roll_in_place(self.mat[rr])

    def roll_south(self):
        for cc in range(self.mat.shape[1]):
            array_roll_in_place_rev(self.mat[:,cc])

    def roll_east(self):
        for rr in range(self.mat.shape[0]):
            array_roll_in_place_rev(self.mat[rr])

    def cycle(self):
        self.roll_north()
        self.roll_west()
        self.roll_south()
        self.roll_east()

    def load_north(self) -> int:
        load = 0
        for kk, r in enumerate(self.mat[::-1]):
            load += (kk+1) * np.sum(r == 2)
        return load

    def solve1(self) -> int:
        self.reset()
        self.roll_north()

        return self.load_north()
        
            

    def solve2(self) -> int:
        from tqdm import trange

        self.reset()

        self.mat_storage: list[bytes] = [self.mat.tobytes()]

        for k in trange(1_000_000_000):
            self.cycle()
            b = self.mat.tobytes()
            if b in self.mat_storage:
                m = self.mat_storage.index(b)
                print(f'Cycle found! {k} matches {m}')
                break
            self.mat_storage += [b]

        remaining = (1_000_000_000 - k - 1)
        cyclen = k - m + 1
        print(f'Remaining: {remaining} -- {cyclen} -- {remaining % cyclen}')

        for _ in range(remaining % cyclen):
            self.cycle()

        return self.load_north()


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
    '#####',
    '.####',
    '.####',
    '.####',
    '.#.#.',
    '.#...',
    '.....',
    '',
    '#####',
    '##.##',
    '.#.##',
    '...##',
    '...#.',
    '...#.',
    '.....',
    '',
    '.....',
    '#....',
    '#....',
    '#...#',
    '#.#.#',
    '#.###',
    '#####',
    '',
    '.....',
    '.....',
    '#.#..',
    '###..',
    '###.#',
    '###.#',
    '#####',
    '',
    '.....',
    '.....',
    '.....',
    '#....',
    '#.#..',
    '#.#.#',
    '#####',
]

MAPPER = {'.': 0, '#': 1}


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        n_items = (len(lines) + 1) // 8

        self.locks: list[np.ndarray] = []
        self.keys: list[np.ndarray] = []

        for it in range(n_items):
            sublines = lines[8 * it:8 * it + 7]
            mat = tl.make_cmapped_int_matrix(sublines, MAPPER)
            rows = np.sum(mat, axis=1)
            cols = np.sum(mat, axis=0)-1

            if rows[0] == 0:
                self.keys += [cols]
            else:
                self.locks += [cols]

    def solve1(self) -> int:

        working_pairs = 0

        for kk in self.keys:
            for ll in self.locks:
                if np.all((kk + ll) <= 5):
                    working_pairs += 1
                
        return working_pairs


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

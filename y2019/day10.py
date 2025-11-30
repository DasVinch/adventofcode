from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] = [
    '.#..##.###...#######',
    '##.############..##.',
    '.#.######.########.#',
    '.###.#######.####.#.',
    '#####.##.#.##.###.##',
    '..#####..#.#########',
    '####################',
    '#.####....###.#.#.##',
    '##.#################',
    '#####.##.###..####..',
    '..######..##.#######',
    '####.##.####...##..#',
    '.#####..#.######.###',
    '##...#.##########...',
    '#.##########.#######',
    '.####.#.###.###.#.##',
    '....##.##.###..#####',
    '.#.#.###########.###',
    '#.#.#.#####.####.###',
    '###.##.####.##.#..##',
]

ADDITIONAL_SAMPLES: list[list[str]] = [
    [
        '.#..#',
        '.....',
        '#####',
        '....#',
        '...##',
    ],
    [
        '......#.#.',
        '#..#.#....',
        '..#######.',
        '.#.#.###..',
        '.#..#.....',
        '..#....#.#',
        '#..#....#.',
        '.##.#..###',
        '##...#..#.',
        '.#....####',
    ],
    [
        '#.#...#.#.',
        '.###....#.',
        '.#....#...',
        '##.#.#.#.#',
        '....#.#.#.',
        '.##..###.#',
        '..#...##..',
        '..##....##',
        '......#...',
        '.####.###.',
    ],
    [
        '.#..#..###',
        '####.###.#',
        '....###.#.',
        '..###.##.#',
        '##.##.#.#.',
        '....###..#',
        '..#.#..#.#',
        '#..#.#.###',
        '.##...##.#',
        '.....#.#..',
    ],
]

import numpy as np, numpy.typing as npt

T_DATA: typ.TypeAlias = set[tuple[int, int]]  # TODO

from math import gcd


class Day:

    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        matrix = tl.make_cmapped_int_matrix(input, {'.': 0, '#': 1})
        wh = np.where(matrix == 1)
        return set(zip(wh[0], wh[1]))

    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug
        ...

    def solve1(self) -> int:
        self.best = 0
        self.best_pos = (0, 0)

        for x, y in self.data:
            count = 0
            blocked_lines = set()
            for xx, yy in self.data:
                if x == xx and y == yy:
                    continue

                g = gcd(abs(x - xx), abs(y - yy))
                if ((x - xx) // g, (y - yy) // g) not in blocked_lines:
                    count += 1
                    blocked_lines.add(((x - xx) // g, (y - yy) // g))

            if count > self.best:
                self.best = count
                self.best_pos = (x, y)

        return self.best

    def solve2(self) -> int:
        self.solve1()

        if self.best < 200:
            return -1

        x, y = self.best_pos

        count = 0
        blocked_lines = set()
        visible = {}

        for xx, yy in self.data:
            if x == xx and y == yy:
                continue

            g = gcd(abs(x - xx), abs(y - yy))
            if ((x - xx) // g, (y - yy) // g) not in blocked_lines:
                count += 1
                blocked_lines.add(((x - xx) // g, (y - yy) // g))
                visible[(xx, yy)] = np.arctan2(yy - y, x - xx) % (2*np.pi)

        vis_list = list(visible.keys())
        vis_list.sort(key=lambda k: visible[k])

        vx, vy = vis_list[199]
        return vy * 100 + vx

from __future__ import annotations

import os
import typing as typ
from tools import get_input
import tools

from tqdm import tqdm

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

MAPPER = {'?': 0, '.': 1, '#': 2}

SAMPLE = [
    '???.### 1,1,3',
    '.??..??...?##. 1,1,3',
    '?#?#?#?#?#?#?#? 1,3,1,6',
    '????.#...#... 4,1,1',
    '????.######..#####. 1,6,5',
    '?###???????? 3,2,1',
]


def string_to_bitmasks(s: str) -> tuple[int, int, int]:
    sure, surenot = 0, 0
    for c in s[::-1]:
        match c:
            case '.':
                sure *= 2
                surenot = 2 * surenot + 1
            case '#':
                sure = 2 * sure + 1
                surenot *= 2
            case '?':
                sure *= 2
                surenot *= 2
            case _:
                raise ValueError()

    return sure, surenot, len(s)


def bitmasks_to_string(sure: int, surenot: int, n: int) -> str:
    char_arr = []
    for _ in range(n):
        s, sn = sure % 2, surenot % 2
        sure //= 2
        surenot //= 2

        match s, sn:
            case 0, 0:
                char_arr.append('?')
            case 1, 0:
                char_arr.append('#')
            case 0, 1:
                char_arr.append('.')
            case _:
                raise ValueError

    return ''.join(char_arr)


import functools


@functools.cache
def position_complies_bit(pos: int, sure: int, surenot: int) -> bool:
    return (pos & surenot) == 0 and (~pos & sure) == 0


@functools.cache
def tree_xplorer_count(hints: tuple[int, ...], sure_int: int, surenot_int: int,
                       n_pos: int):
    n_hints = len(hints)
    if n_hints == 0:  # equiv to [0]
        return sure_int == 0 # careful!! since also when we recurse we don't check the tail of the mask
    if n_pos == 0:
        return 1

    #print(hints, bitmasks_to_string(sure_int, surenot_int, n_pos))

    min_need = sum(hints) + len(hints) - 1 if len(hints) > 1 else hints[0]
    if min_need > n_pos:
        return 0

    tot_positions = 0

    hint = hints[0]
    if len(hints) > 1:
        tail_length = sum(hints[1:]) + len(hints) - 1
    else:
        tail_length = 0

    positioner = 2**hint - 1  # 0b11...111
    masker = 2**(hint+1) - 1
    for sp in range(0, n_pos - tail_length - hint + 1):
        if position_complies_bit(positioner, sure_int & masker, surenot_int & masker):
            # AH! Actually this compliance is only to be checked for the first sp + hint + 1 (?) bits! 
            # Recurse with one less hint
            tot_positions += \
                tree_xplorer_count(hints[1:],
                                   sure_int >> (sp + hint + 1),
                                   surenot_int >> (sp + hint + 1),
                                   n_pos - sp - hint - 1)
        positioner <<= 1
        masker <<= 1
        masker += 1

    return tot_positions

def fiveify_string(s: str) -> str:
    return ((s + '?') * 5)[:-1]


class Day:
    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug
        self.lines = lines

        self.datum = []
        self.datum2 = []

        for line in lines:
            split = line.split()

            self.datum += [(tuple(int(s) for s in split[1].split(',')),
                            *string_to_bitmasks(split[0]))]
            self.datum2 += [(tuple(int(s) for s in split[1].split(',')) * 5,
                            *string_to_bitmasks(fiveify_string(split[0])))]

    def solve1(self) -> int:
        t = 0
        self.results1: list[int] = []
        for k, dat in enumerate(self.datum):
            count = tree_xplorer_count(*dat)
            self.results1 += [count]
            if self.debug:
                print(self.lines[k], count)
            t += count

        return t

    def solve2(self) -> int:
        self.collected2 = {}
        t = 0
        for k, dat in enumerate(self.datum2):
            count = tree_xplorer_count(*dat)
            self.collected2[self.lines[k]] = count
            if self.debug:
                print(self.lines[k], tree_xplorer_count(*self.datum[k]), count)
            t += count

        self.lll = list(self.collected2.keys())
        self.lll.sort(key=self.collected2.get)

        return t


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')
    r = Day(REAL, False)
    print(f'Real p1: {r.solve1()}')

    assert 1 == tree_xplorer_count((1,1,3)*5, *string_to_bitmasks(fiveify_string('???.###')))
    assert 16384 == tree_xplorer_count((1,1,3)*5, *string_to_bitmasks(fiveify_string('.??..??...?##.')))
    assert 1 == tree_xplorer_count((1,3,1,6)*5, *string_to_bitmasks(fiveify_string('?#?#?#?#?#?#?#?')))
    assert 16 == tree_xplorer_count((4,1,1)*5, *string_to_bitmasks(fiveify_string('????.#...#...')))
    assert 2500 == tree_xplorer_count((1,6,5)*5, *string_to_bitmasks(fiveify_string('????.######.#####.')))
    assert 506250 == tree_xplorer_count((3,2,1)*5, *string_to_bitmasks(fiveify_string('?###????????')))

    print(f'Test p2: {t.solve2()}')

    print(f'Real p2: {r.solve2()}')

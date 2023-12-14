from __future__ import annotations

import os
from tools import get_input
import tools

from tqdm import tqdm

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023) + ['']

MAPPER = {
    '.': 0,
    '#': 1,
}

SAMPLE = [
    '#.##..##.',
    '..#.##.#.',
    '##......#',
    '##......#',
    '..#.##.#.',
    '..##..##.',
    '#.#.##.#.',
    '',
    '#...##..#',
    '#....#..#',
    '..##..###',
    '#####.##.',
    '#####.##.',
    '..##..###',
    '#....#..#',
    '',
]

def parse(all_lines: list[str]) -> list[np.ndarray]:
    buffer: list[str] = []
    output: list[np.ndarray] = []
    for line in all_lines:
        if line == '':
            output += [tools.make_cmapped_int_matrix(buffer, cmap=MAPPER)]
            buffer = []
        else:
            buffer += [line]

    return output


def find_sym_cands(arr: np.ndarray) -> set[int]:
    nn = len(arr)
    cands: set[int] = set()
    for ii in range(nn-1):
        for jj in range(min(ii+1, nn-ii-1)):
            if arr[ii-jj] != arr[ii+jj+1]:
                break
        else:
            cands.add(ii)

    return cands

def find_sym_cands_tolerant(arr: np.ndarray) -> tuple[set[int], set[int]]:
    nn = len(arr)
    cands: set[int] = set()
    off_by_smudge_cands: set[int] = set()
    for ii in range(nn-1):
        joker = False
        for jj in range(min(ii+1, nn-ii-1)):
            if arr[ii-jj] != arr[ii+jj+1]:
                if joker:
                    break
                joker = True
        else:
            if joker:
                off_by_smudge_cands.add(ii)
            else:
                cands.add(ii)

    return cands, off_by_smudge_cands

class ORIENT:
    ROWS = 1
    COLS = 100

import itertools
from collections import Counter

def solve_matrix_with_a_smudge(mat: np.ndarray) -> tuple[int, int]:
    mm = mat.shape[0]
    ss_rows = [find_sym_cands_tolerant(row) for row in mat]
    ct0, ct1 = Counter(), Counter()
    for sg, sb in ss_rows:
        ct0.update(sg)
        ct1.update(sb)
    for item in ct0:
        if ct0[item] == mm-1 and ct1[item] == 1:
            return ORIENT.ROWS, item

    nn = mat.shape[1]
    ss_rows = [find_sym_cands_tolerant(row) for row in mat.T]
    ct0, ct1 = Counter(), Counter()
    for sg, sb in ss_rows:
        ct0.update(sg)
        ct1.update(sb)
    for item in ct0:
        if ct0[item] == nn-1 and ct1[item] == 1:
            return ORIENT.COLS, item
        
    raise

def solvesolve_matrix2(mat: np.ndarray) -> int:
    orient, count = solve_matrix_with_a_smudge(mat)
    return orient * (count+1)    


    # The appropriate desmudged pivot must appear in all-but-one of the good components and
    # in exactly one off-by-one row

def solve_matrix(mat: np.ndarray) -> tuple[int, int]:
    s_row = set.intersection(*[find_sym_cands(row) for row in mat])
    s_col = set.intersection(*[find_sym_cands(col) for col in mat.T])
    if len(s_row) > 0:
        assert len(s_row) == 1
        return ORIENT.ROWS, s_row.pop()
    
    assert len(s_col) == 1
    return ORIENT.COLS, s_col.pop()

def solvesolve_matrix(mat: np.ndarray) -> int:
    orient, count = solve_matrix(mat)
    return orient * (count+1)

class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug
        self.lines = lines

        self.datum = parse(self.lines)

    def solve1(self) -> int:
        return sum([solvesolve_matrix(mat) for mat in self.datum])

    def solve2(self) -> int:
        return sum([solvesolve_matrix2(mat) for mat in self.datum])


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')


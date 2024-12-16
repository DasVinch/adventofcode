from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
    '##########',
    '#..O..O.O#',
    '#......O.#',
    '#.OO..O.O#',
    '#..O@..O.#',
    '#O#..O...#',
    '#O..O..O.#',
    '#.OO.O.OO#',
    '#....O...#',
    '##########',
    '',
    '<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^',
    'vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v',
    '><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<',
    '<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^',
    '^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><',
    '^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^',
    '>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^',
    '<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>',
    '^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>',
    'v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^',
]

SAMPLE2 = [
    '########',
    '#..O.O.#',
    '##@.O..#',
    '#...O..#',
    '#.#.O..#',
    '#...O..#',
    '#......#',
    '########',
    '',
    '<^^>>>vv<v>>v<<',
]

SAMPLE3 = [
    '###',
    '#.#',
    '#O#',
    '#@#',
    '',
    '^^',
]


def move_dir(dir: str, i: int, j: int, mat: np.ndarray) -> tuple[int, int]:
    match dir:
        case '>':
            ii, jj = i, j + 1
        case '^':
            ii, jj = i - 1, j
        case '<':
            ii, jj = i, j - 1
        case 'v':
            ii, jj = i + 1, j

    if mat[ii, jj] == '#':
        return i, j

    if mat[ii, jj] == '.' or move_dir(dir, ii, jj, mat) != (ii, jj):
        mat[ii, jj] = mat[i, j]
        mat[i, j] = '.'
        return ii, jj

    return i, j


def can_move_dir_2(dir: str, i: int, j: int, mat: np.ndarray,
                   cache: dict[tuple[int, int], bool]) -> bool:
    if (i, j) in cache:
        return cache[(i, j)]

    match dir:
        case '>':
            ii, jj = i, j + 1
        case '^':
            ii, jj = i - 1, j
        case '<':
            ii, jj = i, j - 1
        case 'v':
            ii, jj = i + 1, j

    if mat[ii, jj] == '#':
        cache[(i, j)] = False
        return False

    if dir in '<>':
        ret = mat[ii, jj] == '.' or can_move_dir_2(dir, ii, jj, mat, cache)
        cache[(i, j)] = ret
        return ret

    if dir in '^v':
        if mat[ii, jj] == '.':
            return True
        if mat[ii, jj] == '[':
            ret = (can_move_dir_2(dir, ii, jj, mat, cache)
                   and can_move_dir_2(dir, ii, j + 1, mat, cache))
            cache[(i, j)] = ret
            return ret
        if mat[ii, jj] == ']':
            ret = (can_move_dir_2(dir, ii, jj, mat, cache)
                   and can_move_dir_2(dir, ii, j - 1, mat, cache))
            cache[(i, j)] = ret
            return ret


def move_dir_2(dir: str, i: int, j: int, mat: np.ndarray) -> tuple[int, int]:
    if mat[i, j] == '.':
        return i, j

    match dir:
        case '>':
            ii, jj = i, j + 1
        case '^':
            ii, jj = i - 1, j
        case '<':
            ii, jj = i, j - 1
        case 'v':
            ii, jj = i + 1, j

    move_dir_2(dir, ii, jj, mat)
    if dir in 'v^':
        if mat[i, j] == '[':
            move_dir_2(dir, ii, jj + 1, mat)
        if mat[i, j] == ']':
            move_dir_2(dir, ii, jj - 1, mat)

        if mat[i, j] == '[':
            mat[ii, jj + 1] = mat[i, j + 1]
            mat[i, j + 1] = '.'
        if mat[i, j] == ']':
            mat[ii, jj - 1] = mat[i, j - 1]
            mat[i, j - 1] = '.'

    else:
        move_dir_2(dir, ii, jj, mat)

    mat[ii, jj] = mat[i, j]
    mat[i, j] = '.'

    return ii, jj


def duplicate_matrix(mat: np.ndarray):
    mat2 = np.stack([mat, mat], axis=2)
    wh = mat == 'O'
    st = mat == '@'

    mat2[wh, 0] = '['
    mat2[wh, 1] = ']'

    mat2[st, 1] = '.'

    mat2 = mat2.reshape(mat.shape[0], 2 * mat.shape[1])

    return mat2


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        break_idx = lines.index('')

        self.mat: np.ndarray = tl.make_char_matrix(lines[:break_idx])

        self.og_mat = self.mat.copy()

        self.moves: str = ''.join(lines[break_idx + 1:])

    def solve1(self) -> int:
        start = np.where(self.mat == '@')
        i, j = start[0][0], start[1][0]

        for move in self.moves:
            #tl.print_matrix(self.mat)
            #input('')
            i, j = move_dir(move, i, j, self.mat)

        stones = np.where(self.mat == 'O')

        #tl.print_matrix(self.mat)

        gps = 0
        for iis, jjs in zip(*stones):
            gps += iis * 100 + jjs

        return gps

    def solve2(self) -> int:

        doublemat = duplicate_matrix(self.og_mat)

        start = np.where(doublemat == '@')
        i, j = start[0][0], start[1][0]

        for move in self.moves:
            #tl.print_matrix(doublemat)
            #input('')
            can = can_move_dir_2(move, i, j, doublemat, {})
            if can:
                i, j = move_dir_2(move, i, j, doublemat)

        stones = np.where((doublemat == '['))

        #tl.print_matrix(self.mat)

        gps = 0
        for iis, jjs in zip(*stones):
            gps += iis * 100 + jjs

        return gps

        return 0


if __name__ == "__main__":
    t3 = Day(SAMPLE3, True)
    print(f'Test p2: {t3.solve2()}')

    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')
    t2 = Day(SAMPLE2, True)
    print(f'Test2 p1: {t2.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)

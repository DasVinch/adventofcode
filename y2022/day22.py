import os

import typing as typ

import tools
from tools import get_input
import re
import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    '        ...#',
    '        .#..',
    '        #...',
    '        ....',
    '...#.......#',
    '........#...',
    '..#....#....',
    '..........#.',
    '        ...#....',
    '        .....#..',
    '        .#......',
    '        ......#.',
]
SAMPLEDIR = '10R5L5R10L4R5L5'
SAMPLE_SIZE = 4
SAMPLE_TILES = np.array([[-1, -1, 0, -1], [1, 2, 3, -1], [-1, -1, 4, 5]])

REALRAW = get_input(DAYDAY, 2022)
REAL = REALRAW[:-2]
REALDIR = REALRAW[-1]
REAL_TILES = np.array([[-1, 0, 1], [-1, 2, -1], [3, 4, -1], [5, -1, -1]])

REAL_SIZE = 50

CMAP = {' ': 0, '.': 1, '#': 2}

T_Trans: typ.TypeAlias = dict[tuple[int, str], tuple[int, str, bool]]

# 12 transition pairs
U, D, L, R = 'U', 'D', 'L', 'R'

TRANS_SAMPLE_P1: T_Trans = {
    (0, U): (4, D, False),
    (0, D): (3, U, False),
    (0, L): (0, R, False),
    (1, U): (1, D, False),
    (1, L): (3, R, False),
    (1, R): (2, L, False),
    (2, U): (2, D, False),
    (2, R): (3, L, False),
    (3, D): (4, U, False),
    (4, L): (5, R, False),
    (4, R): (5, L, False),
    (5, U): (5, D, False),
}
_tmp = {}
for (face_a, side_a), (face_b, side_b, flip) in TRANS_SAMPLE_P1.items():
    _tmp[(face_b, side_b)] = (face_a, side_a, flip)
TRANS_SAMPLE_P1.update(_tmp)
assert len(TRANS_SAMPLE_P1) == 24

TRANS_SAMPLE_P2: T_Trans = {
    (0, U): (1, U, True),
    (0, D): (3, U, False),
    (0, L): (2, U, False),
    (0, R): (5, R, True),

    (1, D): (4, D, True),
    (1, L): (5, D, True),
    (1, R): (2, L, False),

    (2, D): (4, L, True),
    (2, R): (3, L, False),

    (3, D): (4, U, False),
    (3, R): (5, U, True),

    (4, R): (5, L, False),
}
_tmp = {}
for (face_a, side_a), (face_b, side_b, flip) in TRANS_SAMPLE_P2.items():
    _tmp[(face_b, side_b)] = (face_a, side_a, flip)
TRANS_SAMPLE_P2.update(_tmp)
assert len(TRANS_SAMPLE_P2) == 24

TRANS_REAL_P1: T_Trans = {
    (0, U): (4, D, False),
    (0, D): (2, U, False),
    (0, L): (1, R, False),
    (0, R): (1, L, False),
    (1, U): (1, D, False),
    (2, D): (4, U, False),
    (2, L): (2, R, False),
    (3, U): (5, D, False),
    (3, D): (5, U, False),
    (3, L): (4, R, False),
    (3, R): (4, L, False),
    (5, L): (5, R, False),
}
_tmp = {}
for (face_a, side_a), (face_b, side_b, flip) in TRANS_REAL_P1.items():
    _tmp[(face_b, side_b)] = (face_a, side_a, flip)
TRANS_REAL_P1.update(_tmp)
assert len(TRANS_REAL_P1) == 24

'''
  0011
  0011
  22
  22
3344
3344
55
55
'''

TRANS_REAL_P2: T_Trans = {
    (0, U): (5, L, False),
    (0, D): (2, U, False),
    (0, L): (3, L, True),
    (0, R): (1, L, False),
    (1, U): (5, D, False),
    (1, D): (2, R, False),
    (1, R): (4, R, True),
    (2, D): (4, U, False),
    (2, L): (3, U, False),
    (3, D): (5, U, False),
    (3, R): (4, L, False),
    (4, D): (5, R, False),
}
_tmp = {}
for (face_a, side_a), (face_b, side_b, flip) in TRANS_REAL_P2.items():
    _tmp[(face_b, side_b)] = (face_a, side_a, flip)
TRANS_REAL_P2.update(_tmp)
assert len(TRANS_REAL_P2) == 24

# Oh no in cube mode certain pairs could have coordinate inversion!


def pad_and_full_tile_mat(l: list[str]):
    mlen = max([len(s) for s in l])
    l_padded = [s + ' ' * (mlen - len(s)) for s in l]

    return tools.make_cmapped_int_matrix(l_padded, CMAP)

def pad_and_full_tile_str_mat(l: list[str]):
    mlen = max([len(s) for s in l])
    l_padded = [s + ' ' * (mlen - len(s)) for s in l]

    return np.asarray([[c for c in l] for l in l_padded])

def joinprint(char_mat):
    for i in range(char_mat.shape[0]):
        print(''.join(char_mat[i]))
    print()


TURN_RIGHT = {U: R, R: D, D: L, L: U}
TURN_LEFT = {U: L, R: U, D: R, L: D}


class Day:

    def __init__(
        self,
        matrix: np.ndarray,
        dirs: str,
        size: int,
        tilemap: np.ndarray,
        transition_p1: T_Trans,
        transition_p2: T_Trans,
    ) -> None:

        self.matrix = matrix.copy()

        self.instructions: list[str | int] = [
            p.group() for p in re.finditer('(\d+|R|L)', dirs)
        ]
        self.instructions = [
            t if t in ['L', 'R'] else int(t) for t in self.instructions
        ]

        self.tr_p1 = transition_p1
        self.tr_p2 = transition_p2

        self.size = size
        self.tilemap = tilemap

        self.tiles: dict[int, np.ndarray] = {}

        for i in range(6):
            wh = np.where(tilemap == i)
            m, n = wh[0][0], wh[1][0]

            self.tiles[i] = matrix[size * m:size * (m + 1),
                                   size * n:size * (n + 1)]


        self.debug = False


    def next_tile(self, tile: int, pos_i: int, pos_j: int, dir: str,
                  trans: T_Trans) -> tuple[int, int, int, str]:

        if dir == U and pos_i == 0:
            tile_next, side_next, flip = trans[tile, U]
            or_pos = pos_j
        elif dir == D and pos_i == self.size - 1:
            tile_next, side_next, flip = trans[tile, D]
            or_pos = pos_j
        elif dir == L and pos_j == 0:
            tile_next, side_next, flip = trans[tile, L]
            or_pos = pos_i
        elif dir == R and pos_j == self.size - 1:
            tile_next, side_next, flip = trans[tile, R]
            or_pos = pos_i
        else:
            # no tile switching
            if dir == U:
                return tile, pos_i - 1, pos_j, U
            elif dir == D:
                return tile, pos_i + 1, pos_j, D
            elif dir == L:
                return tile, pos_i, pos_j - 1, L
            elif dir == R:
                return tile, pos_i, pos_j + 1, R
            else:
                raise ValueError

        # tile switch
        match side_next, flip:
            case 'U', False:
                return tile_next, 0, or_pos, D
            case 'D', False:
                return tile_next, self.size - 1, or_pos, U
            case 'L', False:
                return tile_next, or_pos, 0, R
            case 'R', False:
                return tile_next, or_pos, self.size - 1, L
            case 'U', True:
                return tile_next, 0, self.size - or_pos - 1, D
            case 'D', True:
                return tile_next, self.size - 1, self.size - or_pos - 1, U
            case 'L', True:
                return tile_next, self.size - or_pos - 1, 0, R
            case 'R', True:
                return tile_next, self.size - or_pos - 1, self.size - 1, L

        raise NameError

    def solve1(self) -> int:

        return self.solve_with(self.tr_p1)

    def solve_with(self, trans_matrix: T_Trans) -> int:
        tile, ii, jj = 0, 0, 0
        orientation = R

        for token in self.instructions:
            if token == L:
                orientation = TURN_LEFT[orientation]
                continue

            if token == R:
                orientation = TURN_RIGHT[orientation]
                continue

            # token is int
            assert isinstance(token, int)
            for _ in range(token):
                next_tile, next_ii, next_jj, next_dir = self.next_tile(
                    tile, ii, jj, orientation, trans_matrix)
                val = self.tiles[next_tile][next_ii, next_jj]
                if val == 2:
                    break
                elif val == 1:
                    tile = next_tile
                    ii = next_ii
                    jj = next_jj
                    orientation = next_dir

                    if self.debug:
                        wh = np.where(self.tilemap == tile)
                        m, n = wh[0][0], wh[1][0]
                        global_i, global_j = m * self.size + ii, n * self.size + jj
                        self.charmatrix[global_i, global_j] = {U: '^', D: 'v', L: '<', R: '>'}[orientation]
                        joinprint(self.charmatrix)
                        input()

                else:
                    raise ValueError

        return self.final_score(tile, ii, jj, orientation)

    def final_score(self, tile: int, pos_i: int, pos_j: int, dir: str) -> int:
        dir_score = {R: 0, D: 1, L: 2, U: 3}[dir]

        wh = np.where(self.tilemap == tile)
        m, n = wh[0][0], wh[1][0]
        global_i, global_j = m * self.size + pos_i + 1, n * self.size + pos_j + 1

        return 1000 * global_i + 4 * global_j + dir_score

    def solve2(self) -> int:

        return self.solve_with(self.tr_p2)


if __name__ == "__main__":
    t = Day(pad_and_full_tile_mat(SAMPLE), SAMPLEDIR, SAMPLE_SIZE,
            SAMPLE_TILES, TRANS_SAMPLE_P1, TRANS_SAMPLE_P2)
    print(t.solve1())

    r = Day(pad_and_full_tile_mat(REAL), REALDIR, REAL_SIZE, REAL_TILES, TRANS_REAL_P1, TRANS_REAL_P2)
    print(r.solve1())


    #t.debug = True
    #t.charmatrix = pad_and_full_tile_str_mat(SAMPLE)
    print(t.solve2())

    #r.debug = True
    #r.charmatrix = pad_and_full_tile_str_mat(REAL)
    print(r.solve2())

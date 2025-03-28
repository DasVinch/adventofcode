from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2020)

SAMPLE = [
    'Tile 2311:',
    '..##.#..#.',
    '##..#.....',
    '#...##..#.',
    '####.#...#',
    '##.##.###.',
    '##...#.###',
    '.#.#.#..##',
    '..#....#..',
    '###...#.#.',
    '..###..###',
    '',
    'Tile 1951:',
    '#.##...##.',
    '#.####...#',
    '.....#..##',
    '#...######',
    '.##.#....#',
    '.###.#####',
    '###.##.##.',
    '.###....#.',
    '..#.#..#.#',
    '#...##.#..',
    '',
    'Tile 1171:',
    '####...##.',
    '#..##.#..#',
    '##.#..#.#.',
    '.###.####.',
    '..###.####',
    '.##....##.',
    '.#...####.',
    '#.##.####.',
    '####..#...',
    '.....##...',
    '',
    'Tile 1427:',
    '###.##.#..',
    '.#..#.##..',
    '.#.##.#..#',
    '#.#.#.##.#',
    '....#...##',
    '...##..##.',
    '...#.#####',
    '.#.####.#.',
    '..#..###.#',
    '..##.#..#.',
    '',
    'Tile 1489:',
    '##.#.#....',
    '..##...#..',
    '.##..##...',
    '..#...#...',
    '#####...#.',
    '#..#.#.#.#',
    '...#.#.#..',
    '##.#...##.',
    '..##.##.##',
    '###.##.#..',
    '',
    'Tile 2473:',
    '#....####.',
    '#..#.##...',
    '#.##..#...',
    '######.#.#',
    '.#...#.#.#',
    '.#########',
    '.###.#..#.',
    '########.#',
    '##...##.#.',
    '..###.#.#.',
    '',
    'Tile 2971:',
    '..#.#....#',
    '#...###...',
    '#.#.###...',
    '##.##..#..',
    '.#####..##',
    '.#..####.#',
    '#..#.#..#.',
    '..####.###',
    '..#.#.###.',
    '...#.#.#.#',
    '',
    'Tile 2729:',
    '...#.#.#.#',
    '####.#....',
    '..#.#.....',
    '....#..#.#',
    '.##..##.#.',
    '.#.####...',
    '####.#.#..',
    '##.####...',
    '##..#.##..',
    '#.##...##.',
    '',
    'Tile 3079:',
    '#.#.#####.',
    '.#..######',
    '..#.......',
    '######....',
    '####.#..#.',
    '.#...#.##.',
    '#.#####.##',
    '..#.###...',
    '..#.......',
    '..#.###...',
    '',
]


SEA_MONSTER = tl.make_cmapped_int_matrix([
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
], {' ': 0, '#': 1})

import re
from dataclasses import dataclass

tup_edge: typ.TypeAlias = tuple[list[int], list[int], list[int], list[int]]


def symcode(s: int, mat: np.ndarray) -> np.ndarray:
    if s == 0:
        return mat
    if s == 1:
        return mat[::-1, :]
    if s == 2:
        return mat[:, ::-1]
    if s == 3:
        return mat[::-1, ::-1]

    return symcode(s - 4, mat.T)



U, D, L, R = 0,1,2,3
@dataclass
class Tile:
    id: int
    content: np.ndarray

    def init_edges(self):
        self.edges_by_symcode: dict[int, tup_edge] = {}
        for s in range(8):
            content = symcode(s, self.content)
            self.edges_by_symcode[s] = (
                list(content[0]),  # Top
                list(content[-1]),  # Bottom
                list(content[:, 0]),  # Left
                list(content[:, -1]),  # Right
            )

    def __hash__(self):
        return self.id.__hash__()


def parse_tiles(lines: list[str]) -> set[Tile]:
    tiles: set[Tile] = set()
    sublist: list[str] = []
    for k, line in enumerate(lines):
        if line == '':
            tiles.add(parse_tile(sublist))
            sublist = []
        else:
            sublist += [line]

    return tiles


def parse_tile(l: list[str]) -> Tile:
    id = int(re.match('Tile (\d+):', l[0]).groups()[0])
    mat = tl.make_cmapped_int_matrix(l[1:], {'.': 0, '#': 1})

    return Tile(id, mat)


def tile_is_allowable(slot: complex, tile: Tile, symcode: int, placed_tiles: dict[complex, tuple[Tile, int]]) -> bool:
    res = True
    if slot + 1 in placed_tiles:
        nei_tile, code = placed_tiles[slot + 1]
        res = res and (
            tile.edges_by_symcode[symcode][R] == nei_tile.edges_by_symcode[code][L]
        )

    if slot - 1 in placed_tiles:
        nei_tile, code = placed_tiles[slot - 1]
        res = res and (
            tile.edges_by_symcode[symcode][L] == nei_tile.edges_by_symcode[code][R]
        )

    if slot + 1j in placed_tiles:
        nei_tile, code = placed_tiles[slot + 1j]
        res = res and (
            tile.edges_by_symcode[symcode][U] == nei_tile.edges_by_symcode[code][D]
        )

    if slot - 1j in placed_tiles:
        nei_tile, code = placed_tiles[slot - 1j]
        res = res and (
            tile.edges_by_symcode[symcode][D] == nei_tile.edges_by_symcode[code][U]
        )
    return res

class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.tiles = parse_tiles(lines)
        for tile in self.tiles:
            tile.init_edges()

    def solve1(self) -> int:

        allowable_tiles = self.tiles.copy()

        placed_tiles: dict[complex, tuple[Tile, int]] = {
            0 + 0j: (allowable_tiles.pop(), 0)
        }

        open_neighbors: set[complex] = {1, -1, 1j, -1j}

        res = self.rec_solve1(allowable_tiles, placed_tiles, open_neighbors)
        print("Found truth!")
        self.truth = placed_tiles

        min_r = min({f.real for f in self.truth.keys()})
        max_r = max({f.real for f in self.truth.keys()})
        min_i = min({f.imag for f in self.truth.keys()})
        max_i = max({f.imag for f in self.truth.keys()})

        corners = [
            self.truth[min_r + 1j*min_i][0],
            self.truth[min_r + 1j*max_i][0],
            self.truth[max_r + 1j*min_i][0],
            self.truth[max_r + 1j*max_i][0],
        ]

        return corners[0].id * corners[1].id * corners[2].id * corners[3].id

    def rec_solve1(self, tile_pool: set[Tile],
                   placed_tiles: dict[complex, tuple[Tile, int]],
                   boundary_slots: set[complex]) -> bool:

        if len(tile_pool) == 0:
            return True
        
        for slot_pos in boundary_slots.copy():
            for tile in tile_pool.copy():
                for s in range(8):
                    if tile_is_allowable(slot_pos, tile, s, placed_tiles):
                        tile_pool.remove(tile)
                        placed_tiles[slot_pos] = (tile, s)
                        boundary_slots_new = {slot_pos + 1, slot_pos - 1, slot_pos + 1j, slot_pos -1j}
                        boundary_slots_new.difference_update(boundary_slots)
                        boundary_slots_new.difference_update(set(placed_tiles.keys()))
                        boundary_slots.update(boundary_slots_new)
                        boundary_slots.remove(slot_pos)

                        is_outcome = self.rec_solve1(tile_pool, placed_tiles, boundary_slots)


                        if is_outcome:
                            return True
                        
                        boundary_slots.difference_update(boundary_slots_new)
                        boundary_slots.add(slot_pos)
                        del placed_tiles[slot_pos]
                        tile_pool.add(tile)


        return False

    def solve2(self) -> int:
        min_r = int(min({f.real for f in self.truth.keys()}))
        max_r = int(max({f.real for f in self.truth.keys()}))
        min_i = int(min({f.imag for f in self.truth.keys()}))
        max_i = int(max({f.imag for f in self.truth.keys()}))

        outer_size = self.truth[0][0].content.shape[0]
        inner_size = self.truth[0][0].content.shape[0] - 2

        extent_in_tiles = max_r - min_r + 1

        self.full_matrix = np.zeros((extent_in_tiles * inner_size, extent_in_tiles * inner_size), np.int32)
        self.fuller_matrix = np.zeros((extent_in_tiles * outer_size, extent_in_tiles * outer_size), np.int32)

        for ki, i in enumerate(range(min_i, max_i + 1)):
            for kj, j in enumerate(range(min_r, max_r + 1)):
                tile, code = self.truth[j + 1j*i]
                self.full_matrix[ki*inner_size:(ki+1)*inner_size,
                            kj*inner_size:(kj+1)*inner_size] = symcode(code, tile.content)[1:-1,1:-1][::-1]
                self.fuller_matrix[ki*outer_size:(ki+1)*outer_size,
                            kj*outer_size:(kj+1)*outer_size] = symcode(code, tile.content)[::-1]

        mi, mj = SEA_MONSTER.shape
        smons = np.sum(SEA_MONSTER)
        for code in range(8):
            locs = []
            matrix_to_scan = symcode(code, self.full_matrix.copy())
            mati, matj = matrix_to_scan.shape
            for ii in range(mati - mi):
                for jj in range(matj - mj):
                    #import pdb; pdb.set_trace()
                    if np.sum(matrix_to_scan[ii:ii+mi, jj:jj+mj] * SEA_MONSTER) == smons:
                        print(f'Found monster at {ii=}, {jj=}, {code=}')
                        locs += [(ii, jj)]
            for ii, jj in locs:
                matrix_to_scan[ii:ii+mi, jj:jj+mj] -= SEA_MONSTER
            print(f'{code=}, remaining {np.sum(matrix_to_scan)}')

        return 0


def write_tiles(tiles: typ.Iterable[Tile]):
    from PIL import Image

    for t in tiles:
        img = Image.fromarray(t.content.astype(np.uint8) * 255)
        img.save(
            str(os.path.abspath(__file__)) +
            f'/../../inputs/2020/20/{t.id}.png')


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)
    '''
    '''

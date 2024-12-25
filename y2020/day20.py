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


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.tiles = parse_tiles(lines)
        for tile in self.tiles:
            tile.init_edges()

    def solve1(self) -> int:

        return 0

    def solve2(self) -> int:

        return 0


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)

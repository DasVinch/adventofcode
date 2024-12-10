from __future__ import annotations
import typing as typ

import os
import numpy as np

from tools import get_input, make_char_matrix

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = make_char_matrix(get_input(DAYDAY, 2023))

SAMPLE = make_char_matrix([
    '#.#####################',
    '#.......#########...###',
    '#######.#########.#.###',
    '###.....#.>.>.###.#.###',
    '###v#####.#v#.###.#.###',
    '###.>...#.#.#.....#...#',
    '###v###.#.#.#########.#',
    '###...#.#.#.......#...#',
    '#####.#.#.#######.#.###',
    '#.....#.#.#.......#...#',
    '#.#####.#.#.#########v#',
    '#.#...#...#...###...>.#',
    '#.#.#v#######v###.###v#',
    '#...#.>.#...>.>.#.###.#',
    '#####v#.#.###v#.#.###.#',
    '#.....#...#...#.#.#...#',
    '#.#########.###.#.#.###',
    '#...###...#...#...#.###',
    '###.###.#.###v#####v###',
    '#...#...#.#.>.>.#.>.###',
    '#.###.###.#.###.#.#v###',
    '#.....###...###...#...#',
    '#####################.#',
])

IN = (0, 1)
OUT = (-1, -2) # don't forget to modulo

from dataclasses import dataclass

Coord: typ.TypeAlias = tuple[int, int]

@dataclass
class TreeNode:
    parent: TreeNode | None
    parent_tile: Coord | None # last tile of parent, for convenience
    single_path: list[Coord]
    children: list[TreeNode]

    def backtrack_length(self):
        if self.parent is None:
            return len(self.single_path)
        else:
            return len(self.single_path) + self.parent.backtrack_length()
        
    def explore_til_decision(self, grid: np.ndarray):
        curr = self.single_path[-1]

         



class Day():
    ...


if __name__ == "__main__":
    t = Day(SAMPLE, True)

    print(f'Test p1: {t.solve1(6)}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')
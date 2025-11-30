from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] | None = [
    '#################',
    '#i.G..c...e..H.p#',
    '########.########',
    '#j.A..b...f..D.o#',
    '########@########',
    '#k.E..a...g..B.n#',
    '########.########',
    '#l.F..d...h..C.m#',
    '#################',
]

ADDITIONAL_SAMPLES: list[list[str]] = []

import numpy as np

T_DATA: typ.TypeAlias = np.ndarray  # TODO


def wh_to_tuple(mat: np.ndarray) -> tuple[int, int]:
    r, c = np.where(mat)
    return r[0], c[0]


class DjkDistanceFinder(tl.AbstractDijkstraer[tuple[int, int]]):

    def __init__(self,
                 grid: np.ndarray,
                 start: tuple[int, int],
                 targets: set[tuple[int, int]],
                 max_depth: int = -1) -> None:

        self.start = start
        self.grid = grid.copy()

        super().__init__(start, targets, max_depth)

    def get_neighbors(
            self, elem: tuple[int,
                              int]) -> typ.Set[tuple[tuple[int, int], int]]:
        neighbor_set: set[tuple[int, int]] = set()

        r, c = elem

        if elem == self.start or self.grid[r, c] in '.@':
            # Open or start, add all non-wall neighbors
            # Can't except if all the edge is wall
            if self.grid[r - 1, c] != '#':
                neighbor_set.add((r - 1, c))
            if self.grid[r + 1, c] != '#':
                neighbor_set.add((r + 1, c))
            if self.grid[r, c - 1] != '#':
                neighbor_set.add((r, c - 1))
            if self.grid[r, c + 1] != '#':
                neighbor_set.add((r, c + 1))

        return {(n, 1) for n in neighbor_set}


class DjkDistanceToNextKey(tl.AbstractDijkstraer[str]):

    def __init__(
        self,
        start: str,
        held_keys: str,
        graph: dict[str, dict[str, int]],
    ) -> None:
        self.start = start
        self.held_keys = held_keys
        self.graph = graph

        super().__init__(self.start, set())

    def get_neighbors(self, elem: str) -> set[tuple[str, int]]:
        nn: set[tuple[str, int]] = set()

        for next_node, distance in self.graph[elem].items():
            if next_node == '@':
                continue
            elif next_node.islower():
                nn.add((next_node, distance))
            elif next_node.isupper() and next_node.lower() in self.held_keys:
                nn.add((next_node, distance))

        return nn


class DjkKeySolver(tl.AbstractDijkstraer[tuple[str, str]]):

    def __init__(self,
                 graph: dict[str, dict[str, int]],
                 targets: set[tuple[str, str]],
                 all_keys: str,
                 max_depth: int = -1) -> None:

        self.start = ('@', '')
        self.graph = graph.copy()
        self.all_keys = ''.join(sorted(all_keys))

        super().__init__(self.start, targets, max_depth)

    def get_neighbors(
            self, elem: tuple[str, str]) -> set[tuple[tuple[str, str], int]]:
        position, keys = elem

        neighbor_set: set[tuple[tuple[str, str], int]] = set()

        assert keys == '' or keys.islower()
        assert position == '@' or position in keys

        next_keys_finder = DjkDistanceToNextKey(position, keys, self.graph)
        next_keys_finder.solveWithoutPath()

        for a, (dist, _) in next_keys_finder.distanceDict.items():
            if a.islower() and not a in keys:
                neighbor_set.add(((a, ''.join(sorted(keys + a))), dist))

        return neighbor_set

    def validate_target(self, elem: tuple[str, str]) -> bool:
        return elem[1] == self.all_keys


class Day:

    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return tl.make_char_matrix(input)

    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug

        self.start: tuple[int, int] = wh_to_tuple(self.data == '@')

        all_chars = list(np.unique(self.data.flatten()))
        all_chars.remove('.')
        all_chars.remove('#')
        self.all_special_chars: list[str] = all_chars

        self.special_chars_by_letter: dict[str, tuple[int, int]] = {}
        self.special_chars_by_location: dict[tuple[int, int], str] = {}

        for char in self.all_special_chars:
            where_char_xx = np.where(self.data == char)
            r, c = where_char_xx[0][0], where_char_xx[1][0]
            self.special_chars_by_letter[char] = (r, c)
            self.special_chars_by_location[(r, c)] = char

        self.graph: dict[str, dict[str, int]] = {}

        for char in self.all_special_chars:
            d = DjkDistanceFinder(self.data,
                                  self.special_chars_by_letter[char], set())
            d.solveWithoutPath()

            for ((r, c), (dist, _)) in d.distanceDict.items():
                if not (r, c) in self.special_chars_by_location:
                    continue
                antichar = self.special_chars_by_location[(r, c)]
                if antichar == char:
                    continue

                if not char in self.graph:
                    self.graph[char] = {}
                if antichar != '@':
                    self.graph[char][antichar] = dist

                if not antichar in self.graph:
                    self.graph[antichar] = {}
                if char != '@':
                    self.graph[antichar][char] = dist

    def solve1(self) -> int:
        all_keys = ''.join(sorted([c for c in self.all_special_chars if c.islower()]))
        self.djk_key_solver = DjkKeySolver(self.graph, set(), all_keys)

        self.djk_key_solver.solveWithoutPath()

        return min({v[0] for t,v in self.djk_key_solver.distanceDict.items() if len(t[1]) == len(all_keys)})

    def solve2(self) -> int:
        ...

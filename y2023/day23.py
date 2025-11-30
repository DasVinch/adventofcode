from __future__ import annotations
import typing as typ

import os
import numpy as np

from tools import get_input, make_char_matrix
import tools

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
OUT = (-1, -2)  # don't forget to modulo

from dataclasses import dataclass

Coord: typ.TypeAlias = tuple[int, int]


@dataclass
class TreeNode:
    parent: TreeNode | None
    parent_tile: Coord | None  # last tile of parent, for convenience
    single_path: list[Coord]
    children: list[TreeNode]

    def backtrack_length(self):
        if self.parent is None:
            return len(self.single_path)
        else:
            return len(self.single_path) + self.parent.backtrack_length()

    def explore_til_decision(self, grid: np.ndarray):
        curr = self.single_path[-1]


class Djk(tools.AbstractDijkstraer[Coord]):

    def __init__(self,
                 start: Coord,
                 targets: set[Coord],
                 untargets: set[Coord],
                 max_depth: int = -1,
                 grid: np.ndarray = None) -> None:
        self.grid = grid
        self.gsm, self.gsn = self.grid.shape

        self.untargets = untargets

        super().__init__(start, targets, max_depth=max_depth)

    def get_neighbors(self, elem: Coord) -> set[tuple[Coord, int]]:
        ii, jj = elem

        neighbors: set[Coord] = set()
        nn = set()
        if ii - 1 >= 0 and self.grid[ii - 1, jj] not in 'v#':
            nn.add((ii - 1, jj))
        if ii + 1 < self.gsm and self.grid[ii + 1, jj] not in '^#':
            nn.add((ii + 1, jj))
        if jj - 1 >= 0 and self.grid[ii, jj - 1] not in '>#':
            nn.add((ii, jj - 1))
        if jj + 1 < self.gsn and self.grid[ii, jj + 1] not in '<#':
            nn.add((ii, jj + 1))

        for nncand in nn:
            if nncand in self.targets:
                neighbors.add(nncand)
            if not nncand in self.untargets:
                neighbors.add(nncand)

        return {(c, 1) for c in neighbors}

class DjkNoSlopes(Djk):
    def get_neighbors(self, elem: Coord) -> set[tuple[Coord, int]]:
        ii, jj = elem

        neighbors: set[Coord] = set()
        nn = set()
        if ii - 1 >= 0 and self.grid[ii - 1, jj] not in '#':
            nn.add((ii - 1, jj))
        if ii + 1 < self.gsm and self.grid[ii + 1, jj] not in '#':
            nn.add((ii + 1, jj))
        if jj - 1 >= 0 and self.grid[ii, jj - 1] not in '#':
            nn.add((ii, jj - 1))
        if jj + 1 < self.gsn and self.grid[ii, jj + 1] not in '#':
            nn.add((ii, jj + 1))

        for nncand in nn:
            if nncand in self.targets:
                neighbors.add(nncand)
            if not nncand in self.untargets:
                neighbors.add(nncand)

        return {(c, 1) for c in neighbors}


class Day():

    def __init__(self, grid: np.ndarray):
        self.grid = grid.copy()
        sr, sc = self.grid.shape

        # Initialize intersections
        oi, oj = OUT[0] % sr, OUT[1] % sc
        self.intersects: dict[int, Coord] = {-1: IN, -2: (oi, oj)}

        # Count intersects
        kk = 0
        for ii in range(1, sr - 1):
            for jj in range(1, sc - 1):
                if self.grid[ii, jj] == '.' and (sum([
                        self.grid[ii + 1, jj] in '><v^', self.grid[ii - 1, jj]
                        in '><v^', self.grid[ii, jj + 1] in '><v^',
                        self.grid[ii, jj - 1] in '><v^'
                ]) >= 2):
                    self.intersects[kk] = (ii, jj)
                    kk += 1

        # Compute intersects distances
        self.distances: dict[int, set[tuple[int, int]]] = {
            ii: set()
            for ii in self.intersects
        }
        self.distances2: dict[int, set[tuple[int, int]]] = {
            ii: set()
            for ii in self.intersects
        }

        for id_a, pos_a in self.intersects.items():
            for id_b, pos_b in self.intersects.items():
                if dist := self.pathlen_between(pos_a, pos_b):
                    self.distances[id_a].add((id_b, dist))
                if dist := self.pathlen_between2(pos_a, pos_b):
                    self.distances2[id_a].add((id_b, dist))

    def pathlen_between(self, a: Coord, b: Coord) -> int | None:
        djk = Djk(a, {b}, set(self.intersects.values()), grid=self.grid)
        djk.solveWithoutPath()
        if b in djk.distanceDict:
            return djk.distanceDict[b][0]
        return None

    def pathlen_between2(self, a: Coord, b: Coord) -> int | None:
        djk = DjkNoSlopes(a, {b}, set(self.intersects.values()), grid=self.grid)
        djk.solveWithoutPath()
        if b in djk.distanceDict:
            return djk.distanceDict[b][0]
        return None

    def solve1(self) -> tuple[int,int]:
        # We've initialized everything and the graph is acyclic!
        min_dists = {k: -1 for k in self.intersects}
        max_dists = {k: -1 for k in self.intersects}
        min_dists[-1] = 0
        max_dists[-1] = 0

        inverted_graph = {k: set() for k in self.intersects}
        for k, downlinks in self.distances.items():
            for c in downlinks:
                inverted_graph[c[0]].add((k, c[1]))

        def rec_solve_p1(node: int):
            for parent, distance in inverted_graph[node]:
                if min_dists[parent] == -1:
                    rec_solve_p1(parent)
                if min_dists[node] == -1 or min_dists[parent] + distance < min_dists[node]:
                    min_dists[node] = min_dists[parent] + distance
                if max_dists[node] == -1 or max_dists[parent] + distance > max_dists[node]:
                    max_dists[node] = max_dists[parent] + distance

        rec_solve_p1(-2)

        return min_dists[-2], max_dists[-2]

    def solve2(self) -> int:
        
        marked_as_visited: set[int] = set()
        self.longest_distances: dict[int, int] = {k: 0 for k in self.intersects}

        def rec_solve_p2(node: int, curr_dist: int):
            if node in marked_as_visited:
                return
            marked_as_visited.add(node)

            if self.longest_distances[node] < curr_dist:
                self.longest_distances[node] = curr_dist

            for child, distance in self.distances2[node]:
                rec_solve_p2(child, distance + curr_dist)

            marked_as_visited.remove(node)

        rec_solve_p2(-1, 0)

        return self.longest_distances[-2]


if __name__ == "__main__":
    t = Day(SAMPLE)

    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

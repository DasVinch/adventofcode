from __future__ import annotations
import typing as typ

import numpy as np

import itertools

from tools import get_input, AbstractDijkstraer, make_cmapped_int_matrix

CMAP = {'#': -2, '.': -1}
for c in '0123456789':
    CMAP[c] = int(c)

TEST_MAP = make_cmapped_int_matrix(
[
    '###########',
    '#0.1.....2#',
    '#.#######.#',
    '#4.......3#',
    '###########',
], CMAP)

REAL_MAP = make_cmapped_int_matrix(get_input(24, 2016), CMAP)

class Djk(AbstractDijkstraer[typ.Tuple[int,int]]):
    def __init__(self, map: np.ndarray, start: tuple[int, int], targets: set[tuple[int, int]]) -> None:
        self.map = map
        super().__init__(start, targets)

    def get_neighbors(self, elem: tuple[int, int]) -> set[tuple[tuple[int, int], int]]:
        x, y = elem

        neighbors: set[tuple[tuple[int, int], int]] = set()
        if x > 0 and self.map[x-1, y] != -2:
            neighbors.add(((x-1,y),1))
        if x < self.map.shape[0]-1 and self.map[x+1, y] != -2:
            neighbors.add(((x+1,y),1))
        if y > 0 and self.map[x, y-1] != -2:
            neighbors.add(((x,y-1),1))
        if y < self.map.shape[1]-1 and self.map[x, y+1] != -2:
            neighbors.add(((x,y+1),1))

        return neighbors

def solve_distances(map: np.ndarray) -> tuple[int, dict[tuple[int, int], int]]:

    max_val_in_map = np.max(map)

    locations: dict[int, tuple[int, int]] = {}

    distances: dict[tuple[int, int], int] = {}

    for kk in range(max_val_in_map+1):
        locations[kk] = next(zip(*np.where(map == kk)))

    for kk in range(max_val_in_map):
        djk = Djk(map, locations[kk], set())
        djk.solveWithoutPath()
        for ll in range(kk+1, max_val_in_map+1):
            distances[(kk, ll)] = djk.distanceDict[locations[ll]]

    return max_val_in_map, distances

def make_salesman_travel(max_idx: int, distances: dict[tuple[int, int], int], ret_zero: bool = False):

    min_count = 1_000_000_000

    for perm in itertools.permutations(range(1, maxval+1)):
        count = distances[(0, perm[0])]
        if ret_zero:
            count += distances[(0, perm[-1])]
        for kk in range(len(perm)-1):
            a, b = min(perm[kk], perm[kk+1]), max(perm[kk], perm[kk+1])
            count += distances[(a,b)]
        if count < min_count:
            print(f'{count} for perm {perm}!')
            min_count = count

    return min_count



if __name__ == '__main__':
    maxval, distances = solve_distances(REAL_MAP)
    t = make_salesman_travel(maxval, distances)
    print(t)
    t2 = make_salesman_travel(maxval, distances, True)
    print(t2)


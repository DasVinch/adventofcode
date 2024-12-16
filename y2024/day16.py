from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
    '###############',
    '#.......#....E#',
    '#.#.###.#.###.#',
    '#.....#.#...#.#',
    '#.###.#####.#.#',
    '#.#.#.......#.#',
    '#.#.#####.###.#',
    '#...........#.#',
    '###.#.#####.#.#',
    '#...#.....#.#.#',
    '#.#.#.###.#.#.#',
    '#.....#...#.#.#',
    '#.###.#.#.#.#.#',
    '#S..#.....#...#',
    '###############',
]

SAMPLE2 = [
    '#################',
    '#...#...#...#..E#',
    '#.#.#.#.#.#.#.#.#',
    '#.#.#.#...#...#.#',
    '#.#.#.#.###.#.#.#',
    '#...#.#.#.....#.#',
    '#.#.#.#.#.#####.#',
    '#.#...#.#.#.....#',
    '#.#.#####.#.###.#',
    '#.#.#.......#...#',
    '#.#.###.#####.###',
    '#.#.#...#.....#.#',
    '#.#.#.#####.###.#',
    '#.#.#.........#.#',
    '#.#.#.#########.#',
    '#S#.............#',
    '#################',
]

import enum
class Dir(str, enum.Enum):
    N = '^'
    W = '<'
    E = '>'
    S = 'v'

    def right(self) -> Dir:
        match self:
            case Dir.N:
                return Dir.E
            case Dir.W:
                return Dir.N
            case Dir.E:
                return Dir.S
            case Dir.S:
                return Dir.W

    def left(self) -> Dir:
        match self:
            case Dir.N:
                return Dir.W
            case Dir.W:
                return Dir.S
            case Dir.E:
                return Dir.N
            case Dir.S:
                return Dir.E

DJK_T: typ.TypeAlias = tuple[Dir, int, int]



class Djk(tl.AbstractDijkstraer[DJK_T]):

    def __init__(self, start: DJK_T, targets: set[DJK_T], map: np.ndarray) -> None:
        
        super().__init__(start, targets)

        self.map = map
        self.tgt_nodir = {(t[1], t[2]) for t in targets}

    def get_neighbors(self, elem: DJK_T) -> set[tuple[DJK_T, int]]:

        s: set[tuple[DJK_T, int]] = set()
        
        d, i, j = elem

        s.add(((d.left(), i, j), 1000))
        s.add(((d.right(), i, j), 1000))

        if d == Dir.N and self.map[i-1, j] != '#':
            s.add(((d, i-1, j), 1))

        if d == Dir.E and self.map[i, j+1] != '#':
            s.add(((d, i, j+1), 1))

        if d == Dir.S and self.map[i+1, j] != '#':
            s.add(((d, i+1, j), 1))

        if d == Dir.W and self.map[i, j-1] != '#':
            s.add(((d, i, j-1), 1))

        return s

    def validate_target(self, elem: DJK_T) -> bool:
        _, i, j = elem
        return (i, j) in self.tgt_nodir


class DjkButGreedyMultipath(Djk):
    def solveWithoutPath(self) -> int | None:
        if self.used:
            raise ValueError('AbstractDijkstraer has been used. Make a new one')
        self.used = True

        while not self.border.empty():
            wrappedelem = self.border.get()
            prio = wrappedelem.priority
            elem = wrappedelem.item

            #print(elem)

            if self.validate_target(elem):
                return prio

            for nei, cost in self.get_neighbors(elem):
                score = prio + cost
                is_new = nei not in self.distanceDict
                if is_new or score < self.distanceDict[nei][0]:
                    self.distanceDict[nei] = (score, [elem])
                    self.border.put(tl.PrioritizedItem(priority=score, item=nei))
                # Add-on!
                elif score == self.distanceDict[nei][0]:
                    score, elem0 = self.distanceDict[nei]
                    self.distanceDict[nei] = (score, elem0 + [elem])



    

class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.mat = tl.make_char_matrix(lines)

        x = np.where(self.mat == 'S')
        self.st = (Dir.E, x[0][0], x[1][0])
        x = np.where(self.mat == 'E')
        self.end = (Dir.E, x[0][0], x[1][0])
        


    def solve1(self) -> int:

        self.djk1 = Djk(self.st, {self.end}, self.mat)

        pathlen = self.djk1.solveWithoutPath()

        return pathlen
        

    def solve2(self) -> int:

        self.djk2 = DjkButGreedyMultipath(self.st, set(), self.mat)
        pathlen = self.djk2.solveWithoutPath()
        
        backtracer: set[DJK_T] = set()
        trace_nodes: set[tuple[int, int]] = set()
        end_minimal = 1000000000000
        for dir, i, j in self.djk2.distanceDict:
            if (i,j) == (self.end[1], self.end[2]):
                dist = self.djk2.distanceDict[(dir,i,j)][0]
                end_minimal = min(end_minimal, dist)

        for (dir, i, j), (w, _) in self.djk2.distanceDict.items():
            if (i,j) == (self.end[1], self.end[2]) and w == end_minimal:
                backtracer.add((dir, i, j))

        while len(backtracer) > 0:
            elem = backtracer.pop()
            trace_nodes.add((elem[1], elem[2]))
            parents = self.djk2.distanceDict[elem][1]
            if parents is not None:
                for p in parents:
                    backtracer.add(p)
            
        self.trace_nodes = trace_nodes
        return len(trace_nodes)




if __name__ == "__main__":
    t = Day(SAMPLE, False)
    print(f'Test p1: {t.solve1()}')
    t2 = Day(SAMPLE2, True)
    print(f'Test p1: {t2.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Test p2: {t2.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)
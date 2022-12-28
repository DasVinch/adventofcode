import os
from tools import get_input, make_cmapped_int_matrix

import numpy as np

from enum import Enum

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    '.....',
    '..##.',
    '..#..',
    '.....',
    '..##.',
    '.....',
]
SAMPLE2 = [
    '..............',
    '..............',
    '.......#......',
    '.....###.#....',
    '...#...#.#....',
    '....#...##....',
    '...#.###......',
    '...##.#.##....',
    '....#..#......',
    '..............',
    '..............',
    '..............',
]

CHARMAP = {'.': 0, '#': 1}

REAL = get_input(DAYDAY, 2022)

class Dir:
    N = 0
    S = 1
    W = 2
    E = 3

    dir_list = [N, S, W, E]
    
    Neval = lambda lnei: not any(lnei[:3])
    Seval = lambda lnei: not any(lnei[-3:])
    Weval = lambda lnei: not any(lnei[::3])
    Eeval = lambda lnei: not any(lnei[2::3])

    direval_list = [Neval, Seval, Weval, Eeval]

    Ncoord = lambda e: (e[0]-1, e[1])
    Scoord = lambda e: (e[0]+1, e[1])
    Wcoord = lambda e: (e[0], e[1]-1)
    Ecoord = lambda e: (e[0], e[1]+1)
    

    dircoord_list = [Ncoord, Scoord, Wcoord, Ecoord]

class Day:
    def __init__(self, lines) -> None:
        mat = make_cmapped_int_matrix(lines, CHARMAP)
        self.elves = {(a, b) for (a, b) in zip(*np.where(mat == 1))}

        self.next_round_dir = Dir.N

    def round(self, dir):
        any_move = False
        proposed = {}
        proposed_w_counts = {}

        # Perform proposals
        for (ex, ey) in self.elves:
            neighbor_elf = []
            for ii in (-1,0,+1):
                for jj in (-1,0,+1):
                    neighbor_elf += [(ex+ii, ey+jj) in self.elves]

            neighbor_elf[4] = False

            if not any(neighbor_elf):
                proposed[(ex, ey)] = None
                continue # self.elves

            for d in range(dir, dir+4):
                if Dir.direval_list[d % 4](neighbor_elf):
                    proposed[(ex, ey)] = Dir.dircoord_list[d % 4]((ex, ey))
                    proposed_w_counts[Dir.dircoord_list[d % 4]((ex, ey))] = \
                        proposed_w_counts.get(Dir.dircoord_list[d % 4]((ex, ey)), 0) + 1
                    any_move = True
                    break # d
            
            if (ex, ey) not in proposed:
                proposed[(ex, ey)] = None

        # Now, move
        new_elves = set()
        for elf in self.elves:
            if proposed[elf] is not None and proposed_w_counts[proposed[elf]] == 1:
                new_elves.add(proposed[elf])
            else:
                new_elves.add(elf)

        self.elves = new_elves

        return any_move

    def nextround(self):

        res = self.round(self.next_round_dir)
        self.next_round_dir = (self.next_round_dir + 1) % 4
        return res

    def bounding_box(self, doprint=False):
        xc = list(map(lambda x: x[0], self.elves))
        yc = list(map(lambda x: x[1], self.elves))

        xmin = min(xc)
        xmax = max(xc)
        ymin = min(yc)
        ymax = max(yc)

        if doprint:
            for x in range(xmin, xmax+1):
                for y in range(ymin, ymax+1):
                    if (x,y) in self.elves:
                        print('##', end='')
                    else:
                        print('--', end='')
                print()

        return (xmax - xmin + 1) * (ymax - ymin + 1) - len(self.elves)

    def solve1(self):
        for i in range(10):
            self.nextround()
        
        return self.bounding_box(True)


    def solve2(self):
        count = 1
        while self.nextround():
            count += 1

        self.bounding_box(True)
        return count

    def solve2special(self):
        count = 1
        while self.nextround():
            self.bounding_box(True)
            input(count)
            count += 1

        return count

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    t2 = Day(SAMPLE2)
    print(t2.solve2())
    r = Day(REAL)
    print(r.solve2())
from __future__ import annotations
import typing as typ

from tools import get_input
import tools

from skimage.morphology import label

import numpy as np

import os
from enum import IntEnum

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)',
]

import re

RE = '(L|R|U|D) (\d+) \(#([0-9a-f]{5})(\d)\)'

Mytup: typ.TypeAlias = tuple[str, int, str, int]

def parses(l: list[str]) -> list[Mytup]:
    return [parse(ll) for ll in l]

def parse(l: str) -> Mytup:
    d,n,c,i = re.match(RE, l).groups()
    return (d, int(n), 'RDLU'[int(i)], int(c, 16))


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.lines = lines
        self.dat = parses(self.lines)

    def solve1(self) -> int:
        # Well shit
        
        curr_x = 0
        curr_y = 0

        alles_poses: list[tuple[int,int]] = [(0,0)]

        for dir, n, *_ in self.dat:
            nn = n
            while nn > 0:
                nn -= 1
                match dir:
                    case 'U':
                        curr_x -= 1
                    case 'D':
                        curr_x += 1
                    case 'L':
                        curr_y -= 1
                    case 'R':
                        curr_y += 1
                alles_poses.append((curr_x, curr_y))

        x_min = min([p[0] for p in alles_poses])
        x_max = max([p[0] for p in alles_poses])
        y_min = min([p[1] for p in alles_poses])
        y_max = max([p[1] for p in alles_poses])

        mat = np.zeros((x_max - x_min + 3, y_max - y_min + 3), bool)

        for x,y in alles_poses:
            mat[x-x_min+1,y-y_min+1] = True

        l_map = label(mat, background=1)

        #tools.print_bool_matrix(mat)

        return len(alles_poses) - 1 + np.sum(l_map == 2) # start is dupped

    def solve2(self) -> int:
        # Create a list of vertices

        curr_x = 0
        curr_y = 0

        alles_poses: list[tuple[int,int]] = [(0,0)]

        for *_, dir, n in self.dat:
            match dir:
                case 'U':
                    curr_x -= n
                case 'D':
                    curr_x += n
                case 'L':
                    curr_y -= n
                case 'R':
                    curr_y += n
            alles_poses.append((curr_x, curr_y))

        area = 0
        for kk in range(len(alles_poses) - 1):
            x0, y0 = alles_poses[kk]
            x1, y1 = alles_poses[kk+1]
            area += x1*y0 - x0*y1

        area //= 2

        border_len = sum([k for (_,_,_,k) in self.dat])

        return area + border_len//2 + 1



if __name__ == "__main__":

    t = Day(SAMPLE, True)

    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')

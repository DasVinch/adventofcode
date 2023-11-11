import typing as typ

from tools import get_input, print_bool_matrix
import numpy as np

from tqdm import tqdm

import re

SAMPLE = [
]

REAL = get_input(8, 2016)

R, C = 6, 50

RE1 = 'rect (\d+)x(\d+)'
RE2 = 'rotate row y=(\d+) by (\d+)'
RE3 = 'rotate column x=(\d+) by (\d+)'
    
from enum import Enum

class PL(Enum):
    RECT = 0
    RROW = 1
    RCOL = 2


def parseline(line: str) -> typ.Tuple[PL, int, int]:
    if m := re.match(RE1, line):
        g = m.groups()
        return (PL.RECT, int(g[0]), int(g[1]))
    elif m := re.match(RE2, line):
        g = m.groups()
        return (PL.RROW, int(g[0]), int(g[1]))
    elif m := re.match(RE3, line):
        g = m.groups()
        return (PL.RCOL, int(g[0]), int(g[1]))
    else:
        raise ValueError("Dafuk")

class Day8:
    def __init__(self, lines: typ.List[str]) -> None:
        self.lines = lines

        self.parsed_lines = [parseline(line) for line in lines]

        self.matrix = np.zeros((R,C), bool)

    def solve1(self) -> int:
        self.matrix &= False

        for typ, a, b in self.parsed_lines:
            match typ:
                case PL.RECT:
                    self.matrix[:b, :a] = True
                case PL.RROW:
                    self.matrix[a] = np.roll(self.matrix[a], b)
                case PL.RCOL:
                    self.matrix[:,a] = np.roll(self.matrix[:,a], b)
                case _:
                    raise ValueError("Dafuk")
        
        return np.sum(self.matrix)
    
    def solve2(self) -> None:
        self.solve1()
        print_bool_matrix(self.matrix)



if __name__ == '__main__':
    t = Day8(SAMPLE)
    print(f'Sample: {t.solve1()}')
    r = Day8(REAL)
    print(f'Real: {r.solve1()}')


    t2 = Day8(SAMPLE)
    print(f'Sample: {t2.solve2()}')
    r = Day8(REAL)
    print(f'Real: {r.solve2()}')
from __future__ import annotations

from tools import get_input
import tools

import os
from enum import IntEnum

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    '.|...\\....',
    '|.-.\\.....',
    '.....|-...',
    '........|.',
    '..........',
    '.........\\',
    '..../.\\\\..',
    '.-.-/..|..',
    '.|....-|.\\',
    '..//.|....',
]



class BeamDir(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

from dataclasses import dataclass

@dataclass
class BeamObj:
    dir: BeamDir
    pos: tuple[int, int]

    def in_grid(self, shape: tuple[int, int]) -> bool:
        x,y = self.pos
        xg, yg = shape

        return x >= 0 and y >= 0 and x < xg and y < yg
    
    def move(self):
        x, y = self.pos
        match self.dir:
            case BeamDir.UP:
                self.pos = (x-1, y)
            case BeamDir.DOWN:
                self.pos = (x+1, y)
            case BeamDir.LEFT:
                self.pos = (x, y-1)
            case BeamDir.RIGHT:
                self.pos = (x, y+1)

    def slash(self): # /
        self.dir = {
            BeamDir.UP: BeamDir.RIGHT,
            BeamDir.DOWN: BeamDir.LEFT,
            BeamDir.LEFT: BeamDir.DOWN,
            BeamDir.RIGHT: BeamDir.UP
        }[self.dir]

    def backslash(self): # \
        self.dir = {
            BeamDir.UP: BeamDir.LEFT,
            BeamDir.DOWN: BeamDir.RIGHT,
            BeamDir.LEFT: BeamDir.UP,
            BeamDir.RIGHT: BeamDir.DOWN
        }[self.dir]

    def prop_against(self, char: str) -> list[BeamObj]:
        # Assum the CHAR is at the current position
        ret: list[BeamObj] = [self]
        match self.dir, char:
            case _, '/':
                self.slash()
            case _, '\\':
                self.backslash()
            case (BeamDir.UP | BeamDir.DOWN), '-':
                self.dir = BeamDir.LEFT
                ret += [BeamObj(BeamDir.RIGHT, self.pos)]
            case (BeamDir.LEFT | BeamDir.RIGHT), '|':
                self.dir = BeamDir.UP
                ret += [BeamObj(BeamDir.DOWN, self.pos)]
            case _:
                pass
        
        for bo in ret:
            bo.move()

        return ret


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.lines = lines

        self.grid_shape = (len(self.lines), len(self.lines[0]))

    def solve1(self) -> int:
        return self.solve_from_init(BeamObj(BeamDir.RIGHT, (0,0)))
        
    def solve_from_init(self, b: BeamObj) -> int:
        we_been_there = set()

        beam_stack = [b]

        while len(beam_stack) > 0:
            beam = beam_stack.pop()
            if (*beam.pos, beam.dir) in we_been_there:
                continue

            we_been_there.add((*beam.pos, beam.dir))

            new_beams = beam.prop_against(self.lines[beam.pos[0]][beam.pos[1]])

            beam_stack += [n for n in new_beams if n.in_grid(self.grid_shape)]

        been_there_pos = {(a,b) for (a,b,_) in we_been_there}

        return len(been_there_pos)

    def solve2(self) -> int:
        m = 0
        for ii in range(self.grid_shape[0]):
            m = max(m, self.solve_from_init(BeamObj(BeamDir.LEFT, (ii, 0))))
            m = max(m, self.solve_from_init(BeamObj(BeamDir.RIGHT, (ii, self.grid_shape[1]-1))))
        for jj in range(self.grid_shape[1]):
            m = max(m, self.solve_from_init(BeamObj(BeamDir.DOWN, (0, jj))))
            m = max(m, self.solve_from_init(BeamObj(BeamDir.UP, (self.grid_shape[0]-1, jj))))

        return m



if __name__ == "__main__":

    t = Day(SAMPLE, True)

    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')
from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] | None = None

ADDITIONAL_SAMPLES: list[list[str]] = []

T_DATA: typ.TypeAlias = list[int]  # TODO

from enum import IntEnum


class Dir(IntEnum):
    U, D, L, R = 1, 2, 3, 4

    @staticmethod
    def turn_right(d: Dir):
        return {Dir.U: Dir.R, Dir.R: Dir.D, Dir.D: Dir.L, Dir.L: Dir.U}[d]

    @staticmethod
    def turn_left(d: Dir):
        return {Dir.U: Dir.L, Dir.R: Dir.U, Dir.D: Dir.R, Dir.L: Dir.D}[d]


class Tile(IntEnum):
    OPEN, WALL, OXY = 0, 1, 2


class Status(IntEnum):
    HIT_WALL = 0
    MOVED = 1
    MOVED_FOUND_O2 = 2


from .komputer import Komputer


class Droid:

    def __init__(self, ribbon: list[int]) -> None:
        self.pos: tuple[int, int] = 0, 0
        self.lastdir: Dir = Dir.U

        self.known_grid: dict[tuple[int, int], Tile] = {(0, 0): Tile.OPEN}

        self.brain = Komputer(ribbon)

        self.has_been_up_from_start = False

    def make_a_move(self, d: Dir) -> Status:
        self.brain.execute_til_input()
        self.brain.pending_input = d
        st = self.brain.execute_til_output()
        self.brain.outputs = []
        return st

    def explore_all(self):
        while True:
            if self.pos == (0, 0) and self.lastdir == Dir.U:
                if self.has_been_up_from_start:
                    break
                else:
                    self.has_been_up_from_start = True

            status = self.make_a_move(self.lastdir)
            x, y = self.pos
            if status == Status.HIT_WALL:
                if self.lastdir == Dir.U:
                    self.known_grid[(x, y + 1)] = Tile.WALL
                elif self.lastdir == Dir.D:
                    self.known_grid[(x, y - 1)] = Tile.WALL
                elif self.lastdir == Dir.L:
                    self.known_grid[(x - 1, y)] = Tile.WALL
                elif self.lastdir == Dir.R:
                    self.known_grid[(x + 1, y)] = Tile.WALL
                self.lastdir = Dir.turn_right(self.lastdir)
            else:
                if self.lastdir == Dir.U:
                    self.pos = (x, y + 1)
                elif self.lastdir == Dir.D:
                    self.pos = (x, y - 1)
                elif self.lastdir == Dir.L:
                    self.pos = (x - 1, y)
                elif self.lastdir == Dir.R:
                    self.pos = (x + 1, y)
                self.known_grid[
                    self.
                    pos] = Tile.OPEN if status == Status.MOVED else Tile.OXY
                self.lastdir = Dir.turn_left(self.lastdir)

            #print(self.pos, self.lastdir, Status(status))
            #breakpoint()


class Djk(tl.AbstractDijkstraer[tuple[int, int]]):

    def get_neighbors(
            self, elem: tuple[int, int]) -> set[tuple[tuple[int, int], int]]:
        neighbors = set()

        x, y = elem
        if self.grid.get((x - 1, y), None) in (Tile.OPEN, Tile.OXY):
            neighbors.add((x - 1, y))
        if self.grid.get((x + 1, y), None) in (Tile.OPEN, Tile.OXY):
            neighbors.add((x + 1, y))
        if self.grid.get((x, y - 1), None) in (Tile.OPEN, Tile.OXY):
            neighbors.add((x, y - 1))
        if self.grid.get((x, y + 1), None) in (Tile.OPEN, Tile.OXY):
            neighbors.add((x, y + 1))

        return {(n, 1) for n in neighbors}


class Day:

    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return [int(t) for t in input[0].split(',')]

    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug

    def solve1(self) -> int:
        robot = Droid(self.data)

        robot.explore_all()

        import numpy as np
        m = np.zeros((60, 60), dtype=bool)
        for (x, y), v in robot.known_grid.items():
            if v == Tile.WALL:
                m[x, y] = 1
            elif v == Tile.OXY:
                m[x, y] = 2
                oxypos = (x, y)
        tl.print_bool_matrix(np.fft.fftshift(m))

        djk = Djk(start=(0, 0), targets={oxypos})
        djk.grid = robot.known_grid

        djk.solveWithoutPath()

        return djk.distanceDict[oxypos][0]

    def solve2(self) -> int:
        robot = Droid(self.data)

        robot.explore_all()

        import numpy as np
        m = np.zeros((60, 60), dtype=bool)
        for (x, y), v in robot.known_grid.items():
            if v == Tile.WALL:
                m[x, y] = 1
            elif v == Tile.OXY:
                m[x, y] = 2
                oxypos = (x, y)
        tl.print_bool_matrix(np.fft.fftshift(m))

        djk = Djk(start=oxypos, targets=set())
        djk.grid = robot.known_grid

        djk.solveWithoutPath()

        return max({v for (v,_) in djk.distanceDict.values()})
